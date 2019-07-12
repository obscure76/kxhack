import praw
from data import Comment, Post

reddit = praw.Reddit(client_id='Wffd8ItbvTdUwQ',
                     client_secret="KJ7pQHa03HGlr1_Mhi35mXeixMw",
                     user_agent='TestUser')


reddit2 = praw.Reddit(client_id='fA5TZDgaxeH3YQ',
                     client_secret="r0B8i0yF7RTZOG1yMRtbL_bj9vY",
                      password="testtest",
                     user_agent='',
                     username="")

print(reddit2.user.me())

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


def get_hot_posts(sub_reddit_name, number=5):
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
            except Exception as e:
                print(e)
                return []
    except Exception as e:
        print(e)
        return []
    return posts


def get_subreddit_posts_by_name(sub_reddit_name):
    try:
        sub_reddits = reddit.subreddits.search_by_name(sub_reddit_name)
        if not sub_reddits:
            return []
        try:
            return get_hot_posts(sub_reddits[0].title)
        except Exception as e:
            print(e)
            return []
    except Exception as e:
        print(e)
        return []


def upvote_a_post(post_id):
    try:
        post = reddit2.submission(post_id)
        print (post)
        post.upvote()

    except Exception as e:
        print (e)

def downvote_a_post(post_id):
    try:
        post = reddit2.submission(post_id)
        print (post)
        post.downvote()

    except Exception as e:
        print (e)

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


for p in get_subreddit_posts_by_name("cricket"):
    print(p)

upvote_a_post()

downvote_a_post()