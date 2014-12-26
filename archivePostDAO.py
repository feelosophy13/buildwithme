import sys
import pytz
import bson
import time
import datetime


## The Archive Post Data Access Object handles interactions with the Archive Posts collection
class archivePostDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.archive_posts = database.archive_posts
        
    
    def insert_entry(self, removal_post):
        
        


        # build a new post (required fields)
        post = {"p": permalink,  # "p" for permalink
                "a": {'u': userID, 'f': firstname},  # "a" for author; "u" for userID; "f" for first name
                "s": title,  # "s" for subject
                "b": postContent,  # "b" for body
                "fc": 0,  # "fc" for feedback count
                "lc": 0  # "lc" for like count
                }
        
        # insert the post
        try:
            self.posts.insert(post)
            return True
        except:
            print "Unexpected error on insert_entry:", sys.exc_info()[0]
            return False

        return permalink
