## Script (Python) "whoami"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=v
##title=
##
return container.json_dumps({
    'user_id': context.REQUEST.AUTHENTICATED_USER.getId(),
})
