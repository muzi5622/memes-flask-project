from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

def get_meme():
    # List of popular meme subreddits
    subreddits = [
        'memes', 'dankmemes', 'wholesomememes', 'funny', 
        'ProgrammerHumor', 'memeeconomy', 'PrequelMemes',
        'historymemes', 'catmemes', 'dogmemes',
        'ComedyCemetery', 'terriblefacebookmemes', 'antimeme'
    ]
    chosen_subreddit = random.choice(subreddits)
    
    # Using Reddit's JSON API
    url = f"https://www.reddit.com/r/{chosen_subreddit}/hot.json?limit=50"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        posts = response.json()['data']['children']
        
        # Filter for posts that have images
        image_posts = [post for post in posts 
                      if post['data'].get('post_hint') == 'image' 
                      and not post['data'].get('over_18', True)]  # Skip NSFW posts
        
        if not image_posts:
            return "https://i.imgur.com/removed.png", chosen_subreddit
            
        # Choose a random image post
        random_post = random.choice(image_posts)
        meme_url = random_post['data']['url']
        return meme_url, chosen_subreddit
        
    except Exception as e:
        print(f"Error fetching meme: {str(e)}")
        return "https://i.imgur.com/removed.png", "Error"


@app.route("/")
def index():
    meme_large, subreddit = get_meme()
    return render_template("index.html", meme=meme_large, subreddit=subreddit)


if __name__ == "__main__":
    app.run(debug=True)
