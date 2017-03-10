import post_collection as pc
import json
import config

for sr in config.subreddits:
  with open(sr + '.json', 'w+') as df: json.dump(pc.collect_posts(sr, 100), df)

