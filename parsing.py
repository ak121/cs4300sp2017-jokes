import praw

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/cs4300)',
                     client_id='5Z2o1haAiZ4i5w', client_secret="qIDD5claq0zRN-IihNWwTDp8jCU",
                     username='cs4300', password='cs4300')


for submission in reddit.subreddit('jokes').hot(limit=None):
    print(submission.title)