# Script (Python) "json_dumps"
# bind container=container
# bind context=context
# bind namespace=
# bind script=script
# bind subpath=traverse_subpath
# parameters=value
# title=
#


def quote(ch):
    ord_ch = ord(ch)
    if 0x20 <= ord(ch) <= 0x7E and ch not in ["\\", '"']:
        return ch
    else:
        assert 0 <= ord_ch <= 0xFFFF
        return "\\u%04x" % ord_ch


def json_dumps(v):
    if v is None:
        return "null"
    elif hasattr(v, "items"):  # dict
        return "{%s}" % ", ".join(
            "%s: %s" % (json_dumps(vk), json_dumps(vv)) for vk, vv in v.items()
        )
    elif hasattr(v, "encode"):  # string
        return '"%s"' % "".join(quote(ch) for ch in v)
    elif v in [True, False]:  # boolean
        return v and "true" or "false"
    elif hasattr(v, "imag"):  # number
        return str(v)
    else:
        raise ValueError("can't encode %r" % v)


return json_dumps(value)
