import bottle
import pymongo

import postDAO
import sessionDAO
import userDAO
import feedbackDAO
import likeDAO
import archivePostDAO

import cgi
import re
import datetime
import pytz

from beaker.middleware import SessionMiddleware
from helpers import create_permalink, validate_post, validate_passwords, validate_signup, validate_profile_update, validate_message, validate_content, send_email, make_rand_str, clean_and_format_post



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






##### TO-DO
# remove_post function
# edit/upload profile image function
# profile image upload
# Like/unlike JS issue

###### Ideas
# include "occupation" field in user profile
# implement category for posts (education, legal, technology, mobile, gaming, medical/healthcare, etc.)
# a 2-column layout for edit_profile template


@bottle.post('/delete_post/<permalink>')
def remove_post(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    permalink = cgi.escape(permalink)

    if userID is None:  # if user is not logged in
        bottle.redirect('/')

    ## removal steps
    # 1. remove post from "posts" collection
    # 2. archive into "deleted_posts" collection
    # 3. remove like documents from the "likes" collection for the deleted post
    
    utc_timestamp = datetime.datetime.utcnow()
    removal_post = posts.remove_post(userID, permalink)
    post_archived = archived_posts.insert_entry(removal_post)  # if post_archived is false, we should try again; for now, just move on
    likes_removed = likes.remove_likes_for_post(permalink)  # if likes_removed is false, we should try again; for now, just move on
    
    if removal_post:
        bottle.redirect('/manage_posts')
    else:
        bottle.redirect('/internal_error')
        


####### BELOW FUNCTIONS ARE COMPLETE #######
@bottle.get('/delete_post/<permalink>')
def remove_post_page(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/')

    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    return bottle.template('delete_post',
                           dict(userID = userID, firstname = firstname, post = post))


@bottle.get('/edit_post/<permalink>')
def edit_post_page(permalink):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    
    if userID is None:
        bottle.redirect('/login')
    if post is None:
        bottle.redirect('/internal_error')
    
    post['l'] = ', '.join(post['l'])
    return bottle.template('post_entry',
                           dict(userID = userID, firstname = firstname, mode = 'edit',
                                post = post, error = ''))


@bottle.post('/edit_post/<permalink>')
def insert_editted_post(permalink):
    permalink = cgi.escape(permalink)
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/login')
        return

    post = {'p': permalink,  # "p" for permalink
            'a':  # "a" for author
                {'u': userID,  # author userID
                 'f': firstname},  # author first name
            's': bottle.request.forms.get("title"),  # "s" for subject; title
            'b':  # "b" for body
                {'c': bottle.request.forms.get("bodySummary"),  # "c" for concise; summary
                 'p': bottle.request.forms.get("bodyProblem"),  # "p" for problem
                 's': bottle.request.forms.get("bodySolution"),  # "s" for solution
                 'm': bottle.request.forms.get("bodyMonetize"),  # "m" for monetization method
                 'a': bottle.request.forms.get("bodyAdvertise")},  # "a" for advertisement method
            'y': bottle.request.forms.get("youtubeLink"),  # "y" for Youtube link
            'l': bottle.request.forms.get("tags"),  # "l" for tags label
            'i': None,  # "i" for interested users' userIDs, or likerIDs (will be imported from the original post document upon date)
            'lc': None,  # "lc" for likes count (will be imported from the original post document upon update)
            'fc': None  # "fc" for feedbacks count (will be imported from the original post document upon update)
            }

    error = {'e':''}

    if validate_post(posts, post, error, mode = 'edit'):
        post = clean_and_format_post(post)        
        postUpdated = posts.update_entry(post)
        if postUpdated:
            bottle.redirect("/post/" + permalink)
        else:
            bottle.redirect('internal_error')
    else:  # if post update not validated
        return bottle.template("post_entry", 
                               dict(userID = userID, firstname = firstname, mode = 'edit',
                                    post = post, error = error['e']))


@bottle.get('/manage_posts')
def manage_posts():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID is None:
        bottle.redirect('/')
        return

    my_posts_summaries = posts.get_post_summaries_by_userID(userID)
    
    return bottle.template("manage_posts",
                           dict(userID = userID, firstname = firstname,
                                summaries = my_posts_summaries))


@bottle.route('/liked_ideas')
def display_liked_ideas():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/')
        return

    liked_posts_permalinks = likes.get_liked_posts_permalinks_by_userID(userID)  # permalinks of posts that a user has liked
    liked_posts = []
    
    for permalink in liked_posts_permalinks:
        post = posts.get_post_by_permalink(permalink)
        XXX
        # post['i'] = str(userID)  # "i" for interested userIDs (or "likerIDs")
        liked_posts.append(post)

    return bottle.template('liked_posts', 
                           dict(userID = userID, firstname = firstname,
                                posts = liked_posts))


@bottle.post('/newfeedback')
def post_feedback():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:  # if user is not logged in (possible hack attempt)
        bottle.redirect('/login')
        return

    feedbackContent = bottle.request.forms.get("feedbackContent")  # will be escaped later (after the body length has been verified)
    permalink = bottle.request.forms.get("permalink"); permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    if post is None:  # if post not found (possible hack attempt)
        bottle.redirect("/post_not_found")
        return 

    if validate_content(content = feedbackContent, max_char_len = 1000, optional = False):
        feedbackContent = cgi.escape(feedbackContent, quote=True).strip()
        feedbackContent = format_newlines(feedbackContent)
        feedback_inserted = feedbacks.insert_feedback(permalink, firstname, userID, feedbackContent)
        if feedback_inserted:
            feedback_count_incremented = posts.increment_feedback_count(permalink)         
            if feedback_count_incremented:
                bottle.redirect("/post/" + permalink)
            else:  # we should try incrementing the count again; for now, just pass
                error = "Sorry, something went wrong."
                bottle.redirect('/internal_error')

    else:
        error = "What are you doing? No funny business is allowed here!"
    return bottle.template("entry_view", 
                            dict(userID = userID, firstname = firstname,
                                error = error, post = post, feedbackContent = ""))


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
                bottle.redirect("/internal_error")

            # bottle.redirect() is buggy in bottle 0.12 version; 
            # it can remove global cookies after redirect; 
            # https://github.com/bottlepy/bottle/issues/386
            # work-around solution (using beaker for session/cookie handling): https://github.com/marciocg/meuengenho_blog

            bottle.response.set_cookie("session", session_id)
            return bottle.redirect('/')

        else:
            bottle.redirect('/internal_error')
    else:
        error = "Sorry, you entered the wrong email address."
        return bottle.template('confirm_signup', 
                               dict(emailID = emailID, error = error))


@bottle.get('/edit_profile')
def edit_profile_page():
    cookie = bottle.request.get_cookie("session")
    userID = sessions.get_userID(cookie) 
    if userID is None:
        bottle.redirect('/login')
        return
    user = users.get_user(userID)
    
    return bottle.template("edit_profile",
                           dict(userID = userID, firstname = user['f'], user = user, error = ""))


@bottle.post('/edit_profile')
def edit_profile():
    cookie = bottle.request.get_cookie("session")
    userID = sessions.get_userID(cookie)
    if userID is None:
        bottle.redirect('/login')
        return
    
    firstname = bottle.request.forms.get("firstname")
    lastname = bottle.request.forms.get("lastname")
    bio = bottle.request.forms.get("bio")
    birthYear = bottle.request.forms.get("birthYear")
    facebookURL = bottle.request.forms.get("facebookURL")
    linkedInURL = bottle.request.forms.get("linkedInURL")
    otherURL = bottle.request.forms.get("otherURL")
    zip = bottle.request.forms.get("zip")
    gender = bottle.request.forms.get("gender")
    links = {'f': facebookURL, 'l': linkedInURL, 'o': otherURL}  # no error in JSON formation even when URLs are not escaped and they contain special characters (", ', >, <, etc.)
    
    error = {}
    
    if validate_profile_update(firstname, lastname, bio, birthYear, links, zip, gender, error):
        # all of the variables except bio should have been cleared of special characters in validate_profile_update();
        # however, we will escape them just for an added security measure
        firstname = cgi.escape(firstname)
        lastname = cgi.escape(lastname)
        bio = cgi.escape(bio, quote = True)
        birthYear = cgi.escape(birthYear)
        links['f'] = cgi.escape(links['f'])
        links['l'] = cgi.escape(links['l'])
        links['o'] = cgi.escape(links['o'])
        zip = cgi.escape(zip)
        gender = cgi.escape(gender)

        users_col_updated = users.edit_user_info(userID, firstname, lastname, bio, birthYear, links, zip, gender)
        posts_col_updated = posts.edit_author_firstname(userID, firstname)
        sessions_col_updated = sessions.edit_user_firstname(userID, firstname)
        feedbacks_col_updated = feedbacks.edit_user_firstname(userID, firstname)

        if users_col_updated and posts_col_updated and sessions_col_updated and feedbacks_col_updated:  # upon failure, we should try again; for now, just move on
            bottle.redirect('/user/' + str(userID))
            return  
        else:
            return bottle.template("error_template",
                                   dict(userID = userID, firstname = firstname))
    else: 
        user = {'f':firstname, 'l':lastname, 'b':bio, 'y':birthYear, 'w':links, 'z':zip, 'g':gender}
        return bottle.template("edit_profile",
                               dict(userID = userID, firstname = firstname, user = user, error = error['e']))


@bottle.get('/help')
def help_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    return bottle.template('help', 
                           dict(userID = userID, firstname = firstname))


@bottle.get('/contact_user/<queriedUserID>')
def contact_user_page(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    queriedUserID = cgi.escape(queriedUserID)
    queriedUser = users.get_user(queriedUserID) 
    
    # users not logged in will view the "please log in" message    
    return bottle.template('user_profile', 
                           dict(userID = userID, firstname = firstname, 
                                mode = 'contact', message = '',
                                queriedUser = queriedUser, 
                                error = ''))


@bottle.post('/contact_user/<queriedUserID>')
def contact_user(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID is None:
        bottle.redirect('/login')
        return

    queriedUserID = cgi.escape(queriedUserID)
    queriedUser = users.get_user(queriedUserID)
    subject = "You've received a message!"
    message = bottle.request.forms.get("message")
    
    error = {'e':''}
    
    if validate_message(message, error):
        email_sent = send_email(queriedUser['e'], subject, message)        
        if email_sent:
            bottle.redirect('/message_sent?targetUserID=' + queriedUserID)
        else:
            # error['e'] = "Sorry, there was an internal error. It wasn't you. It was us."
            bottle.redirect('/internal_error')

    return bottle.template('user_profile', 
                            dict(userID = userID, firstname = firstname, 
                                mode = 'contact', message = message, 
                                queriedUser = queriedUser,
                                error = error['e']
                                ))


@bottle.get('/message_sent')
def message_sent_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    targetUserID = bottle.request.query.get('targetUserID')
    if userID is None:
        bottle.redirect('/')
    
    return bottle.template('message_sent', 
                           dict(userID = userID, firstname = firstname, targetUserID = targetUserID))


@bottle.post('/like_post')
def like():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    permalink = bottle.request.forms.get('permalink'); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    like = likes.get_like(userID, permalink)
    
    if userID is None:
        bottle.redirect('/')
        return
    if post is None:
        bottle.redirect("/post_not_found")
        return
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
        bottle.redirect('/')
        return
    if post is None:
        bottle.redirect("/post_not_found")
        return
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
        bottle.redirect('/login')
        return
        
    return bottle.template("change_password",
                           dict(userID = userID, firstname = firstname,
                                current_password = "", new_password_1 = "", new_password_2 = "",
                                error = ""))


@bottle.post('/change_password')
def change_password():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)     
    if userID is None:
        bottle.redirect('/login')
        return
    
    current_password = bottle.request.forms.get("current_password"); current_password = cgi.escape(current_password)
    new_password = bottle.request.forms.get("new_password"); new_password = cgi.escape(new_password)
    new_password2 = bottle.request.forms.get("new_password2"); new_password2 = cgi.escape(new_password2)

    error = {}
    
    ## if all the passwords are good and a correct user submitted the post request
    if validate_passwords(users, userID, current_password, new_password, new_password2, error):  # blank userIDs are also caught here
        password_updated = users.update_password(userID, new_password)        
        if password_updated:
            bottle.redirect('/user/' + str(userID))
        else:
            return bottle.template("change_password",
                                   dict(userID = userID, firstname = firstname))
    ## if there is a bad password or an incorrect user submitted the post request
    else:
        return bottle.template("change_password", 
                               dict(userID = userID, firstname = firstname,
                                    error = error['e']))
                                    

@bottle.get('/')
def main_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    latest_posts = posts.get_posts_basic(10, 1, likes)

    return bottle.template('main', 
                           dict(userID = userID, firstname = firstname, posts = latest_posts))


@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    feedback_list = feedbacks.get_feedbacks_by_permalink(permalink)
    post_liked_by_user = True if likes.get_like(userID, permalink) else False

    if post is None:
        bottle.redirect("/post_not_found")

    return bottle.template("entry_view2", 
                           dict(userID = userID, firstname = firstname,
                                error = "", 
                                feedbackContent = "",
                                post = post,
                                feedbacks = feedback_list,
                                liked = post_liked_by_user
                                ))


@bottle.get('/insert_post')
def post_entry():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:  # if user is not signed in
        bottle.redirect('/login')

    ## build a blank post to populate form fields
    post = {'a':  # "a" for author
                {'u':userID,  # author userID
                 'f':firstname},  # author first name
            's':'',  # "s" for subject; title
            'b':  # "b" for body
                {'c':'',  # "c" for concise; summary
                 'p':'',  # "p" for problem
                 's':'',  # "s" for solution
                 'm':'',  # "m" for monetization method
                 'a':''},  # "a" for advertisement method
            'y':'',  # "y" for Youtube link
            'l':''  # "l" for label; tags
            }
    return bottle.template("post_entry", 
                           dict(userID = userID, firstname = firstname, mode = 'new_insert',
                                post = post, error = ""))


@bottle.post('/insert_post')
def insert_post():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    if userID is None:
        bottle.redirect('/login')
        return
    
    ## build a post document with submitted information (blank fields are initialized with blank values)
    post = {'a':  # "a" for author
                {'u': userID,  # author userID
                 'f': firstname},  # author first name
            's': bottle.request.forms.get("title"),  # "s" for subject; title
            'b':  # "b" for body
                {'c': bottle.request.forms.get("bodySummary"),  # "c" for concise; summary
                 'p': bottle.request.forms.get("bodyProblem"),  # "p" for problem
                 's': bottle.request.forms.get("bodySolution"),  # "s" for solution
                 'm': bottle.request.forms.get("bodyMonetize"),  # "m" for monetization method
                 'a': bottle.request.forms.get("bodyAdvertise")},  # "a" for advertisement method
            'y': bottle.request.forms.get("youtubeLink"),  # "y" for Youtube link
            'l': bottle.request.forms.get("tags"),  # "l" for tags label
            'i': None,  # 'i' for interested users' userIDs, or likerIDs
            'lc':0,  # "lc" for likes count
            'fc':0  # "fc" for feedbacks count
            }
    post['p'] = create_permalink(post['s'])  # create a permalink from submitted post title
    
    error = {'e':''}

    if validate_post(posts, post, error, mode = 'new_insert'): 
        post = clean_and_format_post(post)
        postInserted = posts.insert_entry(post)
        if postInserted:
            bottle.redirect("/post/" + post['p'])  # redirect to post's permalink
        else:
            bottle.redirect('internal_error')
    else:
        return bottle.template("post_entry",
                               dict(userID = userID, firstname = firstname, mode = 'new_insert',
                                    post = post, error = error['e']))



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
        bottle.redirect("/")
    return bottle.template("signup",
                           dict(firstname = "", lastname = "", emailID = "", password = "", password2 = "",
                                error = ""))


@bottle.post('/signup')
def process_signup():
    emailID = bottle.request.forms.get("emailID")
    firstname = bottle.request.forms.get("firstname")
    lastname = bottle.request.forms.get("lastname")
    password = bottle.request.forms.get("password")
    password2 = bottle.request.forms.get("password2")

    # set these up in case we have an error case
    error = {'e':''}
    
    ## if it was a good signup
    if validate_signup(users, emailID, firstname, lastname, password, password2, error):
        # emailID, firstname, and lastname do not need to be escaped before getting stored into Mongo because we know they do not contain special characters after they were validated by validate_signup()
        # however, for added security, we will escape all the variables anyway
        emailID = cgi.escape(emailID).strip()
        firstname = cgi.escape(firstname).strip()
        lastname = cgi.escape(lastname).strip()
        password = cgi.escape(password)  # DO NOT STRIP PASSWORDS!
        
        signup_conf_str = make_rand_str(32)

        userID = users.add_user(emailID, firstname, lastname, password, signup_conf_str)
        if not userID:  # error inserting
            return bottle.redirect("/internal_error")
        else:  # if user signup successfully inserted into db
            signup_conf_link = base_url + '/confirm_signup/' + signup_conf_str
            subject = "Signup Confirmation"
            message = "Thanks for signing up! You can confirm your signup by visiting this link: %s" % signup_conf_link
            email_sent = send_email(emailID, subject, message)
            if email_sent:
                bottle.redirect('/please_confirm_email')
            else:
                bottle.redirect('/internal_error')


    ## if it was a bad signup
    else: 
        # firstname, lastname, emailID variables do not need to be escaped in the server side as they are escaped in the template engine;
        # in fact, if they were escaped in the server-side, the client-side would escape the escaped strings
        return bottle.template("signup", 
                               dict(firstname = firstname, lastname = lastname, emailID = emailID, password = '', password2 = '',
                                    error = error['e'],
                                    ))


@bottle.get('/please_confirm_email')
def please_confirm_email_page():
    return bottle.template('please_confirm_email')


@bottle.get('/login')
def present_login():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID:
		bottle.redirect("/")
		return
    return bottle.template("login",
                           dict(userID = userID, firstname = firstname,
                                emailID = "", password = "",
                                error = ""
                                ))


@bottle.post('/login')
def process_login():
    emailID = bottle.request.forms.get("emailID"); emailID = cgi.escape(emailID)
    password = bottle.request.forms.get("password"); password = cgi.escape(password)

    error = {'e':''}

    user_record = users.validate_login(emailID, password, error)
    if user_record:  # if valid login credentials provided
        session_id = sessions.start_session(user_record['_id'], user_record['f'])  # start_session() takes in userID and first name
        if session_id is None:
            bottle.redirect("/internal_error")
        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)
        bottle.redirect("/")

    else:  # if 1. invalid login credential provided, 2. user hasn't confirmed his/her email address
        return bottle.template("login",
                               dict(emailID = emailID, password = "",
                                    error = error['e']
                                    ))


@bottle.get('/logout')
def process_logout():
    cookie = bottle.request.get_cookie("session")
    sessions.end_session(cookie)
    bottle.response.set_cookie("session", "")
    bottle.redirect("/")
    
    
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
archive_posts = archivePostDAO.archivePostDAO(database)
users = userDAO.userDAO(database)
sessions = sessionDAO.sessionDAO(database)
feedbacks = feedbackDAO.feedbackDAO(database)
likes = likeDAO.likeDAO(database)

bottle.debug(True)
bottle.run(host="localhost", port=8082)


"""
def main():
    bottle.debug(True)
    run_wsgi_app(bottle.default_app())

if __name__=="__main__":
    main()
"""
