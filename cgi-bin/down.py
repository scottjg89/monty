#!/usr/bin/python3

#import threading
from time import sleep
#import urllib.request
import subprocess
import re
import sys
import os
import cgi
import datetime
#from pushover import Client
#client = Client("ucGDF9dXuEPgUmNFWoGvGxKj9KVEgx", api_token="aALmbjAMS5mAmk4c91H9KqNcqiyobM")

# NEED BETTER LOGGING

topPoints = {}
magdic = {}

def log(logFile, msg):
    ts = datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')
    logFile.write('{}~# {}\n'.format(ts, msg))

def setsize(size, points, show, season, episode, tpe, logFile):
    if tpe == 'film':
        p1min = 699
        p1max = 800
        p2min = 801
        p2max = 1000
        p3min = 1001
        p3max = 1200
        p4min = 1201
        p4max = 1400
        p5min = 1401
        p5max = 2000
        pmin = 2001
        pmax = 5000
    elif tpe == 'season':
        if season == 'complete':
            p1min = 400
            p1max = 50000
            p2min = 50001
            p2max = 10000
            p3min = 10001
            p3max = 20000
            p4min = 20001
            p4max = 40000
            p5min = 40001
            p5max = 60000
            pmin = 60001
            pmax = 150000
        if re.findall(r'season \d{1,2}', season):
            if episode == 'complete':
                p1min = 400
                p1max = 1000
                p2min = 1001
                p2max = 2000
                p3min = 2001
                p3max = 3000
                p4min = 3001
                p4max = 4000
                p5min = 4001
                p5max = 5000
                pmin = 5001
                pmax = 10000
        if re.findall(r'S\d{1,2}', season):
            if episode == 'complete':
                p1min = 400
                p1max = 1000
                p2min = 1001
                p2max = 2000
                p3min = 2001
                p3max = 3000
                p4min = 3001
                p4max = 4000
                p5min = 4001
                p5max = 5000
                pmin = 5001
                pmax = 10000
            elif re.findall(r'E\d{1,2}', episode):
                p1min = 80
                p1max = 100
                p2min = 101
                p2max = 140
                p3min = 141
                p3max = 180
                p4min = 181
                p4max = 220
                p5min = 221
                p5max = 500
                pmin = 501
                pmax = 1500
    if size < p1max > p1min:
        points = points + 1
    elif size < p2max > p2min:
        points = points + 2
    elif size < p3max > p3min:
        points = points + 3
    elif size < p4max > p4min:
        points = points + 4
    elif size < p5max > p5min:
        points = points + 5
    elif size < pmax > pmin:
        points = points + 3
        warning = 'Warning, file size = {}mb for show {}'.format(size, show)
    if size >= pmax:
        points = points - 100
        warning = 'Warning, maximum file size exceded, size = {}mb for show {}'.format(size, show)
    return points


def parse_query(show, getseason, getepisode, getseason3, getepisode3, logFile):
    log(logFile, 'Parsing query...')
    if getseason == None: #if season chkbox has not been clicked
        try:
            season = int(getseason3) # check for a number in season txtbox
            tpe = 'season'
            log(logFile, 'Found season {}'.format(season))
        except:
            log(logFile, 'int error')
        try:
            if len(str(season)) == 1:
                log(logFile, 'len season == 1 prepending a 0')
                season = 'S0{}'.format(season)
            else:
                log(logFile, 'Season len == 2. OK')
                season = 'S{}'.format(season)
        except:
            pass
    elif getseason == 'sall': #if season chkbox is selected
        log(logFile, 'Getting all seasons!')
        season = 'complete'
        episode = ''
        tpe = 'season'
    if getseason == None: #if both chkbox and txtbox are blank look for movie
        if getseason3 == None:
            log(logFile, 'Movie found?')
            tpe = 'film'
            season = 'Movie'
    if getseason == 'sall': #if season all chkbox seleted all eps presumed so pass
        pass
    else:
        if getepisode == None: #if eps chkbox has not been selected
            try:
                episode = int(getepisode3) #test for number in txtbox
                tpe = 'season'
                log(logFile, 'Found episode {}'.format(episode))
            except:
                pass # pass if not number in txtbox
        try:
            if len(str(episode)) == 1:
                episode = 'E0{}'.format(episode)
                log(logFile, 'Episode len == 1 prepending 0')
            else:
                episode = 'E{}'.format(episode)
                log(logFile, 'Episode len == 2. OK ')
        except:
            pass
        if getepisode == 'eall': #if eps chkbox selected
            episode = 'complete'
            season = 'season {}'.format(getseason3)
            tpe = 'season'
            log(logFile, 'Found episodes all. Getting all episodes from season {}'.format(season))
            
#    if getepisode == None: # if nether chkbox or txt box used look for movie
#        if getepisode3 == None:
#            tpe = 'film'
#            episode = 'Movie'
    if tpe == 'season':
        if season == 'complete':
            query = '{} {}'.format(show, season)
        else:
            if episode == 'complete':
                query = '{} {} {}'.format(show, season, episode)
            else:
                query = '{} {}{}'.format(show, season, episode)
    elif tpe == 'film':
        query = show

    squery = query.replace(' ', '%20')
    return query, squery, tpe, season, episode


def getlinks(query, tpe, show, season, episode, url, input_source, logFile):
    mags = re.findall(r"magnet:\?.+\n?.+\n?.+\n?.+\n?right\">\d{1,5}</td>\n?.+right\">\d{1,5}</td>", str(url))
    if len(mags) > 0:
        for mag in mags:
            points = 0
            link = re.findall(r"magnet:\?\S+(?=\")", mag)[0]
            seeds = int(re.findall(r"(?<=right\">)\d{1,5}(?=<\/td>\n.{1,100}\d{1,5}<\/td>)", mag)[0])
#            seeds = int(re.findall(r"(?<=right\">)\d{1,5}(?=<\/td>\n.{1,100}<td align=\"right\">\d{1,5}<\/td>)", mag)[0])
            name = re.findall(r"(?<=dn=).{5,105}(?=tr=)", mag)[0]
            size = float(re.findall(r"(?<=Size )\d{1,4}\.?\d{1,2}?(?=&nbsp;)", mag)[0])
            if "MiB" in mag:
                pass
            elif "GiB" in mag:
                size = size * 1024
            else:
                size = 0
            points = setsize(size, points, show, season, episode, tpe, logFile)
            if seeds == 0:
                points = points - points - 10
            if seeds >= 1 <= 5:
                points = points + 1
            if seeds >= 6 <= 10:
                points = points + 2
            if seeds >= 11 <= 20:
                points = points + 3
            if seeds >= 20:
                points = points + 5
            if '720p' in name:
                points = points + 3
                quality = '720p'
            elif '1080p' in name:
                quality = '1080p'
                points = points + 5
            else:
                quality = 'Unknown'
            if any(word in name for word in ['WEB-DL', 'WEBDL', 'Web-DL', 'webdl', 'web-dl', 'Web-dl', 'Web-Dl', 'Web-Dl', 'WEBRip']):
                source = 'web download'
                points = points - 1
            if any(word in name for word in ['HDRIP', 'HDRip', 'HD-RIP', 'HD-Rip', 'hdrip', 'hd-rip', 'HDTV', 'hdtv', 'blueray', 'BLUERAY', 'Blueray', 'BrRip', 'HD']):
                source = 'HD Rip'
                points = points + 3
            if any(word in name for word in ['DVDRIP', 'DVD-RIP', 'DVDRip', 'dvdrip', 'dvd-rip', 'DVD-Rip']):
                source = 'DVD Rip'
                points = points + 2
            if any(word in name for word in ['[ettv]', '[eztv]']):
                points = points + 2
            else:
                source = 'Unknown'
            procpoints(tpe, name, points, link, input_source, query, logFile)
        procpoints('end', 'end', 0, 0, input_source, query, logFile, show=show, season=season, episode=episode)
    else:
        logFile.write('No magnet links found')
        print('No magnet links found!')


def procpoints(tpe, name, points, magnet, input_source, query, logFile, **kwargs):
    if len(name) >= 4:
        topPoints[name] = points
        magdic[name] = magnet
    elif len(name) == 3:
#        try:
        maxPoints = max(topPoints.values())
        top = list(topPoints.keys())[list(topPoints.values()).index(maxPoints)]
        topMagnet = magdic[top]
#        os.popen('transmission-remote -a \"{}\"'.format(topMagnet))
        transAdd = os.system('transmission-remote localhost -a \"{}\"'.format(topMagnet))
        if not transAdd == 0:
            print('SOME FAILURE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {}'.format(transAdd))
            print(topMagnet)
            sys.exit()
        print('Successefully added to Transmission Daemon. ({})'.format(topMagnet))
        log(logFile, '{} added to download queue'.format(top))
#        client.send_message('{} added to download queue'.format(top), title='Torrent Added')
        cron_tweak('delete', kwargs.get('show'), kwargs.get('season'), kwargs.get('episode'), logFile)
#        except:
#            log(logFile, "Failed to add {} to download queue".format(name))
#            client.send_message("Failed to add {} to download queue".format(name), title="Error!")
        if input_source == 'web':
            print('<head><h1>Redirecting</h1><body bgcolor="#F0F8FF"><meta http-equiv="refresh" content="5;url=download.py" /></head>')
            print('<html><body><p>Please wait you are being redirected...</p>')
            print('{} has been added to download queue</body></html>'.format(query))
            log(logFile, '{} has been added to download queue'.format(query))

#os.system("echo 00 06 {} {} \* root /mnt/data/homes/scott/Backups/Pi2/pi/scripts/tvdb/monty.py download \\\"{}\\\" {} {} >> /etc/crontab".format(day+1, month, show, season, episode))
class cron_tweak:
    def __init__(self, func, show, season, episode, logFile):
        log(logFile, 'Cron_Tweak __init__')
        exists = False
        check_for_cron = open('/etc/crontab', 'r')
        for line in check_for_cron.readlines():
#            if '00 06 16 10 * root /mnt/data/homes/scott/Backups/Pi2/pi/scripts/tvdb/monty.py download "{}" {} {}'.format(datetime.datetime.today().strftime('%d'), datetime.datetime.today().strftime('%m'), show, season[1:], episode[1:]) in line:
            if '"{}" {} {}'.format(show, season[1:], episode[1:]) in line:
                exists = True
        check_for_cron.close()
        if exists and func == 'reshed':
            self.reshed(show, season, episode, logFile)
        elif exists:
            log(logFile, 'Exists + func = '.format(func))
            self.delete(show, season, episode, logFile)
        else:
            log(logFile, 'Cron does not exist func = {}'.format(func))
            #input('Create cron for tomorrow?')
            #if auto create cron flag is set then create cron

    def reshed(self, show, season, episode, logFile):
        os.rename('/etc/crontab', '/etc/crontab.BAK')
        crontab_write = open('/etc/crontab', 'w')
        crontab = open('/etc/crontab.BAK', 'r')
        day = datetime.datetime.today().strftime('%d')
        month = datetime.datetime.today().strftime('%m')
        for tab in crontab.readlines():
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tday = tomorrow.strftime('%d')
            tmonth = tomorrow.strftime('%m')
            if tap == '"{}" {} {}'.format(day, month, show, season, episode):
                crontab.write('00 06 {} {} * root /mnt/data/homes/scott/Backups/Pi2/pi/scripts/tvdb/monty.py download "{}" {} {}'.format(tday, tmonth, show, season, episode))
            else:
                crontab.write(tab)
        crontab.write()

    def create(self, show, season, episode, logFile):
        pass

    def delete(self, show, season, episode, logFile):
        os.rename('/etc/crontab', '/etc/crontab.BAK')
        log(logFile, 'crontab backed up')
        crontab_write = open('/etc/crontab', 'w')
        log(logFile, 'crontab opened for writing')
        crontab = open('/etc/crontab.BAK', 'r')
        log(logFile, 'crontab.BAK opened for reading')
        day = datetime.datetime.today().strftime('%d')
        month = datetime.datetime.today().strftime('%m')
        for tab in crontab.readlines():
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tday = tomorrow.strftime('%d')
            tmonth = tomorrow.strftime('%m')
            if '"{}" {} {}'.format(show, season[1:], episode[1:]) in tab:
                log(logFile, 'Tab found for not writing {} {} {}'.format(show, season, episode))
            else:
                crontab_write.write(tab)
        crontab_write.close()
        log(logFile, 'Crontab written')

def load(show, getseason3, getepisode3):
    logFile = open('/var/log/custom/down.log', 'a')
    log(logFile, 'Down.load() starting. Received {} {} {}'.format(show, getseason3, getepisode3))
    if not __name__ == '__main__':
        input_source = 'cmd'
#        log.write('Input source = {}'.format(input_source))
        getseason = None
        getepisode = None
        query, squery, tpe, season, episode = parse_query(show, getseason, getepisode,
                                    getseason3, getepisode3, logFile)
    elif len(sys.argv) > 2:
        input_source = 'cmd'
        getseason = None
        getepisode = None
        query, squery, tpe, season, episode = parse_query(show, getseason, getepisode,
                                    getseason3, getepisode3, logFile)
    else:
        # -*- coding: UTF-8 -*-
        import cgitb
        cgitb.enable()
        print("Content-Type: text/html")
        print()
        input_source = 'web'
        setshow = cgi.FieldStorage()
        show =  setshow.getvalue('searchbox')
        getseason = setshow.getvalue('seasonall')
        getepisode = setshow.getvalue('episodeall')
        getseason3 = setshow.getvalue('seasonsearch')
        getepisode3 = setshow.getvalue('episodesearch')
        query, squery, tpe, season, episode = parse_query(show, getseason, getepisode,
                                    getseason3, getepisode3, logFile)
    rawurl = 'https://thepirateproxy.ws'
    baseurl = 'https://thepirateproxy.ws/search/{}/0/99/0'.format(squery)
    curl = os.system('curl -4 {} -o cfile.txt 2>&1'.format(baseurl))
    if not curl == 0:
        log(logFile, 'Error receiving page source')
        print('Error revieving page source') # --------------------------------------------------------------
    else:
        url = open('cfile.txt', encoding='utf-8', errors=None).read()
        if 'No hits. Try adding an asterisk in you search phrase' in url:
            log(logFile, 'No hits :(')
            print('No hits :(')
#            cron_tweak('reshed', show, season, episode, logFile)
        else:
            log(logFile, 'Getting Links')
            getlinks(query, tpe, show, season, episode, url, input_source, logFile)
        magdic = {}
        topPoints = {}
    try:
#        print('')
        os.remove('cfile.txt')
    except: # WindowsError:
        log(logFile, 'Error deleting cfile.txt')
        print('Error deleting cfile.txt') # ---------------------------------------------------

if __name__ == '__main__':
    load(sys.argv[2], sys.argv[3], sys.argv[4])

