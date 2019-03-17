import requests
import mysql.connector
from xml.etree import ElementTree as ET
import time
from unidecode import unidecode

feeddataList = []

class NewsFeedsData:
    def __init__(self, title, link, description, pubDate):
        self.title = title
        self.link = link
        self.description = description
        self.pubDate = pubDate

    def toString(self):
        return '"' + str(self.title) + '","'+ str(self.link) + '","'+ str(self.description) + '","'+ str(self.pubDate)

class NewsFeedCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def reformatStr(self, inputStr):
        return unidecode(inputStr).replace('\n', '').replace('\r', '')

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        #print(start_page.text)
        # tree = html.fromstring(start_page.text)

        root = ET.fromstring(start_page.text)
        levels = root.findall('.//item')

        #print(levels)

        for level in levels:
            title = self.reformatStr(level.find('title').text)
            link = self.reformatStr(level.find('link').text)
            description = self.reformatStr(level.find('description').text)
            pubDate = self.reformatStr(level.find('pubDate').text)
            print("====================================")
            print("1)" + title)
            print("2)" + link)
            print("3)" + description)
            print("4)" + pubDate)
            feeddata = NewsFeedsData(title, link, description, pubDate)
            feeddataList.append(feeddata)

# Db handling
class DBHandling:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='mdsklse'
        )

    def insertIntoDB(self, data):
        mycursor = self.mydb.cursor()

        sql = " INSERT INTO mdsklse.newsdata( " \
              " title, link, description, pubDate ) " \
              " VALUES (" \
              " %s, %s, %s, %s " \
              ")"

        val = (str(data.title), str(data.link), str(data.description), str(data.pubDate))

        mycursor.execute(sql, val)
        self.mydb.commit()


links = ['https://www.theedgemarkets.com/mytopstories.rss', 'https://www.malaysiakini.com/en/news.rss']

for strlink in links:
    newsFeedCrawler = NewsFeedCrawler(strlink, 0)
    newsFeedCrawler.crawl()


# Prepare s file name as exported csv file
timeStr = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
newsdataFile = open('csvdata/newsdata_' + timeStr + '.csv', 'w')
newsdataFile.write("title, link, description, pubDate\n")

dbIns = DBHandling()
for fdata in feeddataList:
    print(fdata.toString())
    newsdataFile.write(fdata.toString() + '\n')
    dbIns.insertIntoDB(fdata)

