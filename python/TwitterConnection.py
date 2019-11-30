import json
import config #標準のjsonモジュールとconfig.pyの読み込み

def oauth():
    twitter = config.SetMyOauthSession() #認証処理
    return twitter


def search(q, cnt, resultType):
    twitter = oauth()

    url = 'https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended'

    params = {'q': q,
              'count': cnt,
              'result_type': resultType,
              'include_entities': 'true'}

    res = twitter.get(url, params = params)

    try:
        timelines = json.loads(res.text)
        timelines = timelines['statuses']

    except:
        print(type(json.loads(res.text)))
        print('Error')

    return timelines


def getMyTweet(cnt):
    twitter = oauth()
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?tweet_mode=extended"
    params = {'count': cnt,
              'exclude_replies': 'true',
              'include_rts': 'false'}
    req = twitter.get(url, params=params)

    if req.status_code == 200:
        timelines = json.loads(req.text)
        return timelines

    else:
        print("ERROR: %d" % req.status_code)
        return 0


def retweet(tid):
    twitter = oauth()

    url = 'https://api.twitter.com/1.1/statuses/retweet/' + tid + '.json?tweet_mode=extended'

    params = {'id' : tid}

    res = twitter.post(url, params = params)

    if res.status_code == 200:
        print('Success')

    else:
        print('Failed. : %d'% res.status_code)

