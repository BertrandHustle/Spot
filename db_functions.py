#database functions for storing karma, case numbers, etc.
import functions
import sqlite3
import os

#init
#creates/connects to karma database
karma_db = sqlite3.connect('karma_db')
#we pass SQL commands cursor objects
karma_cursor = karma_db.cursor()
#creates/connects to case database
case_db = sqlite3.connect('case_db')
case_cursor = case_db.cursor()


#initializes databases and database objects
def init_dbs():

        #init tables
        karma_cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, nick TEXT NOT NULL UNIQUE, karma INTEGER)
        ''')
        karma_db.commit()


        case_cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases(id INTEGER PRIMARY KEY, title TEXT, case_number INTEGER)
        ''')
        case_db.commit()


def insert_user_into_db(nick):
    karma_cursor.execute('''
        INSERT INTO users(nick, karma) VALUES(?, ?)
    ''', (nick, 1))
    print ('user added')

    karma_db.commit()


#this listens for karma statements, e.g. 'Name++'
def listen_for_karma(data):

    if functions.reverse_hear(data, '++'):
        #TODO: fix this so decode is included in the parse_message fuction
        message = functions.parse_message(data.decode()).split(' ')
        for word in message:
            #this slices the '++' off the end of the name
            word = word[:-2]
            karma_cursor.execute('SELECT nick FROM users WHERE nick = ?', [word])

            #I believe this is needed because executing the .fetchall twice obliterates the results from the first query?
            query_result_size = len((karma_cursor.fetchall()))
            #if we don't find the user already in the database:
            if query_result_size == 0:
                insert_user_into_db(word)
            #if they're already in the database
            #TODO: this only updates karma when a new user is added...why?
            else:
                karma_cursor.execute('''
                    UPDATE users SET karma = karma + 1 WHERE nick = ?
                ''', [word])
                karma_db.commit()

    #TODO: make this function announce the user's current karma after updating value
    #TODO: add a control flow path for negative karma

def main():

    init_dbs()
    #close dbs after using them
    karma_db.close()
    case_db.close()

if __name__ == '__main__':
    main()
