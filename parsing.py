import praw
import psraw

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/cs4300)',
                     client_id='5Z2o1haAiZ4i5w', client_secret="qIDD5claq0zRN-IihNWwTDp8jCU",
                     username='cs4300', password='cs4300')

def collect_posts(subreddit, num_requests):
    """
    Returns a list of (250 * num_requests) posts in the indicated subreddit.
    """
    topjokes = []
    for i in xrange(num_requests):
        if topjokes == []:
            topjokes += list(psraw.submission_search(
                            reddit, subreddit=subreddit, limit=250, sort='desc'))
        else:
            topjokes += list(psraw.submission_search(
                            reddit, subreddit=subreddit, limit=250, sort='desc',
                            before=str(topjokes[-1].created_utc)))
    return topjokes
