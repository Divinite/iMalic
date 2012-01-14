# logout : remove the attribute 'user' of the session object
delattr(Session(),'user')
# redirect to the home page
raise HTTP_REDIRECTION,'index.py'
