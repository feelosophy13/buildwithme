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

def validate_newpost(postDAO, userID, permalink, title, postContent, youtubeLink, tags, error):
    error['e'] = ''

    if userID is None or len(title) > 120 or len(postContent) > 2000: 
        error['e'] = "Please don't hack us."
        return False
    if postDAO.get_post_by_permalink(permalink):  # if there is another post with the same permalink (and thus with the same title)
        error['e'] = "Sorry, there is another post with the same title."
        return False
    if not validate_content(title, max_char_len = 120, optional = False):
        error['e'] = "Sorry, invalid title."
        return False
    if not validate_content(postContent, max_char_len = 2000, optional = False):
        error['e'] = 'Sorry, invalid body content.'
        return False
    if not validate_URL(youtubeLink, optional = True):
        error['e'] = 'Sorry, invalid link to a Youtube video.'
        return False
    if not validate_tags(tags, optional = True):
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


def validate_signup(userDAO, emailID, firstname, lastname, password, password2, error):
    error['e'] = ""
    
    if userDAO.emailID_exists(emailID):
        error['e'] = "That email ID is already taken. Try another?"
        return False
    if not validate_email(emailID):
        error['e'] = "That's an invalid email address."
        return False
    if not validate_name(firstname) or not validate_name(lastname):
        error['e'] = "Sorry, invalid name."
        return False
    if not validate_password(password):
        error['e'] = "Sorry. Invalid password. At least 3 characters, k?"
        return False
    if password != password2:
        error['e'] = "Grr... The passwords must match!"
        return False
    return True


def validate_profile_update(userID, firstname, lastname, bio, birthYear, links, zip, gender, error):
    error['e'] = ""
    
    if not validate_name(firstname) or not validate_name(lastname):
        error['e'] = "Sorry, invalid name."
        return False
    if not validate_content(bio, max_char_len = 800):
        error['e'] = "Sorry. Bio must be 800 characters or less."
        return False
    if not validate_birth_year(birthYear):
        error['e'] = "Sorry. Please enter a valid birth year."
        return False        
    if not validate_URL(links['f']) or not validate_URL(links['l']) or not validate_URL(links['o']):
        error['e'] = "Sorry, an invalid URL."
        return False
    if not validate_zip(zip):
        error['e'] = "Sorry, that's an invalid zipcode."
        return False
    if not validate_gender(gender):
        return False
    return True


def validate_gender(gender, optional = True):
    if optional and gender == '':
        return True
    return gender == 'f' or gender == 'm' or gender == 'o'


def validate_tags(tags, optional = True):
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


def validate_URL(URL, optional = True):
    if optional and URL is '':
        return True        
    request = urllib2.Request(URL)
    try:	
        response = urllib2.urlopen(request)
        return True
    except urllib2.URLError:
        return False


def validate_zip(zip, optional = True):
    if optional and zip is '':
        return True
    ZIP_RE = re.compile(r"^[0-9]{5}$")
    if not ZIP_RE.match(zip):
        return False
    return True


def validate_birth_year(birth_year, optional = True):
    if optional and birth_year is '':
        return True
    try:        
        birth_year = int(birth_year)
        minimum_birth_year = 1920
        current_year = datetime.datetime.now().year
        return birth_year > minimum_birth_year and birth_year < current_year - 12 
    except:
        return False



def validate_content(content, max_char_len, optional = True):
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


def extract_posts_through_cursor(cursor):
    l = []                    
    for post in cursor:
        utc_timestamp = post['_id'].generation_time  # naive datetime instance (contains no timezone info in the object)
        pt_formatted = convert_utc_to_formatted_pt(utc_timestamp)
        post['t'] = pt_formatted  # store the extract timestamp in Pacific Time
        post['pd'] = extract_preview_description(body = post['b'], n_words = 30, n_chars = 240)

        l.append({
                  'p': post['p'],  # postID or permalink
                  'a': post['a'],  # "a" for author
                  's': post['s'],  # title
                  'b': post['b'],  # body
                  'y': post['y'],  # youtube link
                  'l': post['l'],  # tags
                  'fc': post['fc'],  # feedback count
                  'lc': post['lc'],  # like count
                  't': post['t'],   # timestamp
                  'pd': post['pd']  # preview description
                  })
    return l


def make_rand_str(n_char = None):
	str = ""
	n_char = 32 if n_char is None else n_char

	for i in range(n_char):
		str += random.choice(string.ascii_letters)
	return str


def make_hash(string, salt = None):
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