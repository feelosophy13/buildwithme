import bottle
import pymongo

import postDAO
import sessionDAO
import userDAO
import feedbackDAO
import likeDAO

import cgi
import re
import datetime
import pytz

from beaker.middleware import SessionMiddleware
from helpers import create_permalink, validate_newpost, validate_passwords, validate_signup, validate_profile_update, validate_message, send_email, extract_tags, format_newlines, make_rand_str



@bottle.get('/test')
def test():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    return bottle.template('test')


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
    

@bottle.post('/newfeedback')
def post_feedback():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)

    feedbackContent = bottle.request.forms.get("feedbackContent")  # will be escaped later (after the body length has been verified)
    permalink = bottle.request.forms.get("permalink"); permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    if userID is None:  # if user is not logged in (possible hack attempt)
        bottle.redirect('/login')
    if post is None:  # if post not found (possible hack attempt)
        bottle.redirect("/post_not_found")

    error = {}
    
    if validate_feedback(feedbackContent, error):
        feedbackContent = cgi.escape(feedbackContent, quote=True).strip()
        feedbackContent = format_newline(feedbackContent)
        feedback_inserted = feedbacks.insert_feedback(permalink, firstname, userID, feedbackContent)
        if feedback_inserted:
            feedback_count_incremented = posts.increment_feedback_count(permalink)         
            if feedback_count_incremented:
                return True
            else:  # should try again; for now, just pass
                pass                
        bottle.redirect("/post/" + permalink)
    else:
        feedback = {'b': ""}
        error = "What are you doing? No funny business is allowed here!"
        return bottle.template("entry_template", 
                               dict(userID = userID, firstname = firstname,
                                    error = error, post = post, feedback = feedback))


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



@bottle.route('/edit_post')
def edit_post():
    cookie = bottle.request.get_cookie("session")
    userID = sessions.get_userID(cookie) 
    return "AY!"

    
@bottle.route('/liked_ideas')
def display_liked_ideas():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)
    liked_posts_permalinks = likes.get_liked_posts_permalinks_by_userID(userID)
    
    liked_posts = []
    for permalink in liked_posts_permalinks:
        post = posts.get_post_by_permalink(permalink)
        liked_posts.append(post)
        
    print liked_posts

    return bottle.template('posts_grid_display', 
                           dict(userID = userID, firstname = firstname,
                                posts = liked_posts))




##### TO-DO
# 5. Clean up newfeedback()
# 8. Fix liked posts page
# 9. Like/unlike JS issue

# 11. profile image upload
# 12. Contact us and "Terms and Conditions" pages in the "How We Work" page
# 13. Post grid display in boxes


    
    

####### BELOW FUNCTIONS ARE COMPLETE #######
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
    conf_str_url = cgi.escape(conf_str_url)
    
    if userID:  # if user is already signed in
        bottle.redirect("/")  # redirect to homepage
    
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
    user = users.get_user(userID)
    
    return bottle.template("edit_profile",
                           dict(userID = userID, firstname = user['f'], user = user, error = ""))


@bottle.post('/edit_profile')
def edit_profile():
    cookie = bottle.request.get_cookie("session")
    userID = sessions.get_userID(cookie)
    firstname = bottle.request.forms.get("firstname"); 
    lastname = bottle.request.forms.get("lastname"); 
    bio = bottle.request.forms.get("bio"); 
    birthYear = bottle.request.forms.get("birthYear"); 
    facebookURL = bottle.request.forms.get("facebookURL");
    linkedInURL = bottle.request.forms.get("linkedInURL"); 
    otherURL = bottle.request.forms.get("otherURL"); 
    zip = bottle.request.forms.get("zip"); 
    gender = bottle.request.forms.get("gender")
    links = {'f': facebookURL, 'l': linkedInURL, 'o': otherURL}  # no error in JSON formation even when URLs are not escaped and they contain special characters (", ', >, <, etc.)
    
    error = {}
    
    if validate_profile_update(userID, firstname, lastname, bio, birthYear, links, zip, gender, error):
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

        profile_updated = users.edit_user_info(userID, firstname, lastname, bio, birthYear, links, zip, gender)

        if profile_updated:
            bottle.redirect('/user/' + str(userID))
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
    
    return bottle.template('user_profile', 
                           dict(userID = userID, firstname = firstname, 
                                mode = 'contact', message = '',
                                queriedUser = queriedUser, 
                                error = ''))


@bottle.post('/contact_user/<queriedUserID>')
def contact_user(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
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
    
    if post is None:
        bottle.redirect("/post_not_found")
        return
    if like:  # if user already liked the post
        print "You already liked this post!"
        return False
    
   ## process a like
    like_logged = likes.log_like(userID, permalink)
    if like_logged:  # only if like was logged, increment the like count
        likes_count_incremented = posts.increment_likes_count(permalink)
        if likes_count_incremented:
            return 'success'
        else:  # if there was an error incrementing the like count 
            # should try again; for now, just remove the like log and throw an error
            likes.remove_like(userID, permalink)
            return False              
    else:
        return False  # there was an error logging the like

   
@bottle.post('/unlike_post')
def unlike():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    permalink = bottle.request.forms.get("permalink"); cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)
    like = likes.get_like(userID, permalink)

    if post is None:
        bottle.redirect("/post_not_found")
        return
    if not like:  # if there is no like to unlike
        print "There is no like to remove!"
        return False

    ## process an unlike
    like_removed, likeID = likes.remove_like(userID, permalink)
    if like_removed:  # only if like log was removed, decrement the like count
        likes_count_decremented = posts.decrement_likes_count(permalink)
        if likes_count_decremented:
            return 'success'
        else:  # if there was an error decrementing the like count
            # should try again; for now just, restore the like log and throw and error
            likes.restore_like(likeID, userID, permalink)
            return False
    else: 
        return False  # there was an error removing the like


@bottle.get('/change_password')
def change_password_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 

    return bottle.template("change_password",
                           dict(userID = userID, firstname = firstname,
                                current_password = "", new_password_1 = "", new_password_2 = "",
                                error = ""))


@bottle.post('/change_password')
def change_password():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    current_password = bottle.request.forms.get("current_password"); current_password = cgi.escape(current_password)
    new_password = bottle.request.forms.get("new_password"); new_password = cgi.escape(new_password)
    new_password2 = bottle.request.forms.get("new_password2"); new_password2 = cgi.escape(new_password2)

    error = {}
    
    ## if all the passwords are good
    if validate_passwords(users, userID, current_password, new_password, new_password2, error):
        password_updated = users.update_password(userID, new_password)        
        if password_updated:
            bottle.redirect('/user/' + str(userID))
        else:
            return bottle.template("change_password",
                                   dict(userID = userID, firstname = firstname))
    ## if there is a bad password
    else:
        return bottle.template("change_password", 
                               dict(userID = userID, firstname = firstname,
                                    error = error['e']))
                                    

@bottle.get('/')
def main_page():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    latest_posts = posts.get_posts(10, 1)
    return bottle.template('main', 
                           dict(userID = userID, firstname = firstname, posts = latest_posts))


@bottle.get("/post/<permalink>")
def show_post(permalink="notfound"):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie) 
    permalink = cgi.escape(permalink)
    post = posts.get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post_not_found")

    l = feedbacks.get_feedbacks_by_permalink(permalink)
    return bottle.template("entry_template", 
                           dict(post = post, 
                                userID = userID, firstname = firstname,
                                error = "", 
                                newFeedbackContent = ""))



@bottle.get('/newpost')
def get_newpost():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    

    if userID is None:  # if user is not signed in
        bottle.redirect('/login')
    return bottle.template("newpost_template", 
                           dict(userID = userID, firstname = firstname,
                                title = "", postContent = "", youtubeLink = "", tags = "", 
                                error = ""))


@bottle.post('/newpost')
def post_newpost():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)

    title = bottle.request.forms.get("title");
    postContent = bottle.request.forms.get("postContent"); 
    youtubeLink = bottle.request.forms.get("youtubeLink"); 
    tags = bottle.request.forms.get("tags"); 

    error = {'e':''}
    permalink = create_permalink(title)

    if validate_newpost(posts, userID, permalink, title, postContent, youtubeLink, tags, error):
        
        title = cgi.escape(title, quote = True).strip()
        postContent = cgi.escape(postContent, quote = True).strip()
        youtubeLink = cgi.escape(youtubeLink).strip()
        tags = cgi.escape(tags).strip()
    
        postContent = format_newlines(postContent)
        tags_array = extract_tags(tags)
        
        postInserted = posts.insert_entry(permalink, title, postContent, youtubeLink, tags_array, userID, firstname)
        if postInserted:
            bottle.redirect("/post/" + permalink)
        else:
            bottle.redirect('internal_error')
    else:
        return bottle.template("newpost_template", 
                               dict(userID = userID, firstname = firstname, 
                                    title = title, postContent = postContent, youtubeLink = youtubeLink, tags = tags,
                                    error = error['e']
                                    ))



@bottle.get('/user/<queriedUserID>')
def user_profile(queriedUserID):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    queriedUserID = cgi.escape(queriedUserID)    

    queriedUser = users.get_user(queriedUserID)
    postsByUser = posts.get_posts_by_userID(queriedUserID)
    
    return bottle.template('user_profile',
                           dict(userID = userID, firstname = firstname, mode = 'view',
                                queriedUser = queriedUser, posts = postsByUser))    


# The main page of the blog, filtered by tag
@bottle.route('/tag/<tag>')
def posts_by_tag(tag="notfound"):
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    escaped_tag = cgi.escape(tag)

    posts_by_tag = posts.get_posts_by_tag(escaped_tag, 10)

    return bottle.template('posts_by_tag', 
                           dict(userID = userID, firstname = firstname,
                                tag = tag, posts = posts_by_tag))


@bottle.get('/signup')
def present_signup():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID:  # if user is already signed in
        bottle.redirect("/")  # redirect to homepage
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


# displays the initial login form
@bottle.get('/login')
def present_login():
    cookie = bottle.request.get_cookie("session")
    userID, firstname = sessions.get_userID_firstname(cookie)    
    if userID:
		bottle.redirect("/")
    return bottle.template("login",
                           dict(userID = userID, firstname = firstname,
                                emailID = "", password = "",
                                error = ""
                                ))


# handles a login request
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

    else:  # if invalid login credential provided
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
users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)
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
