#database functions for storing karma, case numbers, etc.
import functions
import sqlite3
import os

#init
#creates/connects to karma database
karma_db = sqlite3.connect('karma_db')
#we pass SQL commands cursor objects
karma_cursor = karma_db.cursor()
#directory where the karma db is
karma_dir = '/home/sgreenbe/Python/Projects/Spot/karma_db'
#creates/connects to case database
case_db = sqlite3.connect('case_db')
case_cursor = case_db.cursor()
case_dir = '/home/sgreenbe/Python/Projects/Spot/case_db'

#initializes databases and database objects
def init_dbs():

        #init tables
        karma_cursor.execute('''
            CREATE TABLE users(id INTEGER PRIMARY KEY, nick TEXT, karma INTEGER)
        ''')
        karma_db.commit()


        case_cursor.execute('''
            CREATE TABLE cases(id INTEGER PRIMARY KEY, title TEXT, case_number INTEGER)
        ''')
        case_db.commit()


def insert_user_into_db():
    nick = 'test_nick'
    karma = 0
    karma_cursor.execute('''
        INSERT INTO users(nick, karma) VALUES(?, ?)
    ''', (nick, karma))
    print ('user added')

    karma_db.commit()


#def insert_case_into_db():


#this listens for karma statements, e.g. 'Name++'
def listen_for_karma(data):
    nick = functions.parse_message(data)

def main():
    #check if tables don't exist already
    if not os.path.isfile(karma_dir) and not os.path.isfile(case_dir):
        init_dbs()

    insert_user_into_db()

    #close dbs after using them
    karma_db.close()
    case_db.close()

if __name__ == '__main__':
    main()
