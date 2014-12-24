import sys
import pytz
import bson
import time

from helpers import convert_utc_to_formatted_pt, extract_posts_through_cursor, extract_preview_description


# The Blog Post Data Access Object handles interactions with the Posts collection
class postDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.posts = database.posts


    # inserts the entry and returns a permalink for the entry
    def insert_entry(self, permalink, title, postContent, youtubeLink, tags_array, userID, firstname): 

        # build a new post
        post = {"p": permalink,  # "p" for permalink
                "a": {'u': userID, 'f': firstname},  # "a" for author; "u" for userID; "f" for first name
                "s": title,  # "s" for subject
                "b": postContent,  # "b" for body
                "y": youtubeLink,  # "y" for Youtube
                "l": tags_array,  # "l" for tags label
                "fc": 0,  # "fc" for feedback count
                "lc": 0  # "lc" for like count
                }
        
        # now insert the post
        try:
            self.posts.insert(post)
            return True
        except:
            print "Unexpected error on insert_entry:", sys.exc_info()[0]
            return False

        return permalink

        
    # returns an array of posts, reverse ordered
    def get_posts(self, n_posts, page_num, likeDAO):
        n_posts_skip = (page_num - 1) * n_posts
        cursor = self.posts.find().sort('_id', direction=-1).skip(n_posts_skip).limit(n_posts)  # sort by date in descending order (recent posts first)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l
    
    
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

        
    # find a post corresponding to a particular permalink
    def get_post_by_permalink(self, permalink):
        post = self.posts.find_one({'p': permalink})
        if post is not None:
            utc_timestamp = post['_id'].generation_time
            pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            post['t'] = pt_formatted
            post['pd'] = extract_preview_description(body = post['b'], n_words = 30, n_chars = 240)
        return post


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


    # returns an array of num_posts posts, reverse ordered, filtered by tag
    def get_posts_by_tag(self, tag, likeDAO, num_posts = 'all'):

        if num_posts == 'all':
            cursor = self.posts.find({'l': tag}).sort('_id', direction = -1)
        else:
            cursor = self.posts.find({'l':tag}).sort('_id', direction = -1).limit(num_posts)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l


    def get_posts_by_userID(self, userID, likeDAO):
        userID = bson.objectid.ObjectId(userID)
        cursor = self.posts.find({'a.u': userID}).sort('_id', direction = -1)
        l = extract_posts_through_cursor(cursor, likeDAO)
        return l
        
    
    def increment_feedback_count(self, permalink):
        try:
            self.posts.update({'p': permalink}, {'$inc': {'fc': 1}})
            return True
        except:
            print "Unexpected error on increment_feedback_count:", sys.exc_info()[0]
            return False

            
    def decrement_feedback_count(self, permalink):
        try: 
            self.posts.update({'p': permalink}, {'$dec': {'fc': 1}})
            return True
        except:
            print "Unexpected error on decrement_feedback_count:", sys.exc_info()[0]
            return False
        
 
    def increment_likes_count(self, permalink):
        try: 
            self.posts.update({'p': permalink}, {'$inc': {'lc': 1}})
            return True
        except:
            print "Unexpected error on increment_likes_count:", sys.exc_info()[0]
            return False


    def decrement_likes_count(self, permalink):
        try: 
            self.posts.update({'p': permalink}, {'$inc': {'lc': -1}})
            return True
        except:
            print "Unexpected error on decrement_likes_count:", sys.exc_info()[0]
            return False
            
            
