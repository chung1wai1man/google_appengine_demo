import webapp2
import urllib

from google.appengine.api import urlfetch
from google.appengine.api import mail
#TODO logging and handle exception
FORM_FIELDS = {'name': 'test', 'pwd': 'test'}
FORM_DATA = urllib.urlencode(FORM_FIELDS)
URL_HOMEPAGE = 'http://www.example.com/'
URL_LOGIN = 'http://www.example.com/?login'
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 Chrome/17.0.963.65',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US',
            'Proxy-Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
          }


class MainPage(webapp2.RequestHandler):
    def get(self):
        #get homepage
        html_homepage = urlfetch.fetch(url=URL_HOMEPAGE,
                            headers={
                                    'Accept': HEADERS['Accept'],
                                    'Accept-Charset': HEADERS['Accept-Charset'],
                                    'Accept-Encoding': HEADERS['Accept-Encoding'],
                                    'Accept-Language': HEADERS['Accept-Language'],
                                    'Proxy-Connection': HEADERS['Proxy-Connection'],
                                    'User-Agent': HEADERS['User-Agent'],
                                    })

        #Cookies are not handled upon redirection, so set follow_redirects false
        if html_homepage.status_code == 200:
            html_redirect = urlfetch.fetch(url=URL_LOGIN, payload=FORM_DATA, method=urlfetch.POST,
                                follow_redirects=False,
                                headers={
                                    'Accept': HEADERS['Accept'],
                                    'Accept-Charset': HEADERS['Accept-Charset'],
                                    'Accept-Encoding': HEADERS['Accept-Encoding'],
                                    'Accept-Language': HEADERS['Accept-Language'],
                                    'Content-Type': HEADERS['Content-Type'],
                                    'Cookie': html_homepage.headers['Set-Cookie'],
                                    'Origin': URL_HOMEPAGE,
                                    'Proxy-Connection': HEADERS['Proxy-Connection'],
                                    'User-Agent': HEADERS['User-Agent'],
                                    'Referer': URL_HOMEPAGE
                                    })
            #If Login Succefully
            if html_redirect.status_code == 302:
                html_home = urlfetch.fetch(url=html_redirect.headers['Location'],
                                headers={
                                    'Accept': HEADERS['Accept'],
                                    'Accept-Charset': HEADERS['Accept-Charset'],
                                    'Accept-Encoding': HEADERS['Accept-Encoding'],
                                    'Accept-Language': HEADERS['Accept-Language'],
                                    'Cookie': html_redirect.headers['Set-Cookie'],
                                    'Proxy-Connection': HEADERS['Proxy-Connection'],
                                    'User-Agent': HEADERS['User-Agent'],
                                    'Referer': URL_HOMEPAGE
                                    })
                content = html_home.content
                #parse content,anything you like 
                #Send email
                if content == '*****':
                    Emailme()                    

                print self.response.out.write('content:' + content)

def Emailme():
    message = mail.EmailMessage(sender='no-rely@appid.appspotmail.com',
                                subject='hello world!')

    message.to = 'test@gmail.com'
    message.body = 'bingo'

    message.send()        

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
