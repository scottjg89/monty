# monty
A set of scripts I have use for some time for downloading and managing media.  They need a lot of work to bring them up to standard

I would not advise trying to run these on your own machine at the moment.

They work great on my box.  I would use a command like - python monty.py check SHOW
The script will check my media directory and compare the contents against the TVDB if it finds any episodes or seasons missing it will then go to the download site and add the missing files to transmission.  If it finds an episode that has not aired yet and TVDB knows the air date a cron job will be added for 6AM the next morning.


