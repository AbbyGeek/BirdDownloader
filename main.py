from bs4 import *
import requests
import os

# Get family descriptions to save to the indexDict variable.

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
    for family in indexDict:
        imgDictList = []
        for itemName in indexDict[family]:
            imgDict = {}
            url = indexDict[family][itemName]
            itemSoup = parsePage(url)
            infobox = itemSoup.find("table", {"class": "infobox"})
            anchors = infobox.find_all('a')
            for anchor in anchors:
                img = anchor.find("img")
                if img != None:
                    src = img["src"]
                    imgUrl = "http:" + src
                    #something in here is not
                    if imgDict:
                         imgDict[itemName + ", male"] = imgDict.pop(itemName)
                         imgDict.update({itemName + ", female": imgUrl})
                    else:
                        imgDict.update({itemName:imgUrl})
                else:
                    print(imgDict)
                    break
        #downloader(imgDictList, family)

def downloader(imgDictList, family):
    cwd = os.getcwd()
    print(cwd)
    os.chdir(cwd+"/"+family)
    for item in imgDictList:
        break
    return

main('https://en.wikipedia.org/wiki/List_of_birds_of_Michigan')