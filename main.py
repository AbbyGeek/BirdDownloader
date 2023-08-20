from bs4 import *
import requests
import os

'''
APPROACH
-import module
-create image folder
get main page html code
create list of all pages to navigate to in order to retrieve images
navigate to each page in list
download specific image
'''
#create image folder
# folder_name = "Bird Images"
# try:
#     os.mkdir(folder_name)
# except:
#     print("Folder by desired name already exists")

#get main page html code
def main(url):
    soup = parsePage(url)
    getLinksAndNames(soup)

def parsePage(url):
     #content of URL
    r = requests.get(url)
    #Parse HTML code
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getLinksAndNames(soup):
    headingCount = 0
    #Find div's w/ div-col class
    for item in soup.find_all("div", {"class": "mw-parser-output"}):
        #Grab all lists and h2 tags
        elements = item.find_all(['h2', 'li'])
        for item in elements:
            #stop at end of content
            if item.find(id='See_also'):
                break
            #handle headings
            if item.name == 'h2':
                createFolders(item.text)
            #handle list items
            if item.name == 'li':
                try:
                    print(item.text)
                    print('https://en.wikipedia.org/' + item.find('a', href=True)['href'])
                except:
                    print("Error with: "+item.text)


def createFolders(headingName):
    #folder creations
    try:
        if headingName.endswith("[edit]"):
            headingName = headingName[:-len("[edit]")]
        os.mkdir(headingName)
    except:
        print("Folder named "+headingName+" alreay exists")

def downloadPics (Name, href):
    return

            


main('https://en.wikipedia.org/wiki/List_of_birds_of_Michigan')