# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Social Feeds"

WELCOME_PROMPT = _("Welcome to Social Feeds! You can start by asking, what's trending")
SORRY_EMPTY_PROMPT = _("Sorry, we are unable to provide content at this time")
GOODBYE_PROMPT = _("Goodbye! See you next time!")

# TODO: create Post class here


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
    def __init__(self, id, title='', text = '', up_votes=0, down_votes=0, url='', comments=[],
                 author='', sub_reddit_name=''):
        self.id = id
        self.title = title
        self.text = text
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
        s += "text=%s," % self.text
        s += "up_votes=%s,"% self.up_votes
        s += "down_votes=%s,"% self.down_votes
        s += "url=%s,"% self.url
        s += "comments=%s," % self.comments
        s += "author=%s," % self.author
        s += "sub_reddit_name=%s" % self.sub_reddit_name
        return s


UTIL_DATA = {
    "welcome_image": "https://media.wired.com/photos/5abece0a9ccf76090d775185/"
                     "master/w_1920,c_limit/hangoutsscreen_2.jpg"
}

MOCK_POST_DATA = {
    "id": "2234",
    "title": "Heard you like Cosplay girls.",
    "up_votes": "21700",
    "down_votes": "333",
    "url": "https://preview.redd.it/dz83osl2op931.jpg"
           "?width=960&crop=smart&auto=webp&s=82d510492631558f71e69332af75c35adafd2864",
    "comments": [
        {
            "text": "Dad please stop posting your cosplay photos, you’re embarrassing me.",
            "up_votes": "3000",
            "down_votes": "12"
        },
        {
            "text": "Why halo there",
            "up_votes": "710",
            "down_votes": "32"
        },
        {
            "text": "-*Sigh* Opens hatch",
            "up_votes": "1100",
            "down_votes": "234"
        }
    ]
}
