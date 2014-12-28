import sys
import bson

from helpers import convert_utc_to_formatted_pt


## The Feedback Data Access Object handles all interactions with the Feedback collection.
class feedbackDAO:

    def __init__(self, db):
        self.db = db
        self.feedbacks = self.db.feedbacks
    

    def insert_feedback(self, feedback):
        try:
            self.feedbacks.insert(feedback)
            return True
        except:
            print "Unexpected error on insert_feedback:", sys.exc_info()[0]
            return False
    
    
    def update_feedback(self, feedback):
        try:
            update_status = self.posts.update({'_id':feedback['_id']}, feedback)
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on update_feedback:", sys.exc_info()[0]
            return False


    def remove_feedback(self, permalink, feedbackByFirstName, feedbackByUserID):
        pass

        
    def remove_feedbacks_for_post(self, permalink):
        try:
            self.feedbacks.remove({'p': permalink})
            return True
        except:
            print "Unexpected error on remove_feedbacks_for_post:", sys.exc_info()[0]
            return False
    
   
    def get_feedbacks_by_permalink(self, permalink, n_feedbacks = 'all'):
        if n_feedbacks == 'all':
            cursor = self.feedbacks.find({'p': permalink}).sort('_id', direction=-1)  # sort by date in descending order (recent posts first)
        else:
            cursor = self.feedbacks.find({'p': permalink}).sort('_id', direction=-1).limit(n_feedbacks)  # sort by date in descending order (recent posts first)
        l = []
        for feedback in cursor:
            utc_timestamp = feedback['_id'].generation_time  # naive datetime instance (contains no timezone info in the object)
            pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            feedback['t'] = pt_formatted  # replace the naive datetime instance with a new timestamp in Pacific Time
            l.append(feedback)
        return l


    def get_feedback_by_feedbackID(self, feedbackID):
        feedbackID = bson.objectid.ObjectId(feedbackID)
        try:
            feedback = self.feedbacks.find_one({'_id':feedbackID})
            return feedback
        except:
            print "Unexpected error on get_feedback_by_feedbackID:", sys.exc_info()[0]
            return None
        

    def update_user_firstname(self, userID, firstname):
        userID = bson.objectid.ObjectId(userID)
        try:
            update_status = self.feedbacks.update({'a.u':userID}, {'$set':{'a.f':firstname}}, multi = True)
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on update_author_firstname:", sys.exc_info()[0]
            return False


    def get_feedback_summaries_by_userID(self, userID):
        userID = bson.objectid.ObjectId(userID)
        try:
            cursor = self.feedbacks.find({'a.u':userID}, {'_id':1, 'p':1})  # get permalink and postID (timestamp)
            l = []
            for summary in cursor:
                utc_timestamp = summary['_id'].generation_time
                pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
                summary['t'] = pt_formatted
                l.append(summary)
            return l
        except:
            print "Unexpected error on get_feedback_summaries_by_userID:", sys.exc_info()[0]
            return None
