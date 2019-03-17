from lxml import html
import requests
import time
import mysql.connector

fundamentalList = []
problemComp = []

class KLSEFundamentalCrawler:
    def __init__(self, starting_url, depth, compCode):
        self.starting_url = starting_url + compCode
        self.depth = depth
        self.apps = []
        self.compCode = compCode

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)
        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]

        _stock_code = tree.xpath('//*[@id="slcontent_0_ileft_0_info"]/ul/div[1]/li[2]/text()')[0]
        _stock_name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]


        for cnt in range(2,5):

            _the_date = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financetableheaad"]/tr/td[' + str(cnt) + ']/span/text()')[0]
            _Net_Turnover_Net_Sales_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[2]/td[' + str(cnt) + ']/text()')[0]
            _EBITDA_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[3]/td[' + str(cnt) + ']/text()')[0]
            _EBIT_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[4]/td[' + str(cnt) + ']/text()')[0]
            _Net_Profit_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[5]/td[' + str(cnt) + ']/text()')[0]
            _Intangibles_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[7]/td[' + str(cnt) + ']/text()')[0]
            _Fixed_Assets_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[8]/td[' + str(cnt) + ']/text()')[0]
            _Long_Term_Investment_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[9]/td[' + str(cnt) + ']/text()')[0]
            _Stocks_Inventories_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[10]/td[' + str(cnt) + ']/text()')[0]
            _Cash_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[11]/td[' + str(cnt) + ']/text()')[0]
            _Current_Liabilities_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[12]/td[' + str(cnt) + ']/text()')[0]
            _Long_Term_Debt_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[13]/td[' + str(cnt) + ']/text()')[0]
            _Provisions_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[14]/td[' + str(cnt) + ']/text()')[0]
            _Minorities_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[15]/td[' + str(cnt) + ']/text()')[0]
            _Total_Shareholders_Equity_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[16]/td[' + str(cnt) + ']/text()')[0]
            _Operating_Margin_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[18]/td[' + str(cnt) + ']/text()')[0]
            _Return_on_Equity_Capital_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[19]/td[' + str(cnt) + ']/text()')[0]
            _Net_Profit_Margin_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[20]/td[' + str(cnt) + ']/text()')[0]
            _Current_Ratio_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[21]/td[' + str(cnt) + ']/text()')[0]
            _Debt_to_Capital_at_Book_str = tree.xpath('//*[@id="slcontent_0_ileft_0_stockprofile_fundamentals_financialtable"]/tr[22]/td[' + str(cnt) + ']/text()')[0]

            sf = Stock_Fundamental(_the_date,
                     _stock_code,
                     self.compCode,
                     _Net_Turnover_Net_Sales_str,
                     _EBITDA_str,
                     _EBIT_str,
                     _Net_Profit_str,
                     _Intangibles_str,
                     _Fixed_Assets_str,
                     _Long_Term_Investment_str,
                     _Stocks_Inventories_str,
                     _Cash_str,
                     _Current_Liabilities_str,
                     _Long_Term_Debt_str,
                     _Provisions_str,
                     _Minorities_str,
                     _Total_Shareholders_Equity_str,
                     _Operating_Margin_str,
                     _Return_on_Equity_Capital_str,
                     _Net_Profit_Margin_str,
                     _Current_Ratio_str,
                     _Debt_to_Capital_at_Book_str)

            fundamentalList.append(sf)


class Stock_Fundamental:
    def __init__(self,
                 _the_date,
                 _stock_code,
                 _comp_code,
                 _Net_Turnover_Net_Sales,
                 _EBITDA,
                 _EBIT,
                 _Net_Profit,
                 _Intangibles,
                 _Fixed_Assets,
                 _Long_Term_Investment,
                 _Stocks_Inventories,
                 _Cash,
                 _Current_Liabilities,
                 _Long_Term_Debt,
                 _Provisions,
                 _Minorities,
                 _Total_Shareholders_Equity,
                 _Operating_Margin,
                 _Return_on_Equity_Capital,
                 _Net_Profit_Margin,
                 _Current_Ratio,
                 _Debt_to_Capital_at_Book):
        self._the_date = _the_date
        self._stock_code = _stock_code
        self._comp_code = _comp_code
        self._Net_Turnover_Net_Sales = _Net_Turnover_Net_Sales
        self._EBITDA = _EBITDA
        self._EBIT = _EBIT
        self._Net_Profit = _Net_Profit
        self._Intangibles = _Intangibles
        self._Fixed_Assets = _Fixed_Assets
        self._Long_Term_Investment = _Long_Term_Investment
        self._Stocks_Inventories = _Stocks_Inventories
        self._Cash = _Cash
        self._Current_Liabilities = _Current_Liabilities
        self._Long_Term_Debt = _Long_Term_Debt
        self._Provisions = _Provisions
        self._Minorities = _Minorities
        self._Total_Shareholders_Equity = _Total_Shareholders_Equity
        self._Operating_Margin = _Operating_Margin
        self._Return_on_Equity_Capital = _Return_on_Equity_Capital
        self._Net_Profit_Margin = _Net_Profit_Margin
        self._Current_Ratio = _Current_Ratio
        self._Debt_to_Capital_at_Book = _Debt_to_Capital_at_Book

    def __str__(self):
        return (
            "Date: " + self._the_date +
            "\r\nNet_Turnover_Net_Sales: " + self._Net_Turnover_Net_Sales +
            "\r\nEBITDA: " + self._EBITDA +
            "\r\nEBIT: " + self._EBIT +
            "\r\nNet_Profit: " + self._Net_Profit +
            "\r\nIntangibles: " + self._Intangibles +
            "\r\nFixed_Assets: " + self._Fixed_Assets +
            "\r\nLong_Term_Investment: " + self._Long_Term_Investment +
            "\r\nStocks_Inventories: " + self._Stocks_Inventories +
            "\r\nCash: " + self._Cash +
            "\r\nCurrent_Liabilities: " + self._Current_Liabilities +
            "\r\nLong_Term_Debt: " + self._Long_Term_Debt +
            "\r\nProvisions: " + self._Provisions +
            "\r\nMinorities: " + self._Minorities +
            "\r\nTotal_Shareholders_Equity: " + self._Total_Shareholders_Equity +
            "\r\nOperating_Margin (%): " + self._Operating_Margin +
            "\r\nReturn_on_Equity_Capital (%): " + self._Return_on_Equity_Capital +
            "\r\nNet_Profit_Margin: " + self._Net_Profit_Margin +
            "\r\nCurrent_Ratio: " + self._Current_Ratio +
            "\r\nDebt_to_Capital_at_Book: " + self._Debt_to_Capital_at_Book + "\r\n");

    def toString(self):
        return '"'+ self._the_date + '","' + self._stock_code + '","' + self._comp_code + '","' + self._Net_Turnover_Net_Sales + '","' + self._EBITDA \
               + '","' + self._EBIT + '","' + self._Net_Profit + '","' + self._Intangibles + '","' + self._Fixed_Assets + '","' + self._Long_Term_Investment\
               + '","' + self._Stocks_Inventories + '","' + self._Cash + '","' + self._Current_Liabilities + '","' + self._Long_Term_Debt + '","' + self._Provisions\
               + '","' + self._Minorities + '","' + self._Total_Shareholders_Equity + '","' + self._Operating_Margin + '","' + self._Return_on_Equity_Capital + '","' + self._Net_Profit_Margin \
               + '","' + self._Current_Ratio + '","' + self._Debt_to_Capital_at_Book + '"'

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

        sql = " INSERT INTO mdsklse.fundamental " \
              " (theDate, stock_code, comp_code, net_Turnover_Net_Sales, EBITDA, " \
              " EBIT, Net_Profit, Intangibles, Fixed_Assets, Long_Term_Investment, " \
              " Stocks_Inventories, Cash, Current_Liabilities, Long_Term_Debt, Provisions, " \
              " Minorities, Total_Shareholders_Equity, Operating_Margin, Return_on_Equity_Capital, Net_Profit_Margin, " \
              " Current_Ratio, Debt_to_Capital_at_Book ) " \
              " VALUES " \
              " (" \
              " %s, %s, %s, %s, %s, " \
              " %s, %s, %s, %s, %s, " \
              " %s, %s, %s, %s, %s, " \
              " %s, %s, %s, %s, %s, " \
              " %s, %s )"

        val = (
            str(data._the_date), str(data._stock_code), str(data._comp_code), str(data._Net_Turnover_Net_Sales), str(data._EBITDA),
            str(data._EBIT), str(data._Net_Profit), str(data._Intangibles), str(data._Fixed_Assets), str(data._Long_Term_Investment),
            str(data._Stocks_Inventories), str(data._Cash), str(data._Current_Liabilities), str(data._Long_Term_Debt), str(data._Provisions),
            str(data._Minorities), str(data._Total_Shareholders_Equity), str(data._Operating_Margin), str(data._Return_on_Equity_Capital), str(data._Net_Profit_Margin), \
            str(data._Current_Ratio), str(data._Debt_to_Capital_at_Book)
        )

        mycursor.execute(sql, val)
        self.mydb.commit()


# crawling process - 1) get the company code from the company code list file
with open('compcode.txt') as f:
    alist = [line.rstrip() for line in f]

# Crawl the data by each of the company code
totalComp = len(alist)

for x in alist:
    if len(x) == 0:
        continue
    try:
        x = x.rstrip('\n')
        x = str.replace(x, '&', '%26')
        url = "https://www.thestar.com.my/business/marketwatch/stocks/?qcounter="
        print(x)
        crawler = KLSEFundamentalCrawler(url, 0, x)
        crawler.crawl()
        del crawler
    except:
        print("Unable to crawl: " + x)
        problemComp.append(x)


"""
crawler = KLSEFundamentalCrawler("https://www.thestar.com.my/business/marketwatch/stocks/?qcounter=", 0, '3A')
crawler.crawl()
"""

# Prepare s file name as exported csv file
timeStr = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
fundOutputFile = open('csvdata/fundamental2_' + timeStr + '.csv', 'w')
fundOutputFile.write("theDate,stock_code,comp_code,net_Turnover_Net_Sales,EBITDA," \
              "EBIT,Net_Profit,Intangibles,Fixed_Assets,Long_Term_Investment," \
              "Stocks_Inventories,Cash,Current_Liabilities,Long_Term_Debt,Provisions," \
              "Minorities,Total_Shareholders_Equity,Operating_Margin,Return_on_Equity_Capital,Net_Profit_Margin," \
              "Current_Ratio,Debt_to_Capital_at_Book\n")

# Generate the csv file and insert into database
dbIns = DBHandling()
for f in fundamentalList:
    fundOutputFile.write(f.toString()+'\n')
    dbIns.insertIntoDB(f)

print("Done the process")


if len(problemComp) > 0 :
    print("Problem Company:")
    for pbComp in problemComp:
        print(pbComp)

"""
_Net_Turnover_Net_Sales
_EBITDA
_EBIT
_Net_Profit
_Intangibles
_Fixed_Assets
_Long_Term_Investment
_Stocks_Inventories
_Cash
_Current_Liabilities
_Long_Term_Debt
_Provisions
_Minorities
_Total_Shareholders_Equity
_Operating_Margin(%)
_Return_on_Equity_Capital(%)
_Net_Profit_Margin
_Current_Ratio	
_Debt_to_Capital_at_Book

"""

