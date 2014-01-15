## Script (Python) "json_dumps"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=value
##title=
##
def quote(ch):
    ord_ch = ord(ch)
    if 0x21 <= ord(ch) <= 0x7e and ch not in ['\\', '"']:
        return ch
    else:
        assert 0 <= ord_ch <= 0xffff
        return '\\u%04x' % ord_ch


def json_dumps(v):
    if v is None:
        return 'null'
    elif hasattr(v, 'items'):  # string
        return '{%s}' % ', '.join('%s: %s' % (json_dumps(vk), json_dumps(vv)) for vk, vv in v.items())
    elif hasattr(v, 'encode'):  # dict
        return '"%s"' % ''.join(quote(ch) for ch in v)
    else:
        raise ValueError("can't encode %r" % v)


return json_dumps(value)
