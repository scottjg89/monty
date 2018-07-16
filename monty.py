#!/usr/local/bin/python3.5
import tvdb_api
import os
import sys
import datetime
import down

# --------- Change these paths to fit your needs

# path is the directory where your media lives which should look like this
# /path/to/media/SHOW/Season 01/EPISODES
# and be defined like this...
path = '/path/to/media/'

# logs directory
log = open('/var/log/custom/monty.log', 'a')

def download(show, season, episode):
    log.write('Monty got {} {} {}'.format(show, season, episode))
    down.load(show, season, episode)

# Check if file already exists
def exists(show, season, episode):
    #print('show = {} season = {} episode = {}'.format(show, season, episode))
    file_exist = False
    if len(str(season)) == 1:
        season = '0%s'%(season)
        #print('SEASON = {}'.format(season))
    if len(str(episode)) == 1:
        episode = '0%s'%(episode)
        #print('EPISODE = {}'.format(episode))
    if os.path.isdir('%s%s'%(path,show)) == True:
        #print('{}{} = dir'.format(path, show))
        if os.path.isdir('%s%s/Season %s'%(path,show,season)) == True:
            #print('{}{}/Season {} = dir'.format(path, show, season))
            for ep in os.listdir('%s%s/Season %s'%(path,show,season)):
                if '[%sx%s]'%(season,episode) in ep:
                    #print('EXISTS!!!!!!!!!!!!!!!!')
                    file_exist = True
                else:
                    pass
        else:
            file_exist = False
    else:
#        print('{}{} = NOT DIR!!'.format(path, show))
        file_exist = False
#    print('exists() debug message: show = %s season = %s episode = %s seasonii$
    return file_exist

# this function is run if checking an indevidual season.  Better way of doing this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def check1(show, **kwargs):
    # Check how many items in path is same as DB, else error (do you want to run SOMETHING first?)
    t = tvdb_api.Tvdb()
    if kwargs.get('season'):
        seasons = [int(kwargs.get('season'))]
    else:
        seasons = t[show].keys()
    for season in seasons: # tvdb_exceptions.tvdb_shownotfound
        if season == 0:
            pass # Dosome specials function
        else:
            for episode in t[show][season].keys():
                try:
                    aired = t[show][season][episode].get('firstaired')
                except:
                    print('Get aired failed')
                srtdte = t[show][int(season)][int(episode)].get('firstaired')
                year = int(srtdte.split('-')[0])
                month = int(srtdte.split('-')[1])
                day = int(srtdte.split('-')[2])
                aired = datetime.datetime(year, month, day)
                if not aired < datetime.datetime.now(): #timedelta(days=1):
                   # print('locked. S%sE%s to be aired %s'%(season,episode, aired.strftime('%d-%m-%Y')))
                    if 'download \"{}\" {} {}'.format(show, season, episode) in open('/etc/crontab').read():
                        print('S{}E{} not yet aired. crontab already exists for {} {}'.format(season, episode, day+1, aired.strftime('%h')))
                    else:
                        os.system("echo 00 06 {} {} \* root /mnt/data/homes/scott/Backups/Pi2/pi/scripts/tvdb/monty.py download \\\"{}\\\" {} {} >> /etc/crontab".format(day+1, month, show, season, episode))
                        print('S{}E{} not yet aired. Added crontabito run on {} {}.'.format(season, episode, day+1, aired.strftime('%h')))
                elif aired < datetime.datetime.now(): #timedelta(days=1):
                    if exists(show,season,episode) == True:
                        pass
                    elif exists(show,season,episode) == False:
                        print('Searching... %s %s %s'%(show, season, episode))
                        down.load(show, season, episode)
                    else:
                        print('Elsing')
                else:
                    pass # Log write?


if __name__ == '__main__':
    if not os.geteuid() == 0:
        cont = input('You have not run this script as root.  I can continue but I wont be able to '
                     'create any cron jobs for any future episodes '
                     'Do you still want to continue? (y/n) ')
        if cont == 'n':
            sys.exit('Exiting')
        elif cont == 'y':
            print('Continuing...')
        else:
            print('Oops, sorry I didnt understand that.')
            sys.exit('Exiting...')
#    try:
    if sys.argv[1] == 'download':
        log.write('\nCalling down.load... {} {} {}\n'.format(sys.argv[2], sys.argv[3], sys.argv[4]))
        down.load(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'check':
        show = sys.argv[2]
        for argu in sys.argv:
            if 'season=' in argu:
                seasons = argu.replace('season=', '')
                check1(show, season=seasons)
        check1(show)
    else:
        print('elsing')
#    except IndexError as er:
#        log.write('\nexcepting {}\n'.format(er))
