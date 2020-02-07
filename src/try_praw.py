import praw
import time
from random import randint

import password_manager

reddit = None

REDDIT_USER_PASA_PALABRA = password_manager.librarian_reddit_pass
CLIENT_ID = password_manager.librarian_reddit_client_id
CLIENT_SECRET = password_manager.librarian_reddit_client_secret

shushes = [
    "Please be quiet.",
    "Please take your 9.5 down to a 3.5.",
    "Please keep it down.",
    "Could you keep it down please?",
    "Please lower your voice."]
subreddits = [
    'anticonsumption',
    'bettereveryloop',
    # 'oddlysatisfying',
    'beamazed',
    # 'television',
    'nonononoyes',
    'macroporn',
    'meditation',
    'getmotivated',
    'natureisfuckinglit',
    'sports',
    'TIHI',
    'facepalm',
    'whatcouldgowrong',
    'rareinsults',
    'idiotsincars',
    'urbanexploration',
    'showerthoughts',
    'askreddit',
    # 'murderedbywords',
    'mildlyinteresting',
    'wholesomememes',
    # 'eyebleach',
    'trees',
    'madlads',
    'space',
    'theydidthefuckyou',
    "Freebies",
    "buildapcsales",
    "buyitforlife",
    "frugalmalefashion",
    "gamedeals",
    "AppHookup",
    "beermoney",
    "frugal",
    "AbandonedPorn",
    "Pareidolia",
    "perfecttiming",
    "minimalism",
    "animalsbeingjerks",
    "BirdsWithArms",
    "trollinganimals",
    "CatPranks",
    "gentlemanimals",
    "ReactionGIFS",
    "HighlightGIFS",
    "GamePhysics",
    "Unexpected",
    "awwwtf",
    "gifsound",
    "BlackpeopleGifs",
    "newreddits",
    "findareddit",
    "tipofmytongue",
    "theoryofreddit",
    "metahub",
    "ideasfortheadmins",
    "TrueReddit",
    "redditdotcom",
    "MuseumOfReddit",
    "OutOfTheLoop",
    "GetMotivated",
    "GetDisciplined",
    "UpliftingNews",
    "ProgressPics",
    "MMFB",
    "MadeMeSmile",
    "FoodPorn",
    "BudgetFood",
    "Jokes",
    "LatvianJokes",
    "standupshots",
    "Screenshots",
    "calvinandhobbes",
    "HumorousReviews",
    "YoutubeComments",
    "Foodforthought",
    "TrueAskReddit",
    "NoStupidQuestions",
    "ChangemyView",
    "offmychest",
    "TalesFromRetail",
    "AskScience",
    "AskHistorians",
    "explainlikeIAmA",
    "RandomKindness",
    "youtubehaiku",
    "ArtisanVideos",
    "netflixbestof",
    "MovieaWeek",
    "MovieSuggestions",
    "trailers",
    "TrueFilm",
    "FanTheories",
    "CordCutters",
    "Cinemagraphs",
    "firstworldproblems",
    "ancientworldproblems",
    "classicrage",
    "Gaming4Gamers",
    "CreepyGaming",
    "gamemusic",
    "playdate",
    "battlestations",
    "shittybattlestations",
    "photoshopbattles",
    "mspaintbattles",
    "ICanDrawThat",
    "redditgetsdrawn",
    "alternativeart",
    "DoodleOrDie",
    "itookapicture",
    "listentothis",
    "albumaday",
    "futurebeats",
    "mashups",
    "MISC",
    "gonewilder",
    "avocadosgonewild",
    "ToasterRights",
    "picsofdeadtoasters",
    "beardporn",
    "shaveoftheday",
    "nyxnyxnyx",
    "FifthWorldPics",
    "whowouldwin",
    "bitchimabus",
    "FuckYouImAShark",
    "GreenDawn",
    "asmr",
    "FiftyFifty",
    "CrazyIdeas",
    "MildlyInteresting",
    "MildlyInfuriating",
    "thingsforants",
    "NotTheOnion",
    "ifyoulikeblank",
    "dataisbeautiful",
    "estimation",
    "fatpeoplestories",
    "Showerthoughts",
    "nostalgia",
    "MorbidReality",
    "pettyrevenge",
    "prorevenge",
    "LucidDreaming",
    "24hoursupport",
    "internetisbeautiful",
    "outside",
    "futurology",
    "puzzles",
    "nononono",
    "nosleep",
    "FearMe",
    "whatisthisthing",
    "whatsthisworth",
    "lifeprotips",
    "lifehacks",
    "zenhabits",
    "howtonotgiveafuck",
    "EDC",
    "DIY",
    "somethingimade",
    "learnprogramming",
    "LearnPython",
    'unexpected',
    # 'hmmm',
    'todayilearned']


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


def initialize_trackers():
    # TODO: Make call to AWS to get a list of all the comments and initialize these accordingly
    print("filler")


def traverse_subreddits():
    print(str(time.ctime()) + " running...")
    reply_count, reply_limit = 0, 5
    while(len(subreddits) > 0 and reply_count <= reply_limit):
        random_index = randint(0, len(subreddits)-1)
        subreddit_title = subreddits[random_index]
        print("Now trying to quiet a redditor in: " + subreddit_title)
        if quiet_a_redditor(subreddit_title):
            reply_count += 1
        subreddits.remove(subreddit_title)


def quiet_a_redditor(subreddit_title, timeout=120):
    global reddit
    query_count, query_limit = 0, 1000

    # Query the comments of chosen subreddit
    subreddit = reddit.subreddit(subreddit_title)
    retrieved_comment_ids = set()
    time_start = time.time()
    # Fetch the latest comments from the subreddit
    for comment in subreddit.stream.comments():
        print(comment.id)
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
                        err = attempt_a_shush(comment)
                        if err is None:
                            # Local/Runtime record
                            comment_ids_replied_to.add(comment_id)
                            comment_ids_replied_to_roots.add(root_id)
                            submission_commented_in.add(comment.submission)
                            # Permanent record
                            # TODO
                            return True
                        else:
                            # TODO
                            print("TODO clearly something terrible has happened")
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


def attempt_a_shush(comment) -> Exception:
    try:
        # Magic
        comment.reply(
            shushes[randint(0, len(shushes)-1)] + " This is a public forum.")
        # Local/Runtime record
        # comment_ids_replied_to.append(comment_id)
        # comment_ids_replied_to_roots.append(root_id)
        # submission_commented_in.append(comment.submission)
        # Permanent record
        # librarian_logger.log_comment(comment.link_permalink, comment_id)
        # librarian_logger.log_submission(comment.submission)
    except praw.exceptions.WebSocketException as err:
        # librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
        # notify()
        return err
    except praw.exceptions.ClientException as err:
        # librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
        return err
    except praw.exceptions.APIException as err:
        # librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
        return err
    except praw.exceptions.PRAWException as err:
        # reddit 		= praw.Reddit('bot1')
        # librarian_logger.log_error("(Attempted " + comment_id + ") " + str(err))
        # notify()
        return err
    except Exception as err:
        # catch all errors
        return err
    finally:
        return None


def merits_a_shush(text):  # Logic of Librarian
    return (text.isupper()) and (len(text) > 6)
    # return (len(text) > 10 and text.count('s') > 4) # dummy test


if __name__ == "__main__":
    initiate_librarian()
    traverse_subreddits()
