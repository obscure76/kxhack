import praw
from data import Comment, Post

reddit = praw.Reddit(client_id='',
                     client_secret="",
                     user_agent='TestUser')


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
        for submission in reddit.subreddits.search_by_name(sub_reddit_name):
            try:
                return get_hot_posts(submission.title)
            except Exception as e:
                print(e)
                return []
    except Exception as e:
        print(e)
        return []


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
