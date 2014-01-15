#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib,urllib,urllib2,re,sys,os,socket,threading,time,random,json,subprocess,xbmcgui,xbmc,xbmcaddon

_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Addon = xbmcaddon.Addon(id='plugin.video.p2p-streams')
addonpath = Addon.getAddonInfo('path').decode('utf-8')
pastaperfil = xbmc.translatePath(Addon.getAddonInfo('profile')).decode('utf-8')
traducaoma= Addon.getLocalizedString
language = Addon.getLocalizedString
server_ip=Addon.getSetting('ip_addr')
prt_file=Addon.getSetting('port_path')
if Addon.getSetting('pausable')=='true': pausable=True
else: pausable=False
if Addon.getSetting('autoexit')=='true': autoexit=True
else: autoexit=False
if Addon.getSetting('autobuf')=='true': autobuf=True
else: autobuf=False
if Addon.getSetting('save')=='true': save=True
else: save=False
#if save and not Addon.getSetting('folder'): Addon.openSettings()
pkey='n51LvQoTlJzNGaFxseRK-uvnvX-sD4Vm5Axwmc4UcoD-jruxmKsuJaH0eVgE'
lock_file = xbmc.translatePath('special://temp/'+ 'ts.lock')
err_file = xbmc.translatePath('special://temp/'+ 'err.avi')
if (sys.platform == 'win32') or (sys.platform == 'win64'):
    lock_file = lock_file.decode('utf-8')
    err_file = err_file.decode('utf-8')
aceport=62062

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

class TSengine():
    
    def __init__(self):
        self.files=None
        xbmc.Player().stop()
        if xbmc.Player().isPlaying():
            xbmc.sleep(300)
        while os.path.exists(lock_file):
            print Addon.getSetting('stopped')
            print 'wait to stop old ts'
            try: print 'go=%s'%go
            except: print 'no go'
            time.sleep(1.3)
        self.dvijitel=ASengine()
        f = file(lock_file, "w")
        f.close()
        self.error=None
        if os.path.exists(err_file): os.remove(err_file)
    def load_torrent(self, torrent, mode, host=server_ip, port=aceport ):
        result=self.dvijitel.load_torrent(torrent, mode, host, port)
        if not result: self.error=True
        self.files=self.dvijitel.files
        return result
    def play_url_ind(self, index=0, title='', icon='', thumb=''):
        if not self.error:
            result=self.dvijitel.play_url_ind(index, title, icon, thumb)
            return result
        return result
    def end(self):
        result=self.dvijitel.end()
        return result

class ASengine(xbmc.Player):
    
    def __init__(self):
        

        
        self.progress = xbmcgui.DialogProgress()
        self.progress.create(traducao(40000), traducao(40046))

        self.filename=None
        self.ind=None
        self.files=None
        self.mode=self.url=''
        self.active=True
        self.r=None
        self.link=None
        self.paused=False

        self.isStream=False
        
        self.host=None
        self.port=None
        self.mode=None
        self.url=None
        
        self.err=None
        self.active=True
        self.activeplay=False

    def start_win_engine(self):
        try:
            needed_value=os.path.join(pastaperfil,'acestream','ace_engine.exe')
            try: 
                os.startfile(needed_value)
            except: 
                self.progress.close()
                self.err=1
                return None
            self.progress.update(0,traducao(40000),traducao(40047),'')
            return 1
        except:
            self.progress.close()
            self.err=1
            return None
        self.progress.close()
        self.err=1
        return None

    def start_lin_engine(self):
    	if os.uname()[4] != "armv6l":
    
        	needed_value=['acestreamengine','--client-console']
                    
        	import subprocess
        	st = None
        	try: self.engine_linux =subprocess.Popen(needed_value)
        	except: 
            		try: 
                		self.engine_linux =subprocess.Popen(Addon.getSetting('prog'))
            		except: 
                		print 'TSEngine not Installed'
                		return None
               	return 1
    	else:
    		needed_value=['python',os.path.join(pastaperfil,'acestream','ace','start.py')]	
		import subprocess
		st = None
		try: self.engine_linux =subprocess.Popen(needed_value)
		except:
			print "Problem loading python TS Engine"
			return None
		return 1
     
            
    def _TSpush(self,command):
        #print ">>%s"%command
        try:
            _sock.send(command+'\r\n')
        except: 
            print 'send error'

    def conn(self,aceport):
        self.r = _ASpull(1)
        self.r.start()
        comm="HELLOBG"# version=3"
        self._TSpush(comm)

        while not self.r.version and not self.progress.iscanceled():
            time.sleep(0.3)
        ready='READY'
        if self.r.key:
            print "key is %s"%self.r.key
            import hashlib
            sha1 = hashlib.sha1()
            
            sha1.update(self.r.key+pkey)
            key=sha1.hexdigest()
            pk=pkey.split('-')[0]
            key="%s-%s"%(pk,key)
            ready='READY key=%s'% key
        if self.progress.iscanceled():
            self.err=1
            self.progress.close()
            return False	
        self._TSpush(ready)
        Addon.setSetting('aceport',str(aceport))
        return True
    
    def get_new_port(self):
        if (sys.platform == 'win32') or (sys.platform == 'win64'):
            try:
                path=os.path.join(pastaperfil,'acestream')
                pfile= os.path.join( path,'acestream.port')
                gf = open(pfile, 'r')
                aceport=int(gf.read())
            except: return None
            return aceport
        return 62062
    
    def ts_init(self):

        self.progress.update(0,traducao(40048),'',"")

        if Addon.getSetting('ip_addr'):
            server_ip=str(Addon.getSetting('ip_addr'))
        else: server_ip='127.0.0.1'
        
        #Get port
        try:
            aceport=int(Addon.getSetting('aceport'))
        except: aceport=62062
        
        #try to connect
        try:
            _sock.connect((server_ip, aceport))
            self.conn(aceport)

        except:
            self.progress.update(0,traducao(40046),'',"")
            if (sys.platform == 'win32') or (sys.platform == 'win64'):
                result=self.start_win_engine()
            else:
                result=self.start_lin_engine()
            if result:
                n=1
                started=None
                while not self.progress.iscanceled() and n!=0:
                    self.progress.update(0,traducao(40046),"%s %s %s"%(traducao(40049),n,traducao(40050)),"")
                    aceport=self.get_new_port()
                    if aceport:
                        try:
                            _sock.connect((server_ip, aceport))
                            started=1
                            print 'Started'
                            n=-1
                        except:
                            started=None
                    time.sleep(1)
                    n=n+1
                    
                if self.progress.iscanceled():
                    self.err=1
                    self.progress.close()
                if started:
                    self.conn(aceport)
            else:
                self.err=1
                print 'not installed'
    
    def load_torrent(self, torrent, mode, host=server_ip, port=aceport ):
        self.host=host
        self.port=port
        self.mode=mode
        self.url=torrent
        self.ts_init()
        if not self.err:
            self.progress.update( 0, traducao(40051),traducao(40052), "" )
            
            if mode!='PID': spons=' 0 0 0'
            else: spons=''
            comm='LOADASYNC '+ str(random.randint(0, 0x7fffffff)) +' '+mode+' ' + torrent + spons
            self._TSpush(comm)
            
            while not self.r.files and not self.progress.iscanceled():
                time.sleep(0.2)
            if self.progress.iscanceled(): 
                self.err=1
                self.progress.close()
                return False
            self.filelist=self.r.files
            self.file_count = self.r.count
            self.files={}
            self.progress.update(89,traducao(40043),'')
            if self.file_count>1:
                flist=json.loads(self.filelist)
                for list in flist['files']:
                    self.files[urllib.unquote_plus(urllib.quote(list[0]))]=list[1]
            elif self.file_count==1:
                flist=json.loads(self.filelist)
                list=flist['files'][0]
                self.files[urllib.unquote_plus(urllib.quote(list[0]))]=list[1]

            self.progress.update(100,traducao(40053))
            return 'Ok'
            
    def play_url_ind(self, index=0, title='', icon='', thumb=''):
        self.ind=index
        self.r.ind=index
        for k,v in self.files.iteritems():
            if v==self.ind: self.filename=k
        try: self.filename=Addon.getSetting('folder')+self.filename
        except: self.filename=err_file
        self.filename=err_file
        try: result=os.path.exists(self.filename)
        except: result=False
        if save and self.r.event:
            try: self.progress.updater(0,traducao(40054),k)
            except: self.progress.updater(0,traducao(40054),"")
            time=0
            comm='SAVE %s path=%s'%(self.r.event[0]+' '+self.r.event[1],urllib.quote(self.filename))
            self._TSpush(comm)
            self.r.event=None
            while not os.path.exists(self.filename):
                print 'fcnk loop'
                xbmc.sleep(300)
            #xbmc.sleep(1000)
            print 'ready to play %s'%self.filename
            i = xbmcgui.ListItem(title)
            print self.filename
            i.setProperty('StartOffset', str(time))
            self.play(self.filename,i)
            self.progress.close()
        else:
            if not self.err:
                self.progress.update( 0, traducao(40055),traducao(40052), "" )
                spons=''
                if self.mode!='PID': spons=' 0 0 0'
                comm='START '+self.mode+ ' ' + self.url + ' '+ str(index) + spons
                self._TSpush(comm)
                local=False
                
                while not self.r.got_url and not self.progress.iscanceled() and not self.r.err and not local:
                    
                    if self.r.last_com=='STATUS':
                        try:
                            if self.r.state: self.progress.update(self.r.progress,self.r.state,self.r.label,'')
                        except: pass
                        xbmc.sleep(1000)
                    if save and self.r.event:
                        try: self.progress.update(0,traducao(40054),k)
                        except: self.progress.update(0,traducao(40054),"")
                        time=0
                        comm='SAVE %s path=%s'%(self.r.event[0]+' '+self.r.event[1],urllib.quote(self.filename))
                        self._TSpush(comm)
                        self.r.event=None
                        while not os.path.exists(self.filename):
                            print 'fcnk loop'
                            xbmc.sleep(300)
                        #xbmc.sleep(1000)
                        print 'ready to play %s'%self.filename
                        i = xbmcgui.ListItem(title)
                        print self.filename
                        i.setProperty('StartOffset', str(time))
                        self.play(self.filename,i)
                        self.progress.close()
                        local=True
                if self.progress.iscanceled() or self.r.err: 
                    self.err=1
                    self.progress.close()
                    return False
                elif not local:
                    self.link=self.r.got_url
                    self.progress.close()
                    self.title=title
                    lit= xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage =thumb)
                    self.play(self.r.got_url,lit)
                    self.r.got_url=None
                    self.loop()
                    return 'Ok'      

    def loop(self):
        print 'start loop'

        visible=False
        pos=[0,25,50,75,100]
        while self.active or self.r.ad:
            
            if self.r.event and save:
                
                comm='SAVE %s path=%s'%(self.r.event[0]+' '+self.r.event[1],urllib.quote(self.filename))
                self._TSpush(comm)
                self.r.event=None
                while not os.path.exists(self.filename):
                    print 'fcnk loop'
                    xbmc.sleep(300)
                xbmc.sleep(1000)
                print 'ready to play %s'%self.filename
                try: time=self.getTime()
                except: time=0
                
                i = xbmcgui.ListItem(self.title)
                i.setProperty('StartOffset', str(time))
                self.play(self.filename,i)
                self.active=False
                self.r.ad=False
               
            if self.r.ad and not self.active:
                self.progress.create(0,traducao(40048),'','')
                while not self.r.got_url and not self.progress.iscanceled() and not self.r.err:
                    
                    if self.r.last_com=='STATUS':
                        try:
                            if self.r.state: self.progress.updater(self.r.progress,self.r.state,self.r.label)
                        except: pass
                        xbmc.sleep(1000)
                if self.progress.iscanceled() or self.r.err: 
                    self.progress.close()
                    break
                self.progress.close()
                lit= xbmcgui.ListItem(self.title)
                self.play(self.r.got_url,lit)
                self.r.got_url=None
                self.active=True
                pos=[0,25,50,75,100]
            if self.isPlaying() and not self.isStream:
                if self.getTotalTime()>0: cpos= int((1-(self.getTotalTime()-self.getTime())/self.getTotalTime())*100)
                else: cpos=0
                if cpos in pos: 
                    #print cpos
                    pos.remove(cpos)
                    comm='PLAYBACK '+self.link.replace('\r','').replace('\n','')+' %s'%cpos
                    self._TSpush(comm)
            if pausable:
                if self.r.pause==1 and not self.paused:
                    self.pause()
                    self.r.pause=None
                    xbmc.sleep(1000)
                if self.r.pause==0 and self.paused:
                    self.pause()
                    self.r.pause=None
        
            xbmc.sleep(1000)
        print 'end loop'
    def end(self):
        print 'ts finally ending'
        try: self.progress.close()
        except: pass
        if not self.err:
            comm="SHUTDOWN"
            self._TSpush(comm)
        if self.r:
            self.r.active=False
            self.r.join(500)
            #self.r=None
        print 'ts shuted up'
        
        if os.path.exists(lock_file): os.remove(lock_file)
        #if self.activeplay and autoexit:
        if xbmc.getCondVisibility('system.platform.windows'):
            if Addon.getSetting('shutdown-engine') == "true":
            	print 'vai matar o processo'
            	subprocess.Popen('taskkill /F /IM ace_engine.exe /T',shell=True)
            else: pass
        elif xbmc.getCondVisibility('system.platform.linux'):
            if Addon.getSetting('shutdown-engine') == "true":
            	try:
            		self.engine_linux.kill()
            		self.engine_linux.wait()
            	except: pass
            else: pass

    def shut(self):
        pass

    def onPlayBackStarted( self ):
        try: self.duration= int(xbmc.Player().getTotalTime()*1000)
        except: self.duration=0
        comm='DUR '+self.link.replace('\r','').replace('\n','')+' '+str(self.duration)
        self._TSpush(comm)
        comm='PLAYBACK '+self.link.replace('\r','').replace('\n','')+' 0'
        self._TSpush(comm)
        self.activeplay=True
    def onPlayBackResumed( self ):
        #comm='EVENT play'
        #self._TSpush(comm)
        self.paused = False
    def onPlayBackEnded( self ):
        #comm='EVENT stop'
        #self._TSpush(comm)
        comm='PLAYBACK '+self.link.replace('\r','').replace('\n','')+' 100'
        self._TSpush(comm)
        self.active = False
        #if not self.r.ad:
        self.end()
    def onPlayBackStopped( self ):
        #comm='EVENT stop'
        #self._TSpush(comm)
        self.active = False
        self.r.ad = False
        self.end()
    def onPlayBackPaused( self ):
        #comm='EVENT pause'
        #self._TSpush(comm)
        self.paused=True
    def onPlayBackSeek(self, time, seekOffset):
        #comm='EVENT seek position=%s'%(int(time/1000))
        #self._TSpush(comm)    
        pass
    def __del__(self):
        pass
        
class _ASpull(threading.Thread):

    def _com_received(self,text):

        comm=text.split(' ')[0]
        self.label=' '
        try:
            if comm=="STATUS":
                ss=re.compile('main:[a-z]+',re.S)
                s1=re.findall(ss, text)[0]
                st=s1.split(':')[1]
                if st=='starting':
                    self.state='Starting...'
                    self.progress=0
                if st=='loading':
                    self.state='Loading...'
                    self.progress=0
                if st=='prebuf': 
                    self.state=language(1100)
                    self.progress=int(text.split(';')[1])+0.1
                    self.label=language(1150)%(text.split(';')[8],text.split(';')[5])
                    self.speed=int(text.split(';')[5])
                if st=='buf': 
                    self.state=language(1101)
                    self.progress=int(text.split(';')[1])+0.1
                    self.label=language(1150)%(text.split(';')[8],text.split(';')[5])
                if st=='dl': 
                    self.state=language(1102)
                    self.progress=int(text.split(';')[1])+0.1
                    self.label=language(1150)%(text.split(';')[6],text.split(';')[3])
                if st=='check': 
                    self.state=language(1103)
                    self.progress=int(text.split(';')[1])
                    self.speed=1
                if st=='idle': 
                    self.state=language(1104)
                    self.progress=0
                if st=='wait': 
                    self.state=language(1105)
                    self.label=language(1151)%(text.split(';')[1])
                    self.progress=0
                if st=='err': 
                    self.err=1
                    #print 'error'
        except: 
            print 'error with text=%s'%text
        return comm

    def __init__(self,interval):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval	
        self.active = True		
        self.lastresolt=None		
        self.received = []		
        self.last_received=None		
        self.last_com=None		
        self.got_url=None		
        self.files=None			
        self.buffer=5000000		
        self.count=None
        self.state=''
        self.status=None
        self.label=''
        self.progress=0
        self.filestemp=None
        self.speed=0
        self.pause=None
        self.version=None
        self.ad=False
        self.err=None
        self.event=None
        self.events=[]
        self.ind=None
        self.key=None
        #self.params=[]
        self.temp=''

    def run(self):
        while self.active and not self.err:
            try:
                self.last_received=_sock.recv(self.buffer)
            except: self.last_received=''
            #print self.last_received
            ind=self.last_received.find('\r\n')
            cnt=self.last_received.count('\r\n')

            if ind!=-1 and cnt==1:
                self.last_received=self.temp+self.last_received[:ind]
                self.temp=''
                #print self.last_received
                self.exec_com()
            elif cnt>1:
                fcom=self.last_received
                ind=1
                while ind!=-1:
                    ind=fcom.find('\r\n')
                    self.last_received=fcom[:ind]
                    #print self.last_received
                    self.exec_com()
                    fcom=fcom[(ind+2):]
            elif ind==-1: 
                self.temp=self.temp+self.last_received
                self.last_received=None
            
    
            #xbmc.sleep(500)
        if self.err: print 'need to shut down'
            
    def exec_com(self):
        #print "<<%s"%(self.last_received)
        self.last_com = self._com_received(self.last_received)
        
        if self.last_com=='START' or self.last_com=='PLAY': 
            self.got_url=self.last_received.split(' ')[1].replace('127.0.0.1',server_ip) # если пришло PLAY URL, то забираем себе ссылку
            self.params=self.last_received.split(' ')[2:]
            if len(self.params)>0:
                if 'ad=1' in self.params: 
                    self.ad=True
                    comm='PLAYBACK '+self.got_url.replace('\r','').replace('\n','')+' 100'
                    
                    _sock.send(comm+'\r\n')
                    self.got_url=None
                else: self.ad=False
                if 'stream=1' in self.params: print 'Is Stream'
                #self.ad=True
            #self.params.append('ad=1')
            #self.ad=self.last_received.split(' ')[2]

        elif self.last_com=='STATUS': pass
            
        elif self.last_com=='STATE': 
            self.status=int(self.last_received.split(' ')[1])
        elif self.last_com=='EVENT': 
            if self.last_received.split(' ')[1]=='cansave':
                self.event=self.last_received.split(' ')[2:4]
                ind= self.event[0].split('=')[1]

                if int(ind)!=int(self.ind): self.event=None
                #self.events.append(self.event)
                #print self.events
        elif self.last_com=='RESUME': self.pause=0
        elif self.last_com=='PAUSE': self.pause=1
        elif self.last_com=='HELLOTS': 
            try: self.version=self.last_received.split(' ')[1].split('=')[1]
            except: self.version='1.0.6'
            try: self.key=self.last_received.split(' ')[2].split('=')[1]
            except: self.key=None
            print self.key
        elif self.last_com=='LOADRESP': 
            fil = self.last_received
            ll= fil[fil.find('{'):len(fil)]
            self.fileslist=ll
        
            json_files=json.loads(self.fileslist)
            try:aa=json_files['infohash']
            except:pass
            if json_files['status']==2:
                self.count=len(json_files['files'])
            if json_files['status']==1:
                self.count=1
            if json_files['status']==0:
                self.count=None
            self.files=self.fileslist.split('\n')[0]
            self.fileslist=None
        #self.pause=None
    #except:
    #	pass

    def end(self):
        self.daemon = False

        
