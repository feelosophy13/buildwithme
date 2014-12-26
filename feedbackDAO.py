import sys
import bson

from helpers import convert_utc_to_formatted_pt


## The Feedback Data Access Object handles all interactions with the Feedback collection.
class feedbackDAO:

    def __init__(self, db):
        self.db = db
        self.feedbacks = self.db.feedbacks
    

    def insert_feedback(self, permalink, feedbackByFirstName, feedbackByUserID, feedbackContent):
        feedback = {'p': permalink, 
                    'a': {'f': feedbackByFirstName, 'u': feedbackByUserID},
                    'b': feedbackContent}
        try:
            self.feedbacks.insert(feedback)
            return True
        except:
            print "Error inserting post"
            print "Unexpected error:", sys.exc_info()[0]
            bottle.redirect('/internal_error')
    
    
    def edit_feedback(self, permalink, feedbackByFirstName, feedbackByUserID, feedbackContent):
        pass
        
        
    def remove_feedback(self, permalink, feedbackByFirstName, feedbackByUserID):
        pass
        
   
    def get_feedbacks_by_permalink(self, permalink, n_feedbacks = 'all'):
        if n_feedbacks == 'all':
            cursor = self.feedbacks.find({'p': permalink}).sort('_id', direction=-1)  # sort by date in descending order (recent posts first)
        else:
            cursor = self.feedbacks.find({'p': permalink}).sort('_id', direction=-1).limit(n_feedbacks)  # sort by date in descending order (recent posts first)
        l = []
        for post in cursor:
            utc_timestamp = post['_id'].generation_time  # naive datetime instance (contains no timezone info in the object)
            pt_timestamp_formatted = convert_utc_to_formatted_pt(utc_timestamp)
            post['t'] = pt_timestamp_formatted  # replace the naive datetime instance with a new timestamp in Pacific Time
                            
            l.append({'p': post['p'],  # parent post permalink
                      'b': post['b'],  # feedback body
                      'a': post['a'],  # feedback author
                      })
        return l


    def edit_user_firstname(self, userID, firstname):
        userID = bson.objectid.ObjectId(userID)
        try:
            update_status = self.feedbacks.update({'a.u':userID}, {'$set':{'a.f':firstname}}, multi = True)
            return update_status['nModified'] > 0
        except:
            print "Unexpected error on edit_author_firstname:", sys.exc_info()[0]
            return False



"""
e.g. feedback JSON document
{
'_id': 1,  # feedbackID
'post_ID': 123,  // postID
'feedback_by': { "id" :  <authorId>, "fname" :  "Howard", "lname": "Song"},
'feedback': 'This is a great idea!',
'timestamp_updated': '2014-08-10-12-32-33'
}
"""