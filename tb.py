#!/usr/bin/python

import web
import markdown
import timesince

import config
from models import Blog
    
#### Helper functions ####
import mimetypes
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

# From http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/303279
from itertools import islice, chain
def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)

def get_entries_range(entries, page):
    start = config.per_page * (page - 1)
    entries = entries[start:start+config.per_page]
    return start, len(entries)

#### Globals
blog = Blog(config.yaml_file)


#### View setup ####
render = web.template.render('templates/', cache=config.cache)
web.template.Template.globals.update(dict(
    datestr = web.datestr,
    timesince = timesince.timesince,
    render = render,
    ctx  = web.ctx,
    blog = blog,
))

#### Controllers  ####
class IndexC:
    def GET(self, page = 1):
        page = int(page)
        
        entries_list = map(list, (batch(blog.entries, config.per_page)))
        
        try:
            entries = entries_list[page-1]
        except IndexError:
            return web.notfound()
        
        try:
            newer = page - 1
            entries_list[newer-1]
        except IndexError:
            newer = None
            
        try:
            older = page + 1
            entries_list[older-1]
        except IndexError:
            older = None
            
        for e in entries:
            e.content = markdown.markdown(e.content)
           
        print render.base(render.entries(entries, older, newer))
            
class EntryC:
    def GET(self, _id):
        if not _id: return web.seeother(blog.url)
        _id = int(_id)
        entry = None
        for e in blog.entries:
            if e.id == _id:
                entry = e
                break
        if not entry:
            return web.notfound()
        
        entry.content = markdown.markdown(entry.content)
        print render.base(render.entry(entry), entry.title)
        
class FeedC:
    def GET(self):
        entries = blog.entries[:config.per_page]
        for e in entries:
            e.content = markdown.markdown(e.content)
        web.header('Content-Type', 'application/atom+xml; charset=UTF-8')
        #web.header('Content-Type', 'text/xml')
        print render.feed(entries)

            
class StaticServerC:
    def GET(self, static_dir):
        try:
            static_file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(static_file_name))
            static_file = open('.' + web.ctx.path, 'rb').read()
            web.ctx.output = static_file
            print static_file_name, web.ctx.path
        except IOError:
            web.notfound()
            
urls = (
    '/(static)/.*', 'StaticServerC',
    '/(templates)/.*', 'StaticServerC',
    '/feed/?', 'FeedC',
    '/entry/(\d*)/?', 'EntryC',
    '/(\d+)/?', 'IndexC',
    '/?', 'IndexC',
    )
    
if __name__ == '__main__':
    web.run(urls, globals(), *config.middleware)
    
