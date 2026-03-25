from requests_oauthlib import OAuth1Session
import os
import json
import argparse
import time

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

required_vars = {
    "CONSUMER_KEY": consumer_key,
    "CONSUMER_SECRET": consumer_secret,
    "ACCESS_TOKEN": access_token,
    "ACCESS_TOKEN_SECRET": access_token_secret
}

for name, value in required_vars.items():
    if not value:
        raise EnvironmentError(f"Missing environment variable: {name}")

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Upload image to Twitter')
    parser.add_argument('--image', help='Path to the image file to upload')
    parser.add_argument('--text', help='Tweet text')
    args = parser.parse_args()
    
    # Use provided image path or default
    image_path = args.image if args.image else "PracticeLineups/ExampleLineup4.png"
    tweet_text = args.text if args.text else "Practice LineUp 07/10/25\n#BuiltForThis vs #GuardsBall"
    
    # Upload image with retries
    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
    media_response = None
    for attempt in range(1, 4):
        with open(image_path, "rb") as image_file:
            media_response = oauth.post(upload_url, files={"media": image_file})
        if media_response.status_code == 200:
            break
        print(f"Media upload attempt {attempt} failed: {media_response.status_code} — retrying in {attempt * 5}s")
        time.sleep(attempt * 5)

    if not media_response or media_response.status_code != 200:
        raise Exception(f"Image upload failed after 3 attempts: {media_response.status_code if media_response else 'no response'}")

    media_id = media_response.json()["media_id_string"]

    payload = {
        "text": tweet_text,
        "media": {"media_ids": [media_id]}
    }

    # Post tweet with retries
    tweet_response = None
    for attempt in range(1, 4):
        tweet_response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
        if tweet_response.status_code == 201:
            break
        print(f"Tweet attempt {attempt} failed: {tweet_response.status_code} — retrying in {attempt * 5}s")
        time.sleep(attempt * 5)

    if not tweet_response or tweet_response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(
                tweet_response.status_code if tweet_response else "no response",
                tweet_response.text if tweet_response else ""
            )
        )


if __name__ == "__main__":
    main()