import bson
import sys


## The Likes Data Access Object handles all interactions with the Like collection.
class likeDAO:

    def __init__(self, db):
        self.db = db
        self.likes = self.db.likes
    

    def get_like(self, userID, permalink):
        userID = bson.objectid.ObjectId(userID)
        try:
            like = self.likes.find_one({'u': userID, 'p': permalink})
            return like
        except:
            print "Unexpected error on get_like:", sys.exc_info()[0]
            return None
        
    
    # log a like
    def log_like(self, userID, permalink):
        like = {'u': userID, 'p': permalink}
        try:
            self.likes.insert(like)
            return True
        except:
            print "Unexpected error on log_like:", sys.exc_info()[0]
            return False


    # unlike a post
    def remove_like(self, userID, permalink):
        try:
            self.likes.remove({'u': userID, 'p': permalink})
            return True
        except:
            print "Unexpected error on remove_like:", sys.exc_info()[0]
            return False  


    # restore a like
    def restore_like(self, likeID, userID, permalink):
        likeID = bson.objectid.ObjectId(likeID)
        like = {'_id': likeID, 'u': userID, 'p': postID}
        try: 
            likes.restore_like(likeID, permalink, userID)
            return True
        except:
            print "Unexpected error on restore_like:", sys.exc_info()[0]
            return False


    def get_liked_posts_permalinks_by_userID(self, userID, n_posts = 'all'):
        if n_posts == 'all':
            cursor = self.likes.find({'u': userID}).sort('_id', direction = -1)
        else:
            cursor = self.likes.find({'u': userID}).sort('_id', direction = -1).limit(n_posts)
        permalinks = []
        for like in cursor:
            permalinks.append(like['p'])
        return permalinks


    def get_likerIDs_by_permalink(self, permalink):
        try:
            like_records_cursor = self.likes.find({'p':permalink}, {'u':1, '_id':0})
            likerIDs = []
            for record in like_records_cursor:
                likerIDs.append(record['u'])
            return likerIDs
        except:
            print "Unexpected error on get_likerIDs:", sys.exc_info()[0]
            return None

    
    def remove_likes_for_post(self, permalink):
        try:
            self.likes.remove({'p':permalink})
            return True
        except:
            print "Unexpected error on remove_likes_for_post:", sys.exc_info()[0]
            return False




"""
e.g. like JSON document
{
'_id': 'abc',  # likeID
'post_id': 123,
'user_id': 'jamesdean@gmail.com',
}
"""