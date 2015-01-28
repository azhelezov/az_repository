import requests
import lxml.html
import re
import json


def getAirportList(firstAirportIata, secondAirportIata):

    """Getting list of airports and IATA codes"""
    
    query = {'searchfor':'departures',
             'searchflightid':'0',
             'departures[]':'',
             'destinations[]':'City, airport',
             'suggestsource[0]':'activeairports',
             'withcountries':'0',
             'withoutroutings':'0',
             'promotion[id]':'',
             'promotion[type]':'',
             'routesource[0]':'airberlin',
             'routesource[1]':'partner'}
    airportListRequest = requests.get('http://www.flyniki.com/en-RU/site/json/suggestAirport.php', params = query)
    airportList = airportListRequest.json()['suggestList']
    for i in airportList:
        if i['code'] == firstAirportIata:
            firstAirportName = i['name']
    for i in airportList:
        if i['code'] == secondAirportIata:
            secondAirportName = i['name']
    return [firstAirportName, secondAirportName]
    

def getFlightInformation(outboundAirportIata, returnAirportIata, outbondDate, returnDate = None):    

    
    airportList = getAirportList(outboundAirportIata, returnAirportIata)
    directions = '1' if not returnDate else ''
    
    """Getting SID"""
    
    r1 = requests.get("http://www.flyniki.com/en-RU/booking/flight/vacancy.php",
                      allow_redirects=False);
    cookies = dict(r1.cookies)
    regRes = re.search('\?sid=(.*)$', r1.headers['location'])
    sid = regRes.group(1)
    
    query = {'_ajax[templates][]':'main',
            '_ajax[requestParams][departure]':airportList[0],
            '_ajax[requestParams][destination]':airportList[1],
            '_ajax[requestParams][returnDeparture]':'',
            '_ajax[requestParams][returnDestination]':'',
            '_ajax[requestParams][outboundDate]':outbondDate,
            '_ajax[requestParams][returnDate]':returnDate,
            '_ajax[requestParams][adultCount]':'1',
            '_ajax[requestParams][childCount]':'0',
            '_ajax[requestParams][infantCount]':'0',
            '_ajax[requestParams][openDateOverview]':'',
            '_ajax[requestParams][oneway]':directions}
        
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/javascript, */*',
            'Origin': 'http://www.flyniki.com'}
    
    """Getting flight prices table"""

    r2 = requests.post("http://www.flyniki.com/en-RU/booking/flight/vacancy.php?sid="+sid,
                       allow_redirects=True, data=query,headers=headers, cookies=cookies)
    htmlFragment = r2.json()['templates']['main']
    htmlCode = '<html><head></head><body>'+htmlFragment+'</body></html>'
    htmlTree = lxml.html.fromstring(htmlCode)

    """Printing flight information"""
    n = [1] if not returnDate else [1, 2]
    for i in n:
        print 'Flight number', i
        FligftPriceList_FlyFlex = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(i) + ']/div[1]/table/tbody/tr/td[5]/label/div[2]/span/text()')
        TimeStartList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(i) + ']/div[1]/table/tbody/tr/td[2]/time[1]/text()')
        TimeEndList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(i) + ']/div[1]/table/tbody/tr/td[2]/time[2]/text()')
        TimeTotalList = htmlTree.xpath('//*[@id="flighttables"]/div[' + str(i) + ']/div[1]/table/tbody/tr/td/table/tfoot/tr/td/text()')

        print 'FlyFlex prices', FligftPriceList_FlyFlex
        print 'Start time', TimeStartList
        print 'End time', TimeEndList
        print 'Total flight time', TimeTotalList


getFlightInformation('DME', 'PAR', '2015-01-29', '2015-01-31')
