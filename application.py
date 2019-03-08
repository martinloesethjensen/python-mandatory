import fnmatch
import json
import os
import subprocess
import urllib.request


class Committer(object):
    @staticmethod
    def git_init():
        subprocess.run(args="git init")

    @staticmethod
    def git_add_remote_origin(url):
        subprocess.run(args="git remote add origin " + url)

    @staticmethod
    def git_add_all():
        subprocess.run(args="git add .")

    @staticmethod
    def git_commit(message):
        subprocess.run(args="git commit -m \"" + message + "\"")

    @staticmethod
    def git_push():
        subprocess.run(args="git push origin master")

    @staticmethod
    def git_fetch():
        subprocess.run(args="git fetch origin master")

    @staticmethod
    def git_pull():
        Committer.git_fetch()
        subprocess.run(args="git pull --allow-unrelated-histories origin master")


class Cloner(object):

    @staticmethod
    def clone_repo(clone_url, name, commit=False, path=None):
        if commit:
            subprocess.run(args="git submodule add " + clone_url + "./" + name)
        elif path is not None and path is not "":
            application_dir_path = os.getcwd()
            os.chdir(path)
            if os.path.exists("./" + name):
                Cloner.if_exists(name)
            else:
                subprocess.run(args="git clone " + clone_url)
            os.chdir(application_dir_path)
        elif os.path.exists("./" + name):
            Cloner.if_exists(name)
        else:
            subprocess.run(args="git clone " + clone_url)

    @staticmethod
    def if_exists(name):
        os.chdir(name)
        subprocess.run(args="git pull origin master")
        os.chdir("../")

    def clone_all_repos(self, clone_urls, data_dict, commit=False, path=None):
        count = 0
        for clone_url in clone_urls:
            self.clone_repo(clone_url=clone_url, name=data_dict['name'][count], commit=commit, path=path)
            count += 1

    @staticmethod
    def path_input():
        path = input(
            "\nWhere do you want to clone the repos?\n"
            "**To clone to current folder just press enter**.\nEnter the whole path: ")
        folder_ok = 1  # Sentinel for the while loop

        # Continue if path is not chosen
        if path == "":
            folder_ok = 0

        # Until a path that exists is being submitted as an input
        while folder_ok != 0:
            if os.path.exists(path):
                folder_ok = 0
            else:
                path = input("Folder doesn't exist... Try again: ")
        return path


class DataFetcher(object):
    def __init__(self, url):
        self.url = url

    # def get_json_data(self):
    #     try:
    #         with urllib.request.urlopen(self.url) as response:
    #             data_json = json.load(response)
    #     except ConnectionError as con_err:
    #         print(con_err)
    #         raise
    #     return data_json

    def get_data_to_text_file(self, filename):
        try:
            with urllib.request.urlopen(self.url) as response:
                data_file = open(filename, "w")
                data_file.write(str(response.read()))
        except ConnectionError as con_err:
            print(con_err)

    @staticmethod
    def data_from_text_to_dict(filename):
        try:
            data_dict = {}

            names = []
            clone_urls = []
            html_urls = []

            data_from_file = open(filename, "r")
            data_string = data_from_file.read().split("\"")

            counter = 0
            for item in data_string:
                data_item = item.replace(":", "").replace(",", "").replace("=", "")
                if counter != 0:

                    if data_item is not "" and counter < len(data_string) - 2:
                        value = data_string[counter + 2]

                        if data_item.lower() == "name":
                            names.append(value)
                            data_dict[data_item] = names

                        if data_item.lower() == "clone_url":
                            clone_urls.append(value)
                            data_dict[data_item] = clone_urls

                        if data_item.lower() == "html_url":
                            html_urls.append(value)
                            data_dict[data_item] = html_urls

                counter += 1

        except EOFError as eof_err:
            print(eof_err)
            raise

        return data_dict

    @staticmethod
    def get_clone_url_list(data_dict):
        clone_urls = data_dict['clone_url']

        # Used for json
        # clone_urls = [item['clone_url'] for item in data]
        return clone_urls

    @staticmethod
    def get_names_and_html_urls(data_dict):
        names = []
        urls = []

        for key, value in data_dict.items():
            if key != "clone_url":
                for item in value:
                    if key == "name":
                        names.append(item)
                    else:
                        urls.append(item)

        names_and_html_urls = dict(zip(names, urls))

        # For json
        # for item in data:
        #     names_and_html_urls[item['name'].replace("-", " ")] = item['html_url']

        return names_and_html_urls


class FileWriter(object):

    @staticmethod
    def get_paragraph(path):
        global data, start, end

        matches = FileWriter.get_matches(path=path)

        if len(matches) != 0:
            for match in matches:
                data = open(match, "r").read()
                start = data.find("## Required reading")
                end = data.find("## Required reading") + len("## Required reading")
                return data[start:end]

        return "## Couldn't find the title"

    @staticmethod
    def get_matches(path):
        matches = []
        for root, dir_names, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, 'README.md'):
                matches.append(os.path.join(root, filename))
        return matches

    @classmethod
    def get_names_and_links(cls, path=os.getcwd()):
        matches = FileWriter.get_matches(path=path)

        names_and_urls = {}

        counter = 0
        for match in matches:
            if counter != 0:  # to avoid README.md from own folder
                data_file = open(match, "r").read()
                if data_file.__contains__("# Mandatory Assignment: Required readings List"):
                    continue
                start_index = data_file.find("## Required reading")
                end_index = start_index + data_file[start_index:].find("### Supplementary reading")
                string = data_file[start_index:end_index].split("\n")

                for split in string:
                    if split is not "" and split != "## Required reading":
                        string_low_and_replace_symbols = split.lower().replace("* [", "").replace(")", "").replace(
                            "â€”", "-")
                        split_to_dict = string_low_and_replace_symbols.split("](")
                        name, url = split_to_dict[0], split_to_dict[1]
                        names_and_urls[name] = url
            counter += 1
        return names_and_urls

    @staticmethod
    def write_to_file(filename):
        file = open(filename, "w+")
        paragraph = FileWriter.get_paragraph(path=os.getcwd())

        names_and_html_urls = FileWriter.get_names_and_links(path=os.getcwd())
        # Start of the file:
        file.write(paragraph + "\n > Python Elective II Spring 2019\n\n")

        # Put all the necessary data in the file in a sorted order
        for name, html_url in sorted(names_and_html_urls.items()):
            file.write("* [" + name[0].upper() + name[1:].replace("-", " ") + "](" + html_url + ")\n")

        file.close()


def main():
    ###
    # Fetches all the data
    ###
    url = "https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100"

    print("Fetching all the data from {}".format(url))
    data_fetcher = DataFetcher(url=url)

    print("\nSaving all the data to a text file ...")
    data_fetcher.get_data_to_text_file("data.txt")

    print("\nGetting the necessary data from the text file to a dictionary ...")
    data_dict = data_fetcher.data_from_text_to_dict("data.txt")

    print("\nGet all the clone urls from the dictionary ...")
    clone_urls = data_fetcher.get_clone_url_list(data_dict)
    # data = data_fetcher.get_json_data()

    ###
    # Clone all repos to directory
    ###
    cloner = Cloner()
    path = cloner.path_input() if cloner.path_input() is not "" else os.getcwd()
    print("\nCloning all the repos in " + path + " ...")
    cloner.clone_all_repos(clone_urls, data_dict=data_dict, path=path)

    ###
    # Get names and html urls
    ###
    print("\nGetting the names and urls from the dictionary ..")
    names_and_html_urls = data_fetcher.get_names_and_html_urls(data_dict)

    ###
    # Create required_reading.md file
    ###
    print("\nCreating required_reading.md file ...")
    FileWriter.write_to_file("required_reading.md")

    ###
    # Commit to GitHub
    ###
    directory = os.getcwd()
    print("\nInitializing a .git in your directory: " + directory + " ...")
    Committer.git_init()

    print("\nAdding submodules for the clone repos ...")
    cloner.clone_all_repos(clone_urls, data_dict, commit=True)

    print("\nAdded the remote origin to the repo url. It will continue if remote origin already exists... ")
    Committer.git_add_remote_origin("https://github.com/martinloesethjensen/python-mandatory.git")

    print("\nAdded all files ...")
    Committer.git_add_all()

    message = input("\nCommit changes ...\nPlease write your message for the commit:\t")
    Committer.git_commit(message=message)

    print("\nFetches and pulls changes if there's any changes on the master that you don't have in your directory ...")
    Committer.git_pull()

    print("\nPushing changes ...")
    Committer.git_push()


if __name__ == '__main__':
    main()
