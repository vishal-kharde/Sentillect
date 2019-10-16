import tweepy
import re
import string
from textblob import TextBlob
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sklearn.preprocessing as sp
from SourceCode import opinionFunctions as omsFunctions

 # Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

 # Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

emoticons = emoticons_happy.union(emoticons_sad)

 #Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

def twitterDataFetch():
    consumer_key = "kmUncR73LePJXmk6itoztmCtY"
    consumer_secret = "6nPoOD9hRvKfzmOVbcfXNP5oRUB814VTBZfh4gu4kF3zu9cfVC"
    access_key = "56310425-lmir33o8IGYQiE0JqGIhHRZugYoFycSST0OE5Schn"
    access_secret = "3xci9Bh2v2c2o9nDEo1tH6Sv0QV0ppgJVZ4X8UUpbr7jn"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    keywords = '#barclays OR @Barclays OR barclays OR @BarclaysUKHelp OR @BarclaysUK '

    # for tweets in tweepy.Cursor(api.search, q=keyword, include_rts=False).items(100):
    searchresult = api.search(q=keywords, lang='en', count=10, truncated=False, tweet_mode='extended')
    tweetslistwithalldetails = []
    tweetlist = []
    i = 0
    for singletweet in searchresult:

        if 'retweeted_status' in singletweet._json:
            if 'extended_tweet' in singletweet._json['retweeted_status']:
                text = 'RT @' + singletweet._json['retweeted_status']['user']['screen_name'] + ':' + \
                       singletweet._json['retweeted_status']['extended_tweet']['full_text']
            else:
                text = 'RT @' + singletweet._json['retweeted_status']['user']['screen_name'] + ':' + \
                       singletweet._json['retweeted_status']['full_text']
        else:
            if 'extended_tweet' in singletweet._json:
                text = singletweet._json['extended_tweet']['full_text']
            else:
                text = singletweet.full_text
        print(str(i) + " " + text)
        i = i+1

    tweetslistwithalldetails.append(singletweet._json)  # contains tweets with all attributes
    tweetlist.append(clean_tweet(text))  # contains only tweets full text


def clean_tweet(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)

    # after tweepy preprocessing the colon left remain after removing mentions
    # or RT sign in the beginning of the tweet
    tweet = tweet.lower()
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)
    # remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    # filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []

    # looping through conditions
    for w in word_tokens:
        # check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    # print(word_tokens)
    # print(filtered_sentence)


print("\nWELCOME TO Sentillect")
print("-------------------------------------------------------------")
twitterDataFetch()

# input("Please Enter any key to continue...")
# print("\n\n\n\n\n\nPREPROCESSING DATA")
# omsFunctions.preProcessing(_ReviewDataset,_PreProcessedData,printResultChoice())
# print("\n\n\n\n\n\nREADING REVIEW COLLECTION...")
# omsFunctions.tokenizeReviews(_ReviewDataset,_TokenizedReviews,printResultChoice())
# print("\n\n\n\n\n\nPART OF SPEECH TAGGING...")
# omsFunctions.posTagging(_TokenizedReviews,_PosTaggedReviews,printResultChoice())
# print("\nThis function will list all the nouns as aspect")
# omsFunctions.aspectExtraction(_PosTaggedReviews,_Aspects,printResultChoice())
# print("\n\n\n\n\n\nIDENTIFYING OPINION WORDS...")
# omsFunctions.identifyOpinionWords(_PosTaggedReviews,_Aspects,_Opinions,printResultChoice())
