import bottle, pymongo
import cgi, re, datetime, pytz

import postDAO, sessionDAO, userDAO, feedbackDAO, likeDAO, archivePostDAO, archiveUserDAO

from helpers import validate_post, validate_feedback, validate_profile_update, validate_signup
from helpers import validate_passwords, validate_message, validate_content
from helpers import clean_and_format_post, clean_and_format_feedback, clean_and_format_user_signup
from helpers import create_permalink, send_email, create_archive_post
from helpers import build_post_JSON, build_user_JSON, build_user_signup_JSON


@bottle.get('/test')
def test():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    return bottle.template('posts_grid_display2')


@bottle.post('/test')
def test():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    URL = bottle.request.forms.get("facebookURL")
    URL_escaped = cgi.escape(URL)
    URL_escaped2 = cgi.escape(URL, quote = True)
    
    links = {'raw': URL, 'escaped': URL_escaped, 'escaped2': URL_escaped2}
    
    print URL
    print URL_escaped
    print URL_escaped2
    print links
    
    return bottle.template('test')
    

"""
@bottle.route('/<page_num:int>')
def main_page(page_num = 1):  # by default, page_num = 1
    cookie = bottle.request.get_cookie("session")
    emailID, firstname = sessions.get_emailID_firstname(cookie)
    
    n_posts_per_page = 10
    l = posts.get_posts(n_posts_per_page, page_num)
    previous_page_exists = posts.previous_page_exists(page_num)
    next_page_exists = posts.next_page_exists(n_posts_per_page, page_num)
    previous_page_num = page_num - 1
    next_page_num = page_num + 1
    
    return bottle.template('main', dict(myposts=l, emailID=emailID, 
                                        page_num=page_num, 
                                        previous_page_exists=previous_page_exists,
                                        next_page_exists=next_page_exists,
                                        previous_page_num=previous_page_num,
                                        next_page_num=next_page_num))
"""

@bottle.get('/deactivate_account/<userID>')
def deactive_account_page(userID):
    pass


@bottle.post('/deactivate_account/<userID>')
def deactivate_account(userID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:  # if user is not logged in
        bottle.redirect('/'); return

    ## account deactivation steps
    # obtain the removal user from "users" collection
    # obtain all the posts that the user has posted
    # obtain all the feedbacks that the user has posted
    # obtain all the likes

    """
    ## post removal steps
    # obtain the removal post from "posts" collection
    # obtain the feedbacks for the removal post
    # obtain the likerIDs for the removal post
    # de-normalize by combining removal post with likerIDs and feedbacks
    # archive the de-normalized removal post into "archived_posts" collection
    # remove post from "posts" collection
    # NO NEED to remove the like documents for the deleted post from "likes" collection because the collection will return None with unmatched permalink
    # NO NEED to remove the feedback documents for the deleted post from "feedbacks" collection because the collection will return None with unmatched permalink
    # however, since likes and feedbacks are archived, we will go ahead and remove them from the active collections
        
    removal_post = posts.get_post_by_permalink(permalink, mode = 'complete')
    feedbacks_list = feedbacks.get_feedbacks_by_permalink(permalink)
    likerIDs = likes.get_likerIDs_by_permalink(permalink)
    archive_post = create_archive_post(removal_post, feedbacks_list, likerIDs)

    archived = archive_posts.insert_archive_post_entry(archive_post)
    if archived:
        post_removed = posts.remove_post(userID, permalink)
        likes_removed = likes.remove_likes_for_post(permalink)
        feedbacks_removed = feedbacks.remove_feedbacks_for_post(permalink)
        if post_removed and likes_removed and feedbacks_removed:
            bottle.redirect('/manage_posts')
            return
        else:  # should try again; for now, throw an error and move on
            bottle.redirect('/internal_error')
            return
    else:  # should try again; for now, throw an error and move on
        bottle.redirect('/internal_error')
        return        
    """





##### TO-DO
# edit/delete feedback
# deactivate user account function

# edit/upload profile image function
# edit/upload post image function
# asynchronous like/unlike JS function

###### Ideas for additional features
# include "occupation" field in user profile
# implement category for posts (education, legal, technology, mobile, gaming, medical/healthcare, etc.)
# a 2-column layout for edit_profile template
# highlight popular ideas
# highlight users' popular ideas in their dashboards

# <td><a href="/edit_feedback/{{summary['_id']}}">Edit</a> | <a href="/delete_feedback/{{summary['_id']}}">Delete</a></td>




####### BELOW FUNCTIONS ARE COMPLETE #######
@bottle.get('/delete_post/<permalink>')
def remove_post_page(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/'); return

    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink, 'complete')
    if post is None:
        bottle.redirect("/post_not_found"); return
    feedbacks_list = feedbacks.get_feedbacks_by_permalink(permalink)  # get the feedbacks for the post

    return bottle.template('entry_view',
                           dict(userID = userID, firstname = firstname, 
                                post = post, feedbacks = feedbacks_list, mode = 'delete'))


@bottle.post('/delete_post/<permalink>')
def remove_post(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    permalink = cgi.escape(permalink)

    if userID is None:  # if user is not logged in
        bottle.redirect('/'); return

    ## post removal steps
    # obtain the removal post from "posts" collection
    # obtain the feedbacks for the removal post
    # obtain the likerIDs for the removal post
    # de-normalize by combining removal post with likerIDs and feedbacks
    # archive the de-normalized removal post into "archived_posts" collection
    # remove post from "posts" collection
    # NO NEED to remove the like documents for the deleted post from "likes" collection because the collection will return None with unmatched permalink
    # NO NEED to remove the feedback documents for the deleted post from "feedbacks" collection because the collection will return None with unmatched permalink
    # however, since likes and feedbacks are archived, we will go ahead and remove them from the active collections
        
    removal_post = posts.get_post_by_permalink(permalink, mode = 'complete')
    feedbacks_list = feedbacks.get_feedbacks_by_permalink(permalink)
    likerIDs = likes.get_likerIDs_by_permalink(permalink)
    archive_post = create_archive_post(removal_post, feedbacks_list, likerIDs)

    archived = archive_posts.insert_archive_post_entry(archive_post)
    if archived:
        post_removed = posts.remove_post(userID, permalink)
        likes_removed = likes.remove_likes_for_post(permalink)
        feedbacks_removed = feedbacks.remove_feedbacks_for_post(permalink)
        if post_removed and likes_removed and feedbacks_removed:
            bottle.redirect('/manage_posts'); return
        else:  # should try again; for now, throw an error and move on
            bottle.redirect('/internal_error'); return
    else:  # should try again; for now, throw an error and move on
        bottle.redirect('/internal_error')
        return        




@bottle.get("/edit_feedback/<feedbackID>")
def update_feedback_page(feedbackID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/'); return 
    
    feedbackID = cgi.escape(feedbackID)
    feedback = feedbacks.get_feedback_by_feedbackID(feedbackID)
    if feedback is None:
        bottle.redirect('/internal_error'); return
        
    post = posts.get_post_by_permalink(feedback['p'], 'complete')
    if post is None:
        bottle.redirect("/post_not_found"); return

    return bottle.template('entry_view',
                           dict(userID = userID, firstname = firstname, mode = 'feedback_edit',
                                post = post, feedbacks = [], feedbackContent = feedback['b'], error = ""))


@bottle.post("/edit_feedback/<feedbackID>")
def update_feedback(feedbackID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/'); return

    feedback = {'_id': cgi.escape(feedbackID),
                'a': 
                   {'u': userID,  # feedback author userID
                    'f': firstname},  # feedback author first name
                'p': bottle.request.forms.get("permalink"),  # permalink of post for which feedback was submitted
                'b': bottle.request.forms.get('feedbackContent')  # feedback body
               }
    
    postID = posts.get_postID_by_permalink(cgi.escape(feedback['p']))
    if not postID:  # if postID not found (possible hack attempt)
        bottle.redirect("/post_not_found"); return
        
    error = {'e':''}
    
    if validate_feedback(feedbacks, feedback, error, mode='update'):
        feedback = clean_and_format_feedback(feedback)
        feedback_updated = feedbacks.update_feedback(feedback)
        if feedback_updated:
            bottle.redirect('/post/' + feedback['p']); return
        else:  # we should try again; for now, just move on
            error['e'] = 'Sorry, something went wrong.'
    
    return bottle.template("entry_view", 
                            dict(userID = userID, firstname = firstname, mode = "feedback_edit",
                                 post = post, feedbacks = [], feedbackContent = feedback['b'], error = error['e']))
            



@bottle.post('/insert_feedback')
def insert_feedback():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:  # if user is not logged in (possible hack attempt)
        bottle.redirect('/login'); return

    feedback = {'a': 
                   {'u': userID,  # feedback author userID
                    'f': firstname},  # feedback author first name
               'p': bottle.request.forms.get("permalink"),  # permalink of post for which feedback was submitted
               'b': bottle.request.forms.get('feedbackContent')  # feedback body
               }

    postID = posts.get_postID_by_permalink(feedback['p'])
    if not postID:  # if postID not found (possible hack attempt)
        bottle.redirect("/post_not_found"); return

    error = {'e':''}

    if validate_feedback(feedbacks, feedback, error, mode="new_insert"):
        feedback = clean_and_format_feedback(feedback)
        feedback_inserted = feedbacks.insert_feedback(feedback)
        if feedback_inserted:
            feedback_count_incremented = posts.increment_feedback_count(feedback['p'])
            if feedback_count_incremented:
                bottle.redirect("/post/" + feedback['p']); return
            else:  # we should try incrementing the count again; for now, just pass
                error['e'] = "Sorry, something went wrong."

    feedbacks_list = feedbacks.get_feedbacks_by_permalink(feedback['p'])  # get the feedbacks for the post
    return bottle.template("entry_view", 
                            dict(userID = userID, firstname = firstname, mode = "view",
                                 post = post, feedbacks = feedbacks_list, feedbackContent = feedback['b'], error = error['e']))


@bottle.get('/edit_profile')
def update_profile_page():
    cookie = bottle.request.get_cookie("session")
    userID = sessions.get_userID(cookie) 
    if userID is None:
        bottle.redirect('/login'); return
    user = users.get_user(userID)
    
    return bottle.template("edit_profile",
                           dict(userID = userID, firstname = user['f'], user = user, error = ""))


@bottle.post('/edit_profile')
def update_profile():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/login'); return

    form_input = bottle.request.forms
    user = build_user_JSON(userID, form_input)
    error = {'e':''}

    if validate_profile_update(users, user, error):
        # all of the variables except bio should have been cleared of any special characters in validate_profile_update();
        # however, we will escape them just for an added security measure
        user = clean_and_format_user(user)

        users_col_updated = users.update_user(user)
        posts_col_updated = posts.update_author_firstname(user['_id'], user['f'])
        sessions_col_updated = sessions.update_user_firstname(user['_id'], user['f'])
        feedbacks_col_updated = feedbacks.update_user_firstname(user['_id'], user['f'])

        if users_col_updated and posts_col_updated and sessions_col_updated and feedbacks_col_updated:  # upon failure, we should try again; for now, just move on
            bottle.redirect('/user/' + str(userID)); return
        else:
            return bottle.template("error_template",
                                   dict(userID = userID, firstname = firstname))
    else: 
        return bottle.template("edit_profile",
                               dict(userID = userID, firstname = firstname, user = user, error = error['e']))


@bottle.get('/edit_post/<permalink>')
def update_post_page(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink, 'complete')
    
    if userID is None:
        bottle.redirect('/login'); return        
    if post is None:
        bottle.redirect('/internal_error'); return
    
    post['l'] = ', '.join(post['l'])
    return bottle.template('post_entry',
                           dict(userID = userID, firstname = firstname, mode = 'edit',
                                post = post, error = ''))


@bottle.post('/edit_post/<permalink>')
def update_post(permalink):
    permalink = cgi.escape(permalink)
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/login'); return

    form_input = bottle.request.forms
    post = build_post_JSON(userID, firstname, form_input, permalink)
    error = {'e':''}

    if validate_post(posts, post, error, mode='update'):
        post = clean_and_format_post(post)        
        postUpdated = posts.update_post(post)
        if postUpdated:
            bottle.redirect("/post/" + permalink); return
        else:
            bottle.redirect('internal_error'); return
    else:  # if post update not validated
        return bottle.template("post_entry", 
                               dict(userID = userID, firstname = firstname, mode = 'edit',
                                    post = post, error = error['e']))


@bottle.get('/insert_post')
def insert_post_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:  # if user is not signed in
        bottle.redirect('/login'); return

    ## build a blank post document to populate the form fields
    post = build_post_JSON(userID, firstname)

    return bottle.template("post_entry", 
                           dict(userID = userID, firstname = firstname, mode = 'new_insert',
                                post = post, error = ""))


@bottle.post('/insert_post')
def insert_post():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/login'); return
    
    ## build a post document with submitted information (blank fields are initialized with blank values)
    form_input = bottle.request.forms
    post = build_post_JSON(userID, firstname, form_input, permalink = None)    
    error = {'e':''}

    if validate_post(posts, post, error, mode='new_insert'): 
        post = clean_and_format_post(post)
        postInserted = posts.insert_post(post)
        if postInserted:
            bottle.redirect("/post/" + post['p']); return  # redirect to post's permalink
        else:
            bottle.redirect('internal_error'); return
    else:
        return bottle.template("post_entry",
                               dict(userID = userID, firstname = firstname, mode = 'new_insert',
                                    post = post, error = error['e']))



@bottle.get('/contact_user/<queriedUserID>')
def contact_user_page(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    queriedUserID = cgi.escape(queriedUserID)
    queriedUser = users.get_user(queriedUserID) 
    
    # users not logged in will view the "please log in" message    
    return bottle.template('user_profile', 
                           dict(userID = userID, firstname = firstname, mode = 'contact', 
                                message = '', error = '',
                                queriedUser = queriedUser))


@bottle.post('/contact_user/<queriedUserID>')
def contact_user(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID is None:
        bottle.redirect('/login'); return

    queriedUserID = cgi.escape(queriedUserID)
    queriedUser = users.get_user(queriedUserID)
    if queriedUser is None:
        bottle.redirect('/internal_error'); return
    
    subject = "You've received a message!"
    message = bottle.request.forms.get("message")
    
    error = {'e':''}
    
    if validate_message(message, error):
        email_sent = send_email(queriedUser['e'], subject, message)        
        if email_sent:
            bottle.redirect('/message_sent?targetUserID=' + queriedUserID); return
        else:
            error['e'] = "Sorry, there was an internal error. It wasn't you. It was us."

    return bottle.template('user_profile', 
                            dict(userID = userID, firstname = firstname, 
                                mode = 'contact', message = message, 
                                queriedUser = queriedUser,
                                error = error['e']))


@bottle.get('/help')
def help_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    return bottle.template('help', 
                           dict(userID = userID, firstname = firstname))


@bottle.get('/message_sent')
def message_sent_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    targetUserID = bottle.request.query.get('targetUserID')
    if userID is None:
        bottle.redirect('/'); return
    
    return bottle.template('message_sent', 
                           dict(userID = userID, firstname = firstname, targetUserID = targetUserID))


@bottle.post('/like_post')
def like():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    permalink = bottle.request.forms.get('permalink'); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink, 'essential')
    like = likes.get_like(userID, permalink)
    
    if userID is None:
        bottle.redirect('/'); return
    if post is None:
        bottle.redirect("/post_not_found"); return
    if like:  # if user already liked the post
        print "You already liked this post!"
        return 'already liked'
    
   ## process a like
    like_logged = likes.log_like(userID, permalink)
    if like_logged:  # only if like was logged, increment the like count
        likes_count_incremented = posts.increment_likes_count(permalink)
        if likes_count_incremented:
            print "like logged and count incremented!"
            return 'success'
        else:  # if there was an error incrementing the like count 
            # should try again; for now, just throw an error and move on
            return False  # there was an error incrementing the likes count
    else:
        return False  # there was an error logging the like

   
@bottle.post('/unlike_post')
def unlike():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    permalink = bottle.request.forms.get("permalink"); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    like = likes.get_like(userID, permalink)

    if userID is None:
        bottle.redirect('/'); return
    if post is None:
        bottle.redirect("/post_not_found"); return
    if not like:  # if there is no like to unlike
        print "There is no like to remove!"
        return 'already unliked'

    ## process an unlike
    like_removed = likes.remove_like(userID, permalink)    
    if like_removed:  # only if like log was removed, decrement the like count
        likes_count_decremented = posts.decrement_likes_count(permalink)
        if likes_count_decremented:
            print "like removed and count decremented!"
            return 'success'
        else:  # if there was an error decrementing the like count
            # should try again; for now just, throw an error and move on
            return False  # there was an error decrementing the likes count
    else: 
        return False  # there was an error removing the like


@bottle.get('/change_password')
def change_password_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)     
    if userID is None:
        bottle.redirect('/login'); return
        
    return bottle.template("change_password",
                           dict(userID = userID, firstname = firstname,
                                current_password = "", new_password_1 = "", new_password_2 = "",
                                error = ""))


@bottle.post('/change_password')
def change_password():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)     
    if userID is None:
        bottle.redirect('/login'); return
    
    current_password = bottle.request.forms.get("current_password"); current_password = cgi.escape(current_password)
    new_password = bottle.request.forms.get("new_password"); new_password = cgi.escape(new_password)
    new_password2 = bottle.request.forms.get("new_password2"); new_password2 = cgi.escape(new_password2)

    error = {}
    
    ## if all the passwords are good and a correct user submitted the post request
    if validate_passwords(users, userID, current_password, new_password, new_password2, error):  # blank userIDs are also caught here
        password_updated = users.update_password(userID, new_password)        
        if password_updated:
            bottle.redirect('/user/' + str(userID)); return
        else:
            return bottle.template("change_password",
                                   dict(userID = userID, firstname = firstname))
    ## if there is a bad password or an incorrect user submitted the post request
    else:
        return bottle.template("change_password", 
                               dict(userID = userID, firstname = firstname,
                                    error = error['e']))
                                    

@bottle.get('/manage_posts')
def manage_posts():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID is None:
        bottle.redirect('/'); return

    my_post_summaries = posts.get_post_summaries_by_userID(userID)
    my_feedback_summaries = feedbacks.get_feedback_summaries_by_userID(userID)
    
    return bottle.template("manage_posts",
                           dict(userID = userID, firstname = firstname,
                                post_summaries = my_post_summaries, feedback_summaries = my_feedback_summaries))


@bottle.route('/liked_ideas')
def display_liked_ideas():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/'); return

    liked_posts_permalinks = likes.get_liked_posts_permalinks_by_userID(userID)  # permalinks of posts that a user has liked
    liked_posts = []  # posts that a user has liked
    
    for permalink in liked_posts_permalinks:
        post = posts.get_post_by_permalink(permalink, mode='essential')
        post['i'] = [userID]  # "i" for interested users' userIDs, or likerIDs; this step is taken in order to mark that the user has liked all the posts that are being served in the page
        liked_posts.append(post)

    return bottle.template('liked_posts', 
                           dict(userID = userID, firstname = firstname,
                                posts = liked_posts))


@bottle.get('/')
def main_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    latest_posts = posts.get_posts(10, 1, likes, 'essential')

    return bottle.template('main', 
                           dict(userID = userID, firstname = firstname, posts = latest_posts))


@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink, 'complete')  # get the relevant post
    feedbacks_list = feedbacks.get_feedbacks_by_permalink(permalink)  # get the feedbacks for the post
    # post_liked_by_user = True if likes.get_like(userID, permalink) else False  # see if the user has liked this post or not

    if post is None:
        bottle.redirect("/post_not_found"); return

    return bottle.template("entry_view", 
                           dict(userID = userID, firstname = firstname,
                                post = post, feedbacks = feedbacks_list,
                                error = "", feedbackContent = ""))


@bottle.get('/user/<queriedUserID>')
def user_profile(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    queriedUserID = cgi.escape(queriedUserID)    
    queriedUser = users.get_user(queriedUserID)
    postsByUser = posts.get_posts_by_userID(queriedUserID, likes)
    
    return bottle.template('user_profile',
                           dict(userID = userID, firstname = firstname, mode = 'view',
                                queriedUser = queriedUser, posts = postsByUser, colNum = 3))    


# The main page of the blog, filtered by tag
@bottle.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    tag = cgi.escape(tag)

    posts_by_tag = posts.get_posts_by_tag(tag = tag, likeDAO = likes, num_posts = 10)

    return bottle.template('posts_by_tag', 
                           dict(userID = userID, firstname = firstname,
                                tag = tag, posts = posts_by_tag))


@bottle.get('/signup')
def present_signup():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID:
        bottle.redirect("/"); return    
    user_signup = build_user_signup_JSON()
    return bottle.template("signup", user_signup = user_signup)


@bottle.post('/signup')
def process_signup():

    form_input = bottle.request.forms
    user_signup = build_user_signup_JSON(form_input)
    error = {'e':''}
    
    ## if it was a good signup
    if validate_signup(users, user_signup, error):
        # user inputs do not need to be escaped they have been validated by validate_signup()
        # however, for added security, we will escape anyway
        user = clean_and_format_user_signup(user_signup)  # removed the second password; contains the raw password

        # insert signed-up user to database and obtain signup confirmation string (for email address verification)
        signup_conf_str = users.insert_user(user)
        
        if not signup_conf_str:  # if there was error inserting signed-up user to database
            return bottle.redirect("/internal_error"); return
        else:  # if user signup successfully inserted into db
            signup_conf_link = base_url + '/confirm_signup/' + signup_conf_str
            subject = "Signup Confirmation"
            message = "Thanks for signing up! You can confirm your signup by visiting this link: %s" % signup_conf_link
            email_sent = send_email(emailID, subject, message)
            if email_sent:
                bottle.redirect('/please_confirm_email'); return
            else:
                bottle.redirect('/internal_error'); return

    ## if it was a bad signup
    else: 
        # firstname, lastname, emailID variables do not need to be escaped in the server side as they are escaped in the template engine;
        # in fact, if they were escaped in the server-side, the client-side would escape the escaped strings
        return bottle.template("signup", 
                               dict(user_signup = user_signup, error = error['e']))


@bottle.get('/please_confirm_email')
def please_confirm_email_page():
    return bottle.template('please_confirm_email')


@bottle.get('/confirm_signup/<conf_str_url>')
def confirm_signup(conf_str_url):
    cookie = bottle.request.get_cookie("session")
    signup_conf_str = bottle.request.get_cookie("signup_conf_str")    
    userID, firstname = sessions.get_userID_firstname(cookie)

    if userID:  # if user is already signed in
        bottle.redirect("/")  # redirect to homepage

    return bottle.template('confirm_signup', 
                           dict(emailID = '', error = ''))


## known issue: session_id not saved after signup confirmation
@bottle.post('/confirm_signup/<conf_str_url>')
def confirm_signup(conf_str_url):
    cookie = bottle.request.get_cookie("session")
    emailID = bottle.request.forms.get("emailID")
    userID, firstname = sessions.get_userID_firstname(cookie)

    if userID:  # if user is already signed in
        bottle.redirect("/")  # redirect to homepage

    conf_str_url = cgi.escape(conf_str_url)    
    signup_conf_str = users.find_signup_conf_str(emailID)
    
    if signup_conf_str == conf_str_url:
        user = users.remove_conf_str(emailID)        
        if user:
            session_id = sessions.start_session(user['_id'], user['f'])  # start_session() takes in userID and first name
            if session_id is None:
                bottle.redirect("/internal_error"); return

            # bottle.redirect() is buggy in bottle 0.12 version; 
            # it can remove global cookies after redirect; 
            # https://github.com/bottlepy/bottle/issues/386
            # work-around solution (using beaker for session/cookie handling): https://github.com/marciocg/meuengenho_blog

            bottle.response.set_cookie("session", session_id)
            return bottle.redirect('/'); return

        else:
            bottle.redirect('/internal_error'); return
    else:
        error = "Sorry, you entered the wrong email address."
        return bottle.template('confirm_signup', 
                               dict(emailID = emailID, error = error))


@bottle.get('/login')
def present_login():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID:
		bottle.redirect("/"); return
    return bottle.template("login",
                           dict(userID = userID, firstname = firstname,
                                emailID = "", password = "",
                                error = ""))


@bottle.post('/login')
def process_login():
    emailID = bottle.request.forms.get("emailID"); emailID = cgi.escape(emailID)
    password = bottle.request.forms.get("password"); password = cgi.escape(password)

    error = {'e':''}

    user_record = users.validate_login(emailID, password, error)
    if user_record:  # if valid login credentials provided
        session_id = sessions.start_session(user_record['_id'], user_record['f'])  # start_session() takes in userID and first name
        if session_id is None:
            bottle.redirect("/internal_error"); return
        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)
        bottle.redirect("/"); return

    else:  # if 1. invalid login credential provided, 2. user hasn't confirmed his/her email address
        return bottle.template("login",
                               dict(emailID = emailID, password = "",
                                    error = error['e']))


@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/"); return
    
    
@bottle.error(403)
@bottle.error(404)
@bottle.get("/post_not_found")
@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    return bottle.template("error_template", 
                           dict(userID = userID, firstname = firstname))


@bottle.route('/static/css/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static/css')


@bottle.route('/static/js/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static/js')


@bottle.route('/static/images/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='static/images')


@bottle.route('/how_it_works')
def how_it_works_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    return bottle.template('how_it_works', userID = userID, firstname = firstname)



base_url = 'http://www.buildwith.me'
connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.buildwithme

posts = postDAO.postDAO(database)
users = userDAO.userDAO(database)
sessions = sessionDAO.sessionDAO(database)
feedbacks = feedbackDAO.feedbackDAO(database)
likes = likeDAO.likeDAO(database)
archive_posts = archivePostDAO.archivePostDAO(database)
archive_users = archiveUserDAO.archiveUserDAO(database)


bottle.debug(True)
bottle.run(host="localhost", port=8082)


"""
def main():
    bottle.debug(True)
    run_wsgi_app(bottle.default_app())

if __name__=="__main__":
    main()
"""
