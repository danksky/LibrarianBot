import logging
import os
import re

formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message)s')
logPath = '../logs'
comments_log_filename 		= 'comments_replied_to'
submissions_log_filename 	= 'submission_logger'
errors_log_filename 		= 'error_logger'

comment_logger, submission_logger, error_logger = None, None, None
COMMENT_TYPE 	= 'COMMENT_TYPE'
SUBMISSION_TYPE	= 'SUBMISSION_TYPE'
ERROR_TYPE 		= 'ERROR_TYPE'

print_to_console = False

def setup_logger(logName, level=logging.INFO):
	#Function setup as many loggers as you want

	fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, logName))        
	fileHandler.setFormatter(formatter)

	streamHandler = logging.StreamHandler() # No need for a path or file
	streamHandler.setFormatter(formatter)

	logger = logging.getLogger(logName)
	logger.setLevel(level)
	logger.addHandler(fileHandler)
	if (print_to_console):
		logger.addHandler(streamHandler) # Print to console, too.

	return logger

def set_logger_printtoconsole(verdict):
	global print_to_console
	print_to_console = verdict

def log_comment(comment_url, comment_id):
	# comment logger
	global comment_logger
	if (comment_logger is None):
		comment_logger = setup_logger(comments_log_filename)
	comment_logger.info('[{0}]\t{1}\t* {2} *'.format('COMMENT', comment_url, comment_id))
	return

def log_submission(submission_id):
	# submission logger
	global submission_logger
	if (submission_logger is None):
		submission_logger = setup_logger(submissions_log_filename)
	submission_logger.info('[{0}]\t* {1} *'.format('SUBMISSION', submission_id))
	return

def log_error(error_message):
	# error logger 
	global error_logger
	if (error_logger is None):
		error_logger = setup_logger(errors_log_filename, logging.ERROR)
	error_logger.error(error_message)

# Edit: Redundancy removed by setting the logger variables as global. 
#		This ensures that there is only one object to which each type of logger var is assigned. 

def populate_log_list(log_type):
	log_id_list = []
	log_file = ''
	if   (log_type == COMMENT_TYPE):
		log_file = logPath + "/" + comments_log_filename 	+ ".log"
	elif (log_type == SUBMISSION_TYPE):
		log_file = logPath + "/" + submissions_log_filename + ".log"
	elif (log_type == ERROR_TYPE): # Why you would need to populate the error list is beyond me (for now?).
		log_file = logPath + "/" + errors_log_filename 		+ ".log"
	else:
		log_error('List population issue!')
		return None

	# Populate <type>log list
	if os.path.isfile(log_file):
		with open(log_file, "r") as f:
			lines = f.read().split("\n")
			# Clean
			while('' in lines):
				lines.remove('')
			# Iterate through id's
			line_num = -1
			for line in lines:
				line_num += 1
				log_id = get_id_from_log_line(log_type, line).strip()
				if log_id_is_valid(log_type, log_id):
					log_id_list.append(log_id)
				else:
					# Something is up with the read
					if (len(log_id) == 0):
						log_error("Log id is being grabbed from empty line") # Meaning cleaning above didn't work
					else:
						log_error("Bad formatting on " + log_type + " log line " + str(line_num) + ":\n\t" + line)
	return log_id_list

def get_id_from_log_line(log_type, line):
	log_id = ''
	if   (log_type == COMMENT_TYPE):
		log_id = line[-9:-2]
	elif (log_type == SUBMISSION_TYPE):
		log_id = line[-8:-2]
	elif (log_type == ERROR_TYPE): # Why you would need to populate the error list is beyond me (for now?).
		indexOfCommentId = line.find('Attempted ') + len(str('Attempted '))
		log_id = line[indexOfCommentId:(indexOfCommentId+7)] # TODO: Test this
	else:
		log_error('Unable to retrieve id from line!')
		return None 
	return log_id

def log_id_is_valid(log_type, log_id):
	if   (log_type == COMMENT_TYPE):
		return ((len(log_id) == 7) and (re.match('^[0-9A-Za-z]+$', log_id) is not None)) # or use `log_id.isalnum()`
	elif (log_type == SUBMISSION_TYPE):
		return ((len(log_id) == 6) and (re.match('^[0-9A-Za-z]+$', log_id) is not None))
	elif (log_type == ERROR_TYPE): 
		return ((len(log_id) == 7) and (re.match('^[0-9A-Za-z]+$', log_id) is not None)) # For now, using comment_id
	else:
		return False 