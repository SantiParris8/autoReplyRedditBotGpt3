import praw
import requests
import time
import os
import openai

# Initialize a Reddit instance
reddit = praw.Reddit(client_id="",
                     client_secret="",
                     username="",
                     password="",
                     user_agent="")

# Select the subreddit you want to monitor
subreddit = reddit.subreddit("SubNAME")

# Set the OpenAI API endpoint URL
openai_url = "https://api.openai.com/v1/engines/text-davinci-003/jobs"

# Set the OpenAI API access key
openai.api_key = ""

# Get the current time
current_time = int(time.time())
replied_posts = set()

while True:
    # Get the latest 100 posts in the subreddit
    for post in subreddit.new(limit=1):

        # Check if this post was created after the chatbot started
        if post.created_utc < current_time:
            break
        
        if post.is_self == False:
            break

        if post.id in replied_posts:
            break

        print (post.title)

        print ('running code')


        # Extract the content of the post
        content = 'Information regardingwhere this is coming from(): '+post.title + ' ' + post.selftext
        # Send the content to the OpenAI API for generating a response

        response = openai.Completion.create(model="text-davinci-003", prompt=content, temperature=0.1, max_tokens=300)

        # Extract the generated response from the API response
        generated_response = response["choices"][0]["text"]
        # Post the generated response as a comment on the post
        replied_posts.add(post.id)


        post.reply('Auto generated response:' + generated_response)