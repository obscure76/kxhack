# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Social Guide"

WELCOME = _("Welcome to Social Feed!")
STOP = _("Okay, see you next time!")
GENERIC_REPROMPT = _("What can I help you with?")


## TODO: create Post class here


class Comment(object):
    def __init__(self, text='', up_votes=0, down_votes=0, author=''):
        self.text = text
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.author = author

    def __str__(self):
        s = ''
        s += "text=%s," % self.text
        s += "up_votes=%s," % self.up_votes
        s += "down_votes=%s," % self.down_votes
        s += "author=%s," % self.author
        return s


class Post(object):
    def __init__(self, id, title='', up_votes=0, down_votes=0, url='', comments=list,
                 author='', sub_reddit_name=''):
        self.id = id
        self.title = title
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.url = url
        self.comments = comments
        self.author = author
        self.sub_reddit_name = sub_reddit_name

    def __str__(self):
        s = ''
        s += "id=%s," % self.id
        s += "title=%s," % self.title
        s += "up_votes=%s,"% self.up_votes
        s += "down_votes=%s,"% self.down_votes
        s += "url=%s,"% self.url
        s += "comments=%s,"% self.comments
        s += "author=%s," % self.author
        s += "sub_reddit_name=%s" % self.sub_reddit_name
        return s
