# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Social Guide"

WELCOME = _("Welcome to Social Feed!")
STOP = _("Okay, see you next time!")
GENERIC_REPROMPT = _("What can I help you with?")

## TODO: create Post class here


class Comment(object):
    def __init__(self, text, up_votes, down_votes):
        self.text = text
        self.up_votes = up_votes
        self.down_votes = down_votes


class Post(object):
    def __init__(self, id, title='', up_votes=0, down_votes=0, url='', comments=list):
        self.id = id
        self.title = title
        self.up_votes = up_votes
        self.down_votes = down_votes
        self.url = url
        self.comments = comments
