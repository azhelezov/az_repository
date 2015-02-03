"""This program gets flights information from www.flyniki.com"""
import cStringIO
import unittest
import sys
import requests
import lxml.html
import re


def get_airport_list(first_airport_iata, second_airport_iata):
    """This function gets list of airports and IATA codes"""

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

    airport_list_request = requests.get('http://www.flyniki.com/en-RU/site/json/suggestAirport.php',
                                        params=query)
    airport_list = airport_list_request.json()['suggestList']
    for airports in airport_list:
        if airports['code'] == first_airport_iata:
            first_airport_name = airports['name']
    for airports in airport_list:
        if airports['code'] == second_airport_iata:
            second_airport_name = airports['name']
    try:
        return [first_airport_name, second_airport_name]
    except UnboundLocalError:
        return ['nonexist_airp', 'nonexist_airp'] # if user entered wrong IATA, we return
                                                  # non-existent airport names

def get_flight_information(outbound_airport_iata, return_airport_iata,
                           outbond_date, return_date=None):
    """This function gets flight information."""

    airport_list = get_airport_list(outbound_airport_iata, return_airport_iata)
    directions_option = '1' if not return_date else '' # If we are requesting for a oneway
                                                       # flight directions_option is equal to ''
    request_sid = requests.get("http://www.flyniki.com/en-RU/booking/flight/" +\
                               "vacancy.php", allow_redirects=False) # Getting sid
    cookies = dict(request_sid.cookies)
    reg_res = re.search('\?sid=(.*)$', request_sid.headers['location'])
    sid = reg_res.group(1)

    query = {'_ajax[templates][]':'main',
             '_ajax[requestParams][departure]':airport_list[0],
             '_ajax[requestParams][destination]':airport_list[1],
             '_ajax[requestParams][returnDeparture]':'',
             '_ajax[requestParams][returnDestination]':'',
             '_ajax[requestParams][outboundDate]':outbond_date,
             '_ajax[requestParams][returnDate]':return_date,
             '_ajax[requestParams][adultCount]':'1',
             '_ajax[requestParams][childCount]':'0',
             '_ajax[requestParams][infantCount]':'0',
             '_ajax[requestParams][openDateOverview]':'',
             '_ajax[requestParams][oneway]':directions_option}

    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json, text/javascript, */*',
               'Origin': 'http://www.flyniki.com'}

    request_flight_table = requests.post("http://www.flyniki.com/" +\
                                         "en-RU/booking/flight/vacancy.php?sid="+sid,
                                         allow_redirects=True, data=query,
                                         headers=headers, cookies=cookies) # Getting flight
                                                                           # prices table
    try:
        html_fragment = request_flight_table.json()['templates']['main']
        html_code = '<html><head></head><body>'+html_fragment+'</body></html>'
        html_tree = lxml.html.fromstring(html_code)
        flight_numbers = [1] if not return_date else [1, 2] # Getting flights number
        for flight in flight_numbers:
            flight_price_list = html_tree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                                ']/div[1]/table/tbody/tr/td[5]/label/div[2]/' +\
                                                'span/text()')
            time_start_list = html_tree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                              ']/div[1]/table/tbody/tr/td[2]/time[1]/text()')
            time_end_list = html_tree.xpath('.//*[@id="flighttables"]/div[' + str(flight) +\
                                            ']/div[1]/table/tbody/tr/td[2]/time[2]/text()')
            time_total_list = html_tree.xpath('//*[@id="flighttables"]/div[' + str(flight) +\
                                              ']/div[1]/table/tbody/tr/td/table/tfoot/' +\
                                              'tr/td/text()')
            if flight_price_list == []:
                print 'There are no flights for your query.'
                break
            else:
                print 'Flight number', flight
                for flight_variant in range(len(flight_price_list)): # Printing flight information
                    print "Variant number " + str(flight_variant) + ": " +\
                           flight_price_list[flight_variant] +" RUB" + ", " +\
                           time_start_list[flight_variant] + " - " +\
                           time_end_list[flight_variant] + ", " + time_total_list[flight_variant]

    except KeyError: # If there are errors, we print some information about it.

        html_error_fragment = request_flight_table.json()['error']
        html_code = '<html><head></head><body>'+html_error_fragment+'</body></html>'
        html_error_tree = lxml.html.fromstring(html_error_fragment)
        error_message = html_error_tree.xpath('//html/body/div/div/p/text()')
        print error_message[0]

def capture_output(test_outbound_iata, test_return_iata, test_outbond_date, test_return_date=None):

    """ This function captures information from the output """

    sys.stdout = cStringIO.StringIO()
    get_flight_information(test_outbound_iata, test_return_iata,
                           test_outbond_date, test_return_date)
    output_result = sys.stdout.getvalue()
    return output_result

class scraper_test(unittest.TestCase):

    """This is the test of scrapper"""

    def test1(self):

        """This function compares scrapper work result with expected one"""

        self.assertEqual(capture_output('DME', 'PAR', '2015-03'),
                         'The entered outbound flight date is invalid. Please correct your ' +\
                         'entry. \n')
        self.assertEqual(capture_output('DME', 'PAR', '2014-03-15'),
                         'The flight details you have entered are invalid. (Outbound or return' +\
                         ' flight date). Please correct your entry.\n')
        self.assertEqual(capture_output('DME', 'PA', '2015-03-15'),
                         'The choice of airport is invalid. Please correct your entry.\n')
        self.assertEqual(capture_output('DME', 'PAR', '2015-03-15'),
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
        self.assertEqual(capture_output('DME', 'PAR', '2015-03-15', '2015-03-18'),
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
                         'uration of journey: 04:55 \nVariant number 2: 39,155.00 RUB, 21:10 ' +\
                         '- 14:00,  duration of journey: 14:50 \nVariant number 3: 39,633.00 ' +\
                         'RUB, 21:10 - 19:15,  duration of journey: 20:05 \n')
        self.assertEqual(capture_output('TLV', 'PEE', '2015-03-15'),
                         'There are no flights for your query.\n')

if __name__ == '__main__':
    unittest.main()

