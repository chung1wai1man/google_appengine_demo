import webapp2
import urllib

from google.appengine.api import urlfetch



class MainPage(webapp2.RequestHandler):
    def get(self):
        form_fields = {"emailAddress": "oran2ge", "pswd": "123654"}
        form_data = urllib.urlencode(form_fields)
        url_homepage = 'http://www.swagbucks.com/'
        url_login = 'http://www.swagbucks.com/?cmd=sb-login&from=%2F%3Fcmd%3Dhome'

        #fetch homepage
        result_homepage = urlfetch.fetch(url=url_homepage,
                            headers={
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65',
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Charset': 'UTF-8,*;q=0.5',
                                    'Accept-Encoding': 'gzip,deflate,sdch',
                                    'Accept-Language': 'en-US',
                                    'Proxy-Connection': 'keep-alive'
                                })
        if result_homepage.status_code == 200:
#            print self.response.out.write('home:' + str(result_homepage.headers) + '\n')
            result_redirect = urlfetch.fetch(url=url_login, payload=form_data, method=urlfetch.POST,
                                follow_redirects=False,
                                headers={
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Charset': 'UTF-8,*;q=0.5',
                                    'Accept-Encoding': 'gzip,deflate,sdch',
                                    'Proxy-Connection': 'keep-alive',
                                    'Accept-Language': 'en-US',
                                    'Origin': 'http://www.swagbucks.com',
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65',
                                    'Cookie': result_homepage.headers['Set-Cookie'],
                                    'P3P': result_homepage.headers['P3P'],
                                    'Referer': url_homepage})

            if result_redirect.status_code == 302:
#                print self.response.out.write('302:' + str(result_redirect.headers) + '\n')
#                print self.response.out.write('cookie:' + result_homepage.headers['Set-Cookie'] + result_redirect.headers['Set-Cookie'] + '\n')
                result_home = urlfetch.fetch(url=result_redirect.headers['Location'],
                                headers={
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Charset': 'UTF-8,*;q=0.5',
                                    'Accept-Encoding': 'gzip,deflate,sdch',
                                    'Proxy-Connection': 'keep-alive',
                                    'Accept-Language': 'en-US',
                                    'P3P': result_homepage.headers['P3P'],
                                    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.65',
                                    'Cookie': result_redirect.headers['Set-Cookie'],
                                    'Referer': url_homepage})
                prefix = '<span class="user">'
                postfix = '</span>You\'ve won'
                content = result_home.content
                name = content[(content.index(prefix)+len(prefix)):content.index(postfix)]
                
                #TODO send email
                print self.response.out.write(name)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
