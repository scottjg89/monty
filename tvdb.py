#!/usr/bin/python2.7
import os,re
import tvdb_api
import datetime
#from tvbd_api import Tvdb

path = '/mnt/Public/Videos/TV Shows/'
dirs = os.listdir(path)
t = tvdb_api.Tvdb()
log = open('/var/log/custom/tvdb', 'a')
#log.write('<--------STARTING-------->')
def checkaired(show, season, episode):
    thisyear = datetime.date.today()
    search = t[show][season][episode]
    aired= search.get('firstaired')
    try:
        if int(aired[0:4]) < int(thisyear.strftime('%Y')):
            lock = 'unlocked'
        elif aired[0:4] == int(thisyear.strftime('%Y')):
            #log.write('checking Month...')
            if aired[5:7] < int(thisyear.strftime('%M')):
                lock = 'unlocked'
            elif aired[5:7] > int(thisyear.strftime('%M')):
                #log.write('Not Aired only low quality copies available! To continue DO SOMETHING ...')
                lock = 'locked'
            elif aired[5:7] == int(thisyear.strftime('%M')):
                #log.write('Checking Day...')
                if aired[8:] < int(thisyear.strftime('%D')):
                    lock = 'unlocked'
                elif aired[8:] >= int(thisyear.strftime('%D')):
                    #log.write('Not Aired only low quality copies available! To continue DO SOMETHING ...')
                    lock = 'locked'
        elif aired > int(thisyear.strftime('%Y')):
            #log.write('Not aired only low quality copies available! To continue DO SOMETHING ...')
            lock = 'locked'
        return lock
    except:
        pass
        #log.write('Fatal error!')
    
def getmissing(show, season, missingeps):
    #log.write(missingeps)
    for i in missingeps:
        lock = checkaired(show, season, i)
        #log.write('LOCK = %s')%(lock)        

def specials(show):
    for i in os.walk(path+show):
        if i == 'Specials':
            for ep in os.listdir(path+show+'/'+Specials):
                search = t[show][0].search(item)
                print(search)


'''
        for key in i:
            for item in key:
                if len(item) > 3:
                    if any(word in item for word in ['avi', 'mkv', 'mp4']):
                    #    ep = re.sub(r'|-', '', item)%(str(show))
                        search = t[show][0].search(item)
                        if len(search) > 2:
                            print(search)
                        else:
                            print('%s not found in TVDB!')%(item)
'''
'''
t[show][0].search(EPISODENAME)
for file in os.walk(path+v):
'''

def main():
    for d in dirs:
        if d.startswith('.'):
            pass
        elif d.startswith('VTS'):
            pass
        else:
            v = re.sub('\[|\]|\'', '', d)
            sname = t[v]
 #               #log.write('sname = %s v = %s')%(sname,v)
            season = re.findall(r'\d{1,2}', str(sname))
            season = re.sub('\[|\]|\'', '', str(season))
            season = int(season) - 1 # dont think it is taking away 1!!!!!!!!
            try:
                shw = re.findall(r'\d{1,2} episodes', str(t[v][int(season)]))
            except:
                pass
                #log.write('Season Error in TVBD for %s Season %s')%(d,season)
            episodes = re.sub(r'\[|\]|\'| episodes', '', str(shw))
            seasonlist = []
            seasonlist.extend(range(1, season+1))
            ##log.write(path+v)
            pathd = os.listdir(path+v)
            for d in pathd:
                specials(v)
            ##log.write('pathd = %s epidoses = %s in %s Season %s')%(len(os.listdir(path+d)),episodes,v, season)
 #            #log.write('----------------------------------------------------------------------')
#             #log.write('sname = %s v = %s season = %s episode = %s')%(sname,v,season,episodes)
#                #log.write('seasonlist = %s')%(seasonlist)
#                #log.write('pathd = %s')%(pathd)
#                #log.write('----------------------------------------------------------------------')
            for i in seasonlist:
                if os.path.exists(path+v+'/Season '+str(i)) == True:
                    seps = len(os.listdir(path+v+'/Season '+str(i)))
                else:
                    seps = 0
                epsini = re.findall(r'\d{1,2}', str(t[v][i]))
                epsini = int(re.sub(r'\[|\]|\'', '', str(epsini)))
       #        if 'Season %s'%(i) in pathd:
                    #log.write('Season '+i+' is preasant in '+v)
        #        else:
                    #log.write('Season '+i+' is missing in '+v)
        #        if seps == epsini:
                    #log.write(v+' Season '+i+' up to date')
        #        elif seps > epsini:
                    #log.write(v+' Season '+i+' may contain junk files')
        #        elif seps < epsini:
                    #log.write(v+' has '+seps+' episodes in Season '+i+' when it should have '+epsini)
                missingeps = []
                missingeps.extend(range(seps+1, epsini+1))
                getmissing(v,i,missingeps)
                specials(v)

if __name__ == '__main__':
    main()

           
'''
        if 'Season %s' % (season) in os.listdir(path+d):
          fipath = os.listdir(path+str(d)+'/'+'Season '+str(season))
          lieps = []
          lieps.extend(range(1, episodes))
#          for i in lieps:
#            if 'episode %s' % (1) in fipath:
#              #log.write('Season %s i')
          sho = t[d][season][episodes]
          aired = sho.get('firstaired')
          if aired == 0:
            #log.write ('No first air date known/set for %s') %s (d)
	  else:
	    if aired <= today:
              #log.write('Download')
	      #log.write('Show= %s Season\ %s') % (d,season)
'''
