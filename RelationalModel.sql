// Strong entities

Table USER {
  user_id int [pk, increment]
  password string
  email email
  name string
  contact_address string
  phone number
  uptime time 
 }
 
Table POST {
  post_id int [pk, increment]
  time timestamp
  text string
  media media
  user_id int
}

Table COMMENT {
  comment_id int [pk, increment]
  text string
  time timestamp
}

Table STORIES {
  story_id int [pk]
  time timestamp
  text string
  media media
}

Table MESSAGE {
  message_id int [pk]
  text string
}

// Weak entities
Enum sex {
    Male
    Female
    Others
    PreferNotToSay
} 

Table PROFILE {
  user_id int [pk]
  date_of_birth date
  sex sex
  education string
}

Table EDUCATION {
  user_id int [pk]
  education string [pk]
}

Enum reactType {
  Like
  Heart
  Haha
  Wow
  Sad 
  Angry
  Dislike
}

// Classes

Table PAGE{
    page_id int [pk, increment]
    page_name string
    owner_id int
}

Table BUSINESS_PLACE{
    page_id int [pk]// Foreign key
    owner string
    location string
}

Table PROD_BP {
    page_id int [pk]// Foreign key
    name string [pk]
    price int [pk]
}

Table COMPANY {
    page_id int [pk]// Foreign key
    work_domain varchar
}

Table BRANCH_COMPANY {
    page_id int [pk]// Foreign key
    branch string [pk]
}

Table BRAND_PRODUCT {
    page_id int [pk]//foreign key
    website string
    cust_service string
} 

Table PUBLIC_FIGURE {
    page_id int [pk]// foreign key
    name string
    field string
}

Table NEWS_PUB_FIG {
    page_id int [pk]// foreign key
    news string
    published_time timestamp [pk]
}

Table ENTERTAINMENT {
    page_id int [pk]// foreign key
    event string
    audience string
}

Table CAUSE_COMMUNITY {
    page_id int [pk]// foreign key
    goal string
    activities string
}

Enum privacyStatus {
    Public
    Private
    Secret
}

Table GROUP {
    group_id int [pk, increment]
    group_name string
    group_privacy privacyStatus
}

// Relations

Table COMMENTS {
  user_id int 
  comment_id int [pk]
  post_id int
}

Table FOLLOWS {
  follower_id int [pk]
  following_id int [pk]
}

Table MAKES_GENERAL_REACT {
   user_id int [pk]
   post_id int [pk]
   reacted_type reactType
}

Table LIKES {
   user_id int [pk]
   page_id int [pk]
}

Table BELONGS_TO {
   user_id int [pk]
   group_id int [pk]
}

Table IS_ADMIN {
   user_id int [pk]
   group_id int [pk]
}

Table IS_MODERATOR {
   user_id int [pk]
   group_id int [pk]
}

Table MAKES_A_REACT {
   user_id int [pk]
   comment_id int [pk]
   post_id int
   reacted_type reactType
}

Table MENTIONS {
   mentioner_id int [pk]
   mentionee_id int [pk]
   comment_id int [pk]
   post_id int
}

Table SENDS_SPECIFIC {
   sender_id int
   reciever_id int
   message_id int [pk]
}

Table SENDS_GENERAL {
   sender_id int
   group_id int
   message_id int [pk]
}

Table RESPONDS {
    reacter_id int [pk]
    story_id int [pk]
    reacted_type reactType
}

Table SHARES {
   user_id int
   post_id int [pk]
   group_id int
}

Table IS_TAGGED {
    user_id int [pk]
    post_id int [pk]
}


Ref: "USER"."user_id" < "PROFILE"."user_id"

Ref: "USER"."user_id" < "POST"."user_id"

Ref: "USER"."user_id" < "COMMENTS"."user_id"
Ref: "POST"."post_id" < "COMMENTS"."post_id"
Ref: "COMMENT"."comment_id" < "COMMENTS"."comment_id"

Ref: "USER"."user_id" < "FOLLOWS"."follower_id"
Ref: "USER"."user_id" < "FOLLOWS"."following_id"

Ref: "USER"."user_id" < "MAKES_GENERAL_REACT"."user_id"
Ref: "POST"."post_id" < "MAKES_GENERAL_REACT"."post_id"

Ref: "USER"."user_id" < "LIKES"."user_id"
Ref: "PAGE"."page_id" < "LIKES"."page_id"

Ref: "USER"."user_id" < "MAKES_A_REACT"."user_id"
Ref: "COMMENT"."comment_id" < "MAKES_A_REACT"."comment_id"
Ref: "POST"."post_id" < "MAKES_A_REACT"."post_id"

Ref: "COMMENT"."comment_id" < "MENTIONS"."comment_id"
Ref: "USER"."user_id" < "MENTIONS"."mentioner_id"
Ref: "USER"."user_id" < "MENTIONS"."mentionee_id"
 Ref: "POST"."post_id" < "MENTIONS"."post_id"

Ref: "USER"."user_id" < "SENDS_SPECIFIC"."sender_id"
Ref: "USER"."user_id" < "SENDS_SPECIFIC"."reciever_id"
Ref: "MESSAGE"."message_id" < "SENDS_SPECIFIC"."message_id"


Ref: "USER"."user_id" < "BELONGS_TO"."user_id"
Ref: "GROUP"."group_id" < "BELONGS_TO"."group_id"

Ref: "USER"."user_id" < "IS_ADMIN"."user_id"
Ref: "GROUP"."group_id" < "IS_ADMIN"."group_id"

Ref: "USER"."user_id" < "IS_MODERATOR"."user_id"
Ref: "GROUP"."group_id" < "IS_MODERATOR"."group_id"

Ref: "USER"."user_id" < "IS_TAGGED"."user_id"
Ref: "POST"."post_id" < "IS_TAGGED"."post_id"

Ref: "USER"."user_id" < "SHARES"."user_id"
Ref: "GROUP"."group_id" < "SHARES"."group_id"
Ref: "POST"."post_id" < "SHARES"."post_id"

 // All page subclass ones
Ref: "PAGE"."page_id" < "BUSINESS_PLACE"."page_id"
Ref: "BUSINESS_PLACE"."page_id" < "PROD_BP"."page_id"
Ref: "PUBLIC_FIGURE"."page_id" < "NEWS_PUB_FIG"."page_id"
Ref: "PAGE"."page_id" < "BRAND_PRODUCT"."page_id"
Ref: "COMPANY"."page_id" < "BRANCH_COMPANY"."page_id"
Ref: "PAGE"."page_id" < "CAUSE_COMMUNITY"."page_id"
Ref: "PAGE"."page_id" < "COMPANY"."page_id"
Ref: "PAGE"."page_id" < "ENTERTAINMENT"."page_id"
Ref: "PAGE"."page_id" < "PUBLIC_FIGURE"."page_id"

//Sends General
Ref: "USER"."user_id" < "SENDS_GENERAL"."sender_id"
Ref: "GROUP"."group_id" < "SENDS_GENERAL"."group_id"
Ref: "MESSAGE"."message_id" < "SENDS_GENERAL"."message_id"

//Responds to story
Ref: "USER"."user_id" < "RESPONDS"."reacter_id"
Ref: "STORIES"."story_id" < "RESPONDS"."story_id"

Ref: "EDUCATION".user_id > "PROFILE"."user_id"

Ref: "PAGE"."owner_id" < "USER"."user_id"

