import praw
import constant
from data import Comment, Post

reddit = praw.Reddit(client_id='Wffd8ItbvTdUwQ',
                     client_secret="KJ7pQHa03HGlr1_Mhi35mXeixMw",
                     user_agent='TestUser')


reddit_with_user_details = praw.Reddit(client_id='fA5TZDgaxeH3YQ',
                     client_secret="r0B8i0yF7RTZOG1yMRtbL_bj9vY",
                     password="testtest",
                     user_agent='AlexaSocialFeed',
                     username="testtest")


def get_hot_trending_post_titles(sub_reddit, number_of_posts):
    titles = []
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=number_of_posts):
            titles.append(submission.title)
    except Exception as e:
        print(e)
        return []
    return titles


def get_subreddits_by_name(name):
    pass


def get_subreddit_titles_by_name(sub_reddit_name):
    titles = []
    try:
        for submission in reddit.subreddits.search_by_name(sub_reddit_name):
            titles.append(submission.title)
    except Exception as e:
        print(e)
        return []
    return titles


def get_hot_posts(sub_reddit_name, number=constant.HOT_TRENDING_POSTS_COUNT):
    posts = []
    try:
        for submission in reddit.subreddit(sub_reddit_name).hot(limit=number):
            try:
                if getattr(submission, 'over_18', False):
                    continue
                if getattr(submission, 'author', None):
                    author = getattr(submission.author, 'name', '')
                else:
                    author = ''
                post = Post(title=getattr(submission, 'title', ''),
                            text=getattr(submission, 'selftext', ''),
                            up_votes=getattr(submission, 'ups', 0),
                            down_votes=getattr(submission, 'downs', 0),
                            url=getattr(submission, 'url', ''),
                            id=getattr(submission, 'id', ''),
                            author=author,
                            sub_reddit_name=sub_reddit_name)
                if post.author == 'AutoModerator':
                    continue
                for c in submission.comments:
                    try:
                        if getattr(submission, 'author', None):
                            author = getattr(submission.author, 'name', '')
                        else:
                            author = ''
                        comment = Comment(text=getattr(c, 'body', ''),
                                          up_votes=getattr(c, 'ups', 0),
                                          down_votes=getattr(c, 'downs', 0),
                                          author=author)
                        post.comments.append(comment)
                        if len(post.comments) == 5:
                            break
                    except Exception as e:
                        print(e)
                        return []
                posts.append(post)
                print(post)
            except Exception as e:
                print(e)
                return []
    except Exception as e:
        print(e)
        return []
    return posts


def get_subreddit_posts_by_name(sub_reddit_name):
    try:
        sub_reddits = reddit.subreddits.search(sub_reddit_name)
        try:
            return get_hot_posts(sub_reddits.next().display_name)
        except Exception as e:
            print(e)
            return []
    except Exception as e:
        print(e)
        return []

def upvote_a_post(post_id):
    try:
        post = reddit_with_user_details.submission(post_id)
        post.upvote()
        return True

    except Exception as e:
        print(e)
        return False

def downvote_a_post(post_id):
    try:
        post = reddit_with_user_details.submission(post_id)
        post.downvote()
        return True

    except Exception as e:
        print(e)
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
        print(e)
        return comments
    return comments

def get_popular_titles():
    return get_hot_trending_post_titles("popular", 3)


def get_home_titles():
    return get_hot_trending_post_titles("home", 3)


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
    print (getthetopcomments_from_a_post("cc3yye",10))

