from sys import modules

tags = ['html', 'body', 'head', 'link', 'meta', 'div', 'p', 'form', 'legend',
        'input', 'select', 'span', 'b', 'i', 'option', 'img', 'script',
        'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'fieldset', 'a', 'title', 'body', 'head', 'title', 'script', 'br', 'table',
        'ul', 'li', 'ol']

selfClose = ['input', 'img', 'link', 'br']

nl = '\n'
doctype = '<!DOCTYPE html>\n'
charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'


class tagBase(list):
    tagname = ''

    def __init__(self, *arg, **kw):
        self.attributes = kw
        if self.tagname:
            name = self.tagname
            self.isSeq = False
        else:
            name = 'sequence'
            self.isSeq = True
        self.id = kw.get('id', name)
        # self.extend(arg)
        for a in arg:
            self.addObj(a)

    def __iadd__(self, obj):
        if isinstance(obj, tagBase) and obj.isSeq:
            for o in obj:
                self.addObj(o)
        else:
            self.addObj(obj)
        return self

    def addObj(self, obj):
        if not isinstance(obj, tagBase):
            obj = str(obj)
        id = self.setID(obj)
        setattr(self, id, obj)
        self.append(obj)

    def setID(self, obj):
        if isinstance(obj, tagBase):
            id = obj.id
            n = len([t for t in self if isinstance(
                t, tagBase) and t.id.startswith(id)])
        else:
            id = 'content'
            n = len([t for t in self if not isinstance(t, tagBase)])
        if n:
            id = '%s_%03i' % (id, n)
        if isinstance(obj, tagBase):
            obj.id = id
        return id

    def __add__(self, obj):
        if self.tagname:
            return tagBase(self, obj)
        self.addObj(obj)
        return self

    def __lshift__(self, obj):
        self += obj
        if isinstance(obj, tagBase):
            return obj

    def render(self):
        result = ''
        if self.tagname:
            result = '<%s%s%s>' % (
                self.tagname, self.renderAtt(), self.selfClose()*' /')
        if not self.selfClose():
            for c in self:
                if isinstance(c, tagBase):
                    result += c.render()
                else:
                    result += c
            if self.tagname:
                result += '</%s>' % self.tagname
        result += '\n'
        return result

    def renderAtt(self):
        result = ''
        for n, v in self.attributes.items():
            if n != 'txt' and n != 'open':
                if n == 'cl':
                    n = 'class'
                result += ' %s="%s"' % (n, v)
        return result

    def selfClose(self):
        return self.tagname in selfClose


def TagFactory(name):
    class f(tagBase):
        tagname = name
    f.__name__ = name
    return f


thisModule = modules[__name__]

for t in tags:
    setattr(thisModule, t, TagFactory(t))
