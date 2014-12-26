import sys
import hmac
import random
import string
import hashlib
import pymongo
import bson
import datetime

from helpers import validate_email


## The User Data Access Object handles all interactions with the User collection.
class userDAO:

    def __init__(self, db):
        self.db = db
        self.users = self.db.users
        self.SECRET = 'verysecret'


    # makes a salt
    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt


    # implement the function make_pw_hash(name, pw) that returns a hashed password
    # of the format:
    # HASH(pw + salt),salt
    # use sha256


    def make_pw_hash(self, pw, salt=None):
        if salt == None:
            salt = self.make_salt();
        return hashlib.sha256(pw + salt).hexdigest()+","+ salt


    def validate_login(self, emailID, password, error):
        error['e'] = ''
        if not validate_email(emailID):
            error['e'] = "Tsk, tsk. That's an invalid email address."
            return None
        user = None
        try:
            user = self.users.find_one({'e': emailID})
        except:
            pass
        if user is None:  # if user not in database
            error['e'] = "What's happening? Something doesn't match."
            return None
        salt = user['p'].split(',')[1]
        if user['p'] != self.make_pw_hash(password, salt):  # if password doesn't a match
            error['e'] = "What's happening? Something doesn't match."
            return None
        if 'c' in user:  # if user has signed up but hasn't yet confirmed his/her email address
            error['e'] = "Please confirm your email address. A confirmation email was sent to %s." % user['e']
            return None

        # if it looks good
        return user


    def passwords_match(self, userID, current_password):
        user = self.get_user(userID)
        if user:
            salt = user['p'].split(',')[1]
            if user['p'] == self.make_pw_hash(current_password, salt):
                return True
            else:
                return False
        else:
            return False
            
            
    def update_password(self, userID, new_password):
        new_password_hash = self.make_pw_hash(new_password)
        userID = bson.objectid.ObjectId(userID)
        try:  # try inserting password without updating the whole user document
            update_status = self.users.update({'_id': userID}, {'$set': {'p': new_password_hash}})
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on update_password:", sys.exc_info()[0]
            return False


    def get_password(self, userID):
        userID = bson.objectid.ObjectId(userID)
        try:
            password = self.users.find_one({'_id': userID}, {'p': 1, '_id': 0})['p']
            return password
        except:
            print "Unexpected error on get_password:", sys.exc_info()[0]
            return None
    
    
    def get_emailID_and_password(self, userID):
        userID = bson.objectid.ObjectId(userID)
        try:
            record = self.users.find_one({'_id': userID}, {'e':1, 'p':1, '_id':0})
            return record['e'], record['p']  # return emailID and password
        except:
            print "Unexpected error on get_emailID_and_password:", sys.exc_info()[0]
            return None, None
    

    def add_user(self, emailID, firstname, lastname, password, signup_conf_str):  # email has already been validated at this point
        password_hash = self.make_pw_hash(password)  # hash the password
        user = self.users.find_one({'e':emailID})  # find user by email ID
        if user is None:  # if no one else has the same email ID            
            user = {'e': emailID, 
                    'f': firstname, 
                    'l': lastname, 
                    'p': password_hash, 
                    'c': signup_conf_str}
            try:
                self.users.insert(user)
                user = self.users.find_one({'e': emailID})
                return user['_id']
            except pymongo.errors.OperationFailure:  # mongo error
                print "Unexpected error on add_user:", sys.exc_info()[0]
                return False
        else:  # if there is another user with that email ID, then return False
            return False


    def edit_user_info(self, userID, firstname, lastname, bio, birthYear, links, zip, gender):
        userID = bson.objectid.ObjectId(userID)
        emailID, password = self.get_emailID_and_password(userID)
        # password = self.get_password(userID)
        
        if emailID is None or password is None:  # if error retrieving emailID or password
            return False
        utc_timestamp = datetime.datetime.utcnow()  # obtain timestamp in UTC        

        ## save no keys for blank fields; only add key-value pairs for the field values that aren't blank
        user = {'_id': userID,
                'p': password,
                'f': firstname,
                'l': lastname,
                'e': emailID,
                'u': utc_timestamp}  # updated timestamp
        if bio:
            user['b'] = bio
        if birthYear:
            user['y'] = birthYear
        if links:
            user['w'] = {}
            if links['f']:  # facebook link
                user['w']['f'] = links['f']
            if links['l']:  # linkedin link
                user['w']['l'] = links['l']
            if links['o']:  # other link
                user['w']['o'] = links['o']                
        if zip:
            user['z'] = zip
        if gender:
            user['g'] = gender
        
        try:
            self.users.update({'_id': userID}, user)
            return True
        except:
            print "Unexpected error on edit_user_info:", sys.exc_info()[0]
            return False

       
    def get_user(self, userID):
        userID = bson.objectid.ObjectId(userID)        
        try:
            user = self.users.find_one({'_id': userID})
            user['b'] = '' if 'b' not in user else user['b']
            user['z'] = '' if 'z' not in user else user['z']
            user['g'] = '' if 'g' not in user else user['g']
        
            if user['g'] == 'm': 
                user['g'] = 'male'
            elif user['g'] == 'f':
                user['g'] = 'female'
            else:
                user['g'] = 'other'

            if 'w' in user:
                user['w']['f'] = '' if 'f' not in user['w'] else user['w']['f']  # facebook
                user['w']['l'] = '' if 'l' not in user['w'] else user['w']['l']  # linkedin
                user['w']['o'] = '' if 'o' not in user['w'] else user['w']['o']  # other
            else:
                user['w'] = {'f':'', 'l':'', 'o':''}

            if 'y' in user:
                current_year = datetime.datetime.now().year
                user['a'] = current_year - int(user['y'])
            else: 
                user['y'] = ''
                user['a'] = ''

            return user

        except:
            print "Unexpected error on get_user:", sys.exc_info()[0]
            return None


    def emailID_exists(self, emailID):
        try:
            emailID = self.users.find_one({'e': emailID}, {'e': 1, '_id': 0})['e']
            return emailID
        except:
            print "Unexpected error on get_user:", sys.exc_info()[0]
            return None


    def find_signup_conf_str(self, emailID):
        try:
            signup_conf_str = self.users.find_one({'e':emailID}, {'c':1, '_id':0})['c']
            return signup_conf_str
        except:
            print "Unexpected error on find_signup_conf_str:", sys.exc_info()[0]
            return None


    def remove_conf_str(self, emailID):
        try:
            return_result = self.users.update({'e': emailID}, {'$unset': {'c':1}})  # this line removes the "c" field (which contains a user's signup confirmation string)
            if return_result['nModified'] > 0:
                return self.users.find_one({'e': emailID})                
            else:
                return False
        except:
            print "Unexpected error on remove_conf_str:", sys.exc_info()[0]
            return False





