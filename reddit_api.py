import praw
import constant
import sys
import os
from data import Comment, Post
from cachetools import cached, TTLCache
cache = TTLCache(maxsize=100, ttl=30)

reddit = praw.Reddit(client_id='Wffd8ItbvTdUwQ',
                     client_secret="KJ7pQHa03HGlr1_Mhi35mXeixMw",
                     user_agent='TestUser')


reddit_with_user_details = praw.Reddit(client_id='fA5TZDgaxeH3YQ',
                                       client_secret="r0B8i0yF7RTZOG1yMRtbL_bj9vY",
                                       password="testtest",
                                       user_agent='AlexaSocialFeed',
                                       username="testtest")


def print_exception_details(e, msg=''):
    print(msg, e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def get_hot_trending_post_titles(sub_reddit, number_of_posts=constant.HOT_TRENDING_POSTS_COUNT):
    titles = []
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=number_of_posts):
            titles.append(submission.title)
    except Exception as e:
        print_exception_details(e)
        return []
    return titles


def get_subreddits_by_name(name):
    print(name)
    pass


def get_subreddit_titles_by_name(sub_reddit_name):
    titles = []
    try:
        for submission in reddit.subreddits.search_by_name(sub_reddit_name):
            titles.append(submission.title)
    except Exception as e:
        print_exception_details(e)
        return []
    return titles


def get_hot_posts(sub_reddit_name, number=constant.HOT_TRENDING_POSTS_COUNT):
    print("Getting", number, "hot subreddit posts for ", sub_reddit_name)
    posts = []
    try:
        for submission in reddit.subreddit(sub_reddit_name).hot(limit=number):
            try:
                print("submission: ", submission.id)
                if getattr(submission, 'over_18', False):
                    continue
                if getattr(submission, 'author', None):
                    author = getattr(submission.author, 'name', '')
                else:
                    author = ''
                print("author: ", author)
                post = Post(title=getattr(submission, 'title', ''),
                            text=getattr(submission, 'selftext', ''),
                            up_votes=getattr(submission, 'ups', 0),
                            down_votes=getattr(submission, 'downs', 0),
                            url=getattr(submission, 'url', ''),
                            id=getattr(submission, 'id', ''),
                            author=author,
                            sub_reddit_name=sub_reddit_name)
                print("Pre cleanup", post)
                if post.author == 'AutoModerator' or len(post.text) > constant.MAX_ALLOWED_CHARS_IN_POST:
                    continue
                # for c in submission.comments:
                #     try:
                #         if getattr(c, 'author', None):
                #             author = getattr(c.author, 'name', '')
                #         else:
                #             author = ''
                #         print("Comment author: ", author)
                #         comment = Comment(text=getattr(c, 'body', ''),
                #                           up_votes=getattr(c, 'ups', 0),
                #                           down_votes=getattr(c, 'downs', 0),
                #                           author=author)
                #         post.comments.append(comment)
                #         if len(post.comments) == constant.MAX_ALLOWED_COMMENTS_ON_POST:
                #             break
                #     except Exception as e:
                #         print_exception_details(e)
                #         return []
                posts.append(post)
                print(submission)
                print("Post cleanup", post)
            except Exception as e:
                print_exception_details(e)
                return []
    except Exception as e:
        print_exception_details(e)
        return []
    return posts


@cached(cache)
def get_subreddit_posts_by_name(sub_reddit_name):
    print("Getting subreddit posts for", sub_reddit_name)
    if sub_reddit_name == constant.DEFAULT_SUB_REDDIT:
        return get_hot_posts(sub_reddit_name)

    try:
        sub_reddits = reddit.subreddits.search(sub_reddit_name)
        try:
            return get_hot_posts(sub_reddits.next().display_name)
        except Exception as e:
            print_exception_details(e)
            return []
    except Exception as e:
        print_exception_details(e)
        return []


def upvote_a_post(post_id):
    try:
        post = reddit_with_user_details.submission(post_id)
        print("Upvoting subreddit post")
        post.upvote()
        return True

    except Exception as e:
        print_exception_details(e)
        return False


def downvote_a_post(post_id):
    try:
        post = reddit_with_user_details.submission(post_id)
        post.downvote()
        return True

    except Exception as e:
        print_exception_details(e)
        return False


def getthetopcomments_from_a_post(post_id, number_of_comments=5):
    comments = []
    count = 0
    try:
        submission = reddit.submission(post_id)
        for top_level_comment in submission.comments:
            comments.append(top_level_comment.body)
            count = count + 1
            if count == number_of_comments:
                break
    except Exception as e:
        print_exception_details(e)
        return comments
    return comments


def get_popular_titles():
    return get_hot_trending_post_titles("popular", constant.HOT_TRENDING_POSTS_COUNT)


def get_home_titles():
    return get_hot_trending_post_titles("home", constant.HOT_TRENDING_POSTS_COUNT)


def get_cricket_subreddits():
    return get_subreddits_by_name("cricket")


def get_cricket_subreddit_titles():
    return get_subreddit_titles_by_name("cricket")


def get_cricket_subreddit_posts():
    return get_subreddit_posts_by_name("cricket")


def upvote_reddit_posts():
    return upvote_a_post('cc3yye')


def downvote_reddit_posts():
    return downvote_a_post('cc3yye')


def getthetop10comments_from_a_post():
    print(getthetopcomments_from_a_post("cc3yye", constant.HOT_TRENDING_POSTS_COUNT))
