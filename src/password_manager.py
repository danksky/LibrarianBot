PASS_PATH = 'private/palabrasas.txt'
CLIENT_PATH = 'private/client.txt'
SEGRET_PATH = 'private/segret.txt'

f_pass = open(PASS_PATH, "r")
f_client = open(CLIENT_PATH, "r")
f_segret = open(SEGRET_PATH, "r")

librarian_reddit_pass = f_pass.readline()
librarian_reddit_client_id = f_client.readline()
librarian_reddit_client_secret = f_segret.readline()
