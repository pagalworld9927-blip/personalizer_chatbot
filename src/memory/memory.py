from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect("memory.db", check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

checkpointer.setup()