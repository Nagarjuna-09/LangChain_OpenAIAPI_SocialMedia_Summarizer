import os
from dotenv import load_dotenv
import tweepy
import requests

# Load environment variables from .env file
load_dotenv()

# Print the bearer token to verify it's loaded correctly (remove this after verification)
print(os.getenv("TWITTER_BEARER_TOKEN"))

# Set up the Twitter client using OAuth 2.0 Bearer Token
twitter_client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN")
)

def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    user = twitter_client.get_user(username=username)
    user_id = user.data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet.text
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list

def scrape_user_tweets_mock(username="EdenEmarco177", num_tweets=5):
    """
    Scrapes pre made Edens's Github Gist file of tweets and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    https://twitter.com/EdenEmarco177
    """
    EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json"
    tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()

    tweet_list = []
    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list

if __name__ == "__main__":
    tweets = scrape_user_tweets(username="The_Nagarjuna")
    print(tweets)
