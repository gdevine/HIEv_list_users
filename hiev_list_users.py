'''
Python script to perform a scrape of the HIEv users list and create a readable csv file of the information

Author: Gerard Devine
Date: August 2015


- Note: This script can only be performed by a HIEv admin  

'''

import os
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text
import csv
from datetime import datetime

# Browser
br = mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Chrome')]



# Navigate to and open the hiev login page 
br.open('https://hiev.uws.edu.au/users/sign_in')

# Select the actual login form in the html
br.select_form(nr=0)

# Fill in user email and password via preset environment variables 
br.form['user[email]'] = os.environ['AdminEmail']
br.form['user[password]'] = os.environ['AdminPass']

# login to the site
br.submit()
html_text = br.open('https://hiev.uws.edu.au/users').read()
soup = BeautifulSoup(html_text)

# scrape the user information and write it out to datestamped csv file 
with open('hiev_userlist_'+datetime.now().strftime('%Y%m%d')+'.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for entry in soup.findAll('tr', {'class': 'field_bg'}):
        id = entry.find('a')['href'].split('/')[-1]
        email = entry.find('td', {'class':'email'}, 'a').text
        
        names = entry.findAll('td', {'class':'name'})
        firstname =  names[0].text
        surname =  names[1].text
        csvwriter.writerow([id, email, firstname, surname])
