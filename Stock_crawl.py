from lxml import html
import requests
import mysql.connector
import time

klseData = [];
totalComp = 0;

#KLSE Data class
class KLSEData:
    #Constructor
    def __init__(self,
                 date, compname, compCode, openTxt, lowTxt,
                 highTxt, lastDoneTxt, chgTxt, chgPercentTxt, volTxt,
                 buyTxt, sellTxt):
        self.date = date
        self.compname = compname
        self.compCode = compCode
        self.openTxt = openTxt
        self.lowTxt = lowTxt
        self.highTxt = highTxt
        self.lastDoneTxt = lastDoneTxt
        self.chgTxt = chgTxt
        self.chgPercentTxt = chgPercentTxt
        self.volTxt = volTxt
        self.buyTxt = buyTxt
        self.sellTxt = sellTxt

    # To return entire info of the class
    def toString(self):
        return '"' + self.date + '","' + self.compname + '","' + self.compCode + '","' + self.openTxt + '","' + self.lowTxt + '","' \
               + self.highTxt + '","' + self.lastDoneTxt + '","' + self.chgTxt + '","' + self.chgPercentTxt + '","' + self.volTxt + '","' \
               + self.buyTxt + '","' + self.sellTxt + '"'

# Handling the DB transaction
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

        sql = "INSERT INTO klse2( " \
              "thedate, " \
              "comp_name, comp_code, open, low, high, " \
              "lastDone, chg, chgPercent, vol, buy, " \
              "sell, crawl_Timestamp) VALUES ( " \
              "STR_TO_DATE('" + data.date + "', '%d %b %Y'), " \
                "%s, %s, %s, %s, %s, " \
                "%s, %s, %s, %s, %s, " \
                "%s, SYSDATE())"

        val = (str(data.compname), str(data.compCode), str(data.openTxt), str(data.lowTxt), str(data.highTxt),
               str(data.lastDoneTxt), str(data.chgTxt), str(data.chgPercentTxt), str(data.volTxt), str(data.buyTxt),
               str(data.sellTxt) )
        
        mycursor.execute(sql, val)
        self.mydb.commit()

    def checkDBCount(self):
        mycursor = self.mydb.cursor()

        sql = "select count(1) from klse2"
        countrow = mycursor.execute(sql)

        print("number of rows: ", mycursor.fetchone())

# KlSE Crawler main class
class KLSECrawler:
    def __init__(self, starting_url, param, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.param = param
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url, self.param )
        return

    def get_app_from_link(self, link, param):

        print(link+param)
        start_page = requests.get(link+param)
        tree = html.fromstring(start_page.text)

        date = tree.xpath('//*[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        compname = tree.xpath('//*[@id="slcontent_0_ileft_0_compnametxt"]/text()')[0]
        openTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        lowTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        highTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        lastDoneTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]

        tmpChgTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_chgtext"]/text()')
        if len(tmpChgTxt) == 0 :
            tmpChgTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_chgtext"]/span/text()')

        chgTxt = tmpChgTxt[0]

        chgPercentTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        volTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buyTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sellTxt = tree.xpath('//*[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]

        klseData.append(KLSEData(date[10:-2], compname, param, openTxt, lowTxt,
                 highTxt, lastDoneTxt, chgTxt, chgPercentTxt, volTxt,
                 buyTxt, sellTxt))

        return

# Main process start here:

#compCodeFile = open('compcode.txt', 'r')
# Get the company code for generating the URL
with open('compcode.txt') as f:
    alist = [line.rstrip() for line in f]

# Crawl the data
totalComp = len(alist)
for x in alist:

    if len(x) == 0:
        continue

    x = x.rstrip('\n')
    x = str.replace(x, '&', '%26')
    url = "https://www.thestar.com.my/business/marketwatch/stocks/?qcounter="
    print(x)
    try:
        crawler = KLSECrawler(url, x, 0)
        crawler.crawl()
        del crawler
    except:
        print("Fail to process: " + x)

# Prepare s file name as exported csv file
timeStr = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
klseOutputFile = open('csvdata/klsedata_' + timeStr + '.csv', 'w')
klseOutputFile.write("thedate,comp_name,comp_code,open,low,high,lastDone,chg,chgPercent,vol,buy,sell\n")

# After the klse data has been extracted, the process:
# 1. generate the csv file
# 2. insert into database
for data in klseData:
    #print(data.toString())
    dbIns = DBHandling()
    klseOutputFile.write(data.toString()+'\n')
    dbIns.insertIntoDB(data)

print("Done process")
qstr = DBHandling()
qstr.checkDBCount()
