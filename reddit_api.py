import praw
reddit = praw.Reddit(client_id='',
                     client_secret="",
                     user_agent='TestUser')
print(reddit.read_only)


def gettheTitles(keyword, number):
        titles = []
        print("\nhere are the " + keyword + " feed" )
        for submission in reddit.subreddit(keyword).hot(limit=number):
            titles.append(submission.title)
        return titles


populartitles = gettheTitles("popular",3)

print(populartitles)

hometitles = gettheTitles("home",3)

print (hometitles)

