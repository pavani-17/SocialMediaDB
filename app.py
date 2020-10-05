import subprocess as sp
import pymysql
import pymysql.cursors
from tabulate import tabulate
from time import time
from datetime import datetime
import time
import datetime

def search():
    search_key = input("Enter the keyword to be searched for: ")
    search_key = search_key+'+'
    print("Enter the domain you want to search in:")
    print("1. User")
    print("2. Post")
    print("3. Comment")
    print("4. Page")
    print("5. Group")
    try:
        search_param = int(input("Enter the number of the required domain: "))
    except Exception as e:
        print(e)
        print("Invalid domain type")
        return
    if search_param==1:
        search_type = "USER"
        search_field = "name"
    elif search_param==2:
        search_type = "POST"
        search_field = "text"
    elif search_param==3:
        search_type = "COMMENT"
        search_field = "text"
    elif search_param==4:
        search_type = "PAGE"
        search_field = "page_name"
    elif search_param==5:
        search_type = "social_media.GROUP"
        search_field = "group_name"
    
    try:
        query = "SELECT * FROM %s WHERE %s REGEXP '%s'" %(search_type,search_field,search_key)
        r = cur.execute(query)
        if r==0:
            print("No result found")
            return
        rows = cur.fetchall()
        viewTable(rows)
    except Exception as e:
        print(e)
        print("Could not perform search")

def generateReport():
    try:
        user_id = int(input("Enter the User ID of the user you want to generate the report for: "))
    except Exception as e:
        print(e)
        print("User ID must be a number")
        return
    try:
        
        query = "SELECT * FROM USER WHERE user_id=%d" %(user_id)
        r = cur.execute(query)
        if r==0:
            print("Could not find details of the given User ID")
            return
        print("The details of the user are as follows: ")
        rows = cur.fetchall()
        viewTable(rows)

        print("Select which report would you like to say: ")
        print("1. Followers")
        print("2. Following")
        print("3. Post")
        print("4. Comments")
        print("5. Post Reacts")
        print("6. Comment Reacts")
        print("7. Pages Created")
        print("8. Pages Liked")
        print("9. Group Admin")
        print("10. Group Moderator")
        print("11. Group Member")

        try:
            report_type = int(input("Enter the number of the report you would like to see: "))
        except Exception as e:
            print(e)
            print("Invalid Choice")
            return

        if report_type==1:
            query = "SELECT * FROM USER WHERE user_id IN (SELECT follower_id FROM FOLLOWS WHERE following_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("There are no followers for the user\n")
            else:
                print("The users following the user are as follows: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==2:
            query = "SELECT * FROM USER WHERE user_id IN (SELECT following_id FROM FOLLOWS WHERE follower_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user does not follow anyone \n")
            else:
                print("The users the given user is following are as follows: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==3:
            query = "SELECT * FROM POST WHERE user_id=%d" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not post any post\n")
            else:
                print("Posts posted by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==4: 
            query = "SELECT COMMENT.comment_id, COMMENT.text, COMMENT.media, COMMENTS.post_id FROM COMMENT INNER JOIN COMMENTS ON COMMENT.comment_id = COMMENTS.comment_id WHERE COMMENTS.user_id = %d" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not post any post\n")
            else:
                print("Comments posted by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==5:
            query = "SELECT POST.post_id, POST.text, POST.media, POST.user_id, MAKES_GENERAL_REACT.reacted_type FROM POST INNER JOIN MAKES_GENERAL_REACT ON POST.post_id = MAKES_GENERAL_REACT.post_id WHERE MAKES_GENERAL_REACT.user_id = %d" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not react on any post\n")
            else:
                print("Posts reacted on by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==6:   
            query = "SELECT COMMENT.comment_id, COMMENT.text, COMMENT.media, COMMENTS.post_id, MAKES_A_REACT.reacted_type FROM COMMENT INNER JOIN COMMENTS ON COMMENT.comment_id = COMMENTS.comment_id INNER JOIN MAKES_A_REACT ON MAKES_A_REACT.comment_id = COMMENT.comment_id WHERE MAKES_A_REACT.comment_id=%d" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not react on any comment\n")
            else:
                print("Comments reacted on by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==7:
            query = "SELECT * FROM PAGE WHERE owner_id = %d" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not create any page\n")
            else:
                print("Pages created by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==8:
            query = "SELECT * FROM PAGE WHERE page_id IN (SELECT page_id FROM LIKES WHERE user_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user did not like any page\n")
            else:
                print("Pages liked by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==9:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM IS_ADMIN WHERE user_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user is not the admin of any group\n")
            else:
                print("Groups the user is the admin of: ")
                rows = cur.fetchall()
                viewTable(rows)
        
        elif report_type==10:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM IS_MODERATOR WHERE user_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user is not the moderator of any group\n")
            else:
                print("Groups the user is the moderator of: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type==11:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM BELONGS_TO WHERE user_id=%d)" %(user_id)
            r = cur.execute(query)
            if r==0:
                print("The user is does not belong to any group\n")
            else:
                print("Groups the user is the belongs to: ")
                rows = cur.fetchall()
                viewTable(rows)

    except Exception as e:
        print(e)
        print("Could not generate report :(")

###############################################################################################
##############################################################################################
def mutual():
    try:

        print("1. Mutual Followings")
        print("2. Mutual Followers")
        print("3. Mutual Liked Pages")
        print("4. Mutual Membership in Groups")

        optn = int(input("Enter chosen option: "))

        user1ID = int(input("Enter UserID of first User: "))
        user2ID = int(input("Enter UserID of second User: "))

        if (optn == 1):
            query = '''
                    SELECT *
                    FROM USER
                    WHERE user_id IN
                                (SELECT following_id
                                FROM FOLLOWS
                                WHERE follower_id = '%s')

                                AND

                        user_id IN
                                (SELECT following_id
                                FROM FOLLOWS
                                WHERE follower_id = '%s')
                    ''' %(user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Followers:")
            if(r==0):
                print("NO MUTUAL FOLLOWERS")
            rows = cur.fetchall()
            viewTable(rows)

        elif (optn == 2):
            query = '''
                    SELECT *
                    FROM USER
                    WHERE user_id IN
                                (SELECT follower_id
                                FROM FOLLOWS
                                WHERE following_id = '%s')

                                AND
                        user_id IN
                                (SELECT follower_id
                                FROM FOLLOWS
                                WHERE following_id = '%s')
                    ''' %(user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Followings:")
            if(r==0):
                print("NO MUTUAL FOLLOWINGS")
            rows = cur.fetchall()
            viewTable(rows)

        elif (optn == 3):
            query = '''
                    SELECT *
                    FROM PAGE
                    WHERE page_id IN
                                (SELECT page_id
                                FROM LIKES
                                WHERE  user_id = '%s')

                                AND
                        page_id IN
                                (SELECT page_id
                                FROM LIKES
                                WHERE user_id = '%s')
                    ''' %(user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Likes to Pages:")
            if(r==0):
                print("NO MUTUAL LIKES")
            rows = cur.fetchall()
            viewTable(rows)

        elif(optn == 4):
            query = '''
                    SELECT *
                    FROM social_media.GROUP
                    WHERE group_id IN
                                (SELECT group_id
                                FROM BELONGS_TO
                                WHERE  user_id = '%s')

                                AND
                        group_id IN
                                (SELECT group_id
                                FROM BELONGS_TO
                                WHERE user_id = '%s')
                    ''' %(user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Likes to Pages:")
            if(r==0):
                print("NO MUTUAL LIKES")
            rows = cur.fetchall()
            viewTable(rows)

        else:
            print("Invalid Option")

    except Exception as e:
        print(e)
        print("ERROR")
        return


def eventTracker():
    try:
        uid = int(input("Enter the UserID for the User you want to check the events for: "))
        date = input("Enter the date for the event tracking in MM-DD format: ")
        querybirthday = '''
                        SELECT * FROM USER WHERE user_id IN
                        (SELECT user_id FROM PROFILE WHERE user_id IN
                            (SELECT following_id FROM FOLLOWS WHERE follower_id = '%d')
                        AND
                        (date_of_birth REGEXP '%s'));
                        '''%(uid, date+'+')

        queryposts = '''
                        SELECT * FROM POST WHERE time REGEXP '%s' AND user_id = '%s';
                     ''' %(date+'+',uid)


        r1 = cur.execute(querybirthday)
        print("Birthdays ->")
        if(r1==0):
            print("No Birthdays")
        else:
            rows = cur.fetchall()
            viewTable(rows)

        r1 = cur.execute(queryposts)
        print("Posts made on this day ->")
        if(r1==0):
            print("No Posts")
        else :
            rows = cur.fetchall()
            viewTable(rows)

    except Exception as e:
        print (e)
        print("ERROR")
        return


def listReacttoPost():
    try:
        post_id=int(input("Choose the PostID you want to see the reacts for: "))
        queryposts = '''
                        SELECT USER.user_id,USER.name,MAKES_GENERAL_REACT.reacted_type FROM (MAKES_GENERAL_REACT INNER JOIN USER ON MAKES_GENERAL_REACT.user_id = USER.user_id ) WHERE MAKES_GENERAL_REACT.post_id = '%d';
                     ''' %(post_id)

        r1 = cur.execute(queryposts)
        print("Reacts to the post ->")
        if(r1==0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")
        return
    return

def listReacttoComment():
    try:
        comment_id=int(input("Choose the CommentID you want to see the reacts for: "))
        query = '''
                        SELECT USER.user_id,USER.name,MAKES_A_REACT.reacted_type FROM (MAKES_A_REACT INNER JOIN USER ON MAKES_A_REACT.user_id = USER.user_id ) WHERE MAKES_A_REACT.comment_id = '%d';
                     ''' %(comment_id)

        r1 = cur.execute(query)
        print("Reacts to the Comment ->")
        if(r1==0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")
        return
    return

def listCommenttoPost():
    try:
        post_id=int(input("Choose the PostID you want to see the comments for: "))
        query = '''
                        SELECT USER.user_id,USER.name,COMMENTS.comment_id,COMMENT.text,COMMENT.time FROM COMMENTS INNER JOIN USER ON COMMENTS.user_id = USER.user_id INNER JOIN COMMENT ON COMMENTS.comment_id = COMMENT.comment_id  WHERE COMMENTS.post_id = '%d';
                     ''' %(post_id)

        r1 = cur.execute(query)
        print("Comments to the Post ->")
        if(r1==0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")
        return
    return

def postListing():
    try:
        print("Choose the option to see suggestions for: ")
        print("1. List all comments to a specific Post")
        print("2. List all Reacts to a specific Post")

        optn = int(input("Enter the choice: "))

        if(optn == 1):
            listCommenttoPost()
        elif(optn == 2):
            listReacttoPost()
        else :
            print("Invalid Option")
        return
    except Exception as e:
        print(e)
        print("ERROR")
        return

def commentListing():
    try:
        print("Choose the option to see suggestions for: ")
        print("1. List all Reacts to a specific Comment")

        optn = int(input("Enter the choice: "))

        if(optn == 1):
            listReacttoComment()
        else :
            print("Invalid Option")
        return
    except Exception as e:
        print(e)
        print("ERROR")
        return

def showSuggestions():
    print("Choose the option to see suggestions for: ")
    print("1. User")
    print("2. Page")
    print("3. Group")
    try:
        optn = int(input("Enter option : "))
        if (optn == 1):
            user_id=int(input("Enter the User ID you want to see the FOLLOWING suggestions for : "))
            query = '''
                        SELECT * FROM USER WHERE user_id IN (
                            SELECT following_id FROM FOLLOWS WHERE follower_id IN (
                            SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                            )
                            )
                            AND user_id NOT IN (
                                SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                            )
                            AND user_id <> '%d';

                        ''' %(user_id,user_id,user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1==0):
                print("No suggestion to show")
            else:
                rows = cur.fetchall()
                viewTable(rows)
            return
        elif (optn == 2):
            user_id=int(input("Enter the User ID you want to see the PAGES suggestions for : "))
            query = '''
                    SELECT * FROM PAGE WHERE page_id IN (
                        SELECT page_id FROM LIKES WHERE user_id IN (
                           SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                        )
                        )
                        AND page_id NOT IN (
                            SELECT page_id FROM LIKES WHERE user_id = '%d'
                        )
                     ''' %(user_id,user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1==0):
                print("No suggestion to show")
            else:
                rows = cur.fetchall()
                viewTable(rows)
            return
        elif (optn == 3):
            user_id=int(input("Enter the User ID you want to see the GROUPS suggestions for : "))
            query = '''
                        SELECT * FROM social_media.GROUP WHERE group_id IN (
                            SELECT group_id FROM BELONGS_TO WHERE user_id IN (
                            SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                            )
                            )
                            AND group_id NOT IN (
                                SELECT group_id FROM BELONGS_TO WHERE user_id = '%d'
                            )
                    ''' %(user_id,user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1==0):
                print("No suggestion to show")
            else:
                rows = cur.fetchall()
                viewTable(rows)
            return
        else:
            print("Invalid Options")
        return
    except Exception as e:
        print(e)
        print("ERROR")
        return


###############################################################################################
##############################################################################################

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
    print("9.  PRODUCTS OF BRANDS AND DETAILS")
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
        query = "SELECT PAGE.page_id, PAGE.page_name, PAGE.owner_id, COUNT(LIKES.user_id) AS Number_of_Likes FROM PAGE LEFT OUTER JOIN LIKES ON PAGE.page_id = LIKES.page_id GROUP BY page_id"
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
        query = "SELECT social_media.GROUP.group_id, social_media.GROUP.group_name, social_media.GROUP.group_privacy, COUNT(BELONGS_TO.user_id) AS Number_of_Members FROM social_media.GROUP INNER JOIN BELONGS_TO ON social_media.GROUP.group_id = BELONGS_TO.group_id GROUP BY group_id"
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


###################################################################################################
###############################################  DELETE ##########################################

def viewTableDel(choice):
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
    elif choice == '18':
        query = "SELECT * FROM COMMENT;"
    # Pages and subclasses
    elif choice == '7':
        query = "SELECT * FROM PAGE;"
    elif choice == '17':
        query = "SELECT * FROM social_media.GROUP"
    # Relationships
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

    try:
        no_of_rows = cur.execute(query)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    rows = cur.fetchall()
    viewTable(rows)
    con.commit()
    return



def delOptions():
    while(1):
        print("Select from the options below :")
        print("1. Deactivate Account")
        print("2. Unfollow")
        print("3. Delete Post")
        print("4. Delete Comment")
        print("5. Delete Message")
        print("6. Delete Story")
        print("7. Remove react from a  Post")
        print("8. Remove react from a Comment")
        print("9. Remove response from a Story")
        print("10. Unlike a liked page")
        print("11. Exit group")
        print("12. Quit being Admin")
        print("13. Quit being Moderator")
        print("14. Remove Tag")
        print("15. Remove Mention")
        print("42. Go Back")

        optn = input("Your option is : ")

        try:
            optn = int(optn)
        except Exception as e:
            print(e)
            return

        if optn==1 :
            delUser()
        elif optn==2:
            unFollow()
        elif optn==3:
            delPost()
        elif optn==4:
            delComment()
        elif optn==5:
            delMessage()
        elif optn==6:
            delStory()
        elif optn==7:
            generalUnreact()
        elif optn==8:
            unReact()
        elif optn==9:
            unRespond()
        elif optn==10:
            unLike()
        elif optn==11:
            exitGroup()
        elif optn==12:
            unAdmin()
        elif optn==13:
            unModerator()
        elif optn==14:
            unTag()
        elif optn==15:
            unMention()
        elif optn==42:
            return
        else:
            print("Oops! Choose an option between 1 to 15")
        return

################# Entities ###################
def delUser():
    global cur
    viewTableDel('1')
    user_id = input("Enter the User ID of the User to be removed: ")
    try :
        user_id = int(user_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query1 = "DELETE FROM USER WHERE user_id='%d';" % (user_id)
    query2 = "DELETE FROM PROFILE WHERE user_id='%d';" % (user_id)
    try:
        cur.execute(query1)
        cur.execute(query2)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('1')
    return

def delComment():
    global cur
    viewTableDel('18')
    comment_id = input("Enter the Comment ID of the Comment to be removed: ")
    try :
        comment_id = int(comment_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM COMMENT WHERE comment_id='%d';" % (comment_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('18')
    return

def delPost():
    global cur
    viewTableDel('2')
    post_id = input("Enter the Post ID of the Post you to be removed: ")
    try :
        post_id = int(post_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM POST WHERE post_id='%d';" % (post_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('2')
    return

def delMessage():
    global cur
    viewTableDel('4')
    message_id = input("Enter the Message ID of the Message to be removed: ")
    try :
        message_id = int(message_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM MESSAGE WHERE message_id='%d';" % (message_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('4')
    return

def delStory():
    global cur
    viewTableDel('3')
    story_id = input("Enter the Story ID of the Story to be removed: ")
    try :
        story_id = int(story_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM STORIES WHERE story_id='%d';" % (story_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('3')
    return

def delPage():
    global cur
    viewTableDel('7')
    page_id = input("Enter the Page ID of the Page to be removed: ")
    try :
        page_id = int(page_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM PAGE WHERE page_id='%d';" % (page_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('7')
    return


############### Relationships #################

def unFollow():
    global cur
    viewTableDel('19')
    follower_id = input("Enter the Follower's User Id: ")
    following_id = input("Enter the User ID of the user to be unfollowed: ")
    try :
        follower_id = int(follower_id)
        following_id = int(following_id)
    except :
        print("Invalid Page ID")
        print("\n\nError!\n")
        return

    query = "DELETE FROM FOLLOWS WHERE follower_id='%d' AND following_id = %d;" % (follower_id,following_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('19')
    return

def generalUnreact():
    global cur
    viewTableDel('20')
    user_id = input("Enter the Reacting User Id: ")
    post_id = input("Enter the Post ID of the Post to be unreacted: ")
    try :
        user_id = int(user_id)
        post_id = int(post_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM MAKES_GENERAL_REACT WHERE user_id='%d' AND post_id = %d;" % (user_id,post_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('20')
    return

def unLike():
    global cur
    viewTableDel('21')
    user_id = input("Enter the User Id of the User who wants to unlike: ")
    page_id = input("Enter the Page ID of the Page to be unliked: ")
    try :
        user_id = int(user_id)
        page_id = int(page_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM FOLLOWS LIKES WHERE user_id='%d' AND page_id = %d;" % (user_id,page_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('21')
    return

def exitGroup():
    global cur
    viewTableDel('22')
    user_id = input("Enter the User ID of the User who wants to exit: ")
    group_id = input("Enter the Group ID of the Group: ")
    try :
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query1 = "DELETE FROM BELONGS_TO WHERE user_id='%d' AND group_id = %d;" % (user_id,group_id)
    query2 = "DELETE FROM IS_ADMIN WHERE user_id='%d' AND group_id = %d;" % (user_id,group_id)
    query3 = "DELETE FROM IS_MODERATOR WHERE user_id='%d' AND group_id = %d;" % (user_id,group_id)
    try:
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('22')
    return

def unAdmin():
    global cur
    viewTableDel('23')
    user_id = input("Enter the User ID of the User to be removed from Admin: ")
    group_id = input("Enter the Group ID of the Group: ")
    try :
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM IS_ADMIN WHERE (user_id='%d') AND (group_id = %d);" % (user_id,group_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('23')
    return


def unModerator():
    global cur
    viewTableDel('24')
    user_id = input("Enter the User ID of the User to be removed from moderator: ")
    group_id = input("Enter the Group ID of the Group: ")
    try :
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM IS_MODERATOR WHERE user_id='%d' AND group_id = %d;" % (user_id,group_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('24')
    return

def unReact():
    global cur
    viewTableDel('25')
    user_id = input("Enter the Reacting User Id: ")
    comment_id = input("Enter the Comment ID of the Comment to be unreacted: ")
    try :
        user_id = int(user_id)
        comment_id = int(comment_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM MAKES_A_REACT WHERE user_id='%d' AND comment_id = %d;" % (user_id,comment_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('25')
    return

def unMention():
    global cur
    viewTableDel('26')
    comment_id = input("Enter the Comment ID to be unmentioned from: ")
    mentionee_id = input("Enter the User ID to be unmentioned: ")
    try :
        comment_id = int(comment_id)
        mentionee_id = int(mentionee_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM MENTIONS WHERE comment_id='%d' AND mentionee_id = %d;" % (comment_id,mentionee_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('26')
    return


def unRespond():
    global cur
    viewTableDel('29')
    story_id = input("Enter the Story ID to unreact: ")
    reacter_id = input("Enter the User ID of the User unreacting: ")
    try :
        story_id = int(story_id)
        reacter_id = int(reacter_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM RESPONDS WHERE story_id='%d' AND reacter_id = %d;" % (story_id,reacter_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('29')
    return

def unTag():
    global cur
    viewTableDel('31')
    post_id = input("Enter the Post ID to be untagged from: ")
    user_id = input("Enter the User ID to be untagged: ")
    try :
        post_id = int(post_id)
        user_id = int(user_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM IS_TAGGED WHERE user_id='%d' AND post_id = %d;" % (user_id,post_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    viewTableDel('31')
    return

###############################################################################################
###############################################################################################
######################################### MODIFY ##############################################

def updatePost():
    viewTableDel('2')
    global cur
    post = {}
    try:
        post["post_id"] = int(input("Enter the post id to be updated:"))
    except Exception as e:
        print(e)
        print("Post ID must be an integer")
        return

    post["media"] = input("Enter the updated media: ")
    post["text"] = input("Enter the updated text: ")

    try:
        query = "UPDATE POST SET media='%s', text='%s' WHERE post_id='%d'" %(post["media"],post["text"],post["post_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('2')
    return

def updateComment():
    viewTableDel('18')
    global cur
    comment = {}
    try:
        comment["comment_id"] = int(input("Enter the comment id of the comment to be updated: "))
    except Exception as e:
        print(e)
        print("Comment ID must be an integer")
        return

    comment["text"] = input("Enter the updated text of the comment: ")

    try:
        query = "UPDATE COMMENT SET text='%s' WHERE comment_id='%d'" %(comment["text"],comment["comment_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('18')
    return

def updateStory():
    viewTableDel('3')
    global cur
    story = {}

    try:
        story["story_id"] = int(input("Enter the story id of the story to be updated: "))
    except Exception as e:
        print(e)
        print("Story ID must be an integer")
        return

    story["text"] = input("Enter the updated text of the story: ")
    story["media"] =input("Enter the updated media of the story: ")

    try:
        query = "UPDATE STORIES SET text='%s', media='%s' WHERE story_id = '%d'" %(story["text"], story["media"], story["story_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('3')
    return

def updatePage():
    viewTableDel('7')
    global cur
    page = {}

    try:
        page["page_id"] = int(input("Enter the page_id of the page to be updated: "))
    except Exception as e:
        print(e)
        print("Page ID must be an integer: ")
        return

    page["page_name"] = input("Enter the updated name of the page: ")

    try:
        query = "UPDATE PAGE SET page_name='%s' WHERE page_id='%s'" %(page["page_name"],page["page_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('7')
    return

def updateGeneralReact():
    viewTableDel('20')
    global cur
    react = {}

    try:
        react["post_id"] = int(input("Enter the post ID of the post you want to update the react on: "))
        react["user_id"] = int(input("Enter the user ID of the User whose react you want to change: "))
    except Exception as e:
        print(e)
        print("Wrong parameters. Try again")
        return

    print("Choose the react type by pressing the corresponding number")
    print("1 . Like")
    print("2 . Dislike")
    print("3 . Wow")
    print("4 . Heart")
    print("5 . Angry")
    print("6 . Haha")
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")
        return

    if reactNum == 1:
        react["reactedType"]="Like"
    elif reactNum == 2:
        react["reactedType"]="Dislike"
    elif reactNum == 3:
        react["reactedType"]="Wow"
    elif reactNum == 4:
        react["reactedType"]="Heart"
    elif reactNum == 5:
        react["reactedType"]="Angry"
    elif reactNum == 6:
        react["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return

    try:
        query = "UPDATE MAKES_GENERAL_REACT SET reacted_type='%s' WHERE post_id = '%d' AND user_id='%d'" %(react["reactedType"], react["post_id"], react["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('20')
    return

def updateMakesReact():
    viewTableDel('25')
    global cur
    react = {}

    try:
        react["comment_id"] = int(input("Enter the comment ID of the comment you want to update the react on: "))
        react["user_id"] = int(input("Enter the user ID of the user whose react on the comment you want to update: "))
    except Exception as e:
        print(e)
        print("Wrong parameters. Try again")
        return

    print("Choose the react type by pressing the corresponding number: ")
    print("1 . Like")
    print("2 . Dislike")
    print("3 . Wow")
    print("4 . Heart")
    print("5 . Angry")
    print("6 . Haha")
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")
        return

    if reactNum == 1:
        react["reactedType"]="Like"
    elif reactNum == 2:
        react["reactedType"]="Dislike"
    elif reactNum == 3:
        react["reactedType"]="Wow"
    elif reactNum == 4:
        react["reactedType"]="Heart"
    elif reactNum == 5:
        react["reactedType"]="Angry"
    elif reactNum == 6:
        react["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return

    try:
        query = "UPDATE MAKES_A_REACT SET reacted_type='%s' WHERE comment_id = '%d' AND user_id='%d'" %(react["reactedType"], react["comment_id"], react["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('25')
    return

def updateResponds():
    viewTableDel('29')
    global cur
    react = {}

    try:
        react["story_id"] = int(input("Enter the Story ID of the Story you want to update the react on: "))
        react["reacter_id"] = int(input("Enter the user ID of the User whose react on the story you want to update: "))
    except Exception as e:
        print(e)
        print("Wrong parameters. Try again")
        return

    print("Choose the react type by pressing the corresponding number: ")
    print("1 . Like")
    print("2 . Dislike")
    print("3 . Wow")
    print("4 . Heart")
    print("5 . Angry")
    print("6 . Haha")
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")
        return

    if reactNum == 1:
        react["reactedType"]="Like"
    elif reactNum == 2:
        react["reactedType"]="Dislike"
    elif reactNum == 3:
        react["reactedType"]="Wow"
    elif reactNum == 4:
        react["reactedType"]="Heart"
    elif reactNum == 5:
        react["reactedType"]="Angry"
    elif reactNum == 6:
        react["reactedType"]="Haha"
    else :
        print("Invalid react Type")
        return

    try:
        query = "UPDATE RESPONDS SET reacted_type='%s' WHERE story_id = '%d' AND reacter_id='%d'" %(react["reactedType"], react["story_id"], react["reacter_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('29')
    return

def updateGroup():
    viewTableDel('17')
    global cur
    group = {}

    try:
        group["group_id"] = int(input("Enter the group ID of the group you want to update: "))
    except Exception as e:
        print(e)
        print("Group ID must be an integer")
        return

    group["group_name"] = input("Enter the new name of the Group Name: ")
    print("Select the new privacy status of the group: ")
    print("1. Public")
    print("2. Private")
    print("3. Secret")

    try:
        groupNum = int(input())
    except Exception as e:
        print(e)
        print("Invalid Group Privacy Type")
        return

    if groupNum==1:
        group["group_privacy"] = "Public"
    elif groupNum==2:
        group["group_privacy"] = "Private"
    elif groupNum==3:
        group["group_privacy"] = "Secret"
    else:
        print("Invalid Group Privacy Type")
        return

    try:
        query = "UPDATE social_media.GROUP SET group_name='%s',group_privacy='%s' WHERE group_id='%d'" %(group["group_name"],group["group_privacy"],group["group_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    viewTableDel('17')
    return

def updateProfile():
    viewTableDel('5')
    global cur
    profile = {}

    try:
        profile["user_id"] = int(input("Enter the User ID of the profile u want to update: "))
    except Exception as e:
        print(e)
        print("User ID should be an integer ")
        return

    profile["dob"] = input("Enter the updated Date of Birth in YYYY-MM-DD format ")

    try:
        query = "UPDATE PROFILE SET date_of_birth='%s' WHERE user_id='%d'" %(profile["dob"],profile["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data")
        return

    viewTableDel('5')
    return

def updatePassword():
    global cur
    query = "SELECT user_id,name,email FROM USER"
    try:
        no_of_rows = cur.execute(query)

    except Exception as e:
        print(e)
        return
    rows = cur.fetchall()
    viewTable(rows)
    con.commit()

    user={}
    try:
        user['uid'] = int(input("Enter your user ID: "))
    except Exception as e:
        print(e)
        print("User ID must be an integer")
        return
    user['prev_password'] = input("Enter your previous password: ")
    try:
        query = "SELECT password FROM USER WHERE user_id = '%d'" %(user['uid'])
        cur.execute(query)
        prev_pass = cur.fetchone()
        prev_pass = str(prev_pass["password"])
    except Exception as e:
        print(e)
        return
    #print(prev_pass,user["prev_password"])
    if (prev_pass == user["prev_password"]):
        user["new_password"]= input("Enter your new password: ")
        try:
            query = "UPDATE USER SET password = '%s' WHERE user_id = '%d'" %(user["new_password"],user['uid'])
            cur.execute(query)
            con.commit()
            print("Password changed succesfully!")
        except Exception as e:
            print(e)
            return

    else:
        print("WRONG PASSWORD!!")
        return

    return


def updOptions():
    while(1):
        print("Select from the options below :")
        print("1. Edit Post")
        print("2. Edit Comment")
        print("3. Edit Story")
        print("4. Edit Page")
        print("5. Change the react to a Post")
        print("6. Change react to Comment")
        print("7. Change react to a Story")
        print("8. Edit Group Info")
        print("9. Edit Profile ")
        print("10. Update Password")
        print("42. Go Back")


        optn = input("Your option is : ")

        try:
            optn = int(optn)
        except Exception as e:
            print(e)
            return

        if optn==1 :
            updatePost()
        elif optn==2:
            updateComment()
        elif optn==3:
            updateStory()
        elif optn==4:
            updatePage()
        elif optn==5:
            updateGeneralReact()
        elif optn==6:
            updateMakesReact()
        elif optn==7:
            updateResponds()
        elif optn==8:
            updateGroup()
        elif optn==9:
            updateProfile()
        elif optn==10:
            updatePassword()
        elif optn==42:
            return
        else:
            print("Oops! Choose an option between 1 to 9")
        return

###############################################################################################

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
    password = 'pavani@17'

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
            print("1.General View Options")
            print("2.Insertion Options")
            print("3.Deletion Options")
            print("4.Modify Options")
            print("5.Search")
            print("6.User-specific View Options and Activity Report Generation")
            print("7.Show Suggestions")
            print("8.View Mutual Relationships")
            print("9.Post-specific View Options")
            print("10.Comment-specific View Options")
            print("11.Quit")
            inp = input("\nENTER: ")
            if(inp == '1'):
                viewOptions()
            elif(inp == '2'):
                insertionOptions()
            elif(inp=='5'):
                search()
            elif(inp=='6'):
                generateReport()
            elif(inp == '7'):
                showSuggestions()
            elif(inp == '8'):
                mutual()
            elif(inp=='9'):
                postListing()
            elif(inp=='10'):
                commentListing()
            elif(inp == '11'):
                exitflag = 1
                print("Exiting.")
                break

            input("Press enter to continue: ")

    if exitflag == 1:
        break
