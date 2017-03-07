from collections import defaultdict

subreddits = {
'Jokes',
'AntiJokes',
'AntiAntiJokes',
'cleanjokes',
'MeanJokes',
'DirtyJokes',
'dadjokes',
'Mommajokes',
'badjokes',
'ClassyJokes',
'3amJokes',
'ShortCleanFunny'
}

#These subs are ground truth of clean.
cleansubs = {'cleanjokes', 'ShortCleanFunny'}

#These subs are not safe for work
nsfwsubs = {'MeanJokes', 'DirtyJokes'}

# These jokes are clean unless marked 18+
ambiguous_subs = {'Jokes', 'dadjokes'}

num_requests = defaultdict(lambda x: 40)
