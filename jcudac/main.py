#import os

import webapp2
import re

import unit1
import unit2
import unit3
import unit4
import unit5
import unit6
import wiki

PAGE_RE = r'((?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([(r'/', unit1.MainPage),
                               (r'/Unit2/rot13', unit2.Rot13),
                               (r'/signup',unit2.Sign_up),
                               (r'/welcome',unit2.Welcome),
                               (r'/blog', unit3.blog),
                               (r'/blog/newpost', unit3.newpost),
                               (r'/blog/(\d+)', unit3.blogentry),
                               ('/blog/signup', unit4.blog_sign_up),
                               ('/blog/welcome', unit4.BlogWelcome),
                               ('/blog/login', unit4.BlogLogin),
							   ('/blog/logout', unit4.BlogLogout),
							   (r'/blog/.json', unit5.BlogWithJSON),
							   (r'/blog/(\d+).json', unit5.BlogEntryWithJSON),
							   ('/blog/flush', unit6.BlogCacheFlush),
							   ('/wiki', wiki.WikiMain),
							   ('/wiki/signup', wiki.Signup),
                               ('/wiki/login', wiki.Login),
                               ('/wiki/logout', wiki.Logout),
                               ('/wiki/_edit/' + PAGE_RE, wiki.EditPage),
                               ('/wiki/' + PAGE_RE, wiki.WikiPage),
							   ('/wiki_init', wiki.WikiInit)
							   ],debug=True)
