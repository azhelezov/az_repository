"""This program gets flights information from www.flyniki.com"""
import cStringIO
import unittest
import sys
import requests
import lxml.html
import re


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

    airportListRequest = requests.get('http://www.flyniki.com/en-RU/site/json/suggestAirport.php',
                                      params=query)
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
        return ['q', 'q'] # if user entered wrong IATA, we return non-existent airport names

def getFlightInformation(outboundAirportIata, returnAirportIata, outbondDate, returnDate=None):

    """This function gets flight information."""

    airportList = getAirportList(outboundAirportIata, returnAirportIata)

    """If we are requesting for a oneway flight directionsOption is equal to '' """

    directionsOption = '1' if not returnDate else ''

    """Getting SID"""

    requestSid = requests.get("http://www.flyniki.com/en-RU/booking/flight/vacancy.php",
                              allow_redirects=False)
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

    requestFlightTable = requests.post("http://www.flyniki.com/en-RU/booking/flight/" +\
                                       "vacancy.php?sid="+sid, allow_redirects=True, data=query,
                                       headers=headers, cookies=cookies)
    try:
        htmlFragment = requestFlightTable.json()['templates']['main']
        htmlCode = '<html><head></head><body>'+htmlFragment+'</body></html>'
        htmlTree = lxml.html.fromstring(htmlCode)

        """Printing flight information"""

        flightNumbers = [1] if not returnDate else [1, 2] # Getting flights number
        for flight in flightNumbers:
            FligftPriceList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                             ']/div[1]/table/tbody/tr/td[5]/label/div[2]/' +\
                                             'span/text()')
            TimeStartList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                           ']/div[1]/table/tbody/tr/td[2]/time[1]/text()')
            TimeEndList = htmlTree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                         ']/div[1]/table/tbody/tr/td[2]/time[2]/text()')
            TimeTotalList = htmlTree.xpath('//*[@id="flighttables"]/div[' + str(flight) +\
                                           ']/div[1]/table/tbody/tr/td/table/tfoot/' +\
                                           'tr/td/text()')
            if FligftPriceList == []:
                print 'There are no flights for your query.'
                break
            else:
                print 'Flight number', flight
                for flightVariant in range(len(FligftPriceList)):
                    print "Variant number " + str(flightVariant) + ": " +\
                            FligftPriceList[flightVariant] +" RUB" + ", " +\
                              TimeStartList[flightVariant] + " - " +\
                              TimeEndList[flightVariant] + ", " + TimeTotalList[flightVariant]

    except KeyError:

        """If there are errors, we print some information about it"""

        htmlErrorFragment = requestFlightTable.json()['error']
        htmlCode = '<html><head></head><body>'+htmlErrorFragment+'</body></html>'
        htmlErrorTree = lxml.html.fromstring(htmlErrorFragment)
        errorMessage = htmlErrorTree.xpath('//html/body/div/div/p/text()')
        print errorMessage[0]

def captureOutput(testOutboundIata, testReturnIata, testoutbondDate, testreturnDate=None):

    """ Capturing information from the output """

    stdout_ = sys.stdout
    stream = cStringIO.StringIO()
    sys.stdout = stream
    getFlightInformation(testOutboundIata, testReturnIata, testoutbondDate, testreturnDate)
    sys.stdout = stdout_
    outputResult = stream.getvalue()
    return outputResult

class XrangeTest(unittest.TestCase):

    """This is the test of scrapper"""

    def test1(self):

        """This function compares scrapper work result with expected one"""

        self.assertEqual(captureOutput('DME', 'PAR', '2015-03'),
                         'The entered outbound flight date is invalid. Please correct your ' +\
                         'entry. \n')
        self.assertEqual(captureOutput('DME', 'PAR', '2014-03-15'),
                         'The flight details you have entered are invalid. (Outbound or return' +\
                         ' flight date). Please correct your entry.\n')
        self.assertEqual(captureOutput('DME', 'PA', '2015-03-15'),
                         'The choice of airport is invalid. Please correct your entry.\n')
        self.assertEqual(captureOutput('DME', 'PAR', '2015-03-15'),
                         'Flight number 1\nVariant number 0: 46,595.00 RUB, 06:35 - 18:45,  ' +\
                         'duration of journey: 14:10 \nVariant number 1: 46,595.00 RUB, 06:35 ' +\
                         '- 18:45,  duration of journey: 14:10 \nVariant number 2: 46,106.00 ' +\
                         'RUB, 06:35 - 20:15,  duration of journey: 15:40 \nVariant number 3: ' +\
                         '46,595.00 RUB, 06:35 - 20:55,  duration of journey: 16:20 \nVariant ' +\
                         'number 4: 46,595.00 RUB, 06:35 - 20:55,  duration of journey: 16:20 ' +\
                         '\nVariant number 5: 47,073.00 RUB, 08:30 - 18:45,  duration of jour' +\
                         'ney: 12:15 \nVariant number 6: 47,073.00 RUB, 08:30 - 18:45,  durat' +\
                         'ion of journey: 12:15 \nVariant number 7: 45,835.00 RUB, 08:30 - 20' +\
                         ':25,  duration of journey: 13:55 \nVariant number 8: 45,835.00 RUB, ' +\
                         '08:30 - 20:25,  duration of journey: 13:55 \nVariant number 9: 47,0' +\
                         '73.00 RUB, 08:30 - 20:55,  duration of journey: 14:25 \nVariant num' +\
                         'ber 10: 47,073.00 RUB, 08:30 - 20:55,  duration of journey: 14:25 ' +\
                         '\nVariant number 11: 45,835.00 RUB, 11:40 - 20:25,  duration of jou' +\
                         'rney: 10:45 \nVariant number 12: 45,835.00 RUB, 11:40 - 20:25,  dur' +\
                         'ation of journey: 10:45 \nVariant number 13: 45,322.00 RUB, 14:45 - ' +\
                         '20:25,  duration of journey: 07:40 \nVariant number 14: 46,071.00 R' +\
                         'UB, 14:45 - 08:10,  duration of journey: 19:25 \nVariant number 15: ' +\
                         '40,977.00 RUB, 17:00 - 20:25,  duration of journey: 05:25 \nVariant ' +\
                         'number 16: 46,106.00 RUB, 17:00 - 08:10,  duration of journey: 17:10 \n')
        self.assertEqual(captureOutput('DME', 'PAR', '2015-03-15', '2015-03-18'),
                         'Flight number 1\nVariant number 0: 38,560.00 RUB, 06:35 - 18:45,  d' +\
                         'uration of journey: 14:10 \nVariant number 1: 38,560.00 RUB, 06:35 ' +\
                         '- 18:45,  duration of journey: 14:10 \nVariant number 2: 39,038.00 ' +\
                         'RUB, 08:30 - 18:45,  duration of journey: 12:15 \nVariant number 3:' +\
                         ' 39,038.00 RUB, 08:30 - 18:45,  duration of journey: 12:15 \nVariant' +\
                         ' number 4: 37,800.00 RUB, 08:30 - 20:25,  duration of journey: 13:55' +\
                         ' \nVariant number 5: 37,800.00 RUB, 08:30 - 20:25,  duration of jour' +\
                         'ney: 13:55 \nVariant number 6: 37,800.00 RUB, 11:40 - 20:25,  durat' +\
                         'ion of journey: 10:45 \nVariant number 7: 37,800.00 RUB, 11:40 - 20' +\
                         ':25,  duration of journey: 10:45 \nVariant number 8: 37,287.00 RUB,' +\
                         ' 14:45 - 20:25,  duration of journey: 07:40 \nVariant number 9: 32,9' +\
                         '42.00 RUB, 17:00 - 20:25,  duration of journey: 05:25 \nFlight numb' +\
                         'er 2\nVariant number 0: 40,767.00 RUB, 07:35 - 19:15,  duration of ' +\
                         'journey: 09:40 \nVariant number 1: 35,007.00 RUB, 09:20 - 16:15,  d' +\
                         'uration of journey: 04:55 \nVariant number 2: 39,155.00 RUB, 21:00 ' +\
                         '- 14:00,  duration of journey: 15:00 \nVariant number 3: 39,633.00 ' +\
                         'RUB, 21:00 - 16:15,  duration of journey: 17:15 \n')
        self.assertEqual(captureOutput('TLV', 'PEE', '2015-03-15'),
                         'There are no flights for your query.\n')

if __name__ == '__main__':
    unittest.main()

