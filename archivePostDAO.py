import sys


## The Archive Post Data Access Object handles interactions with the Archive Posts collection
class archivePostDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.archive_posts = database.archive_posts
        
    
    def insert_archive_post_entry(self, archive_post):
        dupe_archive_post = self.archive_posts.find_one({'_id': archive_post['_id']})
        if dupe_archive_post:
            return False
        else:       
            try:
                self.archive_posts.insert(archive_post)
                return True
            except:
                print "Unexpected error on insert_archive_post_entry:", sys.exc_info()[0]
                return False
