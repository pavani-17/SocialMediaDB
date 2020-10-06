import subprocess as sp
import pymysql
import pymysql.cursors
from tabulate import tabulate
from time import time
from datetime import datetime
import time
import datetime

# ----------------- Functional Requirement Start ---------------


def printWeeklyReport():
    global cur
    query = "select CAST(MIN(CAST(uptime as float)) as TIME) as 'MINIMUM UPTIME' from USER;"
    try:
        cur.execute(query)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        con.rollback()
        print(e)
        return

    query = "select CAST(MAX(CAST(uptime as float)) as TIME) as 'MAXIMUM UPTIME'from USER;"
    try:
        cur.execute(query)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        con.rollback()
        print(e)
        return

    query = "select CAST(AVG(CAST(uptime as float)) as TIME) as 'MEAN UPTIME' from USER;"
    try:
        cur.execute(query)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        con.rollback()
        print(e)
        return

    query = """select CAST(AVG(CAST(med.uptime as float)) as TIME) as 'MEDIAN UPTIME' from (select @rowindex:=@rowindex + 1 as rowindex, USER.uptime from USER order by uptime) AS med where med.rowindex in (FLOOR(@rowindex/2), CEIL(@rowindex/2));"""
    try:
        cur.execute("set@rowindex := -1;")
        con.commit()
        cur.execute(query)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        con.rollback()
        print(e)

    query = "select stddev(uptime) as 'STANDARD DEVIATION OF UPTIME' from USER;"
    try:
        cur.execute(query)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        con.rollback()
        print(e)
        return


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

    if search_param == 1:
        search_type = "USER"
        search_field = "name"
    elif search_param == 2:
        search_type = "POST"
        search_field = "text"
    elif search_param == 3:
        search_type = "COMMENT"
        search_field = "text"
    elif search_param == 4:
        search_type = "PAGE"
        search_field = "page_name"
    elif search_param == 5:
        search_type = "social_media.GROUP"
        search_field = "group_name"
    else:
        print("Invalid Domain Error")
        return

    try:
        query = "SELECT * FROM %s WHERE %s REGEXP '%s'" % (
            search_type, search_field, search_key, )
        r = cur.execute(query)
        if r == 0:
            print("No result found")
            return
        rows = cur.fetchall()
        viewTable(rows)
    except Exception as e:
        print(e)
        print("Could not perform search")


def generateReport():
    try:
        user_id = int(
            input("Enter the User ID of the user you want to generate the report for: "))
    except Exception as e:
        print(e)
        print("User ID must be a number")
        return

    try:

        query = "SELECT * FROM USER WHERE user_id=%d" % (user_id)
        r = cur.execute(query)
        if r == 0:
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
            report_type = int(
                input("Enter the number of the report you would like to see: "))
        except Exception as e:
            print(e)
            print("Invalid Choice")
            return

        if report_type == 1:
            query = "SELECT * FROM USER WHERE user_id IN (SELECT follower_id FROM FOLLOWS WHERE following_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("There are no followers for the user\n")
            else:
                print("The users following the user are as follows: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 2:
            query = "SELECT * FROM USER WHERE user_id IN (SELECT following_id FROM FOLLOWS WHERE follower_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user does not follow anyone \n")
            else:
                print("The users the given user is following are as follows: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 3:
            query = "SELECT * FROM POST WHERE user_id=%d" % (user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not post any post\n")
            else:
                print("Posts posted by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 4:
            query = "SELECT COMMENT.comment_id, COMMENT.text, COMMENT.media, COMMENTS.post_id FROM COMMENT INNER JOIN COMMENTS ON COMMENT.comment_id = COMMENTS.comment_id WHERE COMMENTS.user_id = %d" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not post any post\n")
            else:
                print("Comments posted by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 5:
            query = "SELECT POST.post_id, POST.text, POST.media, POST.user_id, MAKES_GENERAL_REACT.reacted_type FROM POST INNER JOIN MAKES_GENERAL_REACT ON POST.post_id = MAKES_GENERAL_REACT.post_id WHERE MAKES_GENERAL_REACT.user_id = %d" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not react on any post\n")
            else:
                print("Posts reacted on by the user:")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 6:
            query = "SELECT COMMENT.comment_id, COMMENT.text, COMMENT.media, COMMENTS.post_id, MAKES_A_REACT.reacted_type FROM COMMENT INNER JOIN COMMENTS ON COMMENT.comment_id = COMMENTS.comment_id INNER JOIN MAKES_A_REACT ON MAKES_A_REACT.comment_id = COMMENT.comment_id WHERE MAKES_A_REACT.comment_id=%d" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not react on any comment\n")
            else:
                print("Comments reacted on by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 7:
            query = "SELECT * FROM PAGE WHERE owner_id = %d" % (user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not create any page\n")
            else:
                print("Pages created by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 8:
            query = "SELECT * FROM PAGE WHERE page_id IN (SELECT page_id FROM LIKES WHERE user_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user did not like any page\n")
            else:
                print("Pages liked by the user: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 9:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM IS_ADMIN WHERE user_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user is not the admin of any group\n")
            else:
                print("Groups the user is the admin of: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 10:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM IS_MODERATOR WHERE user_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
                print("The user is not the moderator of any group\n")
            else:
                print("Groups the user is the moderator of: ")
                rows = cur.fetchall()
                viewTable(rows)

        elif report_type == 11:
            query = "SELECT * FROM social_media.GROUP WHERE group_id IN (SELECT group_id FROM BELONGS_TO WHERE user_id=%d)" % (
                user_id)
            r = cur.execute(query)
            if r == 0:
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
                    ''' % (user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Followers:")
            if(r == 0):
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
                    ''' % (user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Followings:")
            if(r == 0):
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
                    ''' % (user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Likes to Pages:")
            if(r == 0):
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
                    ''' % (user1ID, user2ID)

            r = cur.execute(query)
            print("Mutual Likes to Pages:")
            if(r == 0):
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
        uid = int(
            input("Enter the UserID for the User you want to check the events for: "))
        date = input("Enter the date for the event tracking in MM-DD format: ")
        querybirthday = '''
                        SELECT * FROM USER WHERE user_id IN
                        (SELECT user_id FROM PROFILE WHERE user_id IN
                            (SELECT following_id FROM FOLLOWS WHERE follower_id = '%d')
                        AND
                        (date_of_birth REGEXP '%s'));
                        ''' % (uid, date+'+', )

        queryposts = '''
                        SELECT * FROM POST WHERE time REGEXP '%s' AND user_id = '%s';
                     ''' % (date+'+', uid, )

        r1 = cur.execute(querybirthday)
        print("Birthdays ->")
        if(r1 == 0):
            print("No Birthdays")
        else:
            rows = cur.fetchall()
            viewTable(rows)

        r1 = cur.execute(queryposts)
        print("Posts made on this day ->")
        if(r1 == 0):
            print("No Posts")
        else:
            rows = cur.fetchall()
            viewTable(rows)

    except Exception as e:
        print(e)
        print("ERROR")


def listReacttoPost():
    try:
        post_id = int(
            input("Choose the PostID you want to see the reacts for: "))
        queryposts = '''
                        SELECT USER.user_id,USER.name,MAKES_GENERAL_REACT.reacted_type FROM (MAKES_GENERAL_REACT INNER JOIN USER ON MAKES_GENERAL_REACT.user_id = USER.user_id ) WHERE MAKES_GENERAL_REACT.post_id = '%d';
                     ''' % (post_id)

        r1 = cur.execute(queryposts)
        print("Reacts to the post ->")
        if(r1 == 0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")


def listReacttoComment():
    try:
        comment_id = int(
            input("Choose the CommentID you want to see the reacts for: "))
        query = '''
                        SELECT USER.user_id,USER.name,MAKES_A_REACT.reacted_type FROM (MAKES_A_REACT INNER JOIN USER ON MAKES_A_REACT.user_id = USER.user_id ) WHERE MAKES_A_REACT.comment_id = '%d';
                     ''' % (comment_id)

        r1 = cur.execute(query)
        print("Reacts to the Comment ->")
        if(r1 == 0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")


def listCommenttoPost():
    try:
        post_id = int(
            input("Choose the PostID you want to see the comments for: "))
        query = '''
                        SELECT USER.user_id,USER.name,COMMENTS.comment_id,COMMENT.text,COMMENT.time FROM COMMENTS INNER JOIN USER ON COMMENTS.user_id = USER.user_id INNER JOIN COMMENT ON COMMENTS.comment_id = COMMENT.comment_id  WHERE COMMENTS.post_id = '%d';
                     ''' % (post_id)

        r1 = cur.execute(query)
        print("Comments to the Post ->")
        if(r1 == 0):
            print("No reacts yet")
        else:
            rows = cur.fetchall()
            viewTable(rows)
    except Exception as e:
        print(e)
        print("ERROR")


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
        else:
            print("Invalid Option")
    except Exception as e:
        print(e)
        print("ERROR")


def commentListing():
    try:
        print("Choose the option to see suggestions for: ")
        print("1. List all Reacts to a specific Comment")

        optn = int(input("Enter the choice: "))

        if(optn == 1):
            listReacttoComment()
        else:
            print("Invalid Option")
    except Exception as e:
        print(e)
        print("ERROR")


def showSuggestions():
    print("Choose the option to see suggestions for: ")
    print("1. User")
    print("2. Page")
    print("3. Group")

    try:
        optn = int(input("Enter option : "))
        if (optn == 1):
            user_id = int(
                input("Enter the User ID you want to see the FOLLOWING suggestions for : "))
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

                        ''' % (user_id, user_id, user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1 == 0):
                print("No suggestion to show")
            else:
                rows = cur.fetchall()
                viewTable(rows)
            return
        elif (optn == 2):
            user_id = int(
                input("Enter the User ID you want to see the PAGES suggestions for : "))
            query = '''
                    SELECT * FROM PAGE WHERE page_id IN (
                        SELECT page_id FROM LIKES WHERE user_id IN (
                           SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                        )
                        )
                        AND page_id NOT IN (
                            SELECT page_id FROM LIKES WHERE user_id = '%d'
                        )
                     ''' % (user_id, user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1 == 0):
                print("No suggestion to show")
            else:
                rows = cur.fetchall()
                viewTable(rows)
            return
        elif (optn == 3):
            user_id = int(
                input("Enter the User ID you want to see the GROUPS suggestions for : "))
            query = '''
                        SELECT * FROM social_media.GROUP WHERE group_id IN (
                            SELECT group_id FROM BELONGS_TO WHERE user_id IN (
                            SELECT following_id FROM FOLLOWS WHERE follower_id = '%d'
                            )
                            )
                            AND group_id NOT IN (
                                SELECT group_id FROM BELONGS_TO WHERE user_id = '%d'
                            )
                    ''' % (user_id, user_id)

            r1 = cur.execute(query)
            print("Suggestions ->")
            if(r1 == 0):
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


# ----------------- Functional Requirement End --------------------------------------------- #
##############################################################################################
##############################################################################################

def checkIsMemberOfGroup(user_id, group_id):
    global cur

    try:
        query = "SELECT * FROM BELONGS_TO WHERE user_id=%d AND group_id=%d;" % (
            int(user_id), int(group_id))
        try:
            cur.execute(query)
            con.commit()
            if cur.rowcount == 0:
                return False
            return True
        except Exception as e:
            con.rollback()
            return False
    except Exception as enx:
        return False


def checkCommentIntegrity(comment_id, user_id):
    global cur

    try:
        query = "SELECT * FROM COMMENTS WHERE user_id=%d AND comment_id=%d;" % (
            int(user_id), int(comment_id))
        try:
            cur.execute(query)
            con.commit()
            if cur.rowcount == 0:
                return False
            return True
        except Exception as e:
            con.rollback()
            return False
    except Exception as enx:
        return False


def getCurrentTimeStamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def isNonEmptyQuery(query, row):
    global cur
    try:
        cur.execute(query, row)
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
    while(1):
        tmp = sp.call('clear', shell=True)
        print("\nChoose the data that you want to see.\n\n")
        print("1.  USERS")
        print("2.  POST")
        print("3.  STORIES")
        print("4.  MESSAGES")
        print("5.  PROFILES")
        print("6.  EDUCATION OF USERS")
        # Pages
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
        # Groups
        print("17. GROUPS")
        # Relationships
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
        # Basically posts in a group - comment to avoid semantical confusion
        print("30. SHARES A POST IN A GROUP")
        print("31. USERS TAGGED IN POSTS")
        print("42. Go back.")
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
            query = "SELECT social_media.GROUP.group_id, social_media.GROUP.group_name, social_media.GROUP.group_privacy, COUNT(BELONGS_TO.user_id) AS Number_of_Members FROM social_media.GROUP LEFT OUTER JOIN BELONGS_TO ON social_media.GROUP.group_id = BELONGS_TO.group_id GROUP BY group_id"
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
        elif choice == '42':
            break
        else:
            input("Invalid input, press enter to continue.")
            continue

        try:
            no_of_rows = cur.execute(query)
            con.commit()
            rows = cur.fetchall()
            viewTable(rows)
            # print(rows)
        except Exception as e:
            con.rollback()
            print(e)
            print("\n\nError!\n")
        input("Press enter to continue.")

# ------------------------------ Insertions Start ----------------------------------------------#


def addUser():
    global cur
    user = {}
    print("Enter the details of the user below.\n")

    user["name"] = input("Please provide name of the user: ")
    user["email"] = input("Please provide the email id of the user: ")
    user["password"] = input("Please provide the password: ")
    user["address"] = input("Please provide the address: ")
    user["phone"] = input(
        "Please enter the phone number [without space or hyphen]: ")

    try:
        query = "INSERT INTO USER VALUES(NULL, %(password)s, %(name)s, %(email)s, %(address)s, %(phone)s, '00:00:00');"
        cur.execute(query, user)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addProfile():
    print("Enter the profile details of the user below.\n")
    profile = {}
    profile['user_id'] = input("Enter user id of the user: ")
    profile['dob'] = input("Enter Date-of-Birth in YYYY-MM-DD format: ")
    profile['sex'] = input(
        "Enter sex of the use [Male, Female, Others, PreferNotToSay]: ")

    try:
        query = "INSERT INTO PROFILE VALUES (%(user_id)s, %(dob)s, %(sex)s);"
        cur.execute(query, profile)
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
        query = "INSERT INTO POST VALUES (NULL, %(time)s, %(text)s, %(media)s, %(user_id)s);"
        cur.execute(query, post)
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

    if len(row["text"]) == 0 and len(row["media"]) == 0:
        print("You can't make an empty comment!")
        return

    try:
        query = "INSERT INTO COMMENT VALUES(NULL, %(time)s, %(text)s, %(media)s);"
        cur.execute(query, row)
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

    if len(row["text"]) == 0 and len(row["media"]) == 0:
        print("You can't make an empty story with no text and no media!")
        return

    try:
        query = "INSERT INTO STORIES VALUES(NULL, %(time)s, %(text)s, %(media)s, %(user_id)s);"
        cur.execute(query, row)
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
        query = 'INSERT INTO MESSAGE VALUES(NULL, %(text)s);'
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addEducation():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user: ")
    row["education"] = input(
        "Enter an educational qualification of the user: ")

    try:
        query = "INSERT INTO EDUCATION VALUES(%(user_id)s, %(education)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addGroup():
    global cur
    row = {}
    row["group_name"] = input("Enter the name of the new group: ")
    row["group_privacy"] = input(
        "Enter the privacy setting of the new group [Public, Private, Secret]: ")

    try:
        query = "INSERT INTO social_media.GROUP VALUES(NULL, %(group_name)s, %(group_privacy)s); "
        cur.execute(query, row)
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
        query = "INSERT INTO PAGE VALUES(NULL, %(page_name)s, %(owner_id)s); "
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addBusinessPlace():
    global cur
    row = {}
    row["page_id"] = input("Enter the ID of the page: ")
    row["owner_name"] = input(
        "Enter the name of the stake holder of this business: ")
    row["location"] = input("Enter the location: ")

    try:
        query = "INSERT INTO BUSINESS_PLACE VALUES(%(page_id)s, %(owner_name)s, %(location)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO PROD_BP VALUES(%(page_id)s, %(name)s, %(price)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO BRAND_PRODUCT VALUES(%(page_id)s, %(website)s, %(cust_service)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO COMPANY VALUES(%(page_id)s, %(work_domain)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO BRANCH_COMPANY VALUES(%(page_id)s, %(branch)s);"
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
        query = "INSERT INTO PUBLIC_FIGURE VALUES(%(page_id)s, %(name)s, %(field)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO NEWS_PUB_FIG VALUES(%(page_id)s, %(news)s, %(published_time)s); "
        cur.execute(query, row)
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
        query = "INSERT INTO ENTERTAINMENT VALUES(%(page_id)s, %(events)s, %(audience)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO CAUSE_COMMUNITY VALUES(%(page_id)s, %(goal)s, %(activities)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addFollows():
    global cur

    row = {}
    row["follower_id"] = input(
        "Enter user ID of the person that wants to follow someone: ")
    row["following_id"] = input(
        "Enter the user ID of the person that will be followed by the former person: ")

    try:
        query = "INSERT INTO FOLLOWS(follower_id, following_id) VALUES(%(follower_id)s, %(following_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addMakesGeneralReact():
    global cur
    row = {}

    row["post_id"] = input("Enter the POST ID: ")
    row["user_id"] = input("Enter your USER ID: ")

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
        row["reactedType"] = "Like"
    elif reactNum == 2:
        row["reactedType"] = "Dislike"
    elif reactNum == 3:
        row["reactedType"] = "Wow"
    elif reactNum == 4:
        row["reactedType"] = "Heart"
    elif reactNum == 5:
        row["reactedType"] = "Angry"
    elif reactNum == 6:
        row["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return
    try:
        query = "INSERT INTO MAKES_GENERAL_REACT(post_id, user_id, reacted_type) VALUES(%(post_id)s, %(user_id)s, %(reactedType)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addLikes():
    global cur
    row = {}
    row["user_id"] = input("Enter the user ID: ")
    row["page_id"] = input("Enter the page ID of the page to like: ")
    try:
        query = "INSERT INTO LIKES(page_id, user_id) VALUES(%(page_id)s, %(user_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addUserToGroup():
    global cur
    row = {}
    row["user_id"] = input(
        "Enter the ID of the user who wants to join a group: ")
    row["group_id"] = input(
        "Enter the ID of the group that the user wants to join: ")
    try:
        query = "INSERT INTO BELONGS_TO VALUES(%(user_id)s, %(group_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def makeUserAdmin():
    global cur
    row = {}
    row["user_id"] = input(
        "Enter the ID of the user to make him an admin of a group: ")
    row["group_id"] = input(
        "Enter the ID of the group for which user should be made an admin of: ")

    query = "SELECT * FROM BELONGS_TO where group_id=%(group_id)s and user_id=%(user_id)s;"

    if isNonEmptyQuery(query, row) == False:
        print("User doesn't belong to the group or invalid query.")
        return
    try:
        query = "INSERT INTO IS_ADMIN VALUES(%(user_id)s, %(group_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def makeUserModerator():
    global cur
    row = {}
    row["user_id"] = input(
        "Enter the ID of the user to make him an moderator of a group: ")
    row["group_id"] = input(
        "Enter the ID of the group for which user should be made an moderator of: ")

    query = "SELECT * FROM BELONGS_TO where group_id=%(group_id)s and user_id=%(user_id)s;"
    if isNonEmptyQuery(query, row) == False:
        print("User doesn't belong to the group or invalid query.")
        return
    try:
        query = "INSERT INTO IS_MODERATOR VALUES(%(user_id)s, %(group_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def makeReactionToAComment():
    global cur
    row = {}
    row["user_id"] = input("Enter the ID of the user who made the reaction: ")
    row["comment_id"] = input(
        "Enter the ID of the comment in which the reaction was made: ")
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
        row["reactedType"] = "Like"
    elif reactNum == 2:
        row["reactedType"] = "Dislike"
    elif reactNum == 3:
        row["reactedType"] = "Wow"
    elif reactNum == 4:
        row["reactedType"] = "Heart"
    elif reactNum == 5:
        row["reactedType"] = "Angry"
    elif reactNum == 6:
        row["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return

    try:
        query = "INSERT INTO MAKES_A_REACT(comment_id, user_id, reacted_type) VALUES(%(comment_id)s, %(user_id)s, %(reactedType)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def mentionInComment():
    global cur
    row = {}
    row["comment_id"] = input("Enter the ID of the comment: ")
    row["mentioner_id"] = input(
        "Enter the ID of the user who mentioned someone: ")
    row["mentionee_id"] = input("Enter the ID of the user who got mentioned: ")
    if checkCommentIntegrity(row["comment_id"], row["mentioner_id"]) == False:
        print("Error: Comment was not created by the user who mentioned.")
        return

    try:
        query = "INSERT INTO MENTIONS VALUES(%(mentioner_id)s, %(mentionee_id)s, %(comment_id)s);"
        cur.execute(query, row)
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
    row["post_id"] = input(
        "Enter the ID of the post in which the comment is made: ")

    try:
        query = "INSERT INTO COMMENTS VALUES(%(comment_id)s, %(user_id)s, %(post_id)s);"
        cur.execute(query, row)
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
    row["message_id"] = message_id
    try:
        query = "INSERT INTO SENDS_SPECIFIC VALUES(%(sender_id)s, %(receiver_id)s, %(message_id)s);"
        cur.execute(query, row)
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
    row["message_id"] = message_id
    if checkIsMemberOfGroup(row["sender_id"], row["group_id"]) == False:
        print("Error: Sender is not a member of the group.")
        return

    try:
        query = "INSERT INTO SENDS_GENERAL VALUES(%(sender_id)s, %(group_id)s, %(message_id)s); "
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addResponds():
    global cur
    row = {}
    row["reacter_id"] = input(
        "Enter the ID of the user who reacts to the story: ")
    row["story_id"] = input("Enter the ID of the story: ")
    print("Choose the react type by entering the corresponding number")
    print("1. Like")
    print("2. Dislike")
    print("3. Wow")
    print("4. Heart")
    print("5. Angry")
    print("6. Haha")
    reactNum = 123  # A random invalid number
    try:
        reactNum = int(input())
    except:
        print("Invalid react Type")

    if reactNum == 1:
        row["reactedType"] = "Like"
    elif reactNum == 2:
        row["reactedType"] = "Dislike"
    elif reactNum == 3:
        row["reactedType"] = "Wow"
    elif reactNum == 4:
        row["reactedType"] = "Heart"
    elif reactNum == 5:
        row["reactedType"] = "Angry"
    elif reactNum == 6:
        row["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return

    try:
        query = "INSERT INTO RESPONDS VALUES(%(reacter_id)s, %(story_id)s,%(reactedType)s);"
        cur.execute(query, row)
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
        query = "INSERT INTO SHARES VALUES(%(user_id)s, %(group_id)s, %(post_id)s);"
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def addIsTagged():
    global cur
    row = {}
    row["post_id"] = input("Enter the ID of the post: ")
    row["user_id"] = input(
        "Enter the ID of the user who is tagged in the post: ")

    try:
        query = "INSERT INTO IS_TAGGED VALUES(%(user_id)s, %(post_id)s); "
        cur.execute(query, row)
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
        print("Error: Check your inputs.")


def showUserCreationOptions():
    while(1):
        tmp = sp.call('clear', shell=True)
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
            cur.execute("SELECT LAST_INSERT_ID();")
            con.commit()
            output = cur.fetchone()
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


# --------------------------------- Insertions End ---------------------------------------------- #

###################################################################################################
###############################################  DELETE ###########################################

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

        if optn == 1:
            delUser()
        elif optn == 2:
            unFollow()
        elif optn == 3:
            delPost()
        elif optn == 4:
            delComment()
        elif optn == 5:
            delMessage()
        elif optn == 6:
            delStory()
        elif optn == 7:
            generalUnreact()
        elif optn == 8:
            unReact()
        elif optn == 9:
            unRespond()
        elif optn == 10:
            unLike()
        elif optn == 11:
            exitGroup()
        elif optn == 12:
            unAdmin()
        elif optn == 13:
            unModerator()
        elif optn == 14:
            unTag()
        elif optn == 15:
            unMention()
        elif optn == 42:
            return
        else:
            print("Oops! Choose an option between 1 to 15")


################# Entities ###################


def delUser():
    global cur
    # viewTableDel('1')
    user_id = input("Enter the User ID of the User to be removed: ")
    try:
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
    # viewTableDel('1')


def delComment():
    global cur
    # viewTableDel('18')
    comment_id = input("Enter the Comment ID of the Comment to be removed: ")
    try:
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
    # viewTableDel('18')


def delPost():
    global cur
    # viewTableDel('2')
    post_id = input("Enter the Post ID of the Post you to be removed: ")
    try:
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
    # viewTableDel('2')


def delMessage():
    global cur
    # viewTableDel('4')
    message_id = input("Enter the Message ID of the Message to be removed: ")
    try:
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
    # viewTableDel('4')


def delStory():
    global cur
    # viewTableDel('3')
    story_id = input("Enter the Story ID of the Story to be removed: ")
    try:
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
    # viewTableDel('3')


def delPage():
    global cur
    # viewTableDel('7')
    page_id = input("Enter the Page ID of the Page to be removed: ")
    try:
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
    # viewTableDel('7')


############### Relationships #################

def unFollow():
    global cur
    # viewTableDel('19')
    follower_id = input("Enter the Follower's User Id: ")
    following_id = input("Enter the User ID of the user to be unfollowed: ")
    try:
        follower_id = int(follower_id)
        following_id = int(following_id)
    except:
        print("Invalid Page ID")
        print("\n\nError!\n")
        return

    query = "DELETE FROM FOLLOWS WHERE follower_id='%d' AND following_id = %d;" % (
        follower_id, following_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('19')


def generalUnreact():
    global cur
    # viewTableDel('20')
    user_id = input("Enter the Reacting User Id: ")
    post_id = input("Enter the Post ID of the Post to be unreacted: ")
    try:
        user_id = int(user_id)
        post_id = int(post_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM MAKES_GENERAL_REACT WHERE user_id='%d' AND post_id = %d;" % (
        user_id, post_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('20')


def unLike():
    global cur
    # viewTableDel('21')
    user_id = input("Enter the User Id of the User who wants to unlike: ")
    page_id = input("Enter the Page ID of the Page to be unliked: ")

    try:
        user_id = int(user_id)
        page_id = int(page_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM FOLLOWS LIKES WHERE user_id='%d' AND page_id = %d;" % (
        user_id, page_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('21')


def exitGroup():
    global cur
    # viewTableDel('22')
    user_id = input("Enter the User ID of the User who wants to exit: ")
    group_id = input("Enter the Group ID of the Group: ")

    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query1 = "DELETE FROM BELONGS_TO WHERE user_id='%d' AND group_id = %d;" % (
        user_id, group_id)
    query2 = "DELETE FROM IS_ADMIN WHERE user_id='%d' AND group_id = %d;" % (
        user_id, group_id)
    query3 = "DELETE FROM IS_MODERATOR WHERE user_id='%d' AND group_id = %d;" % (
        user_id, group_id)
    try:
        cur.execute(query1)
        cur.execute(query2)
        cur.execute(query3)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('22')


def unAdmin():
    global cur
    # viewTableDel('23')
    user_id = input("Enter the User ID of the User to be removed from Admin: ")
    group_id = input("Enter the Group ID of the Group: ")

    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM IS_ADMIN WHERE (user_id='%d') AND (group_id = %d);" % (
        user_id, group_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('23')


def unModerator():
    global cur
    # viewTableDel('24')
    user_id = input(
        "Enter the User ID of the User to be removed from moderator: ")
    group_id = input("Enter the Group ID of the Group: ")

    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM IS_MODERATOR WHERE user_id='%d' AND group_id = %d;" % (
        user_id, group_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('24')


def unReact():
    global cur
    # viewTableDel('25')
    user_id = input("Enter the Reacting User Id: ")
    comment_id = input("Enter the Comment ID of the Comment to be unreacted: ")

    try:
        user_id = int(user_id)
        comment_id = int(comment_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return

    query = "DELETE FROM MAKES_A_REACT WHERE user_id='%d' AND comment_id = %d;" % (
        user_id, comment_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('25')
    return


def unMention():
    global cur
    # viewTableDel('26')
    comment_id = input("Enter the Comment ID to be unmentioned from: ")
    mentionee_id = input("Enter the User ID to be unmentioned: ")
    try:
        comment_id = int(comment_id)
        mentionee_id = int(mentionee_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM MENTIONS WHERE comment_id='%d' AND mentionee_id = %d;" % (
        comment_id, mentionee_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('26')
    return


def unRespond():
    global cur
    # viewTableDel('29')
    story_id = input("Enter the Story ID to unreact: ")
    reacter_id = input("Enter the User ID of the User unreacting: ")
    try:
        story_id = int(story_id)
        reacter_id = int(reacter_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM RESPONDS WHERE story_id='%d' AND reacter_id = %d;" % (
        story_id, reacter_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('29')
    return


def unTag():
    global cur
    # viewTableDel('31')
    post_id = input("Enter the Post ID to be untagged from: ")
    user_id = input("Enter the User ID to be untagged: ")
    try:
        post_id = int(post_id)
        user_id = int(user_id)
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    query = "DELETE FROM IS_TAGGED WHERE user_id='%d' AND post_id = %d;" % (
        user_id, post_id)
    try:
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("\n\nError!\n")
        return
    # viewTableDel('31')
    return

###############################################################################################
###############################################################################################
######################################### MODIFY ##############################################


def updatePost():
    # viewTableDel('2')
    global cur
    post = {}
    try:
        post["post_id"] = int(input("Enter the post id to be updated: "))
    except Exception as e:
        print(e)
        print("Post ID must be an integer")
        return

    post["media"] = input("Enter the updated media: ")
    post["text"] = input("Enter the updated text: ")

    try:
        query = "UPDATE POST SET media=%(media)s, text=%(text)s WHERE post_id=%(post_id)s;"
        cur.execute(query, post)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('2')
    return


def updateComment():
    # viewTableDel('18')
    global cur
    comment = {}
    try:
        comment["comment_id"] = int(
            input("Enter the comment id of the comment to be updated: "))
    except Exception as e:
        print(e)
        print("Comment ID must be an integer")
        return

    comment["text"] = input("Enter the updated text of the comment: ")

    try:
        query = "UPDATE COMMENT SET text=%(text)s WHERE comment_id=%(comment_id)s;"
        cur.execute(query, comment)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('18')


def updateStory():
    # viewTableDel('3')
    global cur
    story = {}

    try:
        story["story_id"] = int(
            input("Enter the story id of the story to be updated: "))
    except Exception as e:
        print(e)
        print("Story ID must be an integer")
        return

    story["text"] = input("Enter the updated text of the story: ")
    story["media"] = input("Enter the updated media of the story: ")

    try:
        query = "UPDATE STORIES SET text=%(text)s, media=%(media)s WHERE story_id = %(story_id)s;"
        cur.execute(query, story)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('3')


def updatePage():
    # viewTableDel('7')
    global cur
    page = {}

    try:
        page["page_id"] = int(
            input("Enter the page_id of the page to be updated: "))
    except Exception as e:
        print(e)
        print("Page ID must be an integer: ")
        return

    page["page_name"] = input("Enter the updated name of the page: ")

    try:
        query = "UPDATE PAGE SET page_name=%(page_name)s WHERE page_id=%(page_id)s;"
        cur.execute(query, page)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('7')


def updateGeneralReact():
    # viewTableDel('20')
    global cur
    react = {}

    try:
        react["post_id"] = int(
            input("Enter the post ID of the post you want to update the react on: "))
        react["user_id"] = int(
            input("Enter the user ID of the User whose react you want to change: "))
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
        react["reactedType"] = "Like"
    elif reactNum == 2:
        react["reactedType"] = "Dislike"
    elif reactNum == 3:
        react["reactedType"] = "Wow"
    elif reactNum == 4:
        react["reactedType"] = "Heart"
    elif reactNum == 5:
        react["reactedType"] = "Angry"
    elif reactNum == 6:
        react["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return

    try:
        query = "UPDATE MAKES_GENERAL_REACT SET reacted_type='%s' WHERE post_id = '%d' AND user_id='%d'" % (
            react["reactedType"], react["post_id"], react["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('20')


def updateMakesReact():
    # viewTableDel('25')
    global cur
    react = {}

    try:
        react["comment_id"] = int(
            input("Enter the comment ID of the comment you want to update the react on: "))
        react["user_id"] = int(input(
            "Enter the user ID of the user whose react on the comment you want to update: "))
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
        react["reactedType"] = "Like"
    elif reactNum == 2:
        react["reactedType"] = "Dislike"
    elif reactNum == 3:
        react["reactedType"] = "Wow"
    elif reactNum == 4:
        react["reactedType"] = "Heart"
    elif reactNum == 5:
        react["reactedType"] = "Angry"
    elif reactNum == 6:
        react["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return

    try:
        query = "UPDATE MAKES_A_REACT SET reacted_type='%s' WHERE comment_id = '%d' AND user_id='%d'" % (
            react["reactedType"], react["comment_id"], react["user_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('25')


def updateResponds():
    # viewTableDel('29')
    global cur
    react = {}

    try:
        react["story_id"] = int(
            input("Enter the Story ID of the Story you want to update the react on: "))
        react["reacter_id"] = int(input(
            "Enter the user ID of the User whose react on the story you want to update: "))
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
        react["reactedType"] = "Like"
    elif reactNum == 2:
        react["reactedType"] = "Dislike"
    elif reactNum == 3:
        react["reactedType"] = "Wow"
    elif reactNum == 4:
        react["reactedType"] = "Heart"
    elif reactNum == 5:
        react["reactedType"] = "Angry"
    elif reactNum == 6:
        react["reactedType"] = "Haha"
    else:
        print("Invalid react Type")
        return

    try:
        query = "UPDATE RESPONDS SET reacted_type='%s' WHERE story_id = '%d' AND reacter_id='%d'" % (
            react["reactedType"], react["story_id"], react["reacter_id"])
        cur.execute(query)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('29')


def updateGroup():
    # viewTableDel('17')
    global cur
    group = {}

    try:
        group["group_id"] = int(
            input("Enter the group ID of the group you want to update: "))
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

    if groupNum == 1:
        group["group_privacy"] = "Public"
    elif groupNum == 2:
        group["group_privacy"] = "Private"
    elif groupNum == 3:
        group["group_privacy"] = "Secret"
    else:
        print("Invalid Group Privacy Type")
        return

    try:
        query = "UPDATE social_media.GROUP SET group_name=%(group_name)s,group_privacy=%(group_privacy)s WHERE group_id=%(group_id)s;"
        cur.execute(query, group)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data :(")
        return

    # viewTableDel('17')


def updateProfile():
    # viewTableDel('5')
    global cur
    profile = {}

    try:
        profile["user_id"] = int(
            input("Enter the User ID of the profile u want to update: "))
    except Exception as e:
        print(e)
        print("User ID should be an integer ")
        return

    profile["dob"] = input(
        "Enter the updated Date of Birth in YYYY-MM-DD format ")

    try:
        query = "UPDATE PROFILE SET date_of_birth=%(dob)s WHERE user_id=%(user_id)s;"
        cur.execute(query, profile)
        con.commit()
    except Exception as e:
        print(e)
        print("Try again with different data")
        return

    # viewTableDel('5')


def updatePassword():
    global cur

    user = {}
    try:
        user['uid'] = int(input("Enter your user ID: "))
    except Exception as e:
        print(e)
        print("User ID must be an integer")
        return
    user['prev_password'] = input("Enter your previous password: ")
    try:
        query = "SELECT password FROM USER WHERE user_id = '%d'" % (
            user['uid'])
        cur.execute(query)
        prev_pass = cur.fetchone()
        prev_pass = str(prev_pass["password"])
    except Exception as e:
        print(e)
        return

    if (prev_pass == user["prev_password"]):
        user["new_password"] = input("Enter your new password: ")
        try:
            query = "UPDATE USER SET password = %(new_password)s WHERE user_id = %(uid)s;"
            cur.execute(query, user)
            con.commit()
            print("Password changed succesfully!")
        except Exception as e:
            print(e)
            return

    else:
        print("WRONG PASSWORD!!")
        return

    return


def updateUptime():
    global cur
    row = {}
    row['user_id'] = input(
        "Enter the user id of the user to update the uptime: ")
    query = "SELECT * from USER where user_id=%(user_id)s;"
    try:
        cur.execute(query, row)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        print(e)
        return
    row['uptime'] = input("Enter the new uptime: ")

    query = "update USER set uptime=%(uptime)s where user_id = %(user_id)s;"
    try:
        cur.execute(query, row)
        con.commit()
        dic = {}
        print(tabulate(cur.fetchall(), headers=dic, tablefmt='psql'))
    except Exception as e:
        print(e)


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
        print("11. Update the uptime of an user")
        print("42. Go Back")

        optn = input("Your option is : ")

        try:
            optn = int(optn)
        except Exception as e:
            print(e)
            return

        if optn == 1:
            updatePost()
        elif optn == 2:
            updateComment()
        elif optn == 3:
            updateStory()
        elif optn == 4:
            updatePage()
        elif optn == 5:
            updateGeneralReact()
        elif optn == 6:
            updateMakesReact()
        elif optn == 7:
            updateResponds()
        elif optn == 8:
            updateGroup()
        elif optn == 9:
            updateProfile()
        elif optn == 10:
            updatePassword()
        elif optn == 11:
            updateUptime()
        elif optn == 42:
            return
        else:
            print("Oops! Choose an option between 1 to 9")


###############################################################################################

while(1):
    tmp = sp.call('clear', shell=True)
    try:
        username = input("Username: ")
        password = input("Password: ")
        port = int(input("Port: "))
        host = input("Host: ")
    except Exception as e:
        print(e)
        print("Try again")
        continue

    try:
        con = pymysql.connect(host=host,
                              user=username,
                              password=password,
                              db='social_media',
                              cursorclass=pymysql.cursors.DictCursor,
                              port=port)
    except Exception as excep:
        print(excep)
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
        continue

    con.escape_string("'")

    with con.cursor() as cur:
        exitflag = 0
        while(1):
            tmp = sp.call('clear', shell=True)
            print("CHOOSE AN OPTION\n")
            print("1. General View Options")
            print("2. Insertion Options")
            print("3. Deletion Options")
            print("4. Modify Options")
            print("5. Search")
            print("6. User-specific View Options and Activity Report Generation")
            print("7. Show Suggestions")
            print("8. View Mutual Relationships")
            print("9. Post-specific View Options")
            print("10. Comment-specific View Options")
            print("11. See weekly report of the user.")
            print("12. Quit")
            inp = input("\nENTER: ")
            if(inp == '1'):
                viewOptions()
            elif(inp == '2'):
                insertionOptions()
            elif(inp == '3'):
                delOptions()
            elif(inp == '4'):
                updOptions()
            elif(inp == '5'):
                search()
            elif(inp == '6'):
                generateReport()
            elif(inp == '7'):
                showSuggestions()
            elif(inp == '8'):
                mutual()
            elif(inp == '9'):
                postListing()
            elif(inp == '10'):
                commentListing()
            elif inp == '11':
                printWeeklyReport()
            elif(inp == '12'):
                exitflag = 1
                print("Exiting.")
                break

            input("Press enter to continue: ")

    if exitflag == 1:
        break
