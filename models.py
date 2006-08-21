import os
import yaml
import web


# Model definitions
class Entry(yaml.YAMLObject):
    yaml_tag = u'!antrix.net,2006-05/tbEntry'

    def __init__(self, id, title, created, modified, content):
        self.id = id
        self.title = title
        self.created = created
        self.modified = modified
        self.content = content

    def __repr__(self):
        return '%s(id=%s, title="%s", created=%s, modified=%s, content="%s")' % (
               self.__class__.__name__, self.id, self.title, self.created,
               self.modified, self.content)
    
    def __cmp__(self, other):
        if self.modified:
            if other.modified:
                return cmp(self.modified, other.modified)
            else:
                return cmp(self.modified, other.created)
        else:
            if other.modified:
                return cmp(self.created, other.modified)
            else:
                return cmp(self.created, other.created)

class Blog:
    def __init__(self, blogfile):
        self._blogf = blogfile
        self._mtime = None
        
    @property
    def blog(self):
        if os.stat(self._blogf).st_mtime != self._mtime:
            self._mtime = os.stat(self._blogf).st_mtime
            d = yaml.load(file(self._blogf))
            d = web.Storage(d)
            d.author = web.Storage(d.author)
            d.entries.sort(reverse = True) #Latest first
            #d.entries.sort()
            self._blog = d
            
        return self._blog
        
    @property
    def entries(self):
        return self.blog.entries
    
    @property
    def author(self):
        return self.blog.author
    
    @property
    def title(self):
        return self.blog.title
    
    @property 
    def url(self):
        return self.blog.url
    
    @property 
    def tagline(self):
        return self.blog.tagline
    