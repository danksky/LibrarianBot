import praw
from praw.models import MoreComments
import time
from random import randint
import traceback
import json
import requests

import password_manager

reddit = None

REDDIT_USER_PASA_PALABRA = password_manager.librarian_reddit_pass
CLIENT_ID = password_manager.librarian_reddit_client_id
CLIENT_SECRET = password_manager.librarian_reddit_client_secret
WEBHOOK_URL = password_manager.librarian_slack_webhook_url

shushes = [
    "Please be quiet.",
    "Please take your 9.5 down to a 3.5.",
    "Please keep it down.",
    "Could you keep it down please?",
    "Please lower your voice."]
banned_subreddits = [
    'hmmm',
    'oddlysatisfying',
    'television',
    'macroporn',
    'murderedbywords',
    'eyebleach']

comment_ids_replied_to = set()
comment_ids_replied_to_roots = set()
submission_commented_in = set()


def initiate_librarian():
    print(str(time.ctime()) + " Initiating librarian...")
    global reddit
    reddit = praw.Reddit(
        user_agent='Macbook Pro!',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username='insistent_librarian',
        password=REDDIT_USER_PASA_PALABRA)


def traverse_subreddits():
    print(str(time.ctime()) + " running...")
    reply_count, reply_limit = 0, 5
    request_count = 25
    while(request_count > 0 and reply_count <= reply_limit):
        print("Requesting feed from r/all with " +
              str(request_count) + " remaining")
        request_count -= 1
        if quiet_a_redditor('all'):
            reply_count += 1
    return reply_count


def alert_slack(notify=False, message=""):
    notifyChannelString = ""
    if (notify):
        notifyChannelString = "<!channel> "
    slack_data = {'text': notifyChannelString + str(message)}
    response = requests.post(
        WEBHOOK_URL, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )


def quiet_a_redditor(subreddit_title, timeout=120):
    global reddit
    query_count, query_limit = 0, 1000

    # Query the comments of chosen subreddit
    subreddit = reddit.subreddit(subreddit_title)
    retrieved_comment_ids = set()
    time_start = time.time()
    # Fetch the latest comments from the subreddit
    for comment in subreddit.stream.comments():
        if isinstance(comment, MoreComments):
            continue
        if (time.time() - time_start > timeout):
            print("Timeout @ " + str(time.ctime()))
            break
        comment_id = comment.id
        # Hopefully prevents repeated comments in the stream
        if (comment_id in retrieved_comment_ids):
            print("found comment id among those already retrieved")
            continue
        retrieved_comment_ids.add(comment_id)
        if comment.id not in comment_ids_replied_to:
            query_count += 1
            if query_count <= query_limit:
                if query_count > query_limit/2:
                    print("Reached " + str(query_limit/2) + " queried comments.")
                if merits_a_shush(comment.body):
                    root_id = get_root_comment_id(comment_id)
                    if distinct_tree(root_id):
                        comment.reply(
                            shushes[randint(0, len(shushes)-1)] + " This is a public forum.")
                        comment_ids_replied_to.add(comment_id)
                        comment_ids_replied_to_roots.add(root_id)
                        submission_commented_in.add(comment.submission)
                        return True
                    else:
                        print("Found " + comment_id +
                              " to shush, but I've already shushed their tree!")
            else:
                print("Reached " + str(query_limit) +
                      " queried comments on subreddit " + subreddit_title + ".")
            break
        else:
            print(comment_id + ": '" +
                  comment.body[:10] + "' has already been shushed!")
    return False


def distinct_tree(attempt_root_id):
    return (attempt_root_id not in comment_ids_replied_to_roots)


def get_root_comment_id(comment_id):
    global reddit
    comment = reddit.comment(comment_id)
    ancestor = comment
    refresh_counter = 0
    while not ancestor.is_root:
        ancestor = ancestor.parent()
        if refresh_counter % 9 == 0:
            ancestor.refresh()
        refresh_counter += 1
    return ancestor.id


def populate_roots(comments_replied_to):
    for comment_id in comments_replied_to:
        comment_ids_replied_to_roots.add(get_root_comment_id(comment_id))


def merits_a_shush(text):  # Logic of Librarian
    return (text.isupper() or "!!!" in text) and (len(text) > 6)


if __name__ == "__main__":
    try:
        initiate_librarian()
        reply_count = traverse_subreddits()
        alert_slack(notify=False,
                    message="Successful run with " + str(reply_count) + " replies.")
    except praw.exceptions.WebSocketException as err:
        alert_slack(notify=True, message=traceback.format_exc())
    except praw.exceptions.ClientException as err:
        alert_slack(notify=True, message=traceback.format_exc())
    except praw.exceptions.APIException as err:
        alert_slack(notify=True, message=traceback.format_exc())
    except praw.exceptions.PRAWException as err:
        alert_slack(notify=True, message=traceback.format_exc())
    except Exception as err:
        alert_slack(notify=True, message=traceback.format_exc())
