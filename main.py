import sys
from bs4 import *
import requests
import os
import urllib.request

#get main page html code
def main():
    url="https://en.wikipedia.org/wiki/List_of_birds_of_Michigan"
    soup = parsePage(url)
    indexDict = getLinksAndNames(soup)
    photoGrabber(indexDict)

def inputs():
    url = input("Enter URL: ")
    state = input("Enter State: ")
    stateUrlDict = {state:url}
    return stateUrlDict

def parsePage(url):
     #content of URL
    r = requests.get(url)
    #Parse HTML code
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getLinksAndNames(soup):
    indexDict = {}
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
                #clear category items when starting a new category
                categoryItems = {}
                headingName = getHeadingName(item.text)
                #create the folder
                createFolders(headingName)
                indexDict.update({headingName:categoryItems})
            #handle list items
            if item.name == 'li':
                try:
                    name = item.text
                    url = 'https://en.wikipedia.org/' + item.find('a', href=True)['href']
                    categoryItems.update({name: url})
                    indexDict[headingName] = categoryItems
                except:
                    print("Error with: "+item.text)
    return indexDict

def getHeadingName(headingName):
    if headingName.endswith("[edit]"):
        headingName = headingName[:-len("[edit]")]
    return(headingName)
    
def createFolders(headingName):
    try:
        os.mkdir(headingName)
    except:
        print("Folder named "+headingName+" alreay exists")

def photoGrabber(indexDict):
    #Iterate through one family at a time
    for family in indexDict:
        print("~~~~~~~~~~~~~~~~~~~~~")
        print("Grabbing photo URLs for: %s" %family)
        imgDict = {}
        #Iterate through items in family
        for itemName in indexDict[family]:
            url = indexDict[family][itemName]
            #parse item's page, find the 'info box' section and extract all anchor tags
            itemSoup = parsePage(url)
            infobox = itemSoup.find("table", {"class": "infobox"})
            tableRows = infobox.find_all('td')
            for row in tableRows:
                anchor = row.find('a')
                if anchor != None:
                    #find the image in the anchor tag
                    img = anchor.find("img")
                    #if there is an image
                    if img != None:
                        src = img["src"]
                        imgUrl = "http:" + src
                        if itemName in imgDict:
                            imgDict[itemName + ", male"] = imgDict.pop(itemName)
                            imgDict.update({itemName + ", female": imgUrl})
                        else:
                            imgDict.update({itemName:imgUrl})
                    #if the anchor tag has no image element within
                    else:
                        break
        downloader(imgDict, family)

def downloader(imgDict, family):
    print("Downloading photos for: %s" %family)
    print("~~~~~~~~~~~~~~~~~~~~~")
    rootDir = os.getcwd()
    os.chdir(os.path.join(os.path.abspath(os.path.curdir),family))
    familyDir = os.getcwd()
    for itemName in imgDict:
        imgUrl = imgDict[itemName]
        imgData = requests.get(imgUrl).content
        try:
            with open(itemName+".jpg", 'wb') as handler:
                handler.write(imgData)
                #Certain files aren't being downloaded fully. Their file size is 2kb while other complete files are ~15-20kb.
                #Cannot find difference between the different images. They all have the same extention and there's no common difference between the files that I can see.
                #Possibly memory overload?
        except:
            print(itemName + " already exists")
    os.chdir(rootDir)


main()