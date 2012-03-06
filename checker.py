import webapp2
import urllib

from google.appengine.api import urlfetch
from google.appengine.api import mail
#TODO logging and handle exception
FORM_FIELDS = {'emailAddress': 'oran2ge', 'pswd': '123654'}
FORM_DATA = urllib.urlencode(FORM_FIELDS)
URL_HOMEPAGE = 'http://www.swagbucks.com/'
URL_LOGIN = 'http://www.swagbucks.com/?cmd=sb-login&from=%2F%3Fcmd%3Dhome'
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 Chrome/17.0.963.65',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US',
            'Proxy-Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
          }

PREFIX = '<span class="user">'
POSTFIX = '</span>You\'ve won'
LUCKYNAME = 'WS3389'


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
                                    'P3P': html_homepage.headers['P3P'],
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
                                    'P3P': html_homepage.headers['P3P'],
                                    'User-Agent': HEADERS['User-Agent'],
                                    'Referer': URL_HOMEPAGE
                                    })
                content = html_home.content

                name = content[(content.index(PREFIX)+len(PREFIX)):content.index(POSTFIX)].upper()
                #Send email
                if name == LUCKYNAME:
                    Emailme()                    

                print self.response.out.write('LuckyMan:' + name)

def Emailme():
    message = mail.EmailMessage(sender='no-rely@code-checker.appspotmail.com',
                                subject='Swagbuck Winner!')

    message.to = 'niuben0405@gmail.com'
    message.body = 'See the subject'

    message.send()        

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
