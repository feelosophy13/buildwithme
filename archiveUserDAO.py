import sys


## The Archive User Data Access Object handles interactions with the Archive Users collection
class archiveUserDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        self.archive_users = database.archive_users
        
    
    def insert_archive_user(self, archive_user):
        dupe_archive_user = self.achive_users.find_one({'_id': archive_user['_id']})
        if dupe_archive_user:
            return False
        else:
            try:
                self.archive_users.insert(archive_user)
                return True
            except:
                print "Unexpected error on insert_archive_user:", sys.exc_info()[0]
                return False
