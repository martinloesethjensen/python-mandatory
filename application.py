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
            subprocess.run(args="git submodule add " + clone_url)
        elif path is not None and path is not "":
            application_dir_path = os.getcwd()
            os.chdir(path)
            if os.path.exists("./" + name):
                Cloner.if_exists(name)
            else:
                subprocess.run(args="git clone " + clone_url)
            os.chdir(application_dir_path)
        elif os.path.exists("./" + name):
            os.chdir(name)
            subprocess.run(args="git pull origin master")
            os.chdir("../")
        else:
            subprocess.run(args="git clone " + clone_url)

    @staticmethod
    def if_exists(name):
        os.chdir(name)
        subprocess.run(args="git pull origin master")
        os.chdir("../")

    def clone_all_repos(self, clone_urls, data, commit=False, path=None):
        count = 0
        for clone_url in clone_urls:
            self.clone_repo(clone_url=clone_url, name=data['name'][count], commit=commit, path=path)
            count += 1

    @staticmethod
    def path_input():
        path = input(
            "\nWhere do you want to clone the repos?\n**To clone to current folder just press enter**.\nEnter the whole path: ")
        folder_ok = 1  # Sentinal for the while loop

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

    def get_json_data(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                data = json.load(response)
        except ConnectionError as con_err:
            print(con_err)
            raise
        return data

    def get_data_to_text_file(self, filename):
        try:
            with urllib.request.urlopen(self.url) as response:
                data = open(filename, "w")
                data.write(str(response.read()))
        except ConnectionError as con_err:
            print(con_err)

    @staticmethod
    def data_from_text_to_dict(filename):
        try:
            data_dict = {}

            names = []
            clone_urls = []
            html_urls = []

            data = open(filename, "r")
            data_string = data.read().split("\"")

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
    def get_clone_url_list(data):
        clone_urls = data['clone_url']

        # Used for json
        # clone_urls = [item['clone_url'] for item in data]
        return clone_urls

    @staticmethod
    def get_names_and_html_urls(data):
        names = []
        urls = []

        for key, value in data.items():
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
    def get_paragraph(filename, names):
        global data, start, end
        for name in names:
            if os.path.exists("./" + name):
                os.chdir(name)
                data = open(filename, "r").read()
                start = data.find("## Required reading")
                end = data.find("## Required reading") + len("## Required reading")
                break
            else:
                return "## Couldn't find the title"

        return data[start:end]

    @staticmethod
    def write_to_file(filename, names_and_html_urls):
        file = open(filename, "w+")

        paragraph = FileWriter.get_paragraph("README.md", names_and_html_urls.keys())

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
    data = data_fetcher.data_from_text_to_dict("data.txt")

    print("\nGet all the clone urls from the dictionary ...")
    clone_urls = data_fetcher.get_clone_url_list(data)
    # data = data_fetcher.get_json_data()

    ###
    # Clone all repos to directory
    ###
    cloner = Cloner()
    path = cloner.path_input() if cloner.path_input() is not "" else os.getcwd()
    print("\nCloning all the repos in " + path + " ...")
    cloner.clone_all_repos(clone_urls, data=data, path=path)

    ###
    # Get names and html urls
    ###
    print("\nGetting the names and urls from the dictionary ..")
    names_and_html_urls = data_fetcher.get_names_and_html_urls(data)

    ###
    # Create required_reading.md file
    ###
    print("\nCreating required_reading.md file ...")
    FileWriter.write_to_file("required_reading.md", names_and_html_urls)

    print("Changing to directory to ./mandatory assignment ... ")
    os.chdir("../")

    ###
    # Commit to GitHub
    ###
    print("\nInitializing a .git in your directory ...")
    Committer.git_init()

    print("\nAdding submodules for the clone repos ...")
    cloner.clone_all_repos(clone_urls, data, commit=True)

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
