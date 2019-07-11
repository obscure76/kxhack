import praw
from data import Comment, Post

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='my user agent')


def get_hot_trending_posts_titles(sub_reddit, number_of_posts):
    titles = []
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=number_of_posts):
            titles.append(submission.title)
    except Exception:
        pass
    return titles


def get_hot_posts(sub_reddit_name, number=10):
    posts = []
    try:
        for submission in reddit.subreddit(sub_reddit_name).hot(limit=number):
            try:
                if submission.over_18:
                    continue
                post = Post(title=getattr(submission, 'title', ''),
                            text=getattr(submission, 'selftext', ''),
                            up_votes=getattr(submission, 'ups', 0),
                            down_votes=getattr(submission, 'downs', 0),
                            url=getattr(submission, 'url', ''),
                            id=getattr(submission, 'id', ''),
                            author=submission.author.name,
                            sub_reddit_name=sub_reddit_name)
                if post.author == 'AutoModerator':
                    continue
                for c in submission.comments:
                    try:
                        comment = Comment(text=getattr(c, 'body', ''),
                                          up_votes=getattr(c, 'ups', 0),
                                          down_votes=getattr(c, 'downs', 0),
                                          author=c.author.name)
                        post.comments.append(comment)
                        if len(post.comments) == 5:
                            break
                    except Exception:
                        pass
                posts.append(post)
            except Exception:
                pass
    except Exception as e:
        print(e)
    return posts


def get_popular_titles():
    return get_hot_trending_posts_titles("popular", 3)


def get_home_titles():
    return get_hot_trending_posts_titles("home", 3)


for p in get_hot_posts("amazonecho"):
    print(p)

