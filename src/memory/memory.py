from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import logging
from src.exceptions import CustomException
import sys

logger = logging.getLogger(__name__)

try:
    conn = sqlite3.connect("memory.db", check_same_thread=False)
    logger.info("Database is created")

    checkpointer = SqliteSaver(conn=conn)
    logger.info("Checkpointer is created sucessfully..")

    checkpointer.setup()

except Exception as e:
    raise CustomException(e, sys)