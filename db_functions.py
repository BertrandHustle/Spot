#database functions for storing karma, case numbers, etc.
import functions
import sqlite3

#initializes databases and database objects
def init_db():
    #creates/connects to karma database
    karma_db = sqlite3.connect('karma_db')
    #we pass SQL commands cursor objects
    karma_cursor = karma_db.cursor()
    #creates/connects to case database
    case_db = sqlite3.connect('case_db')
    case_cursor = case_db.cursor()

    #init tables
    karma_cursor.execute('''
    CREATE TABLE users(id INTEGER PRIMARY KEY, nick TEXT, karma INTEGER)
    ''')
    karma_db.commit()

    case_cursor.execute('''
    CREATE TABLE cases(id INTEGER PRIMARY KEY, title TEXT, case_number INTEGER)
    ''')
    case_db.commit()

    #close dbs after using them
    karma_db.close()
    case_db.close()

#this listens for karma statements, e.g. 'Name++'
def listen_for_karma(data):
    nick = functions.parse_message(data)
