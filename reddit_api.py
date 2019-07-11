import praw
reddit = praw.Reddit(client_id='',
                     client_secret="",
                     user_agent='TestUser')
print(reddit.read_only)


def get_titles(sub_reddit, number):
    titles = []
    try:
        for submission in reddit.subreddit(sub_reddit).hot(limit=number):
            titles.append(submission.title)
    except Exception:
        pass
    return titles


populartitles = get_titles("popular", 3)

print(populartitles)

hometitles = get_titles("home", 3)

print (hometitles)

