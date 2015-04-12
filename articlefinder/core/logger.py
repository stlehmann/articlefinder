import logging


logger = logging.getLogger('articlefinder')
logger.setLevel(logging.DEBUG)

# Filehandler
fh = logging.FileHandler('articlefinder.log')
fh.setLevel(logging.DEBUG)

# Consolehandler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)