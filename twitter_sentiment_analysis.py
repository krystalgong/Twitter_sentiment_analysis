# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd

# VADER Sentiment Analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

# detect language and filter English sentences
from langdetect import detect, DetectorFactory
# make the result unique
DetectorFactory.seed = 0

from datetime import timedelta

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
# From: iPhone 13: 09-24; Apple Watch: 10-15; MacBook Pro: 10-26
# Till: 11-21 (code: 11-22)
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('MacBook Pro since:2021-10-26 until:2021-11-22 lang:en').get_items()):
    try:
        if tweet.content is not None and detect(tweet.content) == 'en':
            Date = tweet.date

            # Combining the date for stock price
            if Date.isoweekday() in range(1,5) and Date.hour in range(15, 24):
                Stock_date = Date.date() + timedelta(days=1)
            elif Date.isoweekday() == 5 and Date.hour in range(15, 24):
                Stock_date = Date.date() + timedelta(days=3)
            elif Date.isoweekday() == 6:
                Stock_date = Date.date() + timedelta(days=2)
            elif Date.isoweekday() == 7:
                Stock_date = Date.date() + timedelta(days=1)
            else:
                Stock_date = Date.date()

            # Analyze sentiment parameters
            vs = analyzer.polarity_scores(tweet.content)

            # Append data to the tweets_list
            tweets_list.append([Date.date(), Date.strftime('%H:%M:%S'), Stock_date, tweet.id, tweet.content,\
                 tweet.username, vs['neg'], vs['neu'], vs['pos'], vs['compound']])
    except:
        print('Here is an error')
    
# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list, columns=['Date','Time', 'Combined_Stock_Date', 'Tweet_Id', 'Text',\
     'Username', 'neg', 'neu', 'pos', 'compound'])

tweets_df.to_csv('/Users/krystalgong/Desktop/twitter2021_iPhone13_MacBookPro.csv')