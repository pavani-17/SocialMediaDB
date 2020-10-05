import subprocess as sp
import pymysql
import pymysql.cursors
from tabulate import tabulate
from time import time
from datetime import datetime
import time
import datetime


def checkIsMemberOfGroup(user_id, group_id):
    global cur

    try:
        query = "SELECT * FROM BELONGS_TO WHERE user_id=%d AND group_id=%d;" %(int(user_id), int(group_id))
        # print(query)
        try:
            cur.execute(query)
            con.commit()
            # print(cur.fetchall())
            if cur.rowcount == 0:
                # print("oops")
                return False
            return True
        except Exception as e:
            con.rollback()
            return False
    except Exception as enx:
        # print("hi")
        return False

def checkCommentIntegrity(comment_id, user_id):
    global cur

    try:
        query = "SELECT * FROM COMMENTS WHERE user_id=%d AND comment_id=%d;" %(int(user_id), int(comment_id))
        # print(query)
        try:
            cur.execute(query)
            con.commit()
            # print(cur.fetchall())
            if cur.rowcount == 0:
                # print("oops")
                return False
            return True
        except Exception as e:
            con.rollback()
            return False
    except Exception as enx:
        # print("hi")
        return False


def getCurrentTimeStamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def isNonEmptyQuery(query):
    global cur
    try:
        cur.execute(query)
        con.commit()
        if cur.rowcount == 0:
            return False
        return True
    except Exception as e:
        con.rollback()
        return False
    

def viewTable(rows):

    a = []
    try:
        a.append(list(rows[0].keys()))
    except:
        print("\n-----------------\nEMPTY TABLE\n-----------------\n")   
        return
    for row in rows:
        b = []
        for k in row.keys():
            b.append(row[k])
        a.append(b)
    print(tabulate(a, tablefmt="psql", headers="firstrow"))
    print()
    return


def viewOptions():
    global cur

    print("\nChoose the data that you want to see.\n\n")
    print("1.  USERS")
    print("2.  POST")
    print("3.  STORIES")
    print("4.  MESSAGES")
    print("5.  PROFILES")
    print("6.  EDUCATION OF USERS")
    #Pages
    print("7.  PAGES")
    print("8.  PAGES OF BUSINESS_PLACE")
    print("9. PRODUCTS OF BRANDS AND DETAILS")
    print("10. PAGES OF COMPANIES")
    print("11. BRANCHES OF COMPANIES")
    print("12. PAGES OF BRAND PRODUCTS")
    print("13. PAGES OF PUBLIC FIGURES")
    print("14. NEWS ABOUT PUBLIC FIGURES")
    print("15. PAGES OF ENTERTAINMENT INDUSTRY ENTITIES")
    print("16. PAGES OF CAUSE COMMUNITIES")
    #Groups
    print("17. GROUPS")
    #RelatioNships
    print("18. COMMENTS RELATIONSHIPS")
    print("19. FOLLOWS RELATIONSHIPS")
    print("20. GENERAL REACTS TO POSTS")
    print("21. LIKES TO PAGES")
    print("22. BELONGS TO GROUP RELATIONSHIP WITH USERS")
    print("23. ADMINS OF GROUPS")
    print("24. MODERATORS OF GROUPS")
    print("25. REACTS TO COMMENTS")
    print("26. MENTIONS OF USERS IN COMMENTS")
    print("27. SPECIFIC MESSAGES BETWEEN USERS - META DETAILS")
    print("28. GENERAL MESSAGES TO GROUPS - META DETAILS")
    print("29. RESPONDS TO STORIES")
    print("30. SHARES A POST IN A GROUP") # Basically posts in a group - comment to avoid semantical confusion
    print("31. USERS TAGGED IN POSTS")
    print("\n")
    choice = input("Enter: ")

    if choice == '1':
        query = "SELECT * FROM USER;"
    elif choice == '2':
        query = "SELECT * FROM POST;"
    elif choice == '3':
        query = "SELECT * FROM STORIES;"
    elif choice == '4':
        query = "SELECT * FROM MESSAGE;"
    elif choice == '5':
        query = "SELECT * FROM PROFILE;"
    elif choice == '6':
        query = "SELECT * FROM EDUCATION;"
    # Pages and subclasses
    elif choice == '7':
        query = "SELECT * FROM PAGE;"
    elif choice == '8':
        query = "SELECT * FROM BUSINESS_PLACE;"
    elif choice == '9':
        query = "SELECT * FROM PROD_BP;"
    elif choice == '10':
        query = "SELECT * FROM COMPANY;"
    elif choice == '11':
        query = "SELECT * FROM BRANCH_COMPANY;"
    elif choice == '12':
        query = "SELECT * FROM BRAND_PRODUCT;"
    elif choice == '13':
        query = "SELECT * FROM PUBLIC_FIGURE;"
    elif choice == '14':
        query = "SELECT * FROM NEWS_PUB_FIG;"
    elif choice == '15':
        query = "SELECT * FROM ENTERTAINMENT"
    elif choice == '16':    
        query = "SELECT * FROM CAUSE_COMMUNITY"
    # Pages over
    elif choice == '17':
        query = "SELECT * FROM social_media.GROUP"
    # Relationships
    elif choice == '18':
        query = "SELECT * FROM COMMENTS;"
    elif choice == '19':
        query = "SELECT * FROM FOLLOWS;"
    elif choice == '20':
        query = "SELECT * FROM MAKES_GENERAL_REACT;"
    elif choice == '21':
        query = "SELECT * FROM LIKES"
    elif choice == '22':
        query = "SELECT * FROM BELONGS_TO"
    elif choice == '23':
        query = "SELECT * FROM IS_ADMIN"
    elif choice == '24':
        query = "SELECT * FROM IS_MODERATOR"
    elif choice == '25':
        query = "SELECT * FROM MAKES_A_REACT;"
    elif choice == '26':
        query = "SELECT * FROM MENTIONS;"
    elif choice == '27':
        query = "SELECT * FROM SENDS_SPECIFIC;"
    elif choice == '28':
        query = "SELECT * FROM SENDS_GENERAL"
    elif choice == '29':
        query = "SELECT * FROM RESPONDS"
    elif choice == '30':
        query = "SELECT * FROM SHARES"
    elif choice == '31':
        query = "SELECT * FROM IS_TAGGED;"
    else:
        print("You have entered an invalid option.")

    try:
        no_of_rows = cur.execute(query)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    
    rows = cur.fetchall()
    viewTable(rows)
    con.commit()



def addUser():
    global cur
    user = {}
    print("Enter the details of the user below.\n")

    user["name"] = input("Please provide name of the user: ")
    user["email"] = input("Please provide the email id of the user: ")
    user["password"] = input("Please provide the password: ")
    user["address"] = input("Please provide the address: ")
    user["phone"] = input("Please enter the phone number [without space or hyphen]: ")

    try:
        query = "INSERT INTO USER VALUES(NULL, '%s','%s','%s','%s',%s, '00:00:00');" %(user["password"],user["name"],user["email"],user["address"],user["phone"])   
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")
   

def addProfile():
    print("Enter the profile details of the user below.\n")
    profile = {}
    # try:
    #     query = "SELECT user_id FROM USER WHERE password='%s' AND name='%s' AND email='%s'" %(user['password'],user['name'],user['email'])
    #     cur.execute(query)
    #     profile["user_id"] = cur.fetchone()[0]
    # except Exception as e:
    #     cur.rollback()
    #     print(e)
    #     print("Something went wrong")
    profile['user_id'] = input("Enter user id of the user: ")
    profile['dob'] = input("Enter Date-of-Birth in YYYY-MM-DD format: ")
    profile['sex'] = input("Enter sex of the use [Male, Female, Others, PreferNotToSay]: ")

    try:
        query = "INSERT INTO PROFILE VALUES (%s,'%s','%s');" %(profile["user_id"],profile["dob"],profile["sex"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addPost():
    global cur
    post = {}

    post['user_id'] = input("Enter the user ID: ")
    post['time'] = getCurrentTimeStamp()
    post['text'] = input("Enter the post text: ")
    post['media'] = input("Enter the link to the associated with the post: ")
    
    try:
        query = "INSERT INTO POST VALUES (NULL, '%s', '%s', '%s', %s);" %(post["time"], post["text"], post["media"], post["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addComment():
    global cur
    row = {}
    row["time"] = getCurrentTimeStamp()
    row["text"] = input("Enter the comment: ")
    row["media"] = input("Enter the link to the media: ")

    # Reminder: Do the following check in all valid places.
    if len(row["text"]) == 0 and len (row["media"]) == 0:
        print("You can't make an empty comment!")
        return

    try:
        query = "INSERT INTO COMMENT VALUES(NULL, '%s', '%s', '%s');" %(row["time"], row["text"], row["media"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addStory():
    global cur
    row = {}
    row["time"] = getCurrentTimeStamp()
    row["text"] = input("Enter what's shared in the story: ")
    row["media"] = input("Enter the link to media shared in the story: ")
    row["user_id"] = input("Enter the ID of the user who made this story: ")

    if len(row["text"]) == 0 and len (row["media"]) == 0:
        print("You can't make an empty story with no text and no media!")
        return

    try:
        query = "INSERT INTO STORIES VALUES(NULL, '%s', '%s', '%s', %s);" % (row["time"], row["text"], row["media"], row["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addMessage():
    global cur
    row = {}
    row["text"] = input("Enter the message: ")

    try:
        query = 'INSERT INTO MESSAGE VALUES(NULL, "%s");' % (row["text"]);
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addEducation():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user: ")
    row["education"] = input("Enter an educational qualification of the user: ")

    try:
        query = "INSERT INTO EDUCATION VALUES(%s, '%s');" % (row["user_id"], row["education"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")
    
def addGroup():
    global cur
    row = {}
    row["group_name"] = input("Enter the name of the new group: ")
    row["group_privacy"] = input("Enter the privacy setting of the new group [Public, Private, Secret]: ")

    try:
        query = "INSERT INTO social_media.GROUP VALUES(NULL, '%s', '%s'); " % (row["group_name"], row["group_privacy"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addPage():
    global cur
    row = {}
    row["page_name"] = input("Enter the name of the page: ")
    row["owner_id"] = input("Enter the user ID of the owner: ")

    try:
        query = "INSERT INTO PAGE VALUES(NULL, '%s', '%s'); " % (row["page_name"], row["owner_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addBusinessPlace():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["owner_name"] = input("Enter the name of the stake holder of this business: ")
    row["location"] = input("Enter the location: ")

    try:
        query = "INSERT INTO BUSINESS_PLACE VALUES(%s, '%s', '%s');" % (row["page_id"], row["owner_name"], row["location"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addProductInBusinessPlace():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["name"] = input("Enter the name of the product: ")
    row["price"] = input("Enter the name price of the product: ")

    try:
        query = "INSERT INTO PROD_BP VALUES('%s', '%s', %s);" % (row["page_id"], row["name"], row["price"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addBrandProduct():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["website"] = input("Enter website address: ")
    row["cust_service"] = input("Enter the customer care number: ")

    try:
        query = "INSERT INTO BRAND_PRODUCT VALUES(%s, '%s', %s);" %(row["page_id"], row["website"], row["cust_service"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addCompany():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["work_domain"] = input("Enter the work domain: ")

    try:
        query = "INSERT INTO COMPANY VALUES(%s, '%s');"% (row["page_id"], row["work_domain"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addBranchCompany():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["branch"] = input("Enter the branch of a company: ")

    try:
        query = "INSERT INTO BRANCH_COMPANY VALUES(%s, '%s');" % (row["page_id"], row["branch"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addPublicFigure():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["name"] = input("Enter the name of the public figure: ")
    row["field"] = input("Enter the field: ")

    try:
        query = "INSERT INTO PUBLIC_FIGURE VALUES(%s, '%s', '%s');" % (row["page_id"], row["name"], row["field"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addNewsOfPublicFigure():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["news"] = input("Enter the news: ")
    row["published_time"] = getCurrentTimeStamp()

    try:
        query = "INSERT INTO NEWS_PUB_FIG VALUES(%s, '%s', '%s'); " % (row["page_id"], row["news"], row["published_time"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addEntertainment():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["events"] = input("Enter the next event: ")
    row["audience"] = input("Enter the intended audience: ")

    try:
        query = "INSERt INTO ENTERTAINMENT VALUES(%s, '%s', '%s'); " % (row["page_id"], row["events"], row["audience"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addCauseCommunity():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["goal"] = input("Enter the goal of this community: ")
    row["activities"] = input("Enter the activities by this community: ")

    try:
        query = "INSERT INTO CAUSE_COMMUNITY VALUES(%s, '%s', '%s');" % (row["page_id"], row["goal"], row["activities"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

# def isValidUserID(user_id):
#     cur.execute("SELECT user_id from USER where user_id=%s;" % (user_id))
#     con.commit()
#     if cur.rowcount == 0:
#         return False
#     return True

def addFollows():
    global cur

    row = {}
    row["follower_id"] = input("Enter user ID of the person that wants to follow someone: ")
    # if isValidUserID(row["follower_id"]) == False:
    #     print("Invalid user_id")
    #     return
    row["following_id"] = input("Enter the user ID of the person that will be followed by the former person: ")
    # if isValidUserID(row["follower_id"]) == False:
    #     print("Invalid user_id")
    #     return
    try:
        query = "INSERT INTO FOLLOWS(follower_id, following_id) VALUES(%s, %s);" % (row["follower_id"], row["following_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addMakesGeneralReact():
    global cur
    row = {}

    # try:
    row["post_id"] = input("Enter the POST ID: ")
    # except Exception as e:
    #     print("Invalid POST ID")
    # try:
    row["user_id"] = input("Enter your USER ID: ")
    # except Exception as e:
    #     print("Invalid USER ID")

    print("Choose the react type by pressing the corresponding number")
    print("1 . Like")
    print("2 . Dislike")
    print("3 . Wow")
    print("4 . Heart")
    print("5 . Angry")
    print("6 . Haha")
    reactNum = 123
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")

    if reactNum == 1:
        row["reactedType"]="Like"
    elif reactNum == 2:
        row["reactedType"]="Dislike"
    elif reactNum == 3:
        row["reactedType"]="Wow"
    elif reactNum == 4:
        row["reactedType"]="Heart"
    elif reactNum == 5:
        row["reactedType"]="Angry"
    elif reactNum == 6:
        row["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return
    try:
        query = "INSERT INTO MAKES_GENERAL_REACT(post_id, user_id, reacted_type) VALUES(%s, %s, '%s');" % (
            row["post_id"], row["user_id"],row["reactedType"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addLikes():
    global cur
    row = {}
    # try:
    row["user_id"] = input("Enter the user ID: ")
    row["page_id"] = input("Enter the page ID of the page to like: ")
    # except Exception as e:
    #     print("Invalid USER ID")
    try:
        query = "INSERT INTO LIKES(page_id, user_id) VALUES(%s, %s);" % (
            row["page_id"], row["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addUserToGroup():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user who wants to join a group: ")
    row["group_id"] = input("Enter the ID of the group that the user wants to join: ")
    try:
        query = "INSERT INTO BELONGS_TO VALUES(%s, %s);" % (row["user_id"], row["group_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def makeUserAdmin():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user to make him an admin of a group: ")
    row["group_id"] = input("Enter the ID of the group for which user should be made an admin of: ")
    # Don't we have to check if the user is a member of the group?
    query = "SELECT * FROM BELONGS_TO where group_id=%s and user_id=%s;" % (row["group_id"], row["user_id"])
    if isNonEmptyQuery(query) == False:
        print("User doesn't belong to the group or invalid query.")
        return
    try:
        query = "INSERT INTO IS_ADMIN VALUES(%s, %s);" % (row["user_id"], row["group_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def makeUserModerator():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user to make him an moderator of a group: ")
    row["group_id"] = input("Enter the ID of the group for which user should be made an moderator of: ")
    # Don't we have to check if the user is a member of the group?
    query = "SELECT * FROM BELONGS_TO where group_id=%s and user_id=%s;" % (row["group_id"], row["user_id"])
    if isNonEmptyQuery(query) == False:
        print("User doesn't belong to the group or invalid query.")
        return
    try:
        query = "INSERT INTO IS_MODERATOR VALUES(%s, %s);" % (row["user_id"], row["group_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def makeReactionToAComment():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user who made the reaction: ")
    row["comment_id"] = input("Enter the ID of the comment in which the reaction was made: ")
    print("Choose the react type by pressing the corresponding number")
    print("1 . Like")
    print("2 . Dislike")
    print("3 . Wow")
    print("4 . Heart")
    print("5 . Angry")
    print("6 . Haha")
    reactNum = 123
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")

    if reactNum == 1:
        row["reactedType"]="Like"
    elif reactNum == 2:
        row["reactedType"]="Dislike"
    elif reactNum == 3:
        row["reactedType"]="Wow"
    elif reactNum == 4:
        row["reactedType"]="Heart"
    elif reactNum == 5:
        row["reactedType"]="Angry"
    elif reactNum == 6:
        row["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return
    
    try:
        query = "INSERT INTO MAKES_A_REACT(comment_id, user_id, reacted_type) VALUES(%s, %s, '%s');" % (
            row["comment_id"], row["user_id"],row["reactedType"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def mentionInComment():
    global cur
    row = {}
    row["comment_id"] = input("Enter the ID of the comment: ")
    row["mentioner_id"] = input("Enter the ID of the user who mentioned someone: ")
    row["mentionee_id"] = input("Enter the ID of the user who got mentioned: ")
    if checkCommentIntegrity(row["comment_id"], row["mentioner_id"]) == False:
        print("Error: Comment was not created by the user who mentioned.")
        return

    try:
        query = "INSERT INTO MENTIONS VALUES(%s, %s, %s);" % (row["mentioner_id"], row["mentionee_id"], row["comment_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addCommmentsRelations():
    global cur
    row = {}
    row["comment_id"] = input("Enter the ID of the comment: ")
    row["user_id"] = input("Enter the ID of the user who made the comment: ")
    row["post_id"] = input("Enter the ID of the post in which the comment is made: ")

    try:
        query = "INSERT INTO COMMENTS VALUES(%s, %s, %s);" % (row["comment_id"], row["user_id"], row["post_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addSendsSpecific(message_id):
    global cur
    row = {}
    row["sender_id"] = input("Enter the ID of the sender: ")
    row["receiver_id"] = input("Enter the ID of the receiver: ")
    # row["message_id"] = input("Enter the ID of the message: ")

    try:
        query = "INSERT INTO SENDS_SPECIFIC VALUES(%s, %s, %d);" % (row["sender_id"], row["receiver_id"], message_id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addSendsGeneral(message_id):
    global cur
    row = {}
    row["sender_id"] = input("Enter the ID of the sender: ")
    row["group_id"] = input("Enter the ID of the group: ")
    # row["message_id"] = input("Enter the ID of the message: ")
    if checkIsMemberOfGroup(row["sender_id"], row["group_id"]) == False:
        print("Error: Sender is not a member of the group.")
        return

    try:
        query = "INSERT INTO SENDS_GENERAL VALUES(%s, %s, %d); " % (row["sender_id"], row["group_id"], message_id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addResponds():
    global cur
    row = {}
    row["reacter_id"] = input("Enter the ID of the user who reacts to the story: ")
    row["story_id"] = input("Enter the ID of the story: ")
    print("Choose the react type by entering the corresponding number")
    print("1. Like")
    print("2. Dislike")
    print("3. Wow")
    print("4. Heart")
    print("5. Angry")
    print("6. Haha")
    reactNum = 123 # A random invalid number
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")

    if reactNum == 1:
        row["reactedType"]="Like"
    elif reactNum == 2:
        row["reactedType"]="Dislike"
    elif reactNum == 3:
        row["reactedType"]="Wow"
    elif reactNum == 4:
        row["reactedType"]="Heart"
    elif reactNum == 5:
        row["reactedType"]="Angry"
    elif reactNum == 6:
        row["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return

    try:
        query = "INSERT INTO RESPONDS VALUES(%s, %s,'%s');" %(row["reacter_id"], row["story_id"], row["reactedType"]) 
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addShares():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of user: ")
    row["group_id"] = input("Enter the ID of the group: ")
    row["post_id"] = input("Enter the ID of the post to share: ")

    if checkIsMemberOfGroup(row["user_id"], row["group_id"]) == False:
        print("Error: Sender is not a member of the group.")
        return

    try:
        query = "INSERT INTO SHARES VALUES(%s, %s, %s);" %(row["user_id"], row["group_id"], row["post_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")

def addIsTagged():
    global cur
    row = {}
    row["post_id"] = input("Enter the ID of the post: ")
    row["user_id"] = input("Enter the ID of the user who is tagged in the post: ")

    try:
        query = "INSERT INTO IS_TAGGED VALUES(%s, %s); " %(row["user_id"], row["post_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def showUserCreationOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Create a new USER.")
        print("2. Create a profile for a user.")
        print("3. Add an educational qualification of the user.")
        print("42. Go back.")

        n = input("Enter: ")
        if n == '1':
            addUser()
        elif n == '2':
            addProfile()
        elif n == '3':
            addEducation()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")


def showPostRelatedOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Create a new post.")
        print("2. Create a new comment.")
        print("3. Add a comment to a post.")
        print("4. Tag someone in a post.")
        print("5. Mention someone in a comment.")
        print("6. React to a post.")
        print("7. React to a comment.")
        print("8. Share a post in a group.")
        print("42. Go back.")

        n = input("Enter: ")
        if n == '1':
            addPost()
        elif n == '2':
            addComment()
        elif n == '3':
            addCommmentsRelations()
        elif n == '4':
            addIsTagged()
        elif n == '5':
            mentionInComment()
        elif n == '6':
            addMakesGeneralReact()
        elif n == '7':
            makeReactionToAComment()
        elif n == '8':
            addShares()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")

def showGroupRelatedOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Create a new group.")
        print("2. Make a new admin in a group.")
        print("3. Make someone a new moderator in a group.")
        print("4. Add a user to a group.")
        print("5. Send a new general message in a group.")
        print("6. Share a post in a group.")
        print("42. Go back.")
        n = input("Enter: ")
        if n == '1':
            addGroup()
        elif n == '2':
            makeUserAdmin()
        elif n == '3':
            makeUserModerator()
        elif n == '4':
            addUserToGroup()
        elif n == '5':
            addMessage()
            # cur.execute("select message_id from MESSAGE order by message_id desc limit 1;")
            cur.execute("SELECT LAST_INSERT_ID();")
            con.commit()
            output = cur.fetchone()
            # print(output['LAST_INSERT_ID()'])
            addSendsGeneral(output['LAST_INSERT_ID()'])
        elif n == '6':
            addShares()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to continue.")
    
        

def showUserToUserOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Follow someone. ") 
        print("2. Send a message to a user. ")
        print("42. Go back.")
        n = input("Enter: ")
        if n == '1':
            addFollows()
        elif n == '2':
            addMessage()
            cur.execute("SELECT LAST_INSERT_ID();")
            con.commit()
            output = cur.fetchone()
            addSendsSpecific(output['LAST_INSERT_ID()'])
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")


def showStoryOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Create a new story. ") 
        print("2. Respond to a story. ")
        print("42. Go back.")
        n = input("Enter: ")
        if n == '1':
            addStory()
        elif n == '2':
            addResponds()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")


def showPageOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Like a page.") 
        print("2. Create a new page.")
        print("3. Make a page for brand product.")
        print("4. Make a page for business place.")
        print("5. Insert a product in a business place page.")
        print("6. Make a page for entertainment.") 
        print("7. Make a page for cause communities.")
        print("8. Make a page for public figures.")
        print("9. Insert a related news in a public figure's page.")
        print("10. Make a page for company.") 
        print("11. Insert a branch in a page for a company.")
        print("42. Go back.")
        n = input("Enter: ")
        if n == '1':
            addLikes()
        elif n == '2':
            addPage()
        elif n == '3':
            addBrandProduct()
        elif n == '4':
            addBusinessPlace()
        elif n == '5':
            addProductInBusinessPlace()
        elif n == '6':
            addEntertainment()
        elif n == '7':
            addCauseCommunity()
        elif n == '8':
            addPublicFigure()
        elif n == '9':
            addNewsOfPublicFigure()
        elif n == '10':
            addCompany()
        elif n == '11':
            addBranchCompany()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")


def insertionOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
        refreshDatabase()
        print("Choose an option from below: ")
        print("1. Insertions related to users and profile.")
        print("2. Insertions related to post.")
        print("3. Insertions related to Groups")
        print("4. Insertions related to action between users.")
        print("5. Insertions related to stories.")
        print("6. Insertions related to pages.")
        print("42. Go back.")

        n = input("Enter: ")

        if n == '1':
            showUserCreationOptions()
        elif n == '2':
            showPostRelatedOptions()
        elif n == '3':
            showGroupRelatedOptions()
        elif n == '4':
            showUserToUserOptions()
        elif n == '5':
            showStoryOptions()
        elif n == '6':
            showPageOptions()
        elif n == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue
        input("Press enter to Continue.")








def refreshDatabase():
    global cur

    # Deleting incorrectly entered data in insert function
    # Have to write this function.
    print("Hello: Refreshing database") #Test printline.

while(1):
    tmp = sp.call('clear', shell=True)
    # The two lines below should be uncommented 
    # username = input("Username: ")
    # password = input("Password: ")

    username = 'root'
    password = 'blahblah'

    try:
        con = pymysql.connect(host='127.0.0.1',
                              user=username,
                              password=password,
                              db='social_media',
                              cursorclass=pymysql.cursors.DictCursor,
                              port=5005)
    except Exception as excep:
        print(excep)
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
        continue

    # print("hi\n")
    # ts = time.time()
    # asdf = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # print("HI: %s\n" %(asdf))
    # input("hisd")
    # # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    con.escape_string("'")
    with con.cursor() as cur:
        exitflag = 0
        while(1):
            tmp = sp.call('clear', shell=True)
            refreshDatabase()
            print("CHOOSE AN OPTION\n")
            print("1.View Options")
            print("2.Insertion Options")
            print("3.Deletion Options")
            print("4.Modify Options")
            print("5.Quit")
            inp = input("\nENTER: ")
            if(inp == '1'):
                # addUser()
                # addProfile()
                # addPost()
                # addFollows()

                # addMakesGe    neralReact()
                # addComment()
                # addStory()
                addMessage()
                # addLikes()
                viewOptions()
            elif(inp == '2'):
                insertionOptions()
            elif(inp == '5'):
                exitflag = 1
                print("Exiting.")
                break
            
            input("Press enter to continue: ")

    if exitflag == 1:
        break
