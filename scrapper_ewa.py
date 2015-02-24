import requests
from lxml import etree
from lxml import html
import lxml.html
import re
import json
import sqlite3 as lite

def getRoute():

    '''Getting cookies'''
    url_for_cookies =  'http://intranet.ttinteractive.com/TTIDOTNET/Transport/TransportNetFO/Ewa/SearchFlight.aspx'
    query_for_cookies = {'daysRange':'3',
                         'IdCurrency':'2',
                         'ServiceClass':'1',
                         'UseFlexibleDates':'true',
                         'roundTrip':'true',
                         'depCode':'AJN',
                         'arrCode':'DZA',
                         'adult':'1',
                         'child':'0',
                         'infant':'0',
                         'outboundDate':'20150227',
                         'returnDate':'20150302',
                         'langId':'2',
                         'topUrl':'http://www.ewa-air.com/moteur_tti/header_moteur_tti.html',
                         'bottomUrl':'http://www.ewa-air.com/moteur_tti/footer_en_moteur_tti.html',
                         'cssOverrideUrl':'http://www.ewa-air.com/moteur_tti/style_moteur_tti.css'}
    get_cookies = requests.post(url_for_cookies,  allow_redirects=False, data = query_for_cookies)

    '''Getting taskId'''   
    url_for_taskId =  'http://intranet.ttinteractive.com/TTIDOTNET/Transport/TransportNetFO/Ewa/' + get_cookies.headers['location']
    cookies = dict(get_cookies.cookies)
    get_task_id = requests.get(url_for_taskId,  allow_redirects=False, cookies=cookies)
    task_id_headers = get_task_id.headers
    taskId = re.search(r'taskId=(.+)&V', str(task_id_headers)).group(1)

    '''Getting additional cookie'''
    get_add_cookie = requests.get('http://intranet.ttinteractive.com/TTIDotNet/Transport'+\
                                  '/TransportNetFO/Ewa/transition/transition_2.asp', cookies=cookies)
    cookies.update(dict(get_add_cookie.cookies))

    '''Getting prices'''   
    url_for_prices = 'http://intranet.ttinteractive.com/TTIDotNet/Transport/TransportNetFO//'+\
                     'Ewa/AjaxCommandHttpHandler.ashx?ServiceDescriptor=FlexibleAvailabilityL'+\
                     'oadDataCommand&taskId='+taskId
    headers = {'Origin':'http://intranet.ttinteractive.com',
               'Referer':'http://intranet.ttinteractive.com'+get_task_id.headers['Location'],
               'Content-type':'application/json; charset=UTF-8',
               'Accept':'application/json, text/javascript, */*',
               'Accept-Language':'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'}
    data = {"OutboundDate":3,
            "ReturnDate":3,
            "AirTripDirection":0,
            "SelectedDay":True,
            "OneWayFares":False}
    
    task_id_headers = json.dumps(data, separators=(',',':'))
    get_prices = requests.post(url_for_prices, cookies=cookies, headers = headers, data=task_id_headers)    

getRoute()
