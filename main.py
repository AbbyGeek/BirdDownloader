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
    getLinksAndNames(
        parsePage(url))

def parsePage(url):
     #content of URL
    r = requests.get(url)
    #Parse HTML code
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getLinksAndNames(soup):
    #Find div's w/ div-col class
    for item in soup.find_all("div", {"class": "div-col"}):
        #Grab all lists
        unorderedLists = item.find_all('ul')
        for unorderedList in unorderedLists:
            listItems = unorderedList.find_all('li')
            for listItem in listItems:
                #print bird name
               print(listItem.text)
               itemHref = listItem.find('a')
                #print link to bird page
               print("https://en.wikipedia.org"+itemHref['href'])


main('https://en.wikipedia.org/wiki/List_of_birds_of_Michigan')