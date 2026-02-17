import logging
import os
from dotenv import load_dotenv

#import environment variables
load_dotenv()

#create a logger for our voice assistant
logger = logging.getLogger('voice-assistant')
logger.setLevel(logging.INFO)

#directory for persisting our index
PERSIST_DIR = "./chat-engine-storage"

