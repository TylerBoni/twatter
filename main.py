import os
import shutil
import tweepy
import json
import time
import datetime
import random
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

USER_KEY = os.getenv('CLIENT_KEY_AM')
USER_SECRET = os.getenv('CLIENT_SECRET_AM')

test = False

client = tweepy.Client(consumer_key=API_KEY,consumer_secret=API_SECRET,access_token=USER_KEY,access_token_secret=USER_SECRET)

auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=USER_KEY,access_token_secret=USER_SECRET
)

api = tweepy.API(auth)

def post_with_media(img,caption,hashtags=''):
    txt = caption + hashtags

    if not test:
        media = api.media_upload(img)
        media_id = str(media.media_id)
        response = client.create_tweet(
            text=txt,
            media_ids=[media.media_id]
        )
        post_id = response.data['id']
    else:
        media_id = str(random.randint(1,1000000000))
        post_id = str(random.randint(1,1000000000))

    shutil.move(img,"./images/am/archive/" + media_id + ".png")
    url = f"https://twitter.com/user/status/{post_id}"
    print(url)
    append_posted(caption,url)

def get_access():    
    print(auth.get_authorization_url())
    verifier = input("Input PIN: ")
    access_token, access_token_secret = auth.get_access_token(
        verifier
    )
    print(access_token)
    print(access_token_secret)

def posted_contains_string(txt):
     # Load the JSON file
    with open('./posted.json', 'r') as file:
        data = json.load(file)

    # Check if the string is already present in the object list
    return txt in data['captions']
    

def append_posted(caption,url):
       # Add the string to the object list
    json_file = './posted.json' 
    with open(json_file, 'r') as file:
        data = json.load(file)

    data['captions'].append(caption)
    data['posts'].append(url)
    print(f"Added '{caption}' to the JSON file.")

        # Save the updated JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
        print("JSON file updated and saved.")

def get_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def get_caption():
    categories = ['jokes','politics']
    category = random.choice(categories)

    caption = ""
    with open('./captions.json', 'r') as file:
        data = json.load(file)

    captions = data[category]['msg']
    hashtags = data[category]['hashtags']


    for c in captions:
        if not posted_contains_string(c):
            caption = c
            break
    hashtag_string = get_hashtags(caption,hashtags)

    return caption,hashtag_string
def get_hashtags(txt,hashtags):
    hashtag_string = '\n\n'
    for h in hashtags:
        new_hashtag_string = hashtag_string + " " + h
        new_txt = txt + new_hashtag_string
        if len(new_txt) >=270:
            break
        else:
            hashtag_string = new_hashtag_string
    return hashtag_string

images = get_file_paths("./images/am/q")

for image in images:
    # image = images[0]
    print('getting caption')

    caption, hashtags = get_caption()
    print(caption)
    print('posting')
    post_with_media(image,caption,hashtags)
    print('sleeping for 1 hour. Time right now is: ' + datetime.datetime.now().strftime('%H:%M:%S'))
    time.sleep(60*60)