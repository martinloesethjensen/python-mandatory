import glob
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


class Cloner(object):

    @staticmethod
    def clone_repo(clone_url, name, commit=False):
        if commit:
            subprocess.run(args="git submodule add " + clone_url)
        elif os.path.exists("./" + name):
            os.chdir(name)
            subprocess.run(args="git pull origin master")
            os.chdir("../")
        else:
            subprocess.run(args="git clone " + clone_url)

    def clone_all_repos(self, clone_urls, data, commit=False):
        count = 0
        for clone_url in clone_urls:
            self.clone_repo(clone_url=clone_url, name=data['name'][count], commit=commit)
            count += 1


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

        count = 0
        for key, value in data.items():
            if key != "clone_url":
                for item in value:
                    if key == "name":
                        names.append(item)
                    else:
                        urls.append(item)
            count += 1

        names_and_html_urls = dict(zip(names, urls))

        # For json
        # for item in data:
        #     names_and_html_urls[item['name'].replace("-", " ")] = item['html_url']

        return names_and_html_urls


class FileWriter(object):

    @staticmethod
    def get_paragraph(filename):
        os.chdir("Lesson-01-Introduction-to-the-Python-elective")
        data = open(filename, "r").read()
        start = data.find("## Required reading")
        end = data.find("## Required reading") + len("## Required reading")
        return data[start:end]

    @staticmethod
    def write_to_file(filename, names_and_html_urls):
        file = open(filename, "w+")

        paragraph = FileWriter.get_paragraph("README.md")

        # Start of the file:
        file.write(paragraph + "\n > Python Elective I Spring 2019\n\n")

        # Put all the necessary data in the file in a sorted order
        for name, html_url in sorted(names_and_html_urls.items()):
            file.write("* [" + name[0].upper() + name[1:] + "](" + html_url + ")\n")

        file.close()


def main():
    # Fetches all the data
    data_fetcher = DataFetcher(url="https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100")
    # data_fetcher.get_data_to_text_file("data.txt")
    data = data_fetcher.data_from_text_to_dict("data.txt")
    # data = data_fetcher.get_json_data()
    clone_urls = data_fetcher.get_clone_url_list(data)

    # Clone all repos to directory
    cloner = Cloner()
    cloner.clone_all_repos(clone_urls, data=data)
    #
    # # Get names and html urls
    names_and_html_urls = data_fetcher.get_names_and_html_urls(data)
    #
    # # Create README.md file
    FileWriter.write_to_file("README.md", names_and_html_urls)

    print(os.chdir("../"))
    # Commit to GitHub
    Committer.git_init()
    # cloner.clone_all_repos(clone_urls, data, commit=True)
    Committer.git_add_all()
    Committer.git_add_remote_origin("https://github.com/martinloesethjensen/python-mandatory.git")
    Committer.git_commit("Finished mandatory")
    Committer.git_push()


if __name__ == '__main__':
    main()
