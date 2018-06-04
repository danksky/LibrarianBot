import logging

formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message)s')
logPath = '../logs'
comments_log_filename = 'comments_replied_to'
submissions_log_filename = 'submission_logger'
errors_log_filename = 'error_logger'

def setup_logger(logName, level=logging.INFO):
	#Function setup as many loggers as you want

	fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, logName))        
	fileHandler.setFormatter(formatter)

	streamHandler = logging.StreamHandler() # No need for a path or file
	streamHandler.setFormatter(formatter)

	logger = logging.getLogger(logName)
	logger.setLevel(level)
	logger.addHandler(fileHandler)
	logger.addHandler(streamHandler) # Print to console, too.

	return logger

def log_comment(comment_url, comment_id):
	# comment logger
	comment_logger = setup_logger(comments_log_filename)
	comment_logger.info('[{0}]\t{1}\t* {2} *'.format('COMMENT', comment_url, comment_id))
	return

def log_submission(submission_id):
	# submission logger
	comment_logger = setup_logger(submissions_log_filename)
	comment_logger.info('[{0}]\t* {1} *'.format('SUBMISSION', submission_id))
	return

def log_error(error_message):
	# error logger 
	error_logger = setup_logger(errors_log_filename, logging.ERROR)
	error_logger.error(error_message)
