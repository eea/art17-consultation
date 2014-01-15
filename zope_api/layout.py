## Script (Python) "layout"
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

return container.json_dumps({
    'standard_html_header': context.standard_html_header(context, request, response),
    'standard_html_footer': context.standard_html_footer(context, request, response),
})
