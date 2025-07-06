from requests_oauthlib import OAuth1Session
import os
import json

# THIS FILE CONTAINS ALL ORIGINAL PARTS FOR OAUTH 1.0A 3-LEGGED AUTHENTICATION FLOW

# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
payload = {"text": "Hello world!"}

# Get request token (original implementation, these request temporary OAuth tokens, not necessary for this bot)
# request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
# oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

# try:
#     fetch_response = oauth.fetch_request_token(request_token_url)
# except ValueError:
#     print(
#         "There may have been an issue with the consumer_key or consumer_secret you entered."
#     )

# resource_owner_key = fetch_response.get("oauth_token")
# resource_owner_secret = fetch_response.get("oauth_token_secret")
# print("Got OAuth token: %s" % resource_owner_key)

# Get authorization (THIS IS FOR NON-AUTOMATED REQUESTS, REQUESTS PIN FOR EACH POST ATTEMPT)
# base_authorization_url = "https://api.twitter.com/oauth/authorize"
# authorization_url = oauth.authorization_url(base_authorization_url)
# print("Please go here and authorize: %s" % authorization_url)
# verifier = input("Paste the PIN here: ")


# THIS BLOCK IS FOR ACCESS REQUEST EACH RUN-TIME, NOT NECESSARY SINCE ACCESS TOKENS ARE STORED IN SECRET FILE
# Get the access token
# access_token_url = "https://api.twitter.com/oauth/access_token"
# oauth = OAuth1Session(
#     consumer_key,
#     client_secret=consumer_secret,
#     resource_owner_key=resource_owner_key,
#     resource_owner_secret=resource_owner_secret,
#     verifier=verifier,
# )
# oauth_tokens = oauth.fetch_access_token(access_token_url)

# access_token = oauth_tokens["oauth_token"]
# access_token_secret = oauth_tokens["oauth_token_secret"]

# These two lines save access tokens, same as above code block
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))