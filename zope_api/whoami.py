## Script (Python) "whoami"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=v
##title=
##
user = context.REQUEST.AUTHENTICATED_USER

return container.json_dumps({
    'user_id': user.getId(),
    'is_ldap_user': repr(user).startswith("<LDAPUser '"),
})
