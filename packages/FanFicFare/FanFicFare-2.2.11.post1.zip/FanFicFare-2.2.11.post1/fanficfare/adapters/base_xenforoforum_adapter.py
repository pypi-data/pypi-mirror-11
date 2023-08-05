#  -*- coding: utf-8 -*-

# Copyright 2015 FanFicFare team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time
import logging
logger = logging.getLogger(__name__)
import re
import urllib2

from ..htmlcleanup import stripHTML
from .. import exceptions as exceptions

from base_adapter import BaseSiteAdapter,  makeDate

logger = logging.getLogger(__name__)

class BaseXenForoForumAdapter(BaseSiteAdapter):

    def __init__(self, config, url):
        BaseSiteAdapter.__init__(self, config, url)

        self.decode = ["utf8",
                       "Windows-1252"] # 1252 is a superset of iso-8859-1.
                               # Most sites that claim to be
                               # iso-8859-1 (and some that claim to be
                               # utf8) are really windows-1252.
							   
							   
        # get storyId from url--url validation guarantees query is only sid=1234
        self.story.setMetadata('storyId',self.parsedUrl.path.split('/',)[2])        
        
        # get storyId from url--url validation guarantees query correct
        m = re.match(self.getSiteURLPattern(),url)
        if m:
            self.story.setMetadata('storyId',m.group('id'))

            # normalized story URL.
            self._setURL(self.getURLPrefix() + '/'+m.group('tp')+'/'+self.story.getMetadata('storyId')+'/')
        else:
            raise exceptions.InvalidStoryURL(url,
                                             self.getSiteDomain(),
                                             self.getSiteExampleURLs())
        
        # Each adapter needs to have a unique site abbreviation.
        self.story.setMetadata('siteabbrev','fsb')

        # The date format will vary from site to site.
        # http://docs.python.org/library/datetime.html#strftime-strptime-behavior
        self.dateformat = "%b %d, %Y at %I:%M %p"
            
    @classmethod
    def getConfigSections(cls):
        "Only needs to be overriden if has additional ini sections."
        return ['base_xenforoforum',cls.getConfigSection()]
    
    @classmethod
    def getURLPrefix(cls):
        # The site domain.  Does have www here, if it uses it.
        return 'https://' + cls.getSiteDomain() 

    @classmethod
    def getSiteExampleURLs(cls):
        return cls.getURLPrefix()+"/threads/some-story-name.123456/"

    def getSiteURLPattern(self):
        return r"https?://"+re.escape(self.getSiteDomain())+r"/(?P<tp>threads|posts)/(.+\.)?(?P<id>\d+)/?"
        
    def use_pagecache(self):
        '''
        adapters that will work with the page cache need to implement
        this and change it to True.
        '''
        return True

    ## Getting the chapter list and the meta data, plus 'is adult' checking.
    def extractChapterUrlsAndMetadata(self):

        useurl = self.url
        logger.info("url: "+useurl)

        try:
            (data,opened) = self._fetchUrlOpened(useurl)
            useurl = opened.geturl()
            logger.info("use useurl: "+useurl)
        except urllib2.HTTPError, e:
            if e.code == 404:
                raise exceptions.StoryDoesNotExist(self.url)
            else:
                raise e

        # use BeautifulSoup HTML parser to make everything easier to find.
        soup = self.make_soup(data)

        a = soup.find('h3',{'class':'userText'}).find('a')
        self.story.addToList('authorId',a['href'].split('/')[1])
        self.story.addToList('authorUrl',self.getURLPrefix()+'/'+a['href'])
        self.story.addToList('author',a.text)

        h1 = soup.find('div',{'class':'titleBar'}).h1
        self.story.setMetadata('title',stripHTML(h1))
        
        if '#' in useurl:
            anchorid = useurl.split('#')[1]
            soup = soup.find('li',id=anchorid)
        else:
            # try threadmarks if no '#' in , require at least 2.
            threadmarksa = soup.find('a',{'class':'threadmarksTrigger'})
            if threadmarksa:
                soupmarks = self.make_soup(self._fetchUrl(self.getURLPrefix()+'/'+threadmarksa['href']))
                markas = soupmarks.find('ol',{'class':'overlayScroll'}).find_all('a')
                if len(markas) > 1:
                    for (atag,url,name) in [ (x,x['href'],stripHTML(x)) for x in markas ]:
                        date = self.make_date(atag.find_next_sibling('div',{'class':'extra'}))
                        if not self.story.getMetadataRaw('datePublished') or date < self.story.getMetadataRaw('datePublished'):
                            self.story.setMetadata('datePublished', date)
                        if not self.story.getMetadataRaw('dateUpdated') or date > self.story.getMetadataRaw('dateUpdated'):
                            self.story.setMetadata('dateUpdated', date)
                            
                        self.chapterUrls.append((name,self.getURLPrefix()+'/'+url))
                        
            soup = soup.find('li',{'class':'message'}) # limit first post for date stuff below. ('#' posts above)
                
        # Now go hunting for the 'chapter list'.
        bq = soup.find('blockquote') # assume first posting contains TOC urls.
        
        bq.name='div'

        for iframe in bq.find_all('iframe'):
            iframe.extract() # calibre book reader & editor don't like iframes to youtube.

        for qdiv in bq.find_all('div',{'class':'quoteExpand'}):
            qdiv.extract() # Remove <div class="quoteExpand">click to expand</div>
            
        self.setDescription(useurl,bq)

        # otherwise, use first post links--include first post since
        # that's often also the first chapter.
        if not self.chapterUrls:
            self.chapterUrls.append(("First Post",useurl))
            for (url,name) in [ (x['href'],stripHTML(x)) for x in bq.find_all('a') ]:
                logger.debug("found chapurl:%s"%url)
                if not url.startswith('http'):
                    url = self.getURLPrefix()+'/'+url
    
                if ( url.startswith(self.getURLPrefix()) or
                     url.startswith('http://'+self.getSiteDomain()) or
                     url.startswith('https://'+self.getSiteDomain()) ) and ('/posts/' in url or '/threads/' in url):
                    # brute force way to deal with SB's http->https change when hardcoded http urls.
                    url = url.replace('http://'+self.getSiteDomain(),self.getURLPrefix())
                    logger.debug("used chapurl:%s"%(url))
                    self.chapterUrls.append((name,url))
                    if url == useurl and 'First Post' == self.chapterUrls[0][0]:
                        # remove "First Post" if included in list.
                        logger.debug("delete dup 'First Post' chapter: %s %s"%self.chapterUrls[0])
                        del self.chapterUrls[0]
                        
            # Didn't use threadmarks, so take created/updated dates
            # from the 'first' posting created and updated.
            date = self.make_date(soup.find('a',{'class':'datePermalink'}))
            if date:
                self.story.setMetadata('datePublished', date)
                self.story.setMetadata('dateUpdated', date) # updated overwritten below if found.
        
            date = self.make_date(soup.find('div',{'class':'editDate'}))
            if date:
                self.story.setMetadata('dateUpdated', date) 
            
        self.story.setMetadata('numChapters',len(self.chapterUrls))

    def make_date(self,parenttag): # forums use a BS thing where dates
                                  # can appear different if recent.
        datestr=None
        try:
            datetag = parenttag.find('span',{'class':'DateTime'})
            if datetag:
                datestr = datetag['title']
            else:
                datetag = parenttag.find('abbr',{'class':'DateTime'})
                if datetag:
                    datestr="%s at %s"%(datetag['data-datestring'],datetag['data-timestring'])
            # Apr 24, 2015 at 4:39 AM
            # May 1, 2015 at 5:47 AM
            datestr = re.sub(r' (\d[^\d])',r' 0\1',datestr) # add leading 0 for single digit day & hours.
            return makeDate(datestr, self.dateformat)
        except:
            logger.debug('No date found in %s'%parenttag)
            return None
        
    # grab the text for an individual chapter.
    def getChapterText(self, url):
        logger.debug('Getting chapter text from: %s' % url)

        origurl = url
        (data,opened) = self._fetchUrlOpened(url)
        url = opened.geturl()
        if '#' in origurl and '#' not in url:
            url = url + origurl[origurl.index('#'):]
        logger.debug("chapter URL redirected to: %s"%url)

        soup = self.make_soup(data)

        if '#' in url:
            anchorid = url.split('#')[1]
            soup = soup.find('li',id=anchorid)
        bq = soup.find('blockquote')

        bq.name='div'

        for iframe in bq.find_all('iframe'):
            iframe.extract() # calibre book reader & editor don't like iframes to youtube.

        for qdiv in bq.find_all('div',{'class':'quoteExpand'}):
            qdiv.extract() # Remove <div class="quoteExpand">click to expand</div>

        return self.utf8FromSoup(url,bq)
