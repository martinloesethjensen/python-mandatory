# Mandatory Assignment: Required readings List

> Mandatory Assignment: creating a Required readings List from the _## Required reading paragraph_ in the readme files, on github.

All the following should be done through Python, not manually. Even though there are many ways to solve the subtasks in this exercise you should only use the elements we covered so far. 

## Requirements for the application
The overall function of this application is that it should be able to generate a **required_reading.md** file containing a list of the litterature you will need to be familiar with at the exam in the end of this semester. An example of this can be seen [here](https://github.com/clbokea/required_reading/blob/master/required_reading.md)
For this, the application should be able to _clone_ and later _pull_ all repositories from the the github organization "Python Elective I spring 2019" (our classroom git repositories) and store it locally on your machine.   
Then it should loop through all the readme.md files and look for the bullet points contained in the _Required readings_ paragraph.  
Then it should write this collected list into a new file (required_reading.md) and push this file to a repository on your github account. The outcome will be that you have a list of links to the material/texts that is the curriculum of this python elective. 

## Step - by - step instructions
1. Get all repositories clone urls from the organization 'python-elective' and save them in a list, tuple, set or dictionary. For this you should make use of the [urllib](https://docs.python.org/3/library/urllib.html?highlight=urllib) module, and you can get all info about the repositories at this [api](https://api.github.com/orgs/python-elective-2-spring-2019/repos?per_page=100).  
_(Treat and read the json data as a text file. imagine something like a repository_info.txt. Then use the string searching and manipulations teqniques that we have worked with so far. Dealing with json data comes later this semester.)_    
2. Clone all repos from the organisation. (for this you will need the modul: [subprocess](https://docs.python.org/3/library/subprocess.html#module-subprocess))
    1. or if the repository is alredy cloned you should make sure that you have an up to date version of the repository by a _pull_ request. (for some of the tasks in this operation you will need the modul: [subprocess](https://docs.python.org/3/library/subprocess.html#module-subprocess) like before and for some you will need the module: [OS](https://docs.python.org/3/library/os.html?highlight=os#module-os)) 
3. Traverse through all repos locally and get the readme files content in a list ie. (for this you will need the module: [glob](https://docs.python.org/3/library/glob.html?highlight=glob#module-glob))
4. Search the content of the list and find the "## Required reading" paragraph and put the content of that paragraph into list.
4. Write the list to a required_reading.md in a new curriculum repository. (for this operation you will again need the modul: [OS](https://docs.python.org/3/library/os.html?highlight=os#module-os)) 
    1. The links in the readme file should be:
        1. Ordered Alphabetically
        1. Beginning character should be capitalized
        1. The list should look good/normal, e.g no blank bullet points, no whitepsaces in wrong places etc.
        1. No dublicate link should occour. 
5. push that repository to your own github account.

### Extra tasks
1. When this is done you should make your application able to dynamically handle the github api url, dynamically handle where on your computer the repositories should be stored. 
1. If a repo online is removed the application should be able to detect this and delete the local version of the repository. Thus keeping the list up to date.

## Project management
Follow the advice in the [5 minutes video](https://www.youtube.com/watch?v=ohr6O78jGzs) we watched in class.
1. First day (7 hours), messy coding
1. Second day (7 hours), Refactor your code into functions, modules ie. 
1. Third day (7 hours), focus on delivery, documentation, making the project ready for the presentation.

## Code Quality
You code should look good, and it should be easy to read. This means it should be commented, it should have nice variable/function names ie. 

## Error handeling
It is important that your application is robust. And you should handle the errors that might occour. 

## Resources
* [Github Api](https://api.github.com/orgs/python-elective-1-spring-2019/repos?per_page=100)
* [urllib](https://docs.python.org/3/library/urllib.html?highlight=urllib)
* [subprocess](https://docs.python.org/3/library/subprocess.html#module-subprocess)
* [glob](https://docs.python.org/3/library/glob.html?highlight=glob#module-glob)
* [OS](https://docs.python.org/3/library/os.html?highlight=os#module-os)
* [HOWTO Fetch Internet Resources Using The urllib Package](https://docs.python.org/3/howto/urllib2.html)

## Timeframe for this mandatory assignment
For this assignment you will have one week. You will at tuesday the 12/03 have to show what you did and explain your application to me (Claus) (for 5 minutes). You are allowed to work together and you are allowed to ask me (Claus) for help when we have lessons, but you should create an individual version of the assignment. (you can not present the assignment as a group). You will have to work on the assignment at home, and you will have time to work on the assignment in class at friday the 8/03, and on tuesday the 12th. The assignment will be evaluated with a "passed" og "not passed". 



&copy; KEA, Claus Bove, 04-01-2019
