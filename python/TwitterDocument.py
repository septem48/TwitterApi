import TwitterConnection


def japanesePopularSearch(cnt):

    # パラメータ設定
    # lang:ja で日本のツイートが取得できる

    q = 'lang:ja'
    cnt = cnt
    resultType = 'popular'

    res = TwitterConnection.search(q, cnt, resultType)
    return res


def getMyTweet(cnt):

    cnt = cnt
    res = TwitterConnection.getMyTweet(cnt)
    return res


def userPopularSearch(cnt, userName):

    # パラメータ設定
    # lang:ja で日本のツイートが取得できる

    cnt = cnt

    res = TwitterConnection.getUserTweet(cnt, userName)
    return res
