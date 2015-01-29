"""This program gets flights information from www.flyniki.com"""
import sys
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
    for airports in airportList:
        if airports['code'] == firstAirportIata:
            firstAirportName = airports['name']
    for airports in airportList:
        if airports['code'] == secondAirportIata:
            secondAirportName = airports['name']
    try:
        return [firstAirportName, secondAirportName]
    except UnboundLocalError:
        print "You entered wrong IATA code. Please try again."
        sys.exit(1)

def getFlightInformation(outboundAirportIata, returnAirportIata, outbondDate, returnDate = None):    


    airportList = getAirportList(outboundAirportIata, returnAirportIata)

    """If we are requesting for a oneway flight directionsOption is equal to '' """

    directionsOption = '1' if not returnDate else '' 
        
    """Getting SID"""
    
    requestSid = requests.get("http://www.flyniki.com/en-RU/booking/flight/vacancy.php",
                          allow_redirects=False);
    cookies = dict(requestSid.cookies)
    regRes = re.search('\?sid=(.*)$', requestSid.headers['location'])
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
             '_ajax[requestParams][oneway]':directionsOption}
        
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json, text/javascript, */*',
               'Origin': 'http://www.flyniki.com'}
    
    """Getting flight prices table"""

    requestFlightTable = requests.post("http://www.flyniki.com/en-RU/booking/flight/vacancy.php?sid="+sid,
                                       allow_redirects=True, data=query,headers=headers, cookies=cookies)
    try:
        htmlFragment = requestFlightTable.json()['templates']['main']
        htmlCode = '<html><head></head><body>'+htmlFragment+'</body></html>'
        htmlTree = lxml.html.fromstring(htmlCode)

        """Printing flight information"""
            
        flightNumbers = [1] if not returnDate else [1, 2]
        for flight in flightNumbers:        
            FligftPriceList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                             ']/div[1]/table/tbody/tr/td[5]/label/div[2]/span/text()')
            TimeStartList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                               ']/div[1]/table/tbody/tr/td[2]/time[1]/text()')
            TimeEndList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                             ']/div[1]/table/tbody/tr/td[2]/time[2]/text()')
            TimeTotalList = htmlTree.xpath('//*[@id="flighttables"]/div[' + str(flight) +\
                                               ']/div[1]/table/tbody/tr/td/table/tfoot/tr/td/text()')
            if FligftPriceList == []:
                print 'There are no flights for your query'
                break
            else:
                print 'Flight number', flight
                for flightVariant in range(len(FligftPriceList)):
                    print "Variant number " + str(flightVariant) + ": " +\
                            FligftPriceList[flightVariant] +" RUB" + ", " +\
                              TimeStartList[flightVariant] + " - " +\
                              TimeEndList[flightVariant] + ", " + TimeTotalList[flightVariant]

    except KeyError:
        htmlErrorFragment = requestFlightTable.json()['error']
        htmlCode = '<html><head></head><body>'+htmlErrorFragment+'</body></html>'
        htmlErrorTree = lxml.html.fromstring(htmlErrorFragment)
        errorMessage = htmlErrorTree.xpath('//html/body/div/div/p/text()')
        print errorMessage[0]


getFlightInformation('DME', 'PAR', '2015-02-01', '2015-02-05')
