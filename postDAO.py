import sys
import pytz
import bson
import time
import datetime

from helpers import convert_utc_to_formatted_pt, extract_posts_through_cursor, extract_preview_description


## The Post Data Access Object handles interactions with the Posts collection
class postDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.posts = database.posts


    def insert_post(self, post):
        try:
            self.posts.insert(post)
            return True
        except:
            print "Unexpected error on insert_post:", sys.exc_info()[0]
            return False


    def update_post(self, post):        
        ## get original post entry and update timestamp
        orig_post = self.posts.find_one({'p':post['p']})

        ## import fields from  document 
        post['_id'] = orig_post['_id']  # postID
        post['p'] = orig_post['p']  # "p" for permalink
        post['fc'] = orig_post['fc']  # "fc" for feedback count
        post['lc'] = orig_post['lc']  # "lc" for like count
        post['u'] = datetime.datetime.utcnow()  # "u" for update timestamp in UTC

        ## update the old post document with the new post
        try:
            self.posts.update({'_id':post['_id']}, post)
            return True
        except:
            print "Unexpected error on update_post:", sys.exc_info()[0]
            return False


    def remove_post(self, userID, permalink):
        post = self.posts.find_one({'p':permalink})
        if userID == post['a']['u']:  # if userID of the user delivering the remove action matches with the post author's userID
            try:
                self.posts.remove({'p': permalink})
                return post  # return the removed post (used for archiving)
            except:
                print "Unexpected error on remove_post_by_permalink:", sys.exc_info()[0]
                return False
        else:  # if someone who's NOT the author of the post attempt the delete
            return False 


    def get_posts(self, n_posts, page_num, likeDAO, mode = 'essential'):
        n_posts_skip = (page_num - 1) * n_posts        
        projection = {'_id':1, 'a':1, 'b.s':1, 'p':1, 's':1, 'lc':1, 'fc':1, 'y':1, 'l':1} if mode == 'essential' else None  # if mode is "essential", then the projection excludes the following body fields: "problem", "solution", "monetization", and "marketing"; else, it's set to return all the fields
        cursor = self.posts.find({}, projection).sort('_id', direction=-1).skip(n_posts_skip).limit(n_posts)  # sort by date in descending order (recent posts first)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l
    
    
    def get_postID_by_permalink(self, permalink):
        try:
            postID = self.posts.find_one({'p':permalink}, {'_id':1})
            return postID
        except:
            print "Unexpected error on increment_feedback_count:", sys.exc_info()[0]
            return False


    def get_post_by_permalink(self, permalink, mode = 'essential'):
        projection = {'_id':1, 'a':1, 'b.s':1, 'p':1, 's':1, 'lc':1, 'fc':1, 'y':1, 'l':1} if mode == 'essential' else None  # if mode is "essential", then the projection excludes the following body fields: "problem", "solution", "monetization", and "marketing"; else, it's set to return all the fields
        post = self.posts.find_one({'p':permalink}, projection)
        if post is not None:
            utc_timestamp = post['_id'].generation_time
            pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            post['t'] = pt_formatted
            # post['pd'] = extract_preview_description(body = post['b'], n_words = 30, n_chars = 240)
            if 'l' not in post:
                post['l'] = []
            if 'y' not in post:
                post['y'] = ''
        return post
        

    def get_posts_by_tag(self, tag, likeDAO, num_posts = 'all', mode = 'essential'):
        projection = {'_id':1, 'a':1, 'b.s':1, 'p':1, 's':1, 'lc':1, 'fc':1, 'y':1, 'l':1} if mode == 'essential' else None  # if mode is "essential", then the projection excludes the following body fields: "problem", "solution", "monetization", and "marketing"; else, it's set to return all the fields
        if num_posts == 'all':
            cursor = self.posts.find({'l': tag}, projection).sort('_id', direction = -1)
        else:
            cursor = self.posts.find({'l':tag}, projection).sort('_id', direction = -1).limit(num_posts)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l


    def get_posts_by_userID(self, userID, likeDAO, mode = 'essential'):
        userID = bson.objectid.ObjectId(userID)
        projection = {'_id':1, 'a':1, 'b.s':1, 'p':1, 's':1, 'lc':1, 'fc':1, 'y':1, 'l':1} if mode == 'essential' else None  # if mode is "essential", then the projection excludes the following body fields: "problem", "solution", "monetization", and "marketing"; else, it's set to return all the fields
        cursor = self.posts.find({'a.u': userID}, projection).sort('_id', direction = -1)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l
        

    def get_post_summaries_by_userID(self, userID):
        userID = bson.objectid.ObjectId(userID)
        try:
            cursor = self.posts.find({'a.u':userID}, {'_id':1, 'p':1, 's':1})  # get permalink, title, timestamp
            l = []
            for summary in cursor:
                utc_timestamp = summary['_id'].generation_time
                pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
                summary['t'] = pt_formatted
                l.append(summary)
            return l
        except:
            print "Unexpected error on get_post_summaries_by_userID:", sys.exc_info()[0]
            return None

    
    def increment_feedback_count(self, permalink):
        try:
            update_status = self.posts.update({'p': permalink}, {'$inc': {'fc': 1}})
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on increment_feedback_count:", sys.exc_info()[0]
            return False

            
    def decrement_feedback_count(self, permalink):
        try: 
            update_status = self.posts.update({'p': permalink}, {'$inc': {'fc': -1}})
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on decrement_feedback_count:", sys.exc_info()[0]
            return False
        
 
    def increment_likes_count(self, permalink):
        try: 
            update_status = self.posts.update({'p': permalink}, {'$inc': {'lc': 1}})
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on increment_likes_count:", sys.exc_info()[0]
            return False


    def decrement_likes_count(self, permalink):
        try: 
            update_status = self.posts.update({'p': permalink}, {'$inc': {'lc': -1}})
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on decrement_likes_count:", sys.exc_info()[0]
            return False
            
    
    def update_author_firstname(self, userID, firstname):
        userID = bson.objectid.ObjectId(userID)
        try:
            update_status = self.posts.update({'a.u':userID}, {'$set':{'a.f':firstname}}, multi = True)
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on update_author_firstname:", sys.exc_info()[0]
            return False

            
    # determine if next_page_exists (next page exists if there are more previous posts)    
    def next_page_exists(self, n_posts_per_page, page_num):
        n_posts_skip = n_posts_per_page * page_num
        cursor = self.posts.find().skip(n_posts_skip).limit(1)
        
        count = 0
        for post in cursor:
            count += 1

        if count > 0:  # if there are more posts to be displayed
            return True
        return False


    # determine if previous_page_exists (previous page always exists unless the current page number is 1)
    def previous_page_exists(self, page_num):
        return page_num != 1


