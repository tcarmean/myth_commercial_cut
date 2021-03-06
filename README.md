myth_commercial_cut
===================

Cut commercials from a MythTV Recording and Transcode

This is a python take on the script created by Reuben Crane:

http://reubencrane.com/blog/mythtv-commercial-cut-script/

It would appear that mythtranscode --honorcutlist no longer works for transcoding files on the frontend (using mythbuntu tracking 0.27+fixes). Some prodding from a friend got me to see if I could do it myself. If you bothered to read the bash script at the link above you can see that this is simply a reimplementation of that script in python with some added bits to configure the database connection from the mysql.txt file that mythbuntu (or something else) created on my behalf when I installed the system.

Requirements (Ubuntu package names):

- libav-tools
- python-mysqldb
- mkvtoolnix
- handbrake-cli

Features:

- Designed to be run as a User Job
- Requires no special configuration (reads mysql.txt in ~/.mythtv/ for database info)

How to call this script as a UserJob:

```
/path/to/myth_commercial_cut.py %DIR% %FILE% %CHANID% %STARTTIMEUTC%
```

Task List:

- [x] Pull needed metadata from the database
- [ ] Use avconv to export a temp file that inserts a key frame at each cut point (convert cut points to time indices and store in a list)
- [ ] Use HandBrakeCLI --start-at frame:### --stop-at frame:### to create segments
- [ ] Check that the cutlist has actually be generated
- [x] Create working directory for transient files
- [x] Remove working directory and transient files when done
- [ ] Tweak the transcode settings for segments (~~both~~ video ~~and audio~~). Current output is pretty low quality.
- [ ] Error checking!!!
