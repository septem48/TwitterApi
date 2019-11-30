import TwitterDocument, CsvView
import emoji, csv, datetime, pytz, time


def main():

    res = TwitterDocument.japanesePopularSearch(cnt=2)

    # リツイート数順でソート
    res.sort(key=lambda x: x['retweet_count'], reverse=True)

    # for line in res:
    #     print(line['user']['name']+'::'+line['full_text'])
    #     print(line['created_at'])
    #     print(line['retweet_count'])
    #
    #     print('*' * 100)

    outPutAsCsv(res)


def outPutAsCsv(dicts):

    header = ['UserName', 'TweetContent', 'RetweetCount', 'LikeCount',
              'FollowerCount', 'TweetedCount', 'CharCount', 'EmojisCount',
              'BrsCount', 'MediaTypes', 'MediaCount', 'MediaUrls',
              'HashtagContents', 'HashtagCount', 'Time']

    body = makeBody(dicts)

    writeList = []

    writeList.append(header)

    for line in body:
        writeList.append(line)

    CsvView.writeCsv(writeList, 'RawData')



def makeBody(dicts):

    body = []

    for line in dicts:
        userName = getUserName(line)
        tweetContent = line['full_text']

        retweetCount = getRetweetCount(line)
        likeCount = getLikeCount(line)

        followerCount = getFollowerCount(line)
        tweetedCount = getTweetedCount(line)

        charCount = makeCharCount(line)

        emojiCount = getEmojiCount(tweetContent)
        brsCount = getBrCount(tweetContent)

        mediaTypes = getMediaType(line)
        mediaCount = len(mediaTypes)

        mediaUrls = getMediaUrls(line)

        hashtagContents = getHashtagContent(line)
        hashtagsCount = len(hashtagContents)

        time = getJapanTime(line)

        elem = [userName, tweetContent, retweetCount, likeCount,
                followerCount, tweetedCount, charCount, emojiCount,
                brsCount, mediaTypes, mediaCount, mediaUrls,
                hashtagContents, hashtagsCount, time]

        body.append(elem)

    return body


def getUserName(dic):
    return dic['user']['name']


def getRetweetCount(dic):
    return dic['retweet_count']


def getLikeCount(dic):
    return dic['favorite_count']


# URL, Mediaを除いた文字数をカウントする
def makeCharCount(dic):
    # 絵文字もlen関数で1文字として抜けるっぽい
    fullCharCount = len(dic['full_text'])

    # URL全部カウント
    urlCharCount = 0

    for url in dic['entities']['urls']:
        urlCharCount += getIndicesCount(includeIndices=url)

    # Media全部カウント
    mediaCharCount = 0

    # Mediaは存在しないことがあるので、存在の検査をする
    if 'media' in dic['entities']:
        for media in dic['entities']['media']:
            mediaCharCount += getIndicesCount(includeIndices=media)

    # TODO: 半角スペース抜くのが必要かどうか確認

    # いらない文字まとめ
    uncountChars = urlCharCount + mediaCharCount

    # URLを引いた文字数をカウント
    return fullCharCount - uncountChars


# indicesの指定する文字数を抜く
def getIndicesCount(includeIndices):
    return int(includeIndices['indices'][1]) - int(includeIndices['indices'][0])


# 絵文字があるかないか検査
def getEmojiCount(string):

    emojiCnt = 0
    for emo in emoji.UNICODE_EMOJI:
        emojiCnt += string.count(emo)

    return emojiCnt

# 改行をカウント
def getBrCount(string):

    # 改行でlist化する
    string = string.splitlines()

    # 1行のみでも1が出るため, 1引いておく
    return len(string) - 1


def getMediaType(dic):

    mediaTypes = []

    if 'media' in dic['entities']:
        for media in dic['extended_entities']['media']:
            mediaTypes.append(media['type'])

    return mediaTypes


def getMediaUrls(dic):

    urls = []

    if 'media' in dic['entities']:
        for media in dic['entities']['media']:
            urls.append(media['media_url_https'])

    return urls


def getHashtagContent(dic):

    hashtagContent = []

    for hashtag in dic['entities']['hashtags']:
        hashtagContent.append(hashtag['text'])

    return hashtagContent


def getFollowerCount(dic):
    return int(dic['user']['followers_count'])


def getTweetedCount(dic):
    return int(dic['user']['statuses_count'])


def getJapanTime(dic):
    st = time.strptime(dic['created_at'], '%a %b %d %H:%M:%S +0000 %Y')  # time.struct_timeに変換
    utc_time = datetime.datetime(st.tm_year, st.tm_mon, st.tm_mday, \
                                 st.tm_hour, st.tm_min, st.tm_sec,
                                 tzinfo=datetime.timezone.utc)  # datetimeに変換(timezoneを付与)
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))  # 日本時間に変換
    str_time = jst_time.strftime("%Y-%m-%d_%H%M%S")  # 文字列で返す
    return str_time


main()
