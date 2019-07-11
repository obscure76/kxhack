import praw

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='my user agent')

print(reddit.read_only)

for submission in reddit.subreddit('learnpython').hot(limit=10):
    print(submission.title)
