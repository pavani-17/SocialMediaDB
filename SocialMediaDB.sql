DROP DATABASE IF EXISTS social_media;
CREATE DATABASE social_media;
USE social_media;

DROP TABLE IF EXISTS USER;
CREATE TABLE USER (
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
insert into USER VALUES(NULL, '#PinRaYI', 'Pinarayi Vijayan',  'cmo@kerala.gov.in', 'Cliff House, Trivandrum', 10020030019, '00:03:00');
insert into USER VALUES(NULL, 'Chowkeedar', 'Narendra Modi',  'pm@gov.in', '7 Lok Kalyan Marg, New Delhi', 1111111111, '100:00:04');

DROP TABLE IF EXISTS POST;
CREATE TABLE POST (
    post_id int not null AUTO_INCREMENT,
    time TIMESTAMP not null,
    text TEXT,
    media varchar(10000),
    user_id int not null,
    PRIMARY KEY(post_id),
    CONSTRAINT OWNS_POST FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE,
    CONSTRAINT CONTENT_PRESENT_IN_POST CHECK (text is NOT NULL OR media is NOT NULL)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;


insert into POST VALUES(NULL, '2020-10-03 00:00:01', "A random news I saw today\n, National Boyfriend Day on October 3rd recognizes the sweetheart in your life. Like special days for family members, this day dedicates attention to the boyfriends in our lives. Whether the relationship is new or seasoned, boyfriends bring unique meaning to our lives.", NULL, 1);
insert into POST VALUES(NULL, '2020-10-03 12:00:09', "Inaugurating 90 new Government Schools.", "https://www.facebook.com/PinarayiVijayan/videos/1244544369240150", 2);
insert into POST VALUES(NULL, '2020-10-03 09:00:01', "Today, I will be inaugurating Atal Tunnel in Manali. It is “world’s longest highway” tunnel and is named Atal Tunnel, Rohtang. The 9.02 kilometres long engineering marvel connects Manali in Himachal Pradesh to Lahaul-Spiti throughout the year. Currently, the area remains cut off for about 6 months each year owing to heavy snowfall and inclement weather. The Atal tunnel has huge strategic significance as it will greatly assist in the movement of armed forces.\n\nAtal Tunnel or the Rohtang tunnel has been built in the Pir Panjal range of Himalayas. The tunnel is located at an altitude of 10,000 Feet from the Mean Sea Level (MSL). The tunnel is set to reduce road distance by 46 kilometres between Leh and Manali. Atal tunnel also reduces the journey time by around 4 to 5 hours. The decision to construct a strategic tunnel below the Rohtang Pass was taken on June 03, 2000 during the tenure of the then Prime Minister Atal Bihari Vajpayee.", "https://images.newindianexpress.com/uploads/user/imagelibrary/2020/10/3/w900X450/Modi_Atal_tunnel_PTI.jpg", 3);
insert into POST VALUES(NULL, '2020-10-03 16:00:01', NULL, "https://d3nuqriibqh3vw.cloudfront.net/attachment-4_resized_0.jpg?Y82N9g17xw0FhDEVnmX8nAs96cyHP.w6", 2);

DROP TABLE IF EXISTS COMMENT;
CREATE TABLE COMMENT(
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

DROP TABLE IF EXISTS STORIES;
CREATE TABLE STORIES(
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
CREATE TABLE MESSAGE(
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

DROP TABLE IF EXISTS PROFILE;
CREATE TABLE PROFILE (
    user_id int PRIMARY KEY,
    date_of_birth DATE not null,
    sex ENUM('Male', 'Female', 'Others', 'PreferNotToSay') not null,
    CONSTRAINT OWNS_PROFILE FOREIGN KEY (user_id) REFERENCES USER (user_id) on DELETE CASCADE on UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

insert into PROFILE VALUES(1, '1923-03-01', 4);
insert into PROFILE VALUES(2, '2000-05-03', 1);
insert into PROFILE VALUES(3, '1992-06-12', 1);

DROP TABLE IF EXISTS EDUCATION;
CREATE TABLE EDUCATION (
    user_id INT,
    education VARCHAR(100),
    PRIMARY KEY (user_id, education),
    FOREIGN KEY (user_id) REFERENCES PROFILE(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into EDUCATION VALUES(1, 'None');
insert into EDUCATION VALUES(1, 'MS in Computational Political Science');
insert into EDUCATION VALUES(2, "Bachelor's degree in Political Science");
-- insert into EDUCATION VALUES(3, "Bachelor's degree in Bulshitting");
insert into EDUCATION VALUES(3, "Doctor of Philosophy in Political Science");


DROP TABLE IF EXISTS PAGE;
CREATE TABLE PAGE (
    page_id int AUTO_INCREMENT NOT NULL PRIMARY KEY,
    page_name varchar(100) NOT NULL,
    owner_id int,
    FOREIGN KEY (owner_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into PAGE VALUES(NULL, "Disney World", 1);
insert into PAGE VALUES(NULL, "BSNL", 3);

DROP TABLE IF EXISTS BUSINESS_PLACE;
CREATE TABLE BUSINESS_PLACE (
    page_id int PRIMARY KEY,
    owner_name varchar(100) NOT NULL,
    location varchar(100),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS PROD_BP;
CREATE TABLE PROD_BP(
    page_id int,
    name varchar(50),
    price decimal(10,2),
    FOREIGN KEY (page_id) REFERENCES BUSINESS_PLACE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(page_id,name,price)
);

DROP TABLE IF EXISTS COMPANY;
CREATE TABLE COMPANY (
    page_id int PRIMARY KEY,
    work_domain varchar(30),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into COMPANY VALUES(2, "Telecom");

DROP TABLE IF EXISTS BRANCH_COMPANY;
CREATE TABLE BRANCH_COMPANY (
    page_id int,
    branch varchar(50),
    FOREIGN KEY (page_id) REFERENCES COMPANY(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id, branch)
);

DROP TABLE IF EXISTS BRAND_PRODUCT;
CREATE TABLE BRAND_PRODUCT (
    page_id int PRIMARY KEY,
    website varchar(50),
    cust_service int(10),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS PUBLIC_FIGURE;
CREATE TABLE PUBLIC_FIGURE (
    page_id int PRIMARY KEY,
    name varchar(50),
    field varchar(50),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS NEWS_PUB_FIG;
CREATE TABLE NEWS_PUB_FIG (
    page_id int ,
    news varchar(1000),
    published_time timestamp,
    FOREIGN KEY (page_id) REFERENCES PUBLIC_FIGURE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (page_id,published_time)
);

DROP TABLE IF EXISTS ENTERTAINMENT;
CREATE TABLE ENTERTAINMENT  (
    page_id int PRIMARY KEY,
    events varchar(300),
    audience varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into ENTERTAINMENT VALUES(1, "Closing ceremony: Closing for unknown period because of the pandemic.", "Anyone wearing masks!");


DROP TABLE IF EXISTS CAUSE_COMMUNITY;
CREATE TABLE CAUSE_COMMUNITY  (
    page_id int PRIMARY KEY,
    goal varchar(300),
    activities varchar(300),
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS social_media.GROUP;
CREATE TABLE social_media.GROUP (
    group_id int AUTO_INCREMENT PRIMARY KEY,
    group_name varchar(50) NOT NULL,
    group_privacy ENUM('Public', 'Private', 'Secret')
);

insert into social_media.GROUP VALUES(NULL, "India", 1);
insert into social_media.GROUP VALUES(NULL, "Kerala", 1);
insert into social_media.GROUP VALUES(NULL, "Representatives", 3);
-- insert into social_media.GROUP VALUES();


-- relationships

DROP TABLE IF EXISTS COMMENTS;
CREATE TABLE COMMENTS (
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

DROP TABLE IF EXISTS FOLLOWS;
CREATE TABLE FOLLOWS (
    follower_id INT NOT NULL ,
    following_id INT NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (following_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(follower_id,following_id)
);
-- follower_id follows the user with following_id
insert into FOLLOWS VALUES(2, 1);
insert into FOLLOWS VALUES(3, 1);
insert into FOLLOWS VALUES(1, 2);
insert into FOLLOWS VALUES(3, 2);
insert into FOLLOWS VALUES(1, 3);
insert into FOLLOWS VALUES(2, 3);

DROP TABLE IF EXISTS MAKES_GENERAL_REACT;
CREATE TABLE MAKES_GENERAL_REACT (
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
CREATE TABLE LIKES (
    user_id INT NOT NULL ,
    page_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (page_id) REFERENCES PAGE(page_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,page_id)
);

DROP TABLE IF EXISTS BELONGS_TO;
CREATE TABLE BELONGS_TO (
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
CREATE TABLE IS_ADMIN (
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
CREATE TABLE IS_MODERATOR (
    user_id INT NOT NULL ,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES social_media.GROUP(group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,group_id)
);

insert into IS_MODERATOR VALUES(2, 1);
insert into IS_MODERATOR VALUES(1, 2);

DROP TABLE IF EXISTS MAKES_A_REACT;
CREATE TABLE MAKES_A_REACT (
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
CREATE TABLE MENTIONS (
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
CREATE TABLE SENDS_SPECIFIC (
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
CREATE TABLE SENDS_GENERAL (
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
CREATE TABLE RESPONDS (
    reacter_id INT NOT NULL ,
    story_id INT NOT NULL,reacted_type ENUM('Like', 'Haha', 'Heart', 'Angry', 'Wow', 'Dislike'),
    FOREIGN KEY (reacter_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (story_id) REFERENCES STORIES(story_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(reacter_id,story_id)
);

insert into RESPONDS VALUES(2, 1, 2);
insert into RESPONDS VALUES(3, 1, 5);

DROP TABLE IF EXISTS SHARES;
CREATE TABLE SHARES (
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
CREATE TABLE IS_TAGGED (
    user_id INT NOT NULL ,
    post_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES POST(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(user_id,post_id)
);

insert into IS_TAGGED VALUES(3, 4); -- Pinarayi tags modi on WearMask post.
