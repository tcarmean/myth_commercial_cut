myth_commercial_cut
===================

Cut commercials from a MythTV Recording and Transcode in Place

Task List:

- [x] Pull needed metadata from the database
- [ ] Check that the cutlist has actually be generated
- [x] Create working directory for transient files
- [ ] Remove working directory and transient files when done (WARNING)

Requirements (Ubuntu package names):

libav-tools
python-mysqldb
mkvtoolnix

This is a python take of the script created by Reuben Crane:

http://reubencrane.com/blog/mythtv-commercial-cut-script/

How to call this script as a UserJob:

```
/path/to/myth_commercial_cut.py %DIR% %FILE% %CHANID% %STARTTIME%
```
