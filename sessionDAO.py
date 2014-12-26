import sys
import random
import string
import bson


## The session Data Access Object handles interactions with the sessions collection
class sessionDAO:

    def __init__(self, database):
        self.db = database
        self.sessions = database.sessions


    def start_session(self, userID, firstname):
        session_id = self.get_random_str(32)  # create a session ID string
        session = {'_id': session_id, 'u': userID, 'f': firstname}
        try:
            self.sessions.insert(session)
        except:
            print "Unexpected error on start_session:", sys.exc_info()[0]
            return None
        return str(session['_id'])


    def end_session(self, session_id):
        if session_id is None:
            return None
        try:
            self.sessions.remove({'_id': session_id})
        except:
            print "Unexpected error on end_session:", sys.exc_info()[0]
        return


    def get_session(self, session_id):
        if session_id is None:
            return None
        session = self.sessions.find_one({'_id': session_id})
        return session


    def get_userID(self, session_id):
        session = self.get_session(session_id)
        if session is None:
            return None, None
        else:
            return session['u']  # return userID


    def get_userID_firstname(self, session_id):
        session = self.get_session(session_id)
        if session is None:
            return None, None
        else:
            return session['u'], session['f']  # return userID and first name

            
    def get_random_str(self, num_chars):
        random_string = ""
        for i in range(num_chars):
            random_string = random_string + random.choice(string.ascii_letters)
        return random_string


    def edit_user_firstname(self, userID, firstname):
        userID = bson.objectid.ObjectId(userID)
        try:
            update_status = self.sessions.update({'u':userID}, {'$set':{'f':firstname}}, multi = True)
            return  update_status['nModified'] > 0  # nModified is zero if there was no session log with the given userID
        except:
            print "Unexpected error on end_session:", sys.exc_info()[0]
            return False
