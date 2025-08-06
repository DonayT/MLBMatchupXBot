from requests_oauthlib import OAuth1Session
import os
import json
import argparse

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
    
    # Opens Image and assigns it to media id
    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        response = oauth.post(upload_url, files=files)

        if response.status_code != 200:
            raise Exception(f"Image upload failed: {response.status_code} {response.text}")

        media_id = response.json()["media_id_string"]

    # Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote T
    payload = {
        "text": tweet_text,
        "media": {
                "media_ids": [media_id]
            }
        }

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    # Saving the response as JSON
    json_response = response.json()

if __name__ == "__main__":
    main()