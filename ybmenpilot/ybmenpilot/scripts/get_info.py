# import statements
from ybmenpilot.models import Participant, GroupPost, GroupComment, Update
import facebook, re, hashlib



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
        self._id = anonymize(post_dict["id"][-15:]) # know that post ids are 17 characters long
        if 'message' in post_dict:
            self._message = post_dict['message']
        else:
            self._message = ""
        self._commenters = [] 
        if 'comments' in post_dict:
            self._comments = [x['message'] for x in post_dict['comments']['data']]
            for h in post_dict['comments']['data']:
                self._commenters.append(anonymize(h['from']['id'])) # TODO anonymize
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
        return tuple([self._id, self._message,len(self._comments),len(self._likes),self._time_posted,self._poster, self._type, self._link, self._imagecontent, self._addl_content, self._appl])

# Personal status update object
class PersonalUpdate(object):
    def __init__(self, update_dict, user_id):
        if update_dict["from"]["id"] == user_id: # if it's a personal update, get other info, otherwise pass
            self._id = anonymize(post_dict["id"][-15:]) # check - know that post ids are 17 characters long
            self._person = user_id # identify update by id, this reps one row
            if 'message' in post_dict:
                self._message = post_dict['message']
            else:
                self._message = ""
            if 'comments' in post_dict:
                self._num_comments = len([x['message'] for x in update_dict['comments']['data']])
            else:
                self._num_comments = 0 
            if 'likes' in post_dict:
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
        return tuple(self._id,self._person,self._message,self._num_comments,self._num_likes,self._imagecontent,self._addl_content,self._appl)

# Participant object (member of group totals/info)
class Participant(object):
    def __init__(self, user_id):
        self._id = user_id
        self._num_posts = 0
        self._num_likes = 0
        self._num_comments = 0
        self._mean_post_len = 0

    def add_num_posts(self): # number of posts posted in group
        self._num_posts += 1
    def add_num_likes(self): # number of likes GIVEN, not received (in group)
        self._num_likes += 1
    def add_num_comments(self): # number of comments COMMENTED, not received (in group)
        self._num_comments += 1

    def get_mean_postlen(self, post_insts):
        post_lengths = []
        for x in post_insts:
            if x._poster == self._id:
                post_lengths.append(len(x._message))
        # for m in [y for y in x._comments for x in post_insts]: # does that double listcomp work
        #   if m['from']['id'] == self._id:
        #       post_lengths.append(len(m['message']))
        self._mean_post_len = np.mean(post_lengths)
        #return self._mean_post_len

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
        user_dict = graph.get_object("{}".format(user_id))
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



# to see for db insert/update
# tuple(self._id,self._person,self._message,self._num_comments,self._num_likes,self._imagecontent,self._addl_content,self._appl)


def get_user_updates(graph,user_id):
    try:
        user_feed = graph.get_object("{}/feed?limit=600".format(user_id)) # need to limit by date
        # iterate through feed and add to UPDATES table, need to do error handling
        for d in user_feed['data']:
            upd = PersonalUpdate(d,user_id)
            tup = upd.__repr__() # returns the tuple of info, add this list to db
            Update.objects.get_or_create(post_id=)
    except IntegrityError:
        pass # should deal with updates


# function for handling user feeds
def from_users(graph,user_id): # user id is -- for EACH user, user id .. in overall fxn
    p = Participant.objects.get(ident=user_id)
    tkn = p.token # this has to exist at this point, so should error handle
    # make call to api for user information here
    graph = facebook.GraphAPI(tkn)
    get_user_stuff(graph)
    get_user_updates(graph) # examine what these return and deal with them appropriately
    # so this function can be run for each authenticated user
    # remember the members thing is currently different ... but expect those to already exist, just include as check adding-new possibility





def run():
    # handle the individual things
    authed_users = Participant.objects.all()
    for au in authed_users:
        # get or create with error handling for update rows
        # save 


    # handle all the group stuff

    pass




    #ps = Participant.objects.all()

    # for each authenticated user, try to get user info - from user gets it all for a given one


    # for each post and comment, create object

    # in each case, save to database as appropriate