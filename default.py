### ############################################################################################################
###	#	
### # Project: 			#		MerDB.ru - by The Highway 2013.
### # Author: 			#		The Highway
### # Version:			#		v0.1.0
### # Description: 	#		Videos @ MerDB.ru
###	#	
### ############################################################################################################
### ############################################################################################################
### Plugin Settings ###
def ps(x):
	return {
		'__plugin__': 					"MerDB.ru"
		,'__authors__': 				"[COLOR white]The[COLOR tan]Highway[/COLOR][/COLOR]"
		,'__credits__': 				""
		,'_addon_id': 					"plugin.video.merdb"
		,'_plugin_id': 					"plugin.video.merdb"
		,'_domain_url': 				"http://merdb.ru"
		,'_database_name': 			"merdb"
		,'_addon_path_art': 		"art"
		,'special.home.addons': 'special:'+os.sep+os.sep+'home'+os.sep+'addons'+os.sep
		,'special.home': 				'special:'+os.sep+os.sep+'home'
		,'content_movies': 			"movies"
		,'content_tvshows': 		"tvshows"
		,'content_episodes': 		"episodes"
		,'content_links': 			"list"
		,'common_word': 				"Anime"
		,'common_word2': 				"Watch"
		,'default_art_ext': 		'.png'
		,'default_cFL_color': 	'green'
		,'cFL_color': 					'lime'
		,'cFL_color2': 					'yellow'
		,'cFL_color3': 					'red'
		,'cFL_color4': 					'grey'
		,'cFL_color5': 					'white'
		,'cFL_color6': 					'blanchedalmond'
		,'clr0': 								'white'
		,'clr1': 								'blue'
		,'clr2': 								'white'
		,'clr3': 								'white'
		,'clr4': 								'white'
		,'clr5': 								'white'
		,'clr6': 								'white'
		,'clr7': 								'white'
		,'clr8': 								'white'
		,'clr9': 								'white'
		,'clr10': 							'ghostwhite'
		,'clr11': 							'green'
		,'clr12': 							'green'
		,'clr13': 							'lavender'
		,'default_section': 		'movies'
		,'section.wallpaper':		'wallpapers'
		,'section.movie': 			'movies'
		,'section.tvshows': 		'tvshows'
		,'section.anime': 			'anime'
		,'section.trailers':		'trailers'
		,'section.trailers.popular':			'trailerspopular'
		,'section.trailers.releasedate':	'trailersreleasedate'
		,'section.users':				'users'
		,'section.tv': 					'tv'
		,'cMI.showinfo.name': 						'Show Information'
		,'cMI.showinfo.url': 							'XBMC.Action(Info)'
	}[x]



### ##### /\ ##### Plugin Settings ###
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Imports #####
##Notes-> Some Default imports so that you can use the functions that are available to them.
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import urllib,urllib2,re,os,sys,htmllib,string,StringIO,logging,random,array,time,datetime
#
import copy
import HTMLParser, htmlentitydefs
##Notes-> Common script.module.___ that is used by many to resolve urls of many video hosters.
## ##Notes-> Sometimes you can will use this method.
## ##Notes-> Sometimes you'll have to parse out the direct/playabe url of a video yourself.
import urlresolver
##Notes-> I often use this in the cache-method for addon favorites.
try: 		import StorageServer
except: import storageserverdummy as StorageServer
##Notes-> t0mm0's common module for addon and net functions.
## ##Notes-> I sometimes toss a copy of these modules into my addon folders just incase they dont have them installed... even if that's not a great practice.  I use them a LOT, so in this case it's a habbit.
try: 		from t0mm0.common.addon 				import Addon
except: from t0mm0_common_addon 				import Addon
try: 		from t0mm0.common.net 					import Net
except: from t0mm0_common_net 					import Net

##Notes-> modules to import if you play to use SQL DB stuff in your addon.
try: 		from sqlite3 										import dbapi2 as sqlite; print "Loading sqlite3 as DB engine"
except: from pysqlite2 									import dbapi2 as sqlite; print "Loading pysqlite2 as DB engine"


##Notes-> how to import another .py file from your addon's folder.  Example: to import "config.py" you'd use: "from config import *"
#from teh_tools 		import *
#from config 			import *

##### /\ ##### Imports #####

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
__plugin__=ps('__plugin__'); 
__authors__=ps('__authors__'); 
__credits__=ps('__credits__'); 
_addon_id=ps('_addon_id'); 
_domain_url=ps('_domain_url'); _du=ps('_domain_url'); 
_database_name=ps('_database_name'); 
_plugin_id=ps('_addon_id')
_database_file=os.path.join(xbmc.translatePath("special://database"),ps('_database_name')+'.db'); 
### 
_addon=Addon(ps('_addon_id'), sys.argv); addon=_addon; _plugin=xbmcaddon.Addon(id=ps('_addon_id')); cache=StorageServer.StorageServer(ps('_addon_id'))
### 
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##Notes-> I placed these here so that they would be before the stuff that they use during setup.
def addst(r,s=''): return _addon.get_setting(r)   ## Get Settings
def addpr(r,s=''): return _addon.queries.get(r,s) ## Get Params
def tfalse(r,d=False): ## Get True / False
	if   (r.lower()=='true' ): return True
	elif (r.lower()=='false'): return False
	else: return d
##### Paths #####
### # ps('')
_addonPath	=xbmc.translatePath(_plugin.getAddonInfo('path'))
_artPath		=xbmc.translatePath(os.path.join(_addonPath,ps('_addon_path_art')))
_datapath 	=xbmc.translatePath(_addon.get_profile()); _artIcon		=_addon.get_icon(); _artFanart	=_addon.get_fanart()
##### /\ ##### Paths #####
##### Important Functions with some dependencies #####
def art(f,fe=ps('default_art_ext')): return xbmc.translatePath(os.path.join(_artPath,f+fe)) ### for Making path+filename+ext data for Art Images. ###
##### /\ ##### Important Functions with some dependencies #####
##### Settings #####
_setting={}; 
##Notes-> options from the settings.xml file.
_setting['enableMeta']	=	_enableMeta			=tfalse(addst("enableMeta"))
_setting['debug-enable']=	_debugging			=tfalse(addst("debug-enable")); _setting['debug-show']	=	_shoDebugging		=tfalse(addst("debug-show"))
_setting['label-empty-favorites']=tfalse(addst('label-empty-favorites'))
##Notes-> some custom settings.
#_setting['meta.movie.domain']=ps('meta.movie.domain'); _setting['meta.movie.search']=ps('meta.movie.search')
#_setting['meta.tv.domain']   =ps('meta.tv.domain');    _setting['meta.tv.search']   =ps('meta.tv.search')
#_setting['meta.tv.page']=ps('meta.tv.page'); _setting['meta.tv.fanart.url']=ps('meta.tv.fanart.url'); 
#_setting['meta.tv.fanart.url2']=ps('meta.tv.fanart.url2'); 
##### /\ ##### Settings #####
##### Variables #####
_default_section_=ps('default_section'); net=Net(); DB=_database_file; BASE_URL=_domain_url;
### ############################################################################################################
##Notes-> Some important time saving functions to shorten your work later.
def eod(): _addon.end_of_directory() ## used at the end of a folder listing to print the list to the screen.
def myNote(header='',msg='',delay=5000,image=''): _addon.show_small_popup(title=header,msg=msg,delay=delay,image=image)
def cFL( t,c=ps('default_cFL_color')): return '[COLOR '+c+']'+t+'[/COLOR]' ### For Coloring Text ###
def cFL_(t,c=ps('default_cFL_color')): return '[COLOR '+c+']'+t[0:1]+'[/COLOR]'+t[1:] ### For Coloring Text (First Letter-Only) ###
def notification(header="", message="", sleep=5000 ): xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )
def WhereAmI(t): ### for Writing Location Data to log file ###
	if (_debugging==True): print 'Where am I:  '+t
def deb(s,t): ### for Writing Debug Data to log file ###
	if (_debugging==True): print s+':  '+t
def debob(t): ### for Writing Debug Object to log file ###
	if (_debugging==True): print t
def nolines(t):
	it=t.splitlines(); t=''
	for L in it: t=t+L
	t=((t.replace("\r","")).replace("\n",""))
	return t
def isPath(path): return os.path.exists(path)
def isFile(filename): return os.path.isfile(filename)
def askSelection(option_list=[],txtHeader=''):
	if (option_list==[]): 
		if (debugging==True): print 'askSelection() >> option_list is empty'
		return None
	dialogSelect = xbmcgui.Dialog();
	index=dialogSelect.select(txtHeader, option_list)
	return index
def iFL(t): return '[I]'+t+'[/I]' ### For Italic Text ###
def bFL(t): return '[B]'+t+'[/B]' ### For Bold Text ###
def _FL(t,c,e=''): ### For Custom Text Tags ###
	if (e==''): d=''
	else: d=' '+e
	return '['+c.upper()+d+']'+t+'[/'+c.upper()+']'
def ParseDescription(plot): ## Cleans up the dumb number stuff thats ugly.
	if ("&amp;"  in plot):  plot=plot.replace('&amp;'  ,'&')#&amp;#x27;
	if ("&nbsp;" in plot):  plot=plot.replace('&nbsp;' ," ")
	if ('&#' in plot) and (';' in plot):
		if ("&#8211;" in plot): plot=plot.replace("&#8211;",";") #unknown
		if ("&#8216;" in plot): plot=plot.replace("&#8216;","'")
		if ("&#8217;" in plot): plot=plot.replace("&#8217;","'")
		if ("&#8220;" in plot): plot=plot.replace('&#8220;','"')
		if ("&#8221;" in plot): plot=plot.replace('&#8221;','"')
		if ("&#215;"  in plot): plot=plot.replace('&#215;' ,'x')
		if ("&#x27;"  in plot): plot=plot.replace('&#x27;' ,"'")
		if ("&#xF4;"  in plot): plot=plot.replace('&#xF4;' ,"o")
		if ("&#xb7;"  in plot): plot=plot.replace('&#xb7;' ,"-")
		if ("&#xFB;"  in plot): plot=plot.replace('&#xFB;' ,"u")
		if ("&#xE0;"  in plot): plot=plot.replace('&#xE0;' ,"a")
		if ("&#0421;" in plot): plot=plot.replace('&#0421;',"")
		if ("&#xE9;" in plot):  plot=plot.replace('&#xE9;' ,"e")
		if ("&#xE2;" in plot):  plot=plot.replace('&#xE2;' ,"a")
		#if (chr(239) in plot):  plot=plot.replace(chr(239) ,"'")
		#plot=plot.replace(chr('0x92'),"'")
		if ('&#' in plot) and (';' in plot):
			try:		matches=re.compile('&#(.+?);').findall(plot)
			except:	matches=''
			if (matches is not ''):
				for match in matches:
					if (match is not '') and (match is not ' ') and ("&#"+match+";" in plot):  plot=plot.replace("&#"+match+";" ,"")
		#if ("\xb7"  in plot):  plot=plot.replace('\xb7'   ,"-")
		#if ('&#' in plot) and (';' in plot): plot=unescape_(plot)
	for i in xrange(127,256):
		plot=plot.replace(chr(i),"")
	return plot
def unescape_(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()
def messupText(t,_html=False,_ende=False,_a=False,Slashes=False):
	if (_html==True): 
		try: t=HTMLParser.HTMLParser().unescape(t)
		except: t=t
		try: t=ParseDescription(t)
		except: t=t
	if (_ende==True): 
		try: t=t.encode('ascii', 'ignore'); t=t.decode('iso-8859-1')
		except: t=t
	if (_a==True): 
		try: t=_addon.decode(t); t=_addon.unescape(t)
		except: t=t
	if (Slashes==True): 
		try: t=t.replace( '_',' ')
		except: t=t
	#t=t.replace("text:u","")
	return t
def aSortMeth(sM,h=int(sys.argv[1])):
	xbmcplugin.addSortMethod(handle=h, sortMethod=sM)
def set_view(content='none',view_mode=50,do_sort=False):
	deb('content type: ',str(content))
	deb('view mode: ',str(view_mode))
	h=int(sys.argv[1])
	if (content is not 'none'): xbmcplugin.setContent(h, content)
	if (tfalse(addst("auto-view"))==True): xbmc.executebuiltin("Container.SetViewMode(%s)" % view_mode)
def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
	if txtMessage=='None': txtMessage=''
	keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
	keyboard.doModal()
	if keyboard.isConfirmed():
		return keyboard.getText()
	else:
		return False # return ''

#Metahandler
try: 		from script.module.metahandler 	import metahandlers
except: from metahandler 								import metahandlers
grab=metahandlers.MetaData(preparezip=False)
def GRABMETA(name,typ,year=None):
	EnableMeta=tfalse(addst("enableMeta"))
	if (year==''): year=None
	if (year==None):
		try: year=re.search('\s*\((\d\d\d\d)\)',name).group(1)
		except: year=None
	if (year is not None): name=name.replace(' ('+year+')','').replace('('+year+')','')
	if (EnableMeta=='true'):
		if (typ=='movie'):
 			### grab.get_meta(media_type, name, imdb_id='', tmdb_id='', year='', overlay=6)
			print name; print year;
			meta = grab.get_meta('movie',name,'',None,year,overlay=6)
			infoLabels={'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'backdrop': meta['backdrop_url'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'],'votes': meta['votes'],'tagline': meta['tagline'],'premiered': meta['premiered'],'trailer_url': meta['trailer_url'],'studio': meta['studio'],'imdb_id': meta['imdb_id'],'thumb_url': meta['thumb_url']}
		elif (typ=='tvshow'):
			meta = grab.get_meta('tvshow',name,'','',year,overlay=6)
			infoLabels={'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],'backdrop_url': meta['backdrop_url'],'status': meta['status'],'premiered': meta['premiered'],'imdb_id': meta['imdb_id'],'tvdb_id': meta['tvdb_id'],'year': meta['year'],'imgs_prepacked': meta['imgs_prepacked'],'overlay': meta['overlay'],'duration': meta['duration']}
		else: infoLabels={}
	else: infoLabels={}
	return infoLabels
def GRABMETA_(name,types):
	type=types; EnableMeta=tfalse(addst("enableMeta"))
	if (EnableMeta==True):
		if ('movie' in type):
			### grab.get_meta(media_type, name, imdb_id='', tmdb_id='', year='', overlay=6)
			meta=grab.get_meta('movie',name,'',None,None,overlay=6)
			infoLabels={'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],'director': meta['director'],'cast': meta['cast'],'backdrop': meta['backdrop_url'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year'],'votes': meta['votes'],'tagline': meta['tagline'],'premiered': meta['premiered'],'trailer_url': meta['trailer_url'],'studio': meta['studio'],'imdb_id': meta['imdb_id'],'thumb_url': meta['thumb_url']}
		elif ('tvshow' in type):
			meta=grab.get_meta('tvshow',name,'','',None,overlay=6)
			infoLabels={'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],'backdrop_url': meta['backdrop_url'],'status': meta['status'],'premiered': meta['premiered'],'imdb_id': meta['imdb_id'],'tvdb_id': meta['tvdb_id'],'year': meta['year'],'imgs_prepacked': meta['imgs_prepacked'],'overlay': meta['overlay'],'duration': meta['duration']}
		else: infoLabels={}
	else: infoLabels={}
	return infoLabels
### ############################################################################################################
### ############################################################################################################
##### Queries #####
_param={}
##Notes-> add more here for whatever params you want to use then you can just put the tagname within _param[''] to fetch it later.  or you can use addpr('tagname','defaultvalue').
_param['mode']=addpr('mode',''); _param['url']=addpr('url',''); _param['pagesource'],_param['pageurl'],_param['pageno'],_param['pagecount']=addpr('pagesource',''),addpr('pageurl',''),addpr('pageno',0),addpr('pagecount',1)
_param['img']=addpr('img',''); _param['fanart']=addpr('fanart',''); _param['thumbnail'],_param['thumbnail'],_param['thumbnail']=addpr('thumbnail',''),addpr('thumbnailshow',''),addpr('thumbnailepisode','')
_param['section']=addpr('section','movies'); _param['title']=addpr('title',''); _param['year']=addpr('year',''); _param['genre']=addpr('genre','')
_param['by']=addpr('by',''); _param['letter']=addpr('letter',''); _param['showtitle']=addpr('showtitle',''); _param['showyear']=addpr('showyear',''); _param['listitem']=addpr('listitem',''); _param['infoLabels']=addpr('infoLabels',''); _param['season']=addpr('season',''); _param['episode']=addpr('episode','')
_param['pars']=addpr('pars',''); _param['labs']=addpr('labs',''); _param['name']=addpr('name',''); _param['thetvdbid']=addpr('thetvdbid','')
_param['plot']=addpr('plot',''); _param['tomode']=addpr('tomode',''); _param['country']=addpr('country','')
_param['thetvdb_series_id']=addpr('thetvdb_series_id',''); _param['dbid']=addpr('dbid',''); _param['user']=addpr('user','')
_param['subfav']=addpr('subfav',''); _param['episodetitle']=addpr('episodetitle',''); _param['special']=addpr('special',''); _param['studio']=addpr('studio','')
##Notes-> another way to do it which my custom function just shortens down.
#_param['']=_addon.queries.get('','')

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Player Functions #####
def PlayURL(url):
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	try: _addon.resolve_url(url)
	except: t=''
	try: play.play(url)
	except: t=''

def PlayVideo(url,img,studio='',title='',showtitle='',year=''):
	WhereAmI('@ PlayVideo -- Getting ID From:  %s' % url)
	#My_infoLabels={ "Title": ShowTitle, "Year": ShowYear, "Plot": ShowPlot, 'IMDbURL': IMDbURL, 'IMDbID': IMDbID, 'IMDb': IMDbID }
	infoLabels={ "Studio": studio, "ShowTitle": showtitle, "Title": title, "Year": year }
	li=xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
	#match=re.search( '/.+?/.+?/(.+?)/', url) ## Example: http://www.solarmovie.so/link/show/1052387/ ##
	#videoId=match.group(1); deb('Solar ID',videoId); url=BASE_URL + '/link/play/' + videoId + '/' ## Example: http://www.solarmovie.so/link/play/1052387/ ##
	html=net.http_GET(url).content; 
	html=messupText(html,True,True,True,False)
	#debob(html)
	##match=re.search('<iframe.*?id="play_bottom".*?src="(http://.+?)"', html, re.IGNORECASE | re.DOTALL); 
	##match=re.search('<iframe.*?src="(http://.+?)"', html, re.IGNORECASE | re.DOTALL); 
	match=re.search('<frame scrolling="\D*" frameborder="\d*" id="play_bottom" name="bottom" src="(http://.+?)"/>', html, re.IGNORECASE | re.DOTALL); 
	#debob(match)
	link=match.group(1); 
	##link=match.group(2); 
	link=link.replace('/embed/', '/file/'); 
	deb('hoster link',link)
	#if (_debugging==True): print listitem
	#if (_debugging==True): print infoLabels
	##xbmc.Player( xbmc.PLAYER_CORE_PAPLAYER ).play(stream_url, li)
	##infoLabels.append('url': stream_url)
	li.setInfo(type="Video", infoLabels=infoLabels ); li.setProperty('IsPlayable', 'true')
	##if (urlresolver.HostedMediaFile(link).valid_url()):
	##else: 
	### _addon.resolve_url(link)
	### _addon.resolve_url(stream_url)
	try: stream_url = urlresolver.HostedMediaFile(link).resolve()
	except: 
		deb('Link URL Was Not Resolved',link); deadNote("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL."); return
	eod()
	#xbmc.Player().stop()
	try: _addon.resolve_url(url)
	except: t=''
	try: _addon.resolve_url(stream_url)
	except: t=''
	play=xbmc.Player(xbmc.PLAYER_CORE_AUTO) ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
	#if (play.isPlayingVideo()==True): return
	try: play.play(stream_url, li) #; xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
	except: t=''
	#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True)
	#try: _addon.resolve_url(url)
	#except: t=''
	#try: _addon.resolve_url(stream_url)
	#except: t=''
	#xbmc.sleep(7000)

### ############################################################################################################
### ############################################################################################################
### ############################################################################################################



def doSearchNormal(url='',section='',title=''):
	WhereAmI('@ Search (Normal Search)')
	#SearchPrefix=_domain_url+'/Search/'+ps('common_word')+'?keyword=%s'
	if (title==''):
		title=showkeyboard(txtMessage=title,txtHeader="Title:  ("+section+")")
		if (title=='') or (title=='none') or (title==None) or (title==False): return
	#title=title.replace(' ','+')
	#_param['url']=SearchPrefix % title; deb('Searching for',_param['url']); 
	BrowseItems(url,section,subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search=title)
	#listItems(section, _param['url'], _param['pageno'], addst('pages'), _param['genre'], _param['year'], _param['title'])


def BrowseEpisodes(url,section='',subsection='',showtitle='',showyear='',showimg=_artIcon,showfanart=_artFanart):
	WhereAmI('@ Browse Episodes (Section: %s ) (Subsection: %s ) -- Url:  %s' % (section,subsection,url))
	html=net.http_GET(url).content
	html=messupText(html,True,True,True,False)
	try: html=unescape_(html)
	except: html=html
	#s='<span class=quality_([A-Za-z0-9]+)></span></td>\s*<td align="left" valign="middle"><span class="movie_version_link">\s*[<img src="http://www.primewire.ag/images/star.gif" title="Verified Link">]*\s*<a href="(/external\.php.+?)" onClick="return  addHit\(\'\d*\', \'\d*\'\)" rel="nofollow" title="Watch Version \d+ of .+?" target="_blank">Version\s*\d+</a>\s*</span></td>\s*<td align="center" width="115" valign="middle"><span class="version_host"><script type="text/javascript">document.writeln\(\'([A-Za-z0-9]+\.*[A-Za-z0-9]+)\'\);</script>'
	s='<div\s+class="tv_episode_item"\s*>\s*<a\s+href="(/tvshow_watch-\d+-[A-Za-z0-9\-_]+_ep_tv-\d+-[A-Za-z0-9\-_]+/season-(\d+)-episode-(\d+))">[Episode]*\s*\d*\s*<span class="tv_episode_name">\s*[-]*\s*(.*?)\s*</span>\s*</a>\s*</div>'
	try: matches=re.compile(s, re.DOTALL).findall(html)
	except: matches=''
	ItemCount=len(matches) # , total_items=ItemCount
	if (len(matches) > 0):
		deb('# of matches in first match',str(len(matches[0])))
		debob(matches)
		for url,sN,eN,eT in matches:
			labs={}; fimg=_artFanart; img=showimg; url=_du+'/'+url; 
			#eT=str(eT).encode('ascii','replace') #.replace(chr(239),"")
			#eT=eT.replace('','')
			print str(eT)
			labs['title']='s'+sN+'e'+eN+'  '+eT
			if (fimg==''): fimg=_artFanart
			if (img==''): img=_artIcon
			pars={'mode':'BrowseHosts','url':url,'studio':showtitle+'  ('+showyear+')'+'  S'+sN+'E'+eN+'  '+eT,'title':showtitle+'  ('+showyear+')','showtitle':showtitle,'year':showyear,'img':showimg,'fanart':showfanart}
			_addon.add_directory(pars,labs,is_folder=True,img=img,fanart=fimg,total_items=ItemCount)
		set_view('episodes',addst('episode-view')); eod()

def BrowseHosts(url,section='',subsection='',showtitle='',showyear='',showimg=_artIcon,showfanart=_artFanart,studio=''):
	WhereAmI('@ Browse Hosts (Section: %s ) (Subsection: %s ) -- Url:  %s' % (section,subsection,url))
	html=net.http_GET(url).content
	html=messupText(html,True,True,True,False)
	#s='<table width="100%" cellpadding="0" cellspacing="0" class="movie_version">\s*<tbody>\s*<tr>\s*<td align="center" width="40" valign="middle">\s*<span class=quality_(.+?)></span></td>\s*<td align="left" valign="middle"><span class="movie_version_link">\s*<a href="(/external\.php.+?)" onClick="return  addHit\(\'\d*\', \'\d*\'\)" rel="nofollow" title="Watch Version \d+ of .+?" target="_blank">Version\s*\d+</a>\s*</span></td>\s*<td align="center" width="115" valign="middle"><span class="version_host"><script type="text/javascript">document.writeln\(\'[A-Za-z0-9]+\.*[A-Za-z0-9]+\'\);</script></span>\s*</td>\s*<td width="\d+" align="center" valign="middle"><span class="version_veiws">\s*\d+\s*view[s]*</span>\s*</td>\s*<td width="80" align="center" valign="middle" >\s*<span class="report_broken">\s*</span>\s*</td>\s*<td align="center" width="100" valign="middle"><div class="movie_ratings">\s*<div id="unit_long[0-9]+">\s*<ul id="unit_[0-9A-Za-z]+" class="unit-rating" style="width:100px;">\s*<li class="current-rating" style="width:80px;">Currently \d*\.*\d*/5</li>\s*<li></li>\s*<li></li>\s*<li></li>\s*<li></li>\s*<li></li>\s*</ul>\s*<center>\s*<div class=not_voted\s*>(\d+ votes)</div>\s*</center>\s*</div>\s*</div></td>\s*</tr>\s*</tbody>\s*</table>'
	s='<span class=quality_([A-Za-z0-9]+)></span></td>\s*<td align="left" valign="middle"><span class="movie_version_link">\s*[<img src="http://www.primewire.ag/images/star.gif" title="Verified Link">]*\s*<a href="(/external\.php.+?)" onClick="return  addHit\(\'\d*\', \'\d*\'\)" rel="nofollow" title="Watch Version \d+ of .+?" target="_blank">Version\s*\d+</a>\s*</span></td>\s*<td align="center" width="115" valign="middle"><span class="version_host"><script type="text/javascript">document.writeln\(\'([A-Za-z0-9]+\.*[A-Za-z0-9]+)\'\);</script>'
	try: matches=re.compile(s, re.DOTALL).findall(html)
	except: matches=''
	ItemCount=len(matches) # , total_items=ItemCount
	if (len(matches) > 0):
		deb('# of matches in first match',str(len(matches[0])))
		debob(matches)
		for quality,url,domain in matches:
			labs={}; fimg=''; img=''; url=_du+'/'+url; 
			labs['title']=domain+'  ['+quality+']'
			if (fimg==''): fimg=_artFanart
			if (img==''): img=_artIcon
			pars={'mode':'PlayVideo','url':url,'studio':studio,'title':showtitle+'  ('+showyear+')','showtitle':showtitle,'year':showyear,'img':showimg,'fanart':showfanart}
			_addon.add_directory(pars,labs,is_folder=False,img=img,fanart=fimg,total_items=ItemCount)
		set_view('list',addst('default-view')); eod()

def BrowseItems(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search='',featured=''):
	search=search.replace('+','%2B').replace(' ','+').replace(':','%3A').replace('&','%26').replace('?','%3F')
	WhereAmI('@ Browse Items (Section: %s ) (Subsection: %s ) -- Url:  %s' % (section,subsection,url))
	if (featured=='1'): path=url+'?featured=%s&sort=%s&page=%s' % (featured,sortby,str(pagestart))
	elif (len(search) > 0): path=url+'?search=%s&genre=%s&year=%s&sort=%s&page=%s' % (search,genre,year,sortby,str(pagestart))
	else: path=url+'?genre=%s&year=%s&sort=%s&page=%s' % (genre,year,sortby,str(pagestart))
	### path=url+'?search=%s&featured=%s&genre=%s&year=%s&sort=%s&page=%s' % (search,featured,genre,year,sortby,str(pagestart))
	deb('path',path)
	html=net.http_GET(path).content
	html=messupText(html,True,True,True,False)
	EnableMeta=tfalse(addst("enableMeta"))
	#<li><a href="?genre=Adventure&page=2">></a></li>
	if ('">></a></li>' in html): _addon.add_directory({'mode':'BrowseItems','section':section,'subsection':subsection,'pagestart':str(int(pagestart)+1),'pagecount':pagecount,'genre':genre,'year':year,'sortby':sortby,'search':search,'featured':featured,'url':url},{'title':cFL(bFL('  >> '+iFL('Next')+'  >>'),'red')},is_folder=True,img=_artIcon,fanart=_artFanart)
	if (section==ps('section.movie')) or (section==''):
		#, re.IGNORECASE | re.MULTILINE | re.DOTALL
		s='<div\s+class="main_list_box"><a\s+href="(watch-\d+-[A-Za-z0-9\-_]+\.html)"'
		s+='\s+title="Watch\s+.+?\s+\(\d\d\d\d\)">\s*\n*\s*'
		s+='<img\s+src="(http://.+?)"'
		s+='\s*\n*\s*class="main_list_picsize"\s*\n*\s*'
		s+='alt="Watch\s+.+?\s+\(\d\d\d\d\)"\s*/>\s*\n*\s*</a>\s*\n*\s*<div\s+class="list_box_title">'
		s+='<a\s+href="(watch-\d+-[A-Za-z0-9\-_]+\.html)"'
		s+='\s+title="Watch\s+((.+?)\s+\((\d\d\d\d)\))">\s*\n*\s*((.+?)\s+\((\d\d\d\d)\))\s*\n*\s*</a>'
		##matches=re.search(s,html).group()
		try: matches=re.compile(s, re.DOTALL).findall(html)
		except: matches=''
		#deb('# of matches',str(len(matches))) # 9
		#print matches[0]
		ItemCount=len(matches) # , total_items=ItemCount
		if (len(matches) > 0):
			deb('# of matches in first match',str(len(matches[0])))
			#return
			#for url,img,url2,t1a,t1b,t1c,t2a,t2b,t2c,va1a,va1b,va2a,va2b,rv1a,rv1b,rc1v,genres in matches:
			for url,img,url2,t1a,t1b,t1c,t2a,t2b,t2c in matches:
				contextMenuItems=[]; labs={}; fimg=''; url=_du+'/'+url; 
				#labs['title']=cFL(t1b+'  ('+cFL(t1c,'red')+')','blue')
				labs['title']=t1b+'  ('+cFL(t1c,'red')+')'
				###
				if (EnableMeta==True):
					#mlabs=GRABMETA(t1b,'movie',year=t1c) #
					mlabs=GRABMETA_(t1b,'movie')
					debob(mlabs)
					if (len(mlabs) > 0):
						if (len(mlabs[u'cover_url']) > 0): 
							img=mlabs[u'cover_url']
							fimg=mlabs[u'cover_url']
						else: fimg=img
						if (len(mlabs[u'backdrop_url']) > 0): fimg=mlabs[u'backdrop_url']
						labs['plot']=messupText(mlabs[u'plot'],True,True,True,False)
						if (len(mlabs['cast']) > 0): labs['cast']=mlabs['cast']
						if (len(mlabs['genre']) > 0): labs['genre']=mlabs['genre']
						if (len(mlabs['studio']) > 0): labs['studio']=mlabs['studio']
						if (len(mlabs['thumb_url']) > 0): labs['thumb_url']=mlabs['thumb_url']
						if (len(mlabs['tmdb_id']) > 0): labs['tmdb_id']=mlabs['tmdb_id']
						if (len(mlabs['director']) > 0): labs['director']=mlabs['director']
						if (len(mlabs['writer']) > 0): labs['writer']=mlabs['writer']
						#if (len(mlabs['rating']) > 0): 
						labs['rating']=mlabs['rating']
						#if (len(mlabs['mpaa']) > 0): 
						labs['mpaa']=mlabs['mpaa']
						#if (len(mlabs['duration']) > 0): 
						labs['duration']=mlabs['duration']
						if (len(mlabs['title']) > 0): labs['showtitle']=mlabs['title']
						if (len(mlabs['premiered']) > 0): labs['premiered']=mlabs['premiered']
						#labs['overlay']=6
						#
						#
						dnotnow=False
					else: dnotnow=True
				else: dnotnow=True
				if (dnotnow==True):
					fimg=img
				###
				if (fimg==''): fimg=_artFanart
				if (img==''): img=_artIcon
				contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
				pars={'mode':'BrowseHosts','url':url,'title':t1b+'  ('+t1c+')','showtitle':t1b,'year':t1c,'img':img,'fanart':fimg}
				_addon.add_directory(pars,labs,is_folder=True,img=img,fanart=fimg,total_items=ItemCount,contextmenu_items=contextMenuItems)
			set_view('movies',addst('movies-view'));
	elif (section==ps('section.tvshows')) or (section==''):
		#, re.IGNORECASE | re.MULTILINE | re.DOTALL
		s='<div\s+class="main_list_box"><a\s+href="(/tvshow/watch-\d+-[A-Za-z0-9\-_]+\.html)"'
		s+='\s+title=".+?">\s*\n*\s*'
		s+='<img\s+src="(http://.+?)"'
		s+='\s*\n*\s*class="main_list_picsize"\s*\n*\s*'
		s+='alt=".+?"\s*/>\s*\n*\s*</a>\s*\n*\s*<div\s+class="list_box_title">'
		s+='<a\s+href="(/tvshow/watch-\d+-[A-Za-z0-9\-_]+\.html)"'
		s+='\s+title="(.+?)">\s*\n*\s*((.+?)\s+\((\d\d\d\d)\))\s*\n*\s*</a>'
		##matches=re.search(s,html).group()
		try: matches=re.compile(s, re.DOTALL).findall(html)
		except: matches=''
		deb('# of matches',str(len(matches)))
		print matches
		ItemCount=len(matches) # , total_items=ItemCount
		if (len(matches) > 0):
			deb('# of matches in first match',str(len(matches[0]))) # 9
			#return
			#for url,img,url2,t1a,t1b,t1c,t2a,t2b,t2c,va1a,va1b,va2a,va2b,rv1a,rv1b,rc1v,genres in matches:
			for url,img,url2,t1b,t2a,t2b,t1c in matches:
				contextMenuItems=[]; labs={}; fimg=''; url=_du+''+url; 
				#labs['title']=cFL(t1b+'  ('+cFL(t1c,'red')+')','blue')
				labs['title']=t1b+'  ('+cFL(t1c,'red')+')'
				###
				if (EnableMeta==True):
					#mlabs=GRABMETA(t1b,'tvshow') #,year=t1c)
					mlabs=GRABMETA_(t1b,'tvshow')
					debob(mlabs)
					if (len(mlabs) > 0):
						if (len(mlabs[u'cover_url']) > 0): 
							img=mlabs[u'cover_url']
							fimg=mlabs[u'cover_url']
						else: fimg=img
						if (len(mlabs[u'backdrop_url']) > 0): fimg=mlabs[u'backdrop_url']
						if (len(mlabs[u'banner_url']) > 0): fimg=mlabs[u'banner_url']
						labs['plot']=messupText(mlabs[u'plot'],True,True,True,False)
						if (len(mlabs['cast']) > 0): labs['cast']=mlabs['cast']
						if (len(mlabs['genre']) > 0): labs['genre']=mlabs['genre']
						if (len(mlabs['studio']) > 0): labs['studio']=mlabs['studio']
						labs['tvdb_id']=mlabs['tvdb_id']
						labs['imdb_id']=mlabs['imdb_id']
						labs['rating']=mlabs['rating']
						labs['mpaa']=mlabs['mpaa']
						labs['duration']=mlabs['duration']
						if (len(mlabs['title']) > 0): labs['showtitle']=mlabs['title']
						if (len(mlabs['premiered']) > 0): labs['premiered']=mlabs['premiered']
						if (len(mlabs['status']) > 0): labs['status']=mlabs['status']
						if (mlabs['overlay'] is not 6): labs['overlay']=mlabs['overlay']
						else: labs['overlay']=6
						#
						### {'rating': meta['rating'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
						### 'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
						### 'cast': meta['cast'],'studio': meta['studio'],'banner_url': meta['banner_url'],
						### 'backdrop_url': meta['backdrop_url'],'status': meta['status'],'premiered': meta['premiered'],
						### 'imdb_id': meta['imdb_id'],'tvdb_id': meta['tvdb_id'],'year': meta['year'],'imgs_prepacked': 
						### meta['imgs_prepacked'],'overlay': meta['overlay'],'duration': meta['duration']}
						dnotnow=False
					else: dnotnow=True
				else: dnotnow=True
				if (dnotnow==True):
					fimg=img
				###
				if (fimg==''): fimg=_artFanart
				if (img==''): img=_artIcon
				contextMenuItems.append((ps('cMI.showinfo.name'),ps('cMI.showinfo.url')))
				pars={'mode':'BrowseEpisodes','url':url,'title':t1b+'  ('+t1c+')','showtitle':t1b,'year':t1c,'img':img,'fanart':fimg}
				_addon.add_directory(pars,labs,is_folder=True,img=img,fanart=fimg,total_items=ItemCount,contextmenu_items=contextMenuItems)
			set_view('tvshows',addst('tvshows-view'));
	eod()

def Just_A_Sub_Menu(title=''): #The Main Menu
	#mode left blank for main menu.
	_addon.add_directory({'mode': ''},{'title':  cFL_('Go To The Main Menu',ps('cFL_color3'))},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode': ''},{'title':  cFL_(title+'  <--',ps('cFL_color3'))},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

def BrowseSort(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search=''):
	WhereAmI('@ Browse Sort')
	sclr=ps('clr13')
	_addon.add_directory({'sortby':'','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Sort By [Nothing]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'views','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Popular',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'ratingp','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Ratings',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'favorite','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Favorites',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'year','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Release Date',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'stamp','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Date Added',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'startwith','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Alphabet',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'sortby':'featured','mode':'BrowseItems','section':section,'subsection':subsection,'genre':genre,'year':year,'search':search,'url':url},{'title':  cFL_('Featured',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

def BrowseYear(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search=''):
	WhereAmI('@ Browse Year')
	sclr=ps('clr12')
	_addon.add_directory({'year':'','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [Nothing]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	ITEMS=['classic','1990','2000','2010']
	for ITEM in ITEMS:
		_addon.add_directory({'year':ITEM,'sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_(ITEM,sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'classic','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [Classic]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'1990','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [1990]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'2000','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [2000]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'2010','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [2010]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

def BrowseYearGenre(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search=''):
	WhereAmI('@ Browse YearGenre')
	sclr=ps('clr11')
	_addon.add_directory({'year':'','sortby':sortby,'mode':'BrowseGenres','BrowseGenres':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [Nothing]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	ITEMS=['classic','1990','2000','2010']
	for ITEM in ITEMS:
		_addon.add_directory({'year':ITEM,'sortby':sortby,'mode':'BrowseGenres','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_(ITEM,sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'classic','sortby':sortby,'mode':'BrowseGenres','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [Classic]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'1990','sortby':sortby,'mode':'BrowseGenres','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [1990]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'2000','sortby':sortby,'mode':'BrowseGenres','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [2000]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'year':'2010','sortby':sortby,'mode':'BrowseGenres','section':section,'subsection':subsection,'genre':genre,'search':search,'url':url},{'title':  cFL_('Year [2010]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

def BrowseGenres(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search=''):
	WhereAmI('@ Browse Genres')
	sclr=ps('clr10')
	_addon.add_directory({'genre':'','sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'year':year,'search':search,'url':url},{'title':  cFL_('Genre [Nothing]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	GENRES=['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Game-Show','History','Horror','Indian','Japanese','Korean','Music','Musical','Mystery','NoGenres','Reality-TV','Romance','Russian','Sci-Fi','Short','Sport','Talk-Show','Thriller','War','Western','Zombies']
	for agenre in GENRES:
		_addon.add_directory({'genre':agenre,'sortby':sortby,'mode':'BrowseSort','section':section,'subsection':subsection,'year':year,'search':search,'url':url},{'title':  cFL_(agenre,sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

	

def MenuMovies(section=''):
	WhereAmI('@ the Movies Menu')
	if (section==''): section=ps('section.movie')
	tvurl=''; sclr=ps('clr1')
	_addon.add_directory({'mode':'Search','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Search',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseGenres','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Genres',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseYearGenre','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Year & Genres',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseYear','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Year',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseSort','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Sort By',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'stamp','featured':'1'},{'title':  cFL_('Featured',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'stamp'},{'title':  cFL_('Date Added',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'views'},{'title':  cFL_('Popular',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'classic'},{'title':  cFL_('Year [Classic]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'1990'},{'title':  cFL_('Year [1990]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'2000'},{'title':  cFL_('Year [2000]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'2010'},{'title':  cFL_('Year [2010]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','genre':'Sci-Fi'},{'title':  cFL_('Genre [Sci-Fi]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

def MenuTVShows(section=''):
	WhereAmI('@ the TVShows Menu')
	if (section==''): section=ps('section.tvshows')
	tvurl='/tvshow'; sclr=ps('clr2')
	_addon.add_directory({'mode':'Search','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Search',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseGenres','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Genres',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseYearGenre','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Year & Genres',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseYear','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Year',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseSort','section':section,'url':_du+tvurl+'/'},{'title':  cFL_('Browse: Sort By',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'stamp','featured':'1'},{'title':  cFL_('Featured',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'stamp'},{'title':  cFL_('Date Added',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','sortby':'views'},{'title':  cFL_('Popular',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'classic'},{'title':  cFL_('Year [Classic]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'1990'},{'title':  cFL_('Year [1990]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'2000'},{'title':  cFL_('Year [2000]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','year':'2010'},{'title':  cFL_('Year [2010]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode':'BrowseItems','section':section,'url':_du+tvurl+'/','genre':'Sci-Fi'},{'title':  cFL_('Genre [Sci-Fi]',sclr)},is_folder=True,img=_artIcon,fanart=_artFanart)
	set_view('list',addst('default-view')); eod()

##Notes-> Your Main Menu
def Menu_MainMenu(): #The Main Menu
	WhereAmI('@ the Main Menu')
	#Added 'title' to the params passed along with mode as an example of how to do it.  Same can be done for 'url' and others stuff, such as an image or fanart.
	_addon.add_directory({'mode': 'MenuMovies'},{'title':  cFL_('Movies',ps('clr1'))},is_folder=True,img=_artIcon,fanart=_artFanart)
	_addon.add_directory({'mode': 'MenuTVShows'},{'title':  cFL_('TV Shows',ps('clr2'))},is_folder=True,img=_artIcon,fanart=_artFanart)
	#
	#_addon.add_directory({'mode': 'ASubMenu','title':'This has been a test.'},{'title':  cFL_('Test Folder',ps('cFL_color3'))},is_folder=True,img=_artIcon,fanart=_artFanart)
	#_addon.add_directory({'mode': 'PlayURL','url':'http://www.eally.org/images/stories/videos/rob-TV.flv'},{'title':  cFL_('Play A Test Video (This is not my video, only an example.)',ps('cFL_color'))},is_folder=False,img=_artIcon,fanart=_artFanart)
	#
	_addon.add_directory({'mode': 'ResolverSettings'},{'title':  cFL_('Url-Resolver Settings',ps('cFL_color2'))},is_folder=False,img=_artIcon,fanart=_artFanart)
	#
	_addon.add_directory({'mode': 'Settings'}, 				{'title':  cFL_('Plugin Settings',ps('cFL_color2'))}			,is_folder=False,img='http://www.merdb.ru/merdb_ipad.png',fanart=_artFanart)
	#Ends the directory listing and prints it to the screen.  if you dont use eod() or something like it, the menu items won't be put to the screen.
	set_view('list',addst('default-view')); eod()




### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
##### Modes #####
def check_mode(mode=''):
	deb('Mode',mode)
	if (mode=='') or (mode=='main') or (mode=='MainMenu'):  Menu_MainMenu() ## Default Menu
	elif (mode=='PlayURL'): 							PlayURL(addpr('url','')) ## Play Video
	elif (mode=='PlayVideo'): 						PlayVideo(addpr('url',''),addpr('img',''),addpr('studio',''),addpr('title',''),addpr('showtitle',''),addpr('year','')) ## Play Video
	elif (mode=='ASubMenu'): 							Just_A_Sub_Menu(_param['title']) ## Play Video
	elif (mode=='BrowseItems'): 					BrowseItems(url=addpr('url',''),section=addpr('section',''),subsection=addpr('subsection',''),pagestart=addpr('pagestart','1'),pagecount=addpr('pagecount','1'),genre=addpr('genre',''),year=addpr('year',''),sortby=addpr('sortby',''),search=addpr('search',''),featured=addpr('featured',''))
	elif (mode=='BrowseHosts'): 					BrowseHosts(addpr('url',''),addpr('section',''),addpr('subsection',''),addpr('showtitle',''),addpr('year',''),addpr('img',''),addpr('fanart',''),studio=addpr('studio',''))
	elif (mode=='BrowseEpisodes'): 				BrowseEpisodes(addpr('url',''),addpr('section',''),addpr('subsection',''),addpr('showtitle',''),addpr('year',''),addpr('img',''),addpr('fanart',''))
	elif (mode=='MenuMovies'): 						MenuMovies()
	elif (mode=='MenuTVShows'): 					MenuTVShows()
	elif (mode=='Settings'): 							_addon.addon.openSettings() # Another method: _plugin.openSettings() ## Settings for this addon.
	elif (mode=='ResolverSettings'): 			urlresolver.display_settings()  ## Settings for UrlResolver script.module.
	elif (mode=='Search'):  							doSearchNormal(url=addpr('url',''),section=addpr('section',''),title=addpr('title',''))
	elif (mode=='BrowseGenres'): 					BrowseGenres(url=addpr('url',''),section=addpr('section',''),subsection=addpr('subsection',''),pagestart=addpr('pagestart',''),pagecount=addpr('pagecount',''),genre=addpr('genre',''),year=addpr('year',''),sortby=addpr('sortby',''),search=addpr('search',''))
	elif (mode=='BrowseYearGenre'): 			BrowseYearGenre(url=addpr('url',''),section=addpr('section',''),subsection=addpr('subsection',''),pagestart=addpr('pagestart',''),pagecount=addpr('pagecount',''),genre=addpr('genre',''),year=addpr('year',''),sortby=addpr('sortby',''),search=addpr('search',''))
	elif (mode=='BrowseYear'): 						BrowseYear(url=addpr('url',''),section=addpr('section',''),subsection=addpr('subsection',''),pagestart=addpr('pagestart',''),pagecount=addpr('pagecount',''),genre=addpr('genre',''),year=addpr('year',''),sortby=addpr('sortby',''),search=addpr('search',''))
	elif (mode=='BrowseSort'): 						BrowseSort(url=addpr('url',''),section=addpr('section',''),subsection=addpr('subsection',''),pagestart=addpr('pagestart',''),pagecount=addpr('pagecount',''),genre=addpr('genre',''),year=addpr('year',''),sortby=addpr('sortby',''),search=addpr('search',''))
	#BrowseGenres(url,section='',subsection='',pagestart='1',pagecount='1',genre='',year='',sortby='',search='')
	#
	#elif (mode=='YourMode'): 						YourFunction(_param['url'])
	#
	#
	#
	else: myNote(header='Mode:  "'+mode+'"',msg='[ mode ] not found.'); Menu_MainMenu() ## So that if a mode isn't found, it'll goto the Main Menu and give you a message about it.
##### /\ ##### Modes #####
### ############################################################################################################
deb('param >> title',_param['title'])
deb('param >> url',_param['url']) ### Simply Logging the current query-passed / param -- URL
check_mode(_param['mode']) ### Runs the function that checks the mode and decides what the plugin should do. This should be at or near the end of the file.
### ############################################################################################################
### ############################################################################################################
### ############################################################################################################
