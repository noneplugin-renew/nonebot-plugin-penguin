# @file: pyh.py
# @purpose: a HTML tag generator
# @author: Emmanuel Turlay <turlay@cern.ch>

__doc__ = """The pyh.py module is the core of the PyH package. PyH lets you
generate HTML tags from within your python code.
See http://code.google.com/p/pyh/ for documentation.
"""
__author__ = "Emmanuel Turlay <turlay@cern.ch>"
__version__ = '$Revision: 63 $'
__date__ = '$Date: 2010-05-21 03:09:03 +0200 (Fri, 21 May 2010) $'

from sys import stdout
from . import tag
nOpen={}

nl = '\n'
doctype = '<!DOCTYPE html>\n'
charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'

def ValidW3C():
    out = tag.a(tag.img(src='http://www.w3.org/Icons/valid-xhtml10', alt='Valid XHTML 1.0 Strict'), href='http://validator.w3.org/check?uri=referer')
    return out

class PyH(tag.tagBase):
    tagname = 'html'
    
    def __init__(self, name='MyPyHPage'):
        self += tag.head()
        self += tag.body()
        self.attributes = dict(lang='zh')
        self.head += tag.title(name)

    def __iadd__(self, obj):
        if isinstance(obj, tag.head) or isinstance(obj, tag.body): self.addObj(obj)
        elif isinstance(obj, tag.meta) or isinstance(obj, tag.link): self.head += obj
        else:
            self.body += obj
            id=self.setID(obj)
            setattr(self, id, obj)
        return self

    def addJS(self, *arg):
        for f in arg: self.head += tag.script(type='text/javascript', src=f)

    def addCSS(self, *arg):
        for f in arg: self.head += tag.link(rel='stylesheet', type='text/css', href=f)
    
    def printOut(self,file=''):
        if file: f = open(file, 'w', encoding='UTF-8')
        else: f = stdout
        f.write(tag.doctype)
        f.write(self.render())
        f.flush()
        if file: f.close()