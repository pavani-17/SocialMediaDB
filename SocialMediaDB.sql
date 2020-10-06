DROP DATABASE IF EXISTS social_media;
CREATE DATABASE social_media;
USE social_media;

DROP TABLE IF EXISTS USER;
CREATE TABLE USER ( -- Done
    user_id INT NOT NULL AUTO_INCREMENT primary key,
    password varchar(120) NOT NULL,
    name varchar(50) NOT NULL,
    email varchar(50) NOT NULL,
    contact_address varchar(300) NOT NULL,
    phone BIGINT,
    uptime TIME not null
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- insert into USER VALUES(NULL, 'sdfsfs', 'NMAE',  'pb@afsd.com', 'voldem', 1231231, '12:12:21');
insert into USER VALUES(NULL, '#unbreakable_password', 'Nirmal',  'nirmal@nmc.com', 'Bakul Nivas, IIIT Hyderabad', 9812517891, '03:12:20');
insert into USER VALUES(NULL, '#PinRaYI', 'Alapan',  'alapan.sau@students.iiit.ac.in', 'Cliff House, Kolkata', 10020030019, '00:03:00');
insert into USER VALUES(NULL, '#Chowkeedar', 'Pavani',  'pavani.babburi@students.iiit.ac.in', '7 Lok Kalyan Marg, Andhra Pradesh', 11113521111, '100:00:04');
insert into USER VALUES(NULL, '#Chowke', 'Alice',  'alice.stanley@students.iiit.ac.in', '7 Lok Kalyan Marg, California', 1111114231, '100:00:04');
insert into USER VALUES(NULL, '#Brokeedar', 'Hasvitha',  'hasvitha.verma@students.iiit.ac.in', '72C, Viskhapatnam, Andhra Pradesh', 11111163281, '10:05:04');
insert into USER VALUES(NULL, '#Chowkeedar', 'Sharadha',  'sharadha.iyer@students.iiit.ac.in', '7 Lok Camel Marg, Bangalore', 1111111111, '194:03:04');
insert into USER VALUES(NULL, '#Chowkdar', 'Pavani',  'pavani.chowdhury@students.iiit.ac.in', '7 Lok Camel Marg, States', 1111167911, '174:03:04');

DROP TABLE IF EXISTS POST;
CREATE TABLE POST ( -- Done
    post_id int not null AUTO_INCREMENT,
    time TIMESTAMP not null,
    text TEXT,
    media varchar(10000),
    user_id int not null,
    PRIMARY KEY(post_id),
    CONSTRAINT OWNS_POST FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE,
    CONSTRAINT CONTENT_PRESENT_IN_POST CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;


insert into POST VALUES(NULL, '2014-11-03 00:00:01', "A random news I saw today\n, National Boyfriend Day on October 3rd recognizes the sweetheart in your life. Like special days for family members, this day dedicates attention to the boyfriends in our lives. Whether the relationship is new or seasoned, boyfriends bring unique meaning to our lives.", NULL, 1);
insert into POST VALUES(NULL, '2011-09-02 12:00:09', "Inaugurating 90 new Government Schools.", "https://www.facebook.com/PinarayiVijayan/videos/1244544369240150", 2);
insert into POST VALUES(NULL, '2013-11-03 09:00:01', "Today, I will be inaugurating Atal Tunnel in Manali. It is “world’s longest highway” tunnel and is named Atal Tunnel, Rohtang. The 9.02 kilometres long engineering marvel connects Manali in Himachal Pradesh to Lahaul-Spiti throughout the year. Currently, the area remains cut off for about 6 months each year owing to heavy snowfall and inclement weather. The Atal tunnel has huge strategic significance as it will greatly assist in the movement of armed forces.\n\nAtal Tunnel or the Rohtang tunnel has been built in the Pir Panjal range of Himalayas. The tunnel is located at an altitude of 10,000 Feet from the Mean Sea Level (MSL). The tunnel is set to reduce road distance by 46 kilometres between Leh and Manali. Atal tunnel also reduces the journey time by around 4 to 5 hours. The decision to construct a strategic tunnel below the Rohtang Pass was taken on June 03, 2000 during the tenure of the then Prime Minister Atal Bihari Vajpayee.", "https://images.newindianexpress.com/uploads/user/imagelibrary/2020/10/3/w900X450/Modi_Atal_tunnel_PTI.jpg", 3);
insert into POST VALUES(NULL, '1987-04-03 16:00:01', NULL, "https://d3nuqriibqh3vw.cloudfront.net/attachment-4_resized_0.jpg?Y82N9g17xw0FhDEVnmX8nAs96cyHP.w6", 2);
insert into POST VALUES(NULL, '2011-10-05 16:00:01', "Just Too Bored","text", 1);
insert into POST VALUES(NULL, '2016-10-03 16:00:01', "Just not yet Bored","text", 6);
insert into POST VALUES(NULL, '2018-04-02 16:00:01', "Life is Boring","text", 4);
insert into POST VALUES(NULL, '2004-06-06 16:00:01', "Online Classes are Boring","text", 2);
insert into POST VALUES(NULL, '2003-04-21 16:00:01', "Hello Bro!","text", 3);
insert into POST VALUES(NULL, '2002-03-04 16:00:01', "Yay!! We won","text", 5);


DROP TABLE IF EXISTS COMMENT;
CREATE TABLE COMMENT( -- Done
    comment_id int not null AUTO_INCREMENT PRIMARY KEY,
    time TIMESTAMP not NULL,
    text TEXT,
    media VARCHAR(10000),
    CONSTRAINT CONTENT_PRESENT_IN_COMMENT CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

insert into COMMENT VALUES(NULL, '2020-10-03 10:00:01', "That is very funny, nirmal!", NULL); -- Mod to Nirmal
-- [comment 1]
insert into COMMENT VALUES(NULL, '2020-10-03 10:00:01', "Are you so jobless?!", NULL); -- Pin to Nirmal
-- [comment 2]
insert into COMMENT VALUES(NULL, '2020-10-03 12:00:09', "Nice work!", "https://en.pimg.jp/047/504/690/1/47504690.jpg"); -- Mod to Pin
-- [comment 3]
insert into COMMENT VALUES(NULL, '2020-10-03 14:00:00', "Congrats on finishing this!", NULL); -- Pin to Mod
-- [comment 4]
insert into COMMENT VALUES(NULL, '2020-10-03 14:20:00', "Thanks:)", NULL); -- Mod to Pin
-- [comment 5]
insert into COMMENT VALUES(NULL, '2020-10-03 14:00:05', NULL, "https://blog.award.co/hubfs/Thankyou.png"); -- Pin to Mod, thank you msg.
-- [comment 6]
insert into COMMENT VALUES(NULL, '2020-10-03 12:00:10', "Amazing work..", NULL); -- Nirmal to Pin
-- [comment 7]

insert into COMMENT VALUES(NULL, '2011-10-02 12:04:11', "Hello Yyy", NULL); -- (1,2) post 4
insert into COMMENT VALUES(NULL, '2011-10-02 12:04:13', "Hello Zzz", NULL);
insert into COMMENT VALUES(NULL, '2011-10-02 12:04:11', "Nice to meet Yyy", NULL);

insert into COMMENT VALUES(NULL, '2012-10-03 12:04:11', "KKR is shit", NULL); -- (2,3) post 6
insert into COMMENT VALUES(NULL, '2012-10-03 12:04:11', "Kohli is great", NULL);
insert into COMMENT VALUES(NULL, '2012-10-03 12:04:11', "You are shit", NULL);

insert into COMMENT VALUES(NULL, '2013-10-05 12:04:11', "ISS was there last sem", NULL); -- (5,6) post 3
insert into COMMENT VALUES(NULL, '2013-10-05 12:04:11', "ISS is a very bad course", NULL);
insert into COMMENT VALUES(NULL, '2013-10-05 12:04:11', "Nope, do you know about Lalit?", NULL);


insert into COMMENT VALUES(NULL, '2014-10-07 12:04:11', "Hey, lets vote for Trump", NULL); -- (1,4) post 2
insert into COMMENT VALUES(NULL, '2014-10-07 12:04:11', "Naah, Biden is a promising candidate", NULL);
insert into COMMENT VALUES(NULL, '2014-10-07 12:04:11', "They shout so much", NULL);
insert into COMMENT VALUES(NULL, '2014-10-07 12:04:11', "Let's just chill out and not elect anyone", NULL);



DROP TABLE IF EXISTS STORIES;
CREATE TABLE STORIES( -- Done
    story_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    time DATETIME,
    text TEXT,
    media VARCHAR(10000),
    user_id int not null,
    CONSTRAINT OWNS_STORY FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE,
    CONSTRAINT CONTENT_PRESENT_IN_STORY CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
insert into STORIES VALUES(NULL, '2020-10-03 15:00:00', "Hey, what a horrific day", "https://st.depositphotos.com/1006250/1214/i/950/depositphotos_12141968-stock-photo-dry-field-road-in-the.jpg", 1);

DROP TABLE IF EXISTS MESSAGE;
CREATE TABLE MESSAGE( -- Done
    message_id int not null PRIMARY KEY AUTO_INCREMENT,
    text TEXT not null
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

insert into MESSAGE VALUES(NULL, "Bhaisaheb.. we need funds.");
-- insert into MESSAGE VALUES();
insert into MESSAGE VALUES(NULL, "Bhai bhai.. please wait. I'm working on it.");
insert into MESSAGE VALUES(NULL, "Hmm..");
insert into MESSAGE VALUES(NULL, "xD");

insert into MESSAGE VALUES(NULL, "Meri pyaari deshvasyon, you are doomed!");
insert into MESSAGE VALUES(NULL, "Irresponsible decision.");
insert into MESSAGE VALUES(NULL, "I knew it.");
-- insert into MESSAGE VALUES();
insert into MESSAGE VALUES(NULL, "Bhai bhai...");
insert into MESSAGE VALUES(NULL, "Nahi..");
insert into MESSAGE VALUES(NULL, "DASA level treat..");
insert into MESSAGE VALUES(NULL, "Avengers assemble.");


DROP TABLE IF EXISTS PROFILE;
CREATE TABLE PROFILE ( -- Done
    user_id int PRIMARY KEY,
    date_of_birth DATE not null,
    sex ENUM('Male', 'Female', 'Others', 'PreferNotToSay') not null,
    CONSTRAINT OWNS_PROFILE FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

insert into PROFILE VALUES(1, '1923-03-01', 4);
insert into PROFILE VALUES(2, '2000-05-03', 1);
insert into PROFILE VALUES(3, '1992-06-12', 2);
insert into PROFILE VALUES(4, '2000-05-03', 3);
insert into PROFILE VALUES(5, '1992-06-12', 4);
insert into PROFILE VALUES(6, '2000-05-03', 2);
insert into PROFILE VALUES(7, '1992-06-12', 1);


DROP TABLE IF EXISTS EDUCATION;
CREATE TABLE EDUCATION ( -- Done
    user_id INT,
    education VARCHAR(100),
    PRIMARY KEY (user_id, education),
    FOREIGN KEY (user_id) REFERENCES PROFILE(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into EDUCATION VALUES(1, 'None');
insert into EDUCATION VALUES(1, 'MS in Computational Political Science');
insert into EDUCATION VALUES(2, "Bachelor's degree in Political Science");
-- insert into EDUCATION VALUES(3, "Bachelor's degree in Bulshitting");
insert into EDUCATION VALUES(3, "Doctor of Philosophy in Computer Science");
insert into EDUCATION VALUES(4, "Doctor of Philosophy in Sex Therapy");
insert into EDUCATION VALUES(5, "Doctor of Philosophy in History");
insert into EDUCATION VALUES(6, "Doctor of Philosophy in Database Systems");
insert into EDUCATION VALUES(7, "Doctor of Philosophy in Youtubing");

DROP TABLE IF EXISTS PAGE;
CREATE TABLE PAGE ( -- Done
    page_id int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    page_name varchar(100) NOT NULL,
    owner_id int,
    FOREIGN KEY (owner_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into PAGE VALUES(NULL, "Disney World", 1);
insert into PAGE VALUES(NULL, "BSNL", 3);
insert into PAGE VALUES(NULL, "IIIT Confession's Page", 3);
insert into PAGE VALUES(NULL, "AITA", 4);
insert into PAGE VALUES(NULL, "Never say Never", 5);
insert into PAGE VALUES(NULL, "Samsung Galaxy Series", 1);
insert into PAGE VALUES(NULL, "Alapan's Best Momo", 2);
insert into PAGE VALUES(NULL, "Virat Kohli", 3);

DROP TABLE IF EXISTS BUSINESS_PLACE;
CREATE TABLE BUSINESS_PLACE ( -- Done
    page_id int PRIMARY KEY,
    owner_name varchar(100) NOT NULL,
    location varchar(100),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);
insert into BUSINESS_PLACE VALUES(7,"Alapan", 2);

DROP TABLE IF EXISTS PROD_BP;
CREATE TABLE PROD_BP( -- Done
    page_id int,
    name varchar(50),
    price decimal(10,2),
    FOREIGN KEY (page_id) REFERENCES BUSINESS_PLACE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(page_id,name,price)
);
insert into PROD_BP VALUES(7, "Momo", 2001);

DROP TABLE IF EXISTS COMPANY;
CREATE TABLE COMPANY ( -- Done
    page_id int PRIMARY KEY,
    work_domain varchar(30),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into COMPANY VALUES(2, "Telecom");

DROP TABLE IF EXISTS BRANCH_COMPANY;
CREATE TABLE BRANCH_COMPANY ( -- Done
    page_id int,
    branch varchar(50),
    FOREIGN KEY (page_id) REFERENCES COMPANY(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id, branch)
);
insert into BRANCH_COMPANY VALUES(2,"South-east Asia");

DROP TABLE IF EXISTS BRAND_PRODUCT;
CREATE TABLE BRAND_PRODUCT ( -- Done
    page_id int PRIMARY KEY,
    website varchar(50),
    cust_service int(10),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);
insert into BRAND_PRODUCT VALUES(6, "www.sam.com", 1263638021);

DROP TABLE IF EXISTS PUBLIC_FIGURE;
CREATE TABLE PUBLIC_FIGURE ( -- Done
    page_id int PRIMARY KEY,
    name varchar(50),
    field varchar(50),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);
insert into PUBLIC_FIGURE VALUES(8, "Virat", "Cricket");

DROP TABLE IF EXISTS NEWS_PUB_FIG;
CREATE TABLE NEWS_PUB_FIG ( -- Done
    page_id int ,
    news varchar(1000),
    published_time timestamp,
    FOREIGN KEY (page_id) REFERENCES PUBLIC_FIGURE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id,published_time)
);
insert into NEWS_PUB_FIG values(8,"He made 43 out of 13 balls",'2020-09-07 12:04:11');

DROP TABLE IF EXISTS ENTERTAINMENT;
CREATE TABLE ENTERTAINMENT  ( -- Done
    page_id int PRIMARY KEY,
    events varchar(300),
    audience varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into ENTERTAINMENT VALUES(1, "Closing ceremony: Closing for unknown period because of the pandemic.", "Anyone wearing masks!");


DROP TABLE IF EXISTS CAUSE_COMMUNITY;
CREATE TABLE CAUSE_COMMUNITY  ( -- Done
    page_id int PRIMARY KEY,
    goal varchar(300),
    activities varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);
insert into CAUSE_COMMUNITY values(7,"Fill Tummy","Eating Momo");

DROP TABLE IF EXISTS social_media.GROUP;
CREATE TABLE social_media.GROUP ( -- Done
    group_id int AUTO_INCREMENT PRIMARY KEY,
    group_name varchar(50) NOT NULL,
    group_privacy ENUM('Public', 'Private', 'Secret')
);

insert into social_media.GROUP VALUES(NULL, "India", 1);
insert into social_media.GROUP VALUES(NULL, "Kerala", 1);
insert into social_media.GROUP VALUES(NULL, "Representatives", 3);
insert into social_media.GROUP VALUES(NULL, "Republicans", 2);
insert into social_media.GROUP VALUES(NULL, "British", 2);
insert into social_media.GROUP VALUES(NULL, "DASA", 3);
-- insert into social_media.GROUP VALUES();


-- relationships

DROP TABLE IF EXISTS COMMENTS;
CREATE TABLE COMMENTS ( -- Done
    comment_id INT NOT NULL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (comment_id) REFERENCES COMMENT(comment_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES POST(post_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into COMMENTS VALUES(1, 3, 1);
insert into COMMENTS VALUES(2, 2, 1);
insert into COMMENTS VALUES(3, 3, 2);
insert into COMMENTS VALUES(4, 2, 3);
insert into COMMENTS VALUES(5, 3, 3);
insert into COMMENTS VALUES(6, 2, 2);
insert into COMMENTS VALUES(7, 1, 2);
insert into COMMENTS VALUES(8, 1, 4);
insert into COMMENTS VALUES(9, 2, 4);
insert into COMMENTS VALUES(10, 2, 4);
insert into COMMENTS VALUES(11, 3, 6);
insert into COMMENTS VALUES(12, 3, 6);
insert into COMMENTS VALUES(13, 2, 6);
insert into COMMENTS VALUES(14, 5, 3);
insert into COMMENTS VALUES(15, 6, 3);
insert into COMMENTS VALUES(16, 5, 3);

DROP TABLE IF EXISTS FOLLOWS;
CREATE TABLE FOLLOWS ( -- Done
    follower_id INT NOT NULL ,
    following_id INT NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (following_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(follower_id,following_id)
    );
-- follower_id follows the user with following_id
-- insert into FOLLOWS VALUES(2, 1);
insert into FOLLOWS VALUES(3, 1);
insert into FOLLOWS VALUES(1, 2);
insert into FOLLOWS VALUES(3, 2);
insert into FOLLOWS VALUES(1, 3);
insert into FOLLOWS VALUES(2, 3);
insert into FOLLOWS VALUES(3, 4);
insert into FOLLOWS VALUES(4, 5);
insert into FOLLOWS VALUES(4, 6);
insert into FOLLOWS VALUES(5, 7);
insert into FOLLOWS VALUES(3, 7);

DROP TABLE IF EXISTS MAKES_GENERAL_REACT;
CREATE TABLE MAKES_GENERAL_REACT ( -- Done
    user_id INT NOT NULL ,
    post_id INT NOT NULL,
    reacted_type ENUM('Like', 'Haha', 'Heart', 'Angry', 'Wow', 'Dislike'),
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES POST(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,post_id)
);
--                          (user_liking_post, post, reactType)
insert into MAKES_GENERAL_REACT VALUES(1, 2, 3); -- Heart react
insert into MAKES_GENERAL_REACT VALUES(1, 3, 1); 
insert into MAKES_GENERAL_REACT VALUES(1, 4, 1);
insert into MAKES_GENERAL_REACT VALUES(2, 3, 1);
insert into MAKES_GENERAL_REACT VALUES(3, 2, 1);
insert into MAKES_GENERAL_REACT VALUES(3, 4, 1);

DROP TABLE IF EXISTS LIKES;
CREATE TABLE LIKES ( -- Done
    user_id INT NOT NULL ,
    page_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,page_id)
);

DROP TABLE IF EXISTS BELONGS_TO;
CREATE TABLE BELONGS_TO ( -- Dine
    user_id INT NOT NULL ,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,group_id)
);

insert INTO BELONGS_TO VALUES(1, 1);
insert INTO BELONGS_TO VALUES(2, 1);
insert INTO BELONGS_TO VALUES(3, 1);
insert INTO BELONGS_TO VALUES(1, 2);
insert INTO BELONGS_TO VALUES(2, 2);
insert INTO BELONGS_TO VALUES(2, 3);
insert INTO BELONGS_TO VALUES(3, 3);

DROP TABLE IF EXISTS IS_ADMIN;
CREATE TABLE IS_ADMIN ( -- Done
    user_id INT NOT NULL ,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,group_id)
);

insert into IS_ADMIN VALUES(3, 1);
insert into IS_ADMIN VALUES(2, 2);
insert into IS_ADMIN VALUES(2, 3);
insert into IS_ADMIN VALUES(3, 3);


DROP TABLE IF EXISTS IS_MODERATOR;
CREATE TABLE IS_MODERATOR ( -- DOne
    user_id INT NOT NULL ,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,group_id)
);

insert into IS_MODERATOR VALUES(2, 1);
insert into IS_MODERATOR VALUES(1, 2);

DROP TABLE IF EXISTS MAKES_A_REACT;
CREATE TABLE MAKES_A_REACT ( -- Done
    user_id INT NOT NULL ,
    comment_id INT NOT NULL,
    reacted_type ENUM('Like', 'Haha', 'Heart', 'Angry', 'Wow', 'Dislike'),
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES COMMENT(comment_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,comment_id)
);
--                  (user_liking_comment, comment, reactType)
insert into MAKES_A_REACT VALUES(1, 1, 2);
insert into MAKES_A_REACT VALUES(1, 2, 4);
insert into MAKES_A_REACT VALUES(2, 3, 3);
insert into MAKES_A_REACT VALUES(3, 4, 3);
insert into MAKES_A_REACT VALUES(2, 7, 3);

DROP TABLE IF EXISTS MENTIONS;
CREATE TABLE MENTIONS ( -- Done
    mentioner_id INT NOT NULL ,
    mentionee_id INT NOT NULL,
    comment_id INT NOT NULL,
    FOREIGN KEY (mentioner_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (mentionee_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES COMMENT(comment_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(comment_id,mentioner_id,mentionee_id)
);

insert into MENTIONS VALUES(3, 2, 5); -- Modi mentions pinarayi in thanks message.
insert into MENTIONS VALUES(2, 3, 6); -- Pinarayi mentions Modi in thanks message.

DROP TABLE IF EXISTS SENDS_SPECIFIC;
CREATE TABLE SENDS_SPECIFIC ( -- Done
    sender_id INT NOT NULL ,
    receiver_id INT NOT NULL,
    message_id INT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (message_id) REFERENCES MESSAGE(message_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(message_id)
);

-- insert into SENDS_SPECIFIC VALUES()
insert into SENDS_SPECIFIC VALUES(2, 3, 1);
insert into SENDS_SPECIFIC VALUES(3, 2, 2);
insert into SENDS_SPECIFIC VALUES(2, 3, 3);
insert into SENDS_SPECIFIC VALUES(3, 2, 4);

DROP TABLE IF EXISTS SENDS_GENERAL;
CREATE TABLE SENDS_GENERAL ( -- Done
    sender_id INT NOT NULL ,
    group_id INT NOT NULL,
    message_id INT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (message_id) REFERENCES MESSAGE(message_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(message_id)
);

insert into SENDS_GENERAL VALUES(3, 1, 5);
insert into SENDS_GENERAL VALUES(2, 1, 6);
insert into SENDS_GENERAL VALUES(1, 1, 7);

DROP TABLE IF EXISTS RESPONDS;
CREATE TABLE RESPONDS ( -- Done
    reacter_id INT NOT NULL ,
    story_id INT NOT NULL,
    reacted_type ENUM('Like', 'Haha', 'Heart', 'Angry', 'Wow', 'Dislike'),
    FOREIGN KEY (reacter_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (story_id) REFERENCES STORIES(story_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(reacter_id,story_id)
);

insert into RESPONDS VALUES(2, 1, 2);
insert into RESPONDS VALUES(3, 1, 5);

DROP TABLE IF EXISTS SHARES;
CREATE TABLE SHARES ( -- Done
    user_id INT NOT NULL ,
    group_id INT NOT NULL,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES POST(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(post_id, group_id, user_id)
);

insert into SHARES VALUES(3, 1, 2);
insert into SHARES VALUES(3, 1, 3);
insert into SHARES VALUES(2, 2, 2);

DROP TABLE IF EXISTS IS_TAGGED;
CREATE TABLE IS_TAGGED ( -- Done
    user_id INT NOT NULL ,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES POST(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,post_id)
);

insert into IS_TAGGED VALUES(3, 4); -- Pinarayi tags modi on WearMask post.
