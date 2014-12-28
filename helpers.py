import datetime
import pytz
import re
import cgi
import smtplib
import sys
import urllib2
import string
import random

from private.email_credentials import smtp_host, smtp_port, sender_emailID, sender_emailPassword


############################################
def build_user_JSON(userID, form_input=None):
    if form_input:
        user = {'_id': userID,
                'f': form_input.get("firstname"),  # "f" for first name
                'l': form_input.get("lastname"),  # "l" for last name
                'b': form_input.get("bio"),  # "b" for bio
                'y': form_input.get("birthYear"),  # "y" for birth year
                'w':  # "w" for web links; JSON safe even when the URLs contain special characters (", ', >, <, etc.)
                     {'f': form_input.get("facebookURL"),  # "f" for Facebook URL
                      'l': form_input.get("linkedInURL"),  # "l" for LinkedIn URL
                      'o': form_input.get("otherURL")},  # "o" for other URL
                'z': form_input.get("zip"),  # "z" for zipcode
                'g': form_input.get("gender"),  # "g" for gender
                'o': form_input.get("occupation")  # "o" for occupation
                }
        return user


def build_user_signup_JSON(form_input=None):
    if form_input is None:
        user_signup = {'e':'', 'f':'', 'l':'', 'p':'', 'p2':''}
    else:
        user_signup = {'e': form_input.get("emailID"),
                       'f': form_input.get("firstname"),
                       'l': form_input.get("lastname"),
                       'p': form_input.get("password"),
                       'p2': form_input.get("password2")}
    return user_signup


def build_post_JSON(userID, firstname, form_input=None, permalink=None):
    
    ## for get requests to "/insert_post" page i.e. for insert_post_page()
    if form_input is None:
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
    
    ## for post requests to "/insert_post" page i.e. for insert_post(), or
    ## for post requests to "/edit_post" page i.e. for update_post()
    else:
        post = {'a':  # "a" for author
                    {'u': userID,  # author userID
                     'f': firstname},  # author first name
                's': form_input.get("title"),  # "s" for subject; title
                'b':  # "b" for body
                    {'c': form_input.get("bodySummary"),  # "c" for concise; summary
                     'p': form_input.get("bodyProblem"),  # "p" for problem
                     's': form_input.get("bodySolution"),  # "s" for solution
                     'm': form_input.get("bodyMonetize"),  # "m" for monetization method
                     'a': form_input.get("bodyAdvertise")},  # "a" for advertisement method
                'y': form_input.get("youtubeLink"),  # "y" for Youtube link
                'l': form_input.get("tags"),  # "l" for tags label
                }
        if permalink is None:  # if permalink wasn't given (in case of a submission for a new post)
            post['p'] = create_permalink(post['s'])  # create a permalink from submitted post title
            post['lc'] = post['fc'] = 0  # "lc" for likes count; "fc" for feedbacks count
        else:  # if permalink was given (in case of updating an existing post)
            post['p'] = permalink
            post['lc'] = post['fc'] = None  # "lc" for likes count (will be imported from the original post document upon update)

    return post


def create_archive_post(post, feedbacks, likerIDs):
    post['d'] = datetime.datetime.utcnow()  # "d" for delete timestamp
    post['i'] = likerIDs  # "i" for interested users' userIDs, or likerIDs
    post.pop('t', 0)  # remove the "t" (PT date/time) key-value pair as we will user postID to get the UTC timestamp

    for feedback in feedbacks:
        feedback['a'] = feedback['a']['u']  # include only the userID information instead of both userID and first name of the feedback author
        feedback.pop('p', 0)  # remove the "p" (permalink) key-value pair as the information is already present in the post document and will become redundant
        feedback.pop('t', 0)  # remove the "t" (PT date/time) key-value pair as we will user feedbackID to get the UTC timestamp
    post['f'] = feedbacks  # "f" for feedbacks
    return post


def clean_and_format_user_signup(user_signup):
    user_signup['e'] =  cgi.escape(user_signup['e']).strip()  # "e" for emailID
    user_signup['f'] = cgi.escape(user_signup['f']).strip()  # "f" for first name
    user_signup['l'] = cgi.escape(user_signup['l']).strip()  # "l" for last name
    user_signup['p'] = cgi.escape(user_signup['p'])  # "p" for password; DO NOT STRIP PASSWORDS; a blank space can be part of the password
    user_signup.pop('p2', 0)  # "p2" for the second (verification) password; remove it since we only need to store one password key-value pair
    return user_signup


def clean_and_format_user(user):
    user['f'] = cgi.escape(user['f'])  # first name
    user['l'] = cgi.escape(user['l'])  # last name
    user['b'] = cgi.escape(user['b'], quote=True)  # bio
    user['b'] = format_newlines(user['b'])  # bio
    user['y'] = cgi.escape(user['y'])  # birth year
    user['w']['f'] = cgi.escape(user['w']['f'])  # Facebook URL
    user['w']['l'] = cgi.escape(user['w']['l'])  # LinkedIn URL
    user['w']['o'] = cgi.escape(user['w']['o'])  # other URL
    user['z'] = cgi.escape(user['z'])  # zipcode
    user['g'] = cgi.escape(user['g'])  # gender
    user['o'] = cgi.escape(user['o'])  # occupation
    return user


def clean_and_format_post(post):
    post['s'] = cgi.escape(post['s'], quote=True)  # "s" for subject"
    for key in post['b'].keys():  # "b" for body; the sub-keys in "b" are "c" for concise summary, "p" for problem, "s" for solution, "m" for monetization, and "a" and advertising
        postContent = cgi.escape(post['b'][key], quote=True).strip()
        postContent = format_newlines(postContent)
        post['b'][key] = postContent
    post['y'] = cgi.escape(post['y']).strip()  # "y" for Youtube link
    post['l'] = cgi.escape(post['l']).strip()  # "l" for tag labels
    post['l'] = extract_tags(post['l'])  # "l" for tag labels
    return post


def clean_and_format_feedback(feedback):
        feedback['b'] = cgi.escape(feedback['b'], quote=True).strip()  # "b" for body
        feedback['b'] = format_newlines(feedback['b'])  # "b" for body
        return feedback


def validate_feedback(feedbackDAO, feedback, error, mode):
    error['e'] = ''
    
    ## if updating a new feedback, check for three things:
    ## 1. make sure there exists an original feedback with the given feedbackID 
    ## 2. the user is the feedback author and can modify the content
    ## 3. the user is submitting a new content (not the same)

    if mode == 'update':
        orig_feedback = feedbacks.get_feedback_by_feedbackID(feedbackID)

        if orig_feedback is None:
            error['e'] = "Sorry, no such post was found."
            return False

        if feedback['a']['u'] != orig_feedback['a']['u']:
            error['e'] = "Sorry, you are not the author of this feedback and don't have the permission to modify the content."
            return False

        if feedback['b'] == orig_feedback['b']:
            error['e'] = "Sorry, you haven't changed anything!"
            return False
        
    ## regardless of the mode, validate feedback body content
    if not validate_content(feedback['b'], max_char_len=1000, optional=False):
        error['e'] = "Sorry, maximum of 1000 characters."
        return False
    return True    


def validate_post(postDAO, post, error, mode):
    error['e'] = ''

    ## if inserting a new post, make sure permalink is unique
    if mode == 'new_insert':  
        if postDAO.get_post_by_permalink(post['p'], 'complete'):  # if there is another post with the same permalink (and thus with the same title)
            error['e'] = "Sorry, there is another post with the same title."
            return False
    
    ## validate post title
    if not validate_content(post['s'], max_char_len=120, optional=False):
        error['e'] = "Sorry, invalid title. Maximum of 120 characters."
        return False

    ## validate post body -- summary
    if not validate_content(post['b']['c'], max_char_len=200, optional=False):
        error['e'] = 'Sorry, invalid summary content. Maximum of 200 characters.'
        return False

    ## validate post body -- problem
    if not validate_content(post['b']['p'], max_char_len=500, optional=False):
        error['e'] = 'Sorry, invalid body content describing the problem. Maximum of 500 characters.'
        return False

    ## validate post body -- solution
    if not validate_content(post['b']['s'], max_char_len=500, optional=False):
        error['e'] = 'Sorry, invalid body content describing the solution. Maximum of 500 characters.'
        return False

    ## validate post body -- monetization
    if not validate_content(post['b']['m'], max_char_len=500, optional=False):
        error['e'] = 'Sorry, invalid body content describing the monetization methods. Maximum of 500 characters.'
        return False

    ## validate post body -- advertise
    if not validate_content(post['b']['a'], max_char_len=500, optional=False):
        error['e'] = 'Sorry, invalid body content describing the marketing methods. Maximum of 500 characters.'
        return False

    ## validate post Youtube link
    if not validate_URL(post['y'], optional=True):
        error['e'] = 'Sorry, invalid link to a Youtube video.'
        return False

    ## validate post tags
    if not validate_tags(post['l'], optional=True):
        error['e'] = "Sorry, invalid tags. Maximum of 6 tags, please."
        return False        
    return True


def send_email(receipient_emailID, subject, message):
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo
    server.login(sender_emailID, sender_emailPassword)
    
    message = message.strip()
    body = '\r\n'.join([
           'To: %s' % receipient_emailID,
           'From: %s' % sender_emailID,
           'Subject: %s' % subject,
           '',
           message
           ])

    try: 
        server.sendmail(sender_emailID, [receipient_emailID], body)
        server.quit()
        return True
    except:
        print "Unexpected error on send_email:", sys.exc_info()[0]
        server.quit()
        return False


def extract_preview_description(body, n_words, n_chars):
    body = body[0:n_chars]
    words_list = body.split(' ')
    preview_words_list = words_list[0:n_words]
    preview_description = ' '.join(preview_words_list)
    preview_description += '...'
    return preview_description


def create_permalink(title):
	exp = re.compile('\W') # match anything not alphanumeric
	whitespace = re.compile('\s')
	temp_title = whitespace.sub("_",title)
	permalink = exp.sub('', temp_title)
	return permalink


def validate_passwords(userDAO, userID, current_password, new_password, new_password2, error):
    error['e'] = ""
    
    if current_password != '' and new_password != '' and new_password2 != '':
        if new_password == new_password2:  # if the two new passwords match
            if validate_password(new_password):    # if the new password is good (at least 3 characters long)
                current_passwords_match = userDAO.passwords_match(userID, current_password)  # if the current passwords match
                if current_passwords_match:
                    return True
                else:
                    error['e'] = "Sorry, your current password doesn't match."
                    return False
            else:
                error['e'] = "Sorry, invalid password. At least 3 characters, please!"
                return False
        else:
            error['e'] = "Your new passwords don't match."
            return False
    else:
        error['e'] = "Please fill out all the fields."
        return False


def validate_signup(userDAO, user_signup, error):
    error['e'] = ""

    if userDAO.emailID_exists(user_signup['e']):
        error['e'] = "That email ID is already taken. Try another?"
        return False
    if not validate_email(user_signup['e']):
        error['e'] = "That's an invalid email address."
        return False
    if not validate_name(user_signup['f']) or not validate_name(user_signup['l']):
        error['e'] = "Sorry, invalid name."
        return False
    if not validate_password(user_signup['p']):
        error['e'] = "Sorry. Invalid password. At least 3 characters, k?"
        return False
    if user_signup['p'] != user_signup['p2']:
        error['e'] = "Grr... The passwords must match!"
        return False
    return True


def validate_profile_update(userDAO, user, error):
    error['e'] = ""
    
    if not validate_name(user['f']) or not validate_name(user['l']):
        error['e'] = "Sorry, invalid name."
        return False
    if not validate_content(user['b'], max_char_len=800):
        error['e'] = "Sorry. Bio must be 800 characters or less."
        return False
    if not validate_birth_year(user['y']):
        error['e'] = "Sorry. Please enter a valid birth year."
        return False        
    if not validate_URL(user['w']['f']) or not validate_URL(user['w']['l']) or not validate_URL(user['w']['o']):
        error['e'] = "Sorry, an invalid URL."
        return False
    if not validate_zip(user['z']):
        error['e'] = "Sorry, that's an invalid zipcode."
        return False
    if not validate_gender(user['g']):
        error['e'] = "Sorry, please select the correct gender."
        return False
    if not validate_occupation(user['o']):
        error['e'] = "Sorry, please enter a valid occupation title."
        return False
        
    return True


def validate_gender(gender, optional=True):
    if optional and gender == '':
        return True
    return gender == 'f' or gender == 'm' or gender == 'o'


def validate_occupation(occupation, optional=True):
    if optional and occupation == '':
        return True
    OCCUP_RE = re.compile(r"^[a-zA-Z-/]{1,30}$")
    if not OCCUP_RE.match(occupation):
        return False
    return True


def validate_tags(tags, optional=True):
    if optional and tags == '':
        return True
    if len(tags) > 120:
        return False
    tags_array = tags.split(',')
    if len(tags_array) > 6:
        return False
    return True


def format_newlines(body):
    body = body.strip()
    newline = re.compile('\r?\n')
    formatted_body = newline.sub("<p>", body)  # substitute some <p> for the paragraph breaks
    return body


def extract_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("",tags)
    tags_array = nowhite.split(',')
    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)
    return cleaned
    

def convert_utc_to_formatted_pt(utc_timestamp):
    pt_tz = pytz.timezone('US/Pacific')  # specify the timezone to convert to
    pt_timestamp = utc_timestamp.astimezone(pt_tz)  # timestamp in Pacific Time (Standard or Daylight-Savings automatically calculated)
    pt_formatted = pt_timestamp.strftime("%A, %B %d, %Y")
    return pt_formatted


def validate_email(emailID):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    if not EMAIL_RE.match(emailID):
        return False
    return True


def validate_name(name):
    NAME_RE = re.compile(r"^[a-zA-Z-]{1,30}$")
    if not NAME_RE.match(name):
        return False
    return True


def validate_password(password):
    PASS_RE = re.compile(r"^.{3,30}$")
    if not PASS_RE.match(password):
        return False
    return True


def validate_URL(URL, optional=True):
    if optional and URL is '':
        return True        
    request = urllib2.Request(URL)
    try:	
        response = urllib2.urlopen(request)
        return True
    except urllib2.URLError:
        return False


def validate_zip(zip, optional=True):
    if optional and zip is '':
        return True
    ZIP_RE = re.compile(r"^[0-9]{5}$")
    if not ZIP_RE.match(zip):
        return False
    return True


def validate_birth_year(birth_year, optional=True):
    if optional and birth_year is '':
        return True
    try:        
        birth_year = int(birth_year)
        minimum_birth_year = 1920
        current_year = datetime.datetime.now().year
        return birth_year > minimum_birth_year and birth_year < current_year - 12 
    except:
        return False



def validate_content(content, max_char_len, optional=True):
    if optional and content is '':
        return True
    char_len = len(content)
    if char_len > max_char_len or char_len == 0:
        return False
    return True

    
def validate_message(message, error):
    message = message.strip()
    if message == '':
        error['e'] = "No blank messages, please."
        return False
    elif len(message) > 2000:
        error['e'] = "Please don't go over the maximum message length."
        return False
    return True


def convert_utc_to_formatted_pt(utc_timestamp):
    pt_tz = pytz.timezone('US/Pacific')  # specify the timezone to convert to
    pt_timestamp = utc_timestamp.astimezone(pt_tz)  # timestamp in Pacific Time (Standard or Daylight-Savings automatically calculated)
    pt_formatted = pt_timestamp.strftime("%A, %B %d, %Y")
    return pt_formatted


def extract_posts_through_cursor(cursor, likeDAO):
    l = []                    
    for post in cursor:
        utc_timestamp = post['_id'].generation_time  # naive datetime instance (contains no timezone info in the object)
        pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)  # store the extracted UTC timestamp in Pacific Time
        likerIDs = likeDAO.get_likerIDs_by_permalink(post['p'])
        # preview = extract_preview_description(body = post['b'], n_words = 30, n_chars = 240)
        
        if 'y' not in post:
            post['y'] = ''
        if 'l' not in post:
            post['l'] = []
        post['t'] = pt_formatted  # "t" for PT timestamp
        post['i'] = likerIDs  # "i" for interested users        
        # post['pd'] = preview  # "pd" for preview description

        l.append(post)
    return l


def make_rand_str(n_char=None):
	str = ""
	n_char = 32 if n_char is None else n_char

	for i in range(n_char):
		str += random.choice(string.ascii_letters)
	return str


def make_hash(string, salt=None):
	if salt == None:
		salt = make_salt();
	return hashlib.sha256(string + salt).hexdigest()+","+ salt


"""
## works if utc_timestamp is a naive instance without timezone information
def convert_utc_to_formatted_pt(utc_timestamp):
    utc_tz = pytz.timezone('UTC')  # UTC timezone
    utc_timestamp = utc_tz.localize(utc_timestamp)  # datetime instance with UTC timezone info stored in the object (no longer naive instance)
    pt_tz = pytz.timezone('US/Pacific')  # specify the timezone to convert to
    pt_timestamp = utc_timestamp.astimezone(pt_tz)  # timestamp in Pacific Time (Standard or Daylight-Savings automatically calculated)
    pt_formatted = pt_timestamp.strftime("%A, %B %d, %Y")
#    pt_timestamp = pt_timestamp.strftime("%A, %B %d, %Y at %I:%M %p")  # specify the date format

    return pt_formatted
"""