import praw
reddit = praw.Reddit(client_id='',
                     client_secret="",
                     user_agent='TestUser')
print(reddit.read_only)


def get_hot_trending_posts_titles(sub_reddit, numberOfPosts):
    titles = []
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=numberOfPosts):
            titles.append(submission.title)
    except Exception:
        pass
    return titles


populartitles = get_hot_trending_posts_titles("popular", 3)

print(populartitles)

hometitles = get_hot_trending_posts_titles("home", 3)

print (hometitles)

