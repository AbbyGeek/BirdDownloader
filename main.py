from bs4 import *
import requests
import os
import urllib.request

#get main page html code
def main(url):
     soup = parsePage(url)
     indexDict = getLinksAndNames(soup)
     photoGrabber(indexDict)

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
    try:
        if headingName.endswith("[edit]"):
            headingName = headingName[:-len("[edit]")]
    except:
        print("Folder named "+headingName+" alreay exists")
    return(headingName)
    
def createFolders(headingName):
    #folder creations
    try:
        os.mkdir(headingName)
    except:
        print("Folder named "+headingName+" alreay exists")

def photoGrabber(indexDict):
    #Iterate through one family at a time
    for family in indexDict:
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
    rootDir = os.getcwd()
    os.chdir(os.path.join(os.path.abspath(os.path.curdir),family))
    familyDir = os.getcwd()
    for itemName in imgDict:
        urllib.request.urlretrieve(imgDict[itemName],itemName+".jpg")
    os.chdir(rootDir)


main('https://en.wikipedia.org/wiki/List_of_birds_of_Michigan')