import math
import json
import requests
import itertools
import numpy as np
import time
from datetime import datetime, timedelta
import praw
from praw.models import Comment
import csv
import regex as re


def make_request(uri, max_retries = 5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)
    current_tries = 1
    while current_tries < max_retries:
        try:
            time.sleep(1)
            response = fire_away(uri)
            return response
        except:
            time.sleep(1)
            current_tries += 1
    return fire_away(uri)


def pull_posts_for(subreddit, start_at, end_at):

    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'prefix': 't4_'
        }, posts))

    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'

    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                subreddit, start_at, end_at, SIZE))['data'])
    n = len(post_collections)


    return post_collections


def give_me_intervals(start_at, number_of_days_per_interval = 1):

    end_at = math.ceil(datetime.utcnow().timestamp())

    ## 1 day = 86400,
    period = (86400 * number_of_days_per_interval)
    end = start_at + period
    yield (int(start_at), int(end))
    padding = 1
    while end <= end_at:
        start_at = end + padding
        end = (start_at - padding) + period
        yield int(start_at), int(end)

#########################################################################################################################################



Counter = 0

subreddit = 'wallstreetbets'
start_at = math.floor(
    (datetime.utcnow() - timedelta(days=632)).timestamp())
posts = []
for interval in give_me_intervals(start_at, 1):
    pulled_posts = pull_posts_for(
        subreddit, interval[0], interval[1])

    posts.extend(pulled_posts)
    time.sleep(.500)

reddit = praw.Reddit(client_id='##############', client_secret='###########################', user_agent='my_user_agent')



limitvariable = None


with open('C:\\Users\\Grant\\Desktop\\Random\\SPARK_PROJECT\\' + subreddit + '.csv', 'w',encoding="utf-8") as csv_output:
    with open('C:\\Users\\Grant\\Desktop\\Random\\SPARK_PROJECT\\' + subreddit + '_metadata.csv', 'w',encoding="utf-8") as csv_meta_output:
        comment_writer = csv.writer(csv_output, delimiter = "|")
        comment_writer.writerow(["Subreddit","Create_Date", "Title", "Comment"])
        comment_writer_meta = csv.writer(csv_meta_output, delimiter = "|")
        comment_writer_meta.writerow(["Subreddit", "Create_Date", "Title", "Total_Num_Comments"])
        posts_from_reddit = []
        comments_from_reddit = []
        try:
            for submission_id in np.unique([ post['id'] for post in posts ]):
                try:
                    submission = reddit.submission(id=submission_id)
                    if  bool(re.search("What Are Your Moves", submission.title)):
                        print(submission.title)
                        comment_writer_meta.writerow([subreddit, submission.created_utc, submission.title, submission.num_comments])
                        print("Posts Completed = ", Counter)
                        Counter += 1
                        print("LENGTH = ", submission.num_comments)
                        if len(submission.comments) > 200:
                            limitvariable = None #might need to change this back to 0 if i get errors
                        else:
                            limitvariable = None
                        submission.comments.replace_more(limit=limitvariable)

                        for comment in submission.comments.list():
                            if isinstance(comment, praw.models.Comment):
                                comment_writer.writerow(
                                    [subreddit, submission.created_utc, submission.title,
                                     comment.body.replace("\n", " ")])
                except Exception as e:
                    print("ERROR OCCURED ", e)
                    continue




        except Exception as e:
            print(e)
            print("ERROR OCCURED OUTER LOOP")
