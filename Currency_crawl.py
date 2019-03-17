import selenium as se

from selenium import webdriver

from lxml import html
import requests
import mysql.connector
import time
import bs4
import re
from time import sleep


currlist = []

# Currency exchange data
class CurrencyData:
    #Constructor
    def __init__(self, thedate, thetime, curName, currCode, unit, buyingVal, invBuyingVal, sellingVal, invSellingVal,
                 middleRate, invMiddleRate):

        self.thedate = thedate
        self.thetime = thetime
        self.curName = curName
        self.currCode = currCode
        self.unit = unit
        self.buyingVal = buyingVal
        self.invBuyingVal = invBuyingVal
        self.sellingVal = sellingVal
        self.invSellingVal = invSellingVal
        self.middleRate = middleRate
        self.invMiddleRate = invMiddleRate

    def toString(self):
        return '"' + self.thedate + '","' +  self.thetime + '","' +  self.curName + '","' +  self.currCode + '","' + \
               self.unit + '","' +  self.buyingVal + '","' + self.invBuyingVal + '","' +  self.sellingVal + '","' + \
               self.invSellingVal + '","' +  self.middleRate + '","' + \
               self.invMiddleRate + '"'

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

        sql = " INSERT INTO currex2( " \
              " thedate, thetime, curName, currCode, unit, " \
              " buyingVal ,invBuyingVal, sellingVal, invSellingVal, middleRate, invMiddleRate " \
              " ) VALUES ( " \
              "%s, %s, %s, %s, %s," \
              "%s, %s, %s, %s, %s, %s )"

        val = (str(data.thedate), str(data.thetime), str(data.curName), str(data.currCode), str(data.unit),
               str(data.buyingVal), str(data.invBuyingVal), str(data.sellingVal), str(data.invSellingVal),
               str(data.middleRate), str(data.invMiddleRate))

        mycursor.execute(sql, val)
        self.mydb.commit()


# Currency crawler class
class CurrencyCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def getUnitCode(self, currName):
        result = re.findall(r"\bd+", currName)

        return result



    def get_app_from_link(self, link):

        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        #driver = se.webdriver.Chrome(chrome_options=options)
        driver = webdriver.Chrome("C:/Users/QR/Downloads/chromedriver.exe")

        driver.get(link)
        innerHTML = driver.execute_script("return document.body.innerHTML")
        sleep(1)
        root=bs4.BeautifulSoup(innerHTML,"lxml")

        tree = html.fromstring(innerHTML)

        theDate = tree.xpath('//*[@id="Content1700"]/tbody/tr[1]/th[2]/b/text()')[0]
        theTime = tree.xpath('//*[@id="Session1700"]/option[@selected]/text()')[0].strip()

        for i in range(3,29):
            currName = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[1]/text()')[0]
            unit = currName.split()[0]
            currCode = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[2]/text()')[0]
            currBuying = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[3]/text()')[0]

            if len(tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[4]/text()')) != 0:
                currInvBuying = '-'
            else :
                currInvBuying = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[4]/span/text()')[0]

            currSelling = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[5]/text()')[0]

            if len(tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[6]/text()')) != 0:
                invCurrinvSeling = '-'
            else :
                invCurrinvSeling = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[6]/span/text()')[0]

            currMiddleRate = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[7]/text()')[0]

            if len(tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[8]/text()')) != 0:
                currInvMiddleRate = '-'
            else :
                currInvMiddleRate = tree.xpath('//*[@id="Content1700"]/tbody/tr['+ str(i) + ']/td[8]/span/text()')[0]

            currlist.append(CurrencyData(theDate, theTime, currName, currCode, unit, currBuying, currInvBuying,
                                         currSelling, invCurrinvSeling,currMiddleRate, currInvMiddleRate))

        return

#main function
url = "http://www.bnm.gov.my/?tpl=exchangerates"
crawler = CurrencyCrawler(url,0)
crawler.crawl()

# Prepare s file name as exported csv file
timeStr = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
currRateOutputFile = open('csvdata/currRate_' + timeStr + '.csv', 'w')
currRateOutputFile.write("thedate,thetime,curName,currCode,unit,buyingVal,invBuyingVal,sellingVal,invSellingVal,"
                     "middleRate, invMiddleRate\n")

for data in currlist:
    #print(data.toString())
    dbIns = DBHandling()
    currRateOutputFile.write(data.toString()+'\n')
    dbIns.insertIntoDB(data)

print('Done process')
