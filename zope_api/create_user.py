## Script (Python) "create_user"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
response =  request.response


request_key = request.form['api_key']
if request_key != container.ACL_MANAGER_API_KEY:
    response.setStatus(403)
    return "Api key is not valid"

username = request.form['username']
password = request.form['password']

if context.acl_users.getUser(username):
    response.setStatus(409)
    return 'Username already exists'
else:
    context.acl_users.userFolderAddUser(
            name=username,
            password=password,
            roles=[],
            domains=[]
    )
    return 'ok'
