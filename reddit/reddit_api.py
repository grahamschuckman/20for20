"""
This script accepts system arguments for specific subreddits.
The last system argument should be the number of posts requested.
Ex: python reddit_api.py funny memes 100
"""

import praw
import pandas as pd
import json
from datetime import datetime
import sys

# Create a client using the following credentials
reddit = praw.Reddit(client_id='',  # Put the string under "personal use script" here
                     client_secret='',  # Put the secret here
                     user_agent='',  # Put the name of your app here
                     username='',  # Put your reddit username here
                     password='')  # Put your reddit password here

# Count the system arguments (chat/channel names)
arguments = len(sys.argv) - 1
print(sys.argv)
if arguments == 0:
    sys.exit("Please provide at least one valid subreddit name. Ex: python reddit_api.py funny memes 100")

# Assign the last system argument to be the number of messages retrieved from each subreddit
last_argument = len(sys.argv) - 1

# Exit the script if no number of messages system argument was provided
try:
    num_messages = int(sys.argv[last_argument])
except:
    sys.exit(
        "Enter the last argument as the number of messages to retrieve. Ex: python reddit_api.py funny memes 100")

# Get the requested number of posts for each subreddit
position = 1
while (arguments > position):
    print(sys.argv[position])

    try:

        # Choose to examine a given subreddit
        subreddit_name = sys.argv[position]
        subreddit = reddit.subreddit(subreddit_name)

        # Returns a list-like object with the top (newest = subreddit.new) n submissions to the subreddit (limit of 1000)
        top_subreddit = subreddit.top(limit=num_messages)

    except:
        sys.exit("Please confirm that all subreddit names are valid. Ex: python reddit_api.py funny memes 100")

    # Create a dictionary to store data
    reddit_dict = {"author": [],
                   "title": [],
                   "score": [],
                   "id": [], "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": [],
                   "subscribers": [],
                   "subreddit": []}

    # Iterate through the top subreddit posts and append to the dictionary
    for submission in top_subreddit:
        # The author must be converted to a string because of the way it is contained in the Redditor class
        reddit_dict["author"].append(str(submission.author))
        reddit_dict["title"].append(submission.title)
        reddit_dict["score"].append(submission.score)
        reddit_dict["id"].append(submission.id)
        reddit_dict["url"].append(submission.url)
        reddit_dict["comms_num"].append(submission.num_comments)
        reddit_dict["created"].append(submission.created)
        reddit_dict["body"].append(submission.selftext)
        reddit_dict["subscribers"].append(submission.subreddit_subscribers)
        reddit_dict["subreddit"].append(subreddit_name)

    # Pass the dictionary into a dataframe for easier viewing
    reddit_data = pd.DataFrame(reddit_dict)
    reddit_data.head()

    # The formatting of the created column is not very intelligible. We can change it to ISO from UNIX/UTC
    def get_date(created):
        return datetime.utcfromtimestamp(created).isoformat() + '+00:00'

    # Apply the above function to the "created" column, and then rename it to timestamp for easier understanding
    reddit_data["created"] = reddit_data["created"].apply(get_date)
    reddit_data.rename(columns = {"created" : "timestamp"}, inplace = True)

    # Convert the dataframe back to a dictionary for rapid exporting to JSON
    reddit_dict = reddit_data.to_dict('records')

    # Export reddit data to JSON
    with open("./posts/" + subreddit_name + "_subreddit.json", 'w+') as f:
        json.dump(reddit_dict, f)

    print("All data has been successfully exported to a JSON file.")

    # Loop to the next system argument
    position = position + 1
