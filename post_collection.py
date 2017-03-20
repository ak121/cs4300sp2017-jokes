import praw
import psraw
import config

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/cs4300)',
                     client_id='5Z2o1haAiZ4i5w', client_secret="qIDD5claq0zRN-IihNWwTDp8jCU",
                     username='cs4300', password='cs4300')

def useful_from_post(post):
 
  return {
    'title': post.title,
    'selftext': post.selftext,
    'domain': post.domain,
    'over_18': post.over_18,
    #'ups': post.ups,
    #'downs': post.downs,
    #'num_comments': post.num_comments,
    'created_utc': int(post.created_utc),
    'id': post.id
  }

def collect_posts(subreddit, num_requests):
    """
    Returns a list of (250 * num_requests) posts in the indicated subreddit.
    """
    topjokes = []
    for i in xrange(num_requests):
        if topjokes == []:
            postgen = psraw.submission_search(
                            reddit, subreddit=subreddit, limit=250, sort='desc')
            for post in postgen:
                topjokes.append(useful_from_post(post))
        else:
            postgen = psraw.submission_search(
                            reddit, subreddit=subreddit, limit=250, sort='desc',
                            before=str(topjokes[-1]['created_utc']))
            for post in postgen:
                topjokes.append(useful_from_post(post))
    return topjokes

def collect_posts_praw(subreddit):
  """
  Uses the praw API to retrieve things
  """
  pass


def nsfw_truth(postdict):
  """
  Returns whether or not a post is ground-truth NSFW
  """
  subreddit = postdict['domain'].split('.')[1]
  return ((subreddit in config.nsfwsubs) or (subreddit in config.ambiguous_subs and postdict['over_18']))

def clean_truth(postdict):
  """
  Returns whether or not a post is ground-truth clean
  """
  subreddit = postdict['domain'].split('.')[1]
  return ((subreddit in config.cleansubs) or (subreddit in config.ambiguous_subs and not postdict['over_18']))
