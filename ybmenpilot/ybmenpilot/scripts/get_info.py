# import statements
from ybmenpilot.models import GroupPost, GroupComment, Update
from ybmenpilot.models import Participant 
import re, hashlib
# import facebook
from django.contrib import admin
from django.db import IntegrityError
from open_facebook import OpenFacebook as ofc

# GROUP ID INFORMATION
GROUP_ID = "723681984369358"
# should save these in database by study - different groups?

## helper functions

def anonymize(ident):
  m = hashlib.sha224(ident).hexdigest()
  return m

def get_links_from_message(msg):
    """Function to pull out FIRST link content from posts (generic/loose fitting)"""
    match = re.findall(r"(https?:\/\/(www)?.?\w*.[a-zA-Z0-9]*.?[\S]+)",msg)
    if match:
        #print msg
        return str(match[0][0])
    else:
        return "None" # safety so string for db

## objects to handle information
# #Post object
class Post(object):
    """Object representing post on group"""
    def __init__(self, post_dict):
        self._id = anonymize(post_dict["id"][-15:]) # know post id length for now (summer 2014)
        if 'message' in post_dict:
            self._message = post_dict['message']
        else:
            self._message = ""
        self._commenters = [] 
        self._comments_dicts = []
        if 'comments' in post_dict:
            self._comments = [x['message'] for x in post_dict['comments']['data']]
            for h in post_dict['comments']['data']:
                self._commenters.append(anonymize(h['from']['id']))
                self._comments_dicts.append(h)
        else:
            self._comments = []
        if 'likes' in post_dict:
            self._likes = [anonymize(x['id']) for x in post_dict['likes']['data']]
        else:
            self._likes = []
        self._time_posted = post_dict['created_time']
        self._poster = anonymize(post_dict['from']['id']) # id? or name too? id, and can easily cipher them
        if "type" in post_dict:
            self._type = post_dict["type"]
        else:
            self._type = "post" # the generic. otherwise -- link, or photo
        if "description" in post_dict:
            self._type = "link"
            self._url = post_dict["link"]
        else:
            self._url = "" # None or empty string? probably empty string is safer
        if "link" in post_dict:
            self._link = post_dict["link"]
        elif get_links_from_message(self._message) != "None":
            self._link = get_links_from_message(self._message)
        else:
            self._link = "None" # string -- this is terrible but maybe safer for now TODO
        if "picture" in post_dict:
            self._imagecontent = post_dict["picture"]
        else:
            self._imagecontent = "None"
        if "object_id" in post_dict:
            self._addl_content = str(post_dict["object_id"]) #str check
        else:
            self._addl_content = "None"
        if "application" in post_dict:
            self._appl = post_dict["application"]["name"]
        else:
            self._appl = "Web"
        # if get_links_from_message(self._message) != "None": #and self._link == "None":
        #   self._link = get_links_from_message(self._message)

    def get_num_comments(self):
        return len(self._comments)
    def get_num_likes(self):
        return len(self._likes)

    def __repr__(self):
        return (self._id, self._message,len(self._comments),len(self._likes),self._time_posted,self._poster, self._type, self._link, self._imagecontent, self._addl_content, self._appl)

# Personal status update object
class PersonalUpdate(object):
    def __init__(self, update_dict, user_id):
        if update_dict["from"]["id"] == user_id: # if it's a personal update, get other info, otherwise pass
            self._id = anonymize(update_dict["id"][-15:]) # check - know that post ids are 17 characters long
            self._person = user_id # identify update by id, this reps one row
            self._date_posted = update_dict['created_time'][:10]
            self._time_posted = update_dict['created_time'][10:]
            if "type" in update_dict:
                self._type = update_dict["type"]
            else:
                self._type = "status"
            if 'message' in update_dict:
                self._message = update_dict['message']
            else:
                self._message = ""
            if 'comments' in update_dict:
                self._num_comments = len([x['message'] for x in update_dict['comments']['data']])
            else:
                self._num_comments = 0 
            if 'likes' in update_dict:
                self._num_likes = len([anonymize(x['id']) for x in update_dict['likes']['data']])
            else:
                self._num_likes = 0
            if "picture" in update_dict:
                self._imagecontent = update_dict["picture"]
            else:
                self._imagecontent = "None"
            if "object_id" in update_dict:
                self._addl_content = str(update_dict["object_id"]) #str check
            else:
                self._addl_content = "None"
            if "application" in update_dict:
                self._appl = update_dict["application"]["name"]
            else:
                self._appl = "Web" 

    def __repr__(self):
        return (self._id,self._person,self._date_posted, self._time_posted, self._message,self._num_comments,self._num_likes,self._type,self._imagecontent,self._addl_content,self._appl)

# Particip object (member of group totals/info)
class Particip(object):
    def __init__(self, user_id):
        self._id = user_id
        self._num_posts = 0
        self._num_likes = 0
        self._num_comments = 0
        self._group_admin = False
        # there is now extra info encoded here because database doesn't repeat; leaving for the moment

    def add_num_posts(self): # number of posts posted in group
        self._num_posts += 1
    def add_num_likes(self): # number of likes GIVEN, not received (in group) - this remains
        self._num_likes += 1
    def add_num_comments(self): # number of comments COMMENTED, not received (in group)
        self._num_comments += 1

    def change_admin_status(self):
        if self._group_admin:
            self._group_admin = False
        else:
            self._group_admin = True

    def __repr__(self):
        return tuple([self._id, self._num_posts, self._num_comments, self._num_likes])

# object for comment in group
class Comment(object): # group comment
    """Object representing comment to post in group"""
    def __init__(self,comment_dict):
        self._id = anonymize(comment_dict['id'])
        self._commenter = anonymize(comment_dict['from']['id'])
        if "message" in comment_dict:
            self._text = comment_dict["message"]
        else:
            self._text = ""
        if "like_count" in comment_dict:
            self._num_likes =  comment_dict["like_count"]
        else:
            self._num_likes = 0
        self._time_posted = comment_dict["created_time"]

    def __repr__(self):
        return tuple([self._id,self._commenter,self._text,self._num_likes,str(self._time_posted)[:10]]) # not getting time of day yet TODO


# get user information
# functions for handling user info
def get_user_stuff(graph,user_id): # not using object because it's so few things
    info_list = []
    try:
        user_dict = graph.get_object("me")#.format(user_id))
        # now grab and save information about user
        name = user_dict["name"]
        if "hometown" in user_dict:
            hometown = user_dict["hometown"]["name"]
        else:
            hometown = ""
        if "gender" in user_dict:
            gender = user_dict["gender"]
        else:
            gender = ""
        # anything else?
        info_list.append(name)
        info_list.append(hometown)
        info_list.append(gender)

    except IntegrityError: # how to identify which caused the error and update everything else
        # maybe can update / re-save everything except the primary key?? maybe this isn't a problem?
        pass
    return tuple(info_list) # returns the tuple of the list for each user
    # other structure will ADD to user per user and check to see if authorized,
    # if not authorized, create user obj and add group information relevant


def get_user_updates(feed,user_id):
    try:
        user_feed = feed#"ab"#graph.get_object("{}/statuses?limit=1000".format(user_id)) # need to limit by date
        # iterate through feed and add to UPDATES table, need to do error handling
        for d in user_feed['data']:
            upd = PersonalUpdate(d,user_id)
            tup = upd.__repr__() # returns the tuple of info, add this list to db
            Update.objects.get_or_create(post_id=tup[0],person_id=tup[1],date_posted=tup[2],link=get_links_from_message(tup[4]),content=tup[4],time_posted=tup[3],num_comments_recd=tup[5],num_likes_recd=tup[6],content_type=tup[7],imagecontent=tup[8],addl_content=tup[9],application=tup[10])
            
    except IntegrityError:
        pass # should deal with updates
        print "passed one"

# function for handling user feeds
def from_users(user_id, me_feed, arl): # user id is -- for EACH user, user id .. in overall fxn
    p = Participant.objects.get(ident=user_id)
    # make call to api for user information here
    # have access to ofc api, from which got me_feed dictionary
    p.name = me_feed["name"]
    if "gender" in me_feed:
        p.gender = me_feed["gender"]
    if arl is not None:
        p.age_min = arl[0]["age_range"]["min"]
        p.hometown = str(arl[0]["hometown_location"])
    p.save()

    # so this function can be run for each authenticated user
    # remember the members thing is currently different ... 
    # but expect those to already exist, just include as check adding- a new possibility in case


#######

# functions to handle participants and posts from group
def use_feed(feed,members,users,posts,comments):
    # make sure getting ALL users by iterating over group members !!
    # also, pip install facebook-sdk in new venv with internet
    #usrs_lst = []
    users = users
    posts = posts
    comments = comments
    members = members # for data feed
    for p in feed['data']:
        pst = Post(p)
        posts.append(pst)
    for u in members['data']:
        if anonymize(u['id']) not in users:
            anonid = anonymize(u['id'])
            #print anonid
            users[anonid] = Particip(anonid)
            if u['administrator'] == True: # right way to encode fb bools?
                users[anonid].change_admin_status() # to true from default false

    for y in posts:
        # users[y._poster].add_num_posts() # repetitive
        # for c in y._commenters:
        #     users[c].add_num_comments()
        for lk in y._likes:
            users[lk].add_num_likes() 
        for cm in y._comments_dicts:
            #print cm
            cmt = Comment(cm)
            comments.append(cmt)

def main_jobs(feed, members):
    #while "paging" in feed:
    users = {}
    posts = []
    comments = []
    use_feed(feed, members, users, posts, comments)
        #feed = json.loads(requests.get(feed["paging"]["next"]).text) # that needs to be..appended to a url, right?
        #self.stdout.write(feed)
    # create list of users
    usrs_list = [users[k] for k in users.keys()]
    # create lists of tuples for database entry
    psts_in_db = [p.__repr__() for p in posts]
    usrs_in_db = [u.__repr__() for u in usrs_list]
    cmts_in_db = [c.__repr__() for c in comments]
    # and by in_db here we really mean for_db

    # may need to rework these
    for pt in psts_in_db:
        try:
            #GroupPost.objects.get_or_create(ident=pt[0],message=pt[1],num_comments=pt[2],num_likes=pt[3],date_posted=str(pt[4])[:10],poster=pt[5],type_post=pt[6],link=pt[7],imagecontent=pt[8],addl_content=pt[9],application=pt[10], num_shares=pt[11])
            # this needs to be rewritten:
            #GroupPost.objects.get_or_create()
            pass
        except IntegrityError:
            g = GroupPost.objects.get(ident=pt[0])
            g.num_comments,g.num_likes,g.num_shares = pt[2],pt[3],pt[11]
            g.save()
    for us in usrs_in_db: # should already exist and should add stuff is the idea
        pr = Participant.objects.filter(ident=us[0]) # participant with correct id
        if len(pr) == 0: 
            pass # handle case where it doesn't exist yet -- insert public profile info
        else:
            pt = pr[0]
            pt.num_likes=us[3]
            pt.save()
    for ct in cmts_in_db:
        GroupComment.objects.get_or_create(ident=ct[0],poster=ct[1],num_likes_recd=ct[3],content=ct[2],date_posted=ct[4]) # should handle time posted also


def run():
    # handle the individual things
    authed_users = Participant.objects.all() # what is up with the participant model
    for au in authed_users:
        # get or create with error handling for update rows
        # save 
        uid = au.ident 
        token = au.token
        facebook = ofc(token)
        fb = facebook.get('me')
        fc = facebook.fql('SELECT age_range, hometown_location FROM user WHERE uid = me()') # may need to update -- currently 'me' is the curr user id/token 
        from_users(uid,fb,fc)
        # now add all appropriate updates for user
        feed = facebook.get('me/feed')
        get_user_updates(feed,uid)

    # handle the group information
    # get group feed:
    grp_feed = facebook.get('{}/feed'.format(GROUP_ID))
    members = facebook.get('{}/members'.format(GROUP_ID)) # this should be the list of group members, how to get that
    main_jobs(grp_feed,members)

    #print members
    #print grp_feed

        
 




