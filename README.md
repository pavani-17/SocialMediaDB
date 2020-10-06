# Social Media DB

A simple database application designed with miniworld as a social media, with CLI interface, which allows users to perform all the tasks in an actual social media such as sharing posts, reacting and commenting to posts, update profile details, etc.

## Steps to Run


```shell 
 mysql -h <local host> -u <username> --port=<port> -p < SocialMediaDB.sql
 python3 app.py
```

The `SocialMediaDB.sql` creates the database, the necessary tables and also populates the database with some data. <br>
The actual CLI application is in `app.py`
