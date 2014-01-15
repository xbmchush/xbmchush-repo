# -*- coding: utf-8 -*-

""" p2p-streams
    2014 enen92 fightnight"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess

####################################################### CONSTANTES #####################################################

versao = '0.1.1'
addon_id = 'plugin.video.p2p-streams'
MainURL = 'http://google.com'
WiziwigURL = 'http://www.wiziwig.tv'
TorrentTVURL = 'http://torrent-tv.ru/'
linkwiki = 'http://bit.ly/1j43Bbn'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
iconpequeno=addonpath + art + 'iconpq.jpg'
traducaoma= settings.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
#downloadPath = settings.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
startpath=os.path.join(pastaperfil,'acestream','ace','start.py')

### SOPCAST ###
LISTA_SOP='http://www.sopcast.com/chlist.xml'
SPSC_BINARY = "sp-sc-auth"
SPSC = os.path.join(pastaperfil,'sopcast',SPSC_BINARY)
SPSC_LOG = os.path.join(pastaperfil,'sopcast','sopcast.log')
LOCAL_PORT = settings.getSetting('local_port')
VIDEO_PORT = settings.getSetting('video_port')
BUFER_SIZE = int(settings.getSetting('buffer_size'))
if(settings.getSetting('auto_ip')):
    LOCAL_IP=xbmc.getIPAddress()
else: LOCAL_IP=settings.getSetting('localhost')

### ACESTREAM ##

aceport=62062

#################

sopcastidteste='8893'
acestreamidteste='9e4914630f4f9055ffbfb77e70714ce835c1d321'

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

def menu_principal():
      addDir(traducao(40001),MainURL,11,'',2,True)
      addDir(traducao(40002),MainURL,8,'',2,True)
      if xbmc.getCondVisibility('system.platform.linux'):
          #addDir('Lista Sopcast Oficial',MainURL,6,'',1,False)
          addDir(traducao(40003),MainURL,13,'',1,True)
          #addDir('Lista Remota',MainURL,6,'',1,False)
      
      addLink('','','')
      
      if xbmc.getCondVisibility('system.platform.windows') or xbmc.getCondVisibility('system.platform.linux'):
          #addDir('[COLOR red]Testar Acestream[/COLOR] ('+acestreamidteste+')',acestreamidteste,1,'',2,False)
          addDir(traducao(40004),MainURL,4,'',1,False)

      if xbmc.getCondVisibility('system.platform.linux'):
          #addDir('[COLOR red]Testar Sopcast[/COLOR] ('+sopcastidteste+')',sopcastidteste,2,'',2,False)
          addDir(traducao(40005),MainURL,3,'',1,False)
          addDir(traducao(40006),MainURL,5,'',1,False)

      elif xbmc.getCondVisibility('system.platform.windows'):
          addDir(traducao(40007),MainURL,7,'',1,False)

      if xbmc.getCondVisibility('System.Platform.OSX') or xbmc.getCondVisibility('System.Platform.IOS') or xbmc.getCondVisibility('System.Platform.ATV2') or xbmc.getCondVisibility('System.Platform.Android'):
          addLink(traducao(40056),'','')
          
      xbmc.executebuiltin("Container.SetViewMode(50)")

def sopcast_ucoz():
    conteudo=clean(abrir_url('http://sopcast.ucoz.com'))
    listagem=re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a></div>').findall(conteudo)
    for urllist,titulo in listagem:
        addDir(titulo,urllist,14,'',len(listagem),False)

def sopcast_ucoz_play(name,url):
    conteudo=clean(abrir_url(url))
    try:
        sopcast=re.compile('sop://(.+?)<').findall(conteudo)[0]
        sopstreams(name,'','sop://' + sop)
    except:
        mensagemok(traducao(40000),traducao(40008))

def torrenttv():
    conteudo=clean(abrir_url('http://torrent-tv.ru/channels.php'))
    cat=re.compile('<li style="height:.+?<a href=".+?" class="simple-link".+?>(.+?)</a>(.+?)</ul>').findall(conteudo)
    for nomecat,chcat in cat:
        addLink('[B][COLOR blue]' + nomecat + '[/COLOR][/B]','','')
        channels=re.compile('<a href="(.+?)">(.+?)</a>').findall(chcat)
        for churl,chname in channels:
            addDir(chname,churl,12,'',len(channels),False)
        addLink('','','')
        pass

def torrenttv_play(url):
    conteudo=clean(abrir_url(TorrentTVURL + url))
    try:torrent=re.compile('this.loadTorrent.+?"(.+?)",').findall(conteudo)[0]
    except:torrent=re.compile('this.loadPlayer.+?"(.+?)",').findall(conteudo)[0]
    try:
        name=re.compile('<div class="channel-name">(.+?)</div>').findall(conteudo)[0]
        name=name.replace('&mdash; ','')
    except:name=traducao(40008)
    acestreams(name,'',torrent)

def wiziwig_cats():
    addDir(traducao(40009),WiziwigURL + '/index.php?part=sports',9,'',1,True)
    addDir(traducao(40010),WiziwigURL + '/competition.php?part=sports&discipline=americanfootball&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/americanfootball.gif',1,True)
    addDir(traducao(40011),WiziwigURL + '/competition.php?part=sports&discipline=football&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/football.gif',1,True)
    addDir(traducao(40012),WiziwigURL + '/competition.php?part=sports&discipline=basketball&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/basketball.gif',1,True)
    addDir(traducao(40013),WiziwigURL + '/competition.php?part=sports&discipline=icehockey&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/icehockey.gif',1,True)
    addDir(traducao(40014),WiziwigURL + '/competition.php?part=sports&discipline=baseball&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/baseball.gif',1,True)
    addDir(traducao(40015),WiziwigURL + '/competition.php?part=sports&discipline=tennis&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/tennis.gif',1,True)
    addDir(traducao(40016),WiziwigURL + '/competition.php?part=sports&discipline=motorsports&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/motorsports.gif',1,True)
    addDir(traducao(40017),WiziwigURL + '/competition.php?part=sports&discipline=rugby&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/rugby.gif',1,True)
    addDir(traducao(40018),WiziwigURL + '/competition.php?part=sports&discipline=golf&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/golf.gif',1,True)
    addDir(traducao(40019),WiziwigURL + '/competition.php?part=sports&discipline=cricket&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/cricket.gif',1,True)
    addDir(traducao(40020),WiziwigURL + '/competition.php?part=sports&discipline=cycling&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/cycling.gif',1,True)
    addDir(traducao(40021),WiziwigURL + '/competition.php?part=sports&discipline=other&archive=no&allowedDays=1,2,3,4,5,6,7',9,WiziwigURL + '/gfx/disciplines/other.gif',1,True)
    xbmc.executebuiltin("Container.SetViewMode(50)")

def wiziwig_events(url):
    conteudo=clean(abrir_url(url))
    eventos=re.compile('<div class="date" [^>]+>([^<]+)</div>\s*<span class="time" rel=[^>]+>([^<]+)</span> -\s*<span class="time" rel=[^>]+>([^<]+)</span>\s*</td>\s*<td class="home".+?<img[^>]* src="([^"]*)"[^>]*>([^<]+)<img [^>]+></td>.*?<td class="broadcast"><a class="broadcast" href="([^"]+)">Live</a></td>').findall(conteudo)
    for date,time1,time2,icon,team1,url in eventos:
        datefinal=date.split(', ')
        addDir('[B](' + datefinal[1] + ' ' + time1 + ')[/B] ' + team1 + ' - Falta',WiziwigURL + url,10,WiziwigURL + icon,len(eventos),False)
    xbmc.executebuiltin("Container.SetViewMode(51)")        
    
def wiziwig_servers(url):
    conteudo=clean(abrir_url(url))
    if re.search('Sorry, streams will only appear',conteudo):
        try:nrestacoes='[B]' + re.compile('</h2><p>There.+?<strong>(.+?) ').findall(conteudo)[0] + ' estações[/B] vão transmitir o jogo.'
        except:nrestacoes=''
        mensagemok(traducao(40000),'Os links para o jogo são vão aparecer','uma 1hora antes do jogo começar.',nrestacoes)
        return
    ender=[]
    titulo=[]
    streams=re.compile('.*?<tr class="streamrow[^"]*">\s*<td>\s*([^\s]+)\s*</td>\s*<td>\s*<a class="broadcast go" href="((?!adserver|http://torrent-tv.ru|forum|www\.bet365|BWIN)[^"]+)" target="_blank">Play now!</a>\s*<a[^>]*>[^>]*</a>\s*</td>\s*<td>([^<]+)</td>').findall(conteudo)
    for nome,chid,quality in streams:
        if re.search('Sopcast',nome,re.IGNORECASE) or re.search('Acestream',nome,re.IGNORECASE) or re.search('TorrentStream',nome,re.IGNORECASE):
            titulo.append(nome + ' ('+quality+')')
            ender.append(chid)
    if len(ender)==0:mensagemok(traducao(40000),traducao(40022))
    else:
        index = xbmcgui.Dialog().select(traducao(40023), titulo)
        if index > -1:
            nomeescolha=titulo[index]
            linkescolha=ender[index]
            if re.search('acestream',nomeescolha,re.IGNORECASE) or re.search('TorrentStream',nomeescolha,re.IGNORECASE): acestreams(nomeescolha,'',linkescolha)
            #elif re.search('Streamtorrent',nomeescolha,re.IGNORECASE):
            elif re.search('sopcast',nomeescolha,re.IGNORECASE):
                if xbmc.getCondVisibility('system.platform.windows'):sopserver()
                else:sopstreams(nomeescolha,'',linkescolha)
            else: mensagemok(traducao(40000),traducao(40024))


def lista_sop():
    link=abrir_url(LISTA_SOP)
    canaisgrupos=re.compile('<group.+?en="(.+?)".+?>(.+?)</group>').findall(link)
    for groupname,groupchannels in canaisgrupos:
        addLink('[COLOR blue][B]' + groupname + '[/B][/COLOR]','','')
        allchannels=re.compile('<channel.+?>(.+?)</channel>').findall(groupchannels)
        for canais in allchannels:
            addDir('yoyo','gg',2,'',2,False)
        addLink('','','')
            
def autoconf():
    import tarfile
    sopcast_raspberry = "http://p2p-strm.googlecode.com/svn/trunk/sopcast-raspberry.tar.gz"
    sopcast_linux_generico =  "http://p2p-strm.googlecode.com/svn/trunk/sp-aut.tar.gz"
    try:
        if os.uname()[1] == "OpenELEC": acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/openelec-for-userdata.tar.gz"
        elif os.uname()[1] == "raspbmc": acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/raspbmc-for-userdata.tar.gz"
        elif os.uname()[1] == "xbian": acestream_rpi = "http://p2p-strm.googlecode.com/svn/trunk/xbian-userdata.tar.gz"
        else: acestream_rpi = ""
    except: acestream_rpi = "" #da erro de script no windows, workaround porque diferente rpi
    acestream_windows = "http://p2p-strm.googlecode.com/svn/trunk/windows-package.tar.gz"
    
    if xbmc.getCondVisibility('system.platform.linux'):
        print "Detected OS: Linux"
        
        #arq = "armv6l"
        if os.uname()[4] == "armv6l":
            print "Detected Platform Raspberry PI"
            #Sop

            SPSC_KIT = os.path.join(addonpath,sopcast_raspberry.split("/")[-1])
            download_tools().Downloader(sopcast_raspberry,SPSC_KIT,traducao(40025),traducao(40000))
            
            if tarfile.is_tarfile(SPSC_KIT):
                path_libraries = os.path.join(pastaperfil,"sopcast")
                download_tools().extract(SPSC_KIT,path_libraries)
                xbmc.sleep(500)
                download_tools().remove(SPSC_KIT)

            #Ace
            SPSC_KIT = os.path.join(addonpath,acestream_rpi.split("/")[-1])
            download_tools().Downloader(acestream_rpi,SPSC_KIT,traducao(40026),traducao(40000))
        
            if tarfile.is_tarfile(SPSC_KIT):
                path_libraries = os.path.join(pastaperfil,"acestream")
                download_tools().extract(SPSC_KIT,path_libraries)
                xbmc.sleep(500)
                download_tools().remove(SPSC_KIT)

            settings.setSetting('autoconfig',value='false')
                
        else:
            print "Detected Other Linux Plataform"
            #Sop
            if os.path.isfile("/usr/lib/libstdc++.so.5") and os.path.isfile("/usr/lib/libstdc++.so.5.0.1"):
                print "Sopcast configuration: Linux has sop libs already"
            else: 
                mensagemok(traducao(40000),traducao(40027),traducao(40028) + linkwiki,traducao(40029))
                sys.exit(0)
            SPSC_KIT = os.path.join(addonpath,sopcast_linux_generico.split("/")[-1])
            download_tools().Downloader(sopcast_linux_generico,SPSC_KIT,traducao(40030),traducao(40000))
            import tarfile
            if tarfile.is_tarfile(SPSC_KIT):
            	path_libraries = os.path.join(pastaperfil,"sopcast")
            	download_tools().extract(SPSC_KIT,path_libraries)
            	xbmc.sleep(500)
            	download_tools().remove(SPSC_KIT)
	    #Ace
            import subprocess
            proc_response = []
            proc = subprocess.Popen(['whereis','acestreamengine'],stdout=subprocess.PIPE)
            for line in proc.stdout:
                print "Output of acestream subprocess check",line.rstrip()
                proc_response.append(line.rstrip())
            if "acestreamengine: /" in str(proc_response):
                print "Acestream engine is already installed"
                try:
                    proc.kill()
                    proc.wait()
                except:pass
            else:
                mensagemok(traducao(40031),traducao(40027),traducao(40028) + linkwiki,traducao(40029))
                sys.exit(0)
            settings.setSetting('autoconfig',value='false')


    elif xbmc.getCondVisibility('system.platform.windows'):
        print "Detected OS: Windows"
        #Sop not available in windows
        #Ace
        SPSC_KIT = os.path.join(addonpath,acestream_windows.split("/")[-1])
        download_tools().Downloader(acestream_windows,SPSC_KIT,traducao(40026),traducao(40000))
        import tarfile
        if tarfile.is_tarfile(SPSC_KIT):
            path_libraries = os.path.join(pastaperfil,"acestream")
            download_tools().extract(SPSC_KIT,path_libraries)
            download_tools().remove(SPSC_KIT)
        settings.setSetting('autoconfig',value='false')

def irparaid(yeee):
	if yeee=='ace':
		keyb = xbmc.Keyboard('', traducao(40033))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				acestreams(traducao(40035),'',str(channel_id))
	elif yeee=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, traducao(40033))
		sopstreams(traducao(40035),'',str(channel_id))
	elif yeee=='sop_url':
		keyb = xbmc.Keyboard('sop://', traducao(40034) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sopstreams(traducao(40036),'',str(channel_id))

def acestreams(name,thumb,chid):
    try:from acecore import TSengine as tsengine
    except:
        mensagemok(traducao(40000),traducao(40037))
        return
    xbmc.executebuiltin('Action(Stop)')
    if chid != '':
        chid=chid.replace('acestream://','').replace('ts://','').replace('st://','')
        print "Starting Player Ace hash: " + chid
        TSPlayer = tsengine()
        out = None
        if chid.find('http://') == -1:
            out = TSPlayer.load_torrent(chid,'PID',port=aceport)
        else:
            out = TSPlayer.load_torrent(chid,'TORRENT',port=aceport)
        if out == 'Ok':
            TSPlayer.play_url_ind(0,name + ' (' + chid + ')','','')#0,id,iconaddon,iconcanal
            TSPlayer.end()
            return
        else:    
            mensagemok(traducao(40000),traducao(40038))
            TSPlayer.end()
            return
    else:
        mensagemprogresso.close()
        
#PODES USAR ESTA FUNCAO PARA VER O OUTPUT DE UM CMD
#def rp():
#	command = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),"sop://124.232.150.188:3912/9761","1234","9001"]
#	for line in run_command(command):
#		print(line)    

def sopstreams(name,iconimage,sop):
    try:
        os.system("killall -9 "+SPSC_BINARY)
        if "sop://" not in sop: sop = "sop://broker.sopcast.com:3912/" + sop
        else: pass
        print "Starting Player Sop URL: " + str(sop)
        global spsc
        if os.uname()[4] == "armv6l":
            if settings.getSetting('sop_debug_mode') == "false":
                cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,"1234","9001"]
            else: 
              	cmd = [os.path.join(pastaperfil,'sopcast','qemu-i386'),os.path.join(pastaperfil,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(pastaperfil,'sopcast',"lib"),os.path.join(pastaperfil,'sopcast','sp-sc-auth'),sop,"1234","9001",">",SPSC_LOG]
        else: 
            if settings.getSetting('sop_debug_mode') == "false":
                cmd = [SPSC, sop, str(LOCAL_PORT), str(VIDEO_PORT)]
            else:
                cmd = [SPSC, sop, str(LOCAL_PORT), str(VIDEO_PORT),">",SPSC_LOG]
        print SPSC
        print sop
        print cmd
        spsc = subprocess.Popen(cmd, shell=False, bufsize=BUFER_SIZE,stdin=None, stdout=None, stderr=None)
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
        listitem.setLabel(name)
        listitem.setInfo('video', {'Title': name})

        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(int(settings.getSetting('wait_time')))
        res=False
        counter=50
        ret = mensagemprogresso.create(traducao(40000),traducao(40039))
        mensagemprogresso.update(0)
        while counter > 0 and os.path.exists("/proc/"+str(spsc.pid)):
            xbmc.sleep(400)
            counter -= 1
            try:
                urllib2.urlopen(url)
                counter=0
                res=sop_sleep(200 , spsc.pid)
                break
            except:pass
                    
        if res:
            player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=spsc.pid , listitem=listitem)
            player.play(url, listitem)
            while player._playbackLock:
                xbmc.sleep(500)
        else: xbmc.executebuiltin("Notification(%s,%s,%i)" % (traducao(40000), traducao(40040), 1))
    except: pass
    try: os.kill(self.spsc_pid,9)
    except: pass
    xbmc.sleep(100)
    try:os.system("killall -9 "+SPSC_BINARY)
    except:pass
    xbmc.sleep(100)
    try:spsc.kill()
    except:pass
    xbmc.sleep(100)
    try:spsc.wait()
    except:pass
    xbmc.sleep(100)           
    try: os.kill(spsc.pid,9)
    except: pass
    mensagemprogresso.close()
    print "Player chegou mesmo ao fim"


def sop_sleep(time , spsc_pid):
    counter=0
    increment=200
    path="/proc/%s" % str(spsc_pid)
    try:
      while counter < time and spsc_pid>0 and not xbmc.abortRequested and os.path.exists(path):
        counter += increment
        xbmc.sleep(increment)
    except: return True
        
    if counter < time: return False
    else: return True

def checker():
	import socket
	sock = socket.socket(socket.AF_INET, socket.int(VIDEO_PORT))
	result = sock.connect_ex(('127.0.0.1',9000))
	if result == 0:
   		return True
	else:
   		return False	

def sopserver():
    opcao= xbmcgui.Dialog().yesno(traducao(40000), traducao(40041), linkwiki, traducao(40042))
    if opcao: comecarvideo(name,'')

class streamplayer(xbmc.Player):
    def __init__( self , *args, **kwargs):
        self.spsc_pid=kwargs.get('spsc_pid')
        self.listitem=kwargs.get('listitem')
        self._playbackLock = True

    def onPlayBackStarted(self):
        mensagemprogresso.close()
        if xbmc.Player(xbmc.PLAYER_CORE_AUTO).getPlayingFile() != "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/":
            try: os.kill(self.spsc_pid,9)
            except: pass
        else: autostart(self.listitem.getLabel())

    def onPlayBackEnded(self):
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying():
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)     
        #else: 
            #try:
            
            #except: pass

    def onPlayBackStopped(self):
        self._playbackLock = False
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying(): 
                player = streamplayer(xbmc.PLAYER_CORE_AUTO , spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)
        else:
            try: os.kill(self.spsc_pid,9)
            except: pass

########################################################### PLAYER ################################################

def comecarvideo(titulo,thumb):
      playlist = xbmc.PlayList(1)
      playlist.clear()
      listitem = xbmcgui.ListItem(titulo, iconImage="DefaultVideo.png", thumbnailImage=thumb)            
      listitem.setInfo("Video", {"Title":titulo})
      listitem.setProperty('mimetype', 'video/x-msvideo')
      listitem.setProperty('IsPlayable', 'true')
      dialogWait = xbmcgui.DialogProgress()
      dialogWait.create(traducao(40000), traducao(40043))
      playlist.add('http://127.0.0.1:8902/tv.asf', listitem)
      dialogWait.close()
      del dialogWait
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)           

######################################################## OUTRAS FUNCOES ###############################################

def savefile(filename, contents):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou o marcador de: %s" % filename

def openfile(filename):
    try:
        destination = os.path.join(pastaperfil, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu o marcador de: %s" % filename
        return None

def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&#039;':'','&#39;':"'",'&#227;':'ã','&170;':'ª','&#233;':'é','&#231;':'ç','&#243;':'ó','&#226;':'â','&ntilde;':'ñ','&#225;':'á','&#237;':'í','&#245;':'õ','&#201;':'É','&#250;':'ú','&amp;':'&','&#193;':'Á','&#195;':'Ã','&#202;':'Ê','&#199;':'Ç','&#211;':'Ó','&#213;':'Õ','&#212;':'Ó','&#218;':'Ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

class download_tools():
	def Downloader(self,url,dest,description,heading):
		dp = xbmcgui.DialogProgress()
		dp.create(heading,description,'')
		dp.update(0)
		urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: self._pbhook(nb,bs,fs,dp))
		
	def _pbhook(self,numblocks, blocksize, filesize,dp=None):
		try:
			percent = int((int(numblocks)*int(blocksize)*100)/int(filesize))
			dp.update(percent)
		except:
			percent = 100
			dp.update(percent)
		if dp.iscanceled(): 
			dp.close()
	
	def extract(self,file_tar,destination):
		import tarfile
		dp = xbmcgui.DialogProgress()
		dp.create(traducao(40000),traducao(40044))
		tar = tarfile.open(file_tar)
		tar.extractall(destination)
		dp.update(100)
		tar.close()
		dp.close()
		
	def remove(self,file_):
		dp = xbmcgui.DialogProgress()
		dp.create(traducao(40000),traducao(40045))
		os.remove(file_)
		dp.update(100)
		dp.close()


params=get_params()
url=None
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
      print "Versao Instalada: v" + versao
      if settings.getSetting('autoconfig') == "true": autoconf()
      menu_principal()

#plugin.video.p2p-streams/?url=idstream&mode=1or2&name=nameofstream
elif mode==1: acestreams(name,'',url)
elif mode==2: sopstreams(name,'',url)
elif mode==3: irparaid('sop_id')
elif mode==4: irparaid('ace')
elif mode==5: irparaid('sop_url')
elif mode==6: lista_sop()
elif mode==7: sopserver()
elif mode==8: wiziwig_cats()
elif mode==9: wiziwig_events(url)
elif mode==10: wiziwig_servers(url)
elif mode==11: torrenttv()
elif mode==12: torrenttv_play(url)
elif mode==13: sopcast_ucoz()
elif mode==14: sopcast_ucoz_play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
