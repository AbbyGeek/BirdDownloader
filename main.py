from bs4 import *
import requests
import os

'''
ToDo:
method to navigate to bird page and download image into correct folder
'''
#get main page html code
def main(url):
    soup = parsePage(url)
    namesDict = getLinksAndNames(soup)
    photoGrabber(namesDict)
    print("In the create folder method, there needs to be a way to return a dictionary with 'h2 name': [name, name, name]")
    print("pass this dictionary into the photodownloader method so it can match up the bird names w/ the correct folder they're supposed to be in")

def parsePage(url):
     #content of URL
    r = requests.get(url)
    #Parse HTML code
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getLinksAndNames(soup):
    nameDict = {}
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
                    name = item.text
                    url = 'https://en.wikipedia.org/' + item.find('a', href=True)['href']
                    nameDict.update({name: url})
                except:
                    print("Error with: "+item.text)
    return nameDict


def createFolders(headingName):
    #folder creations
    try:
        if headingName.endswith("[edit]"):
            headingName = headingName[:-len("[edit]")]
        os.mkdir(headingName)
    except:
        print("Folder named "+headingName+" alreay exists")

def photoGrabber(namesDict):
    for item in namesDict:
        itemUrl = namesDict[item]
        urlList = photoUrlGrabber(item, itemUrl)
        photoDownloader(item, urlList)

def photoUrlGrabber(item, itemUrl):
    imageUrlList = []
    #print name of item
    #parse item page
    itemSoup = parsePage(itemUrl)
    #find table w/ main photos/info
    itemTable = itemSoup.find(("table", {"class": "mw-parser-output"}))
    anchors = itemTable.find_all('a')
    for anchor in anchors:
        images = anchor.find_all('img')
        for image in images:
            #if image is an icon (commonly the first anchor following main pic(s)), or map.
            #this should be cleaned up
            source = image['src']
            if source == "//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/OOjs_UI_icon_edit-ltr.svg/15px-OOjs_UI_icon_edit-ltr.svg.png" or source.endswith("map.svg.png"): 
                break
            imageUrlList.append("http:" + source)
    if len(imageUrlList) == 0:
        #Need to handle when empty list is returned
        print("No URLs found for " + item)
    return(imageUrlList)

def photoDownloader(item, urlList):
    print(item)
    return



            


main('https://en.wikipedia.org/wiki/List_of_birds_of_Michigan')