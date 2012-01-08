# set the attribute 'user' of the session object
so = Session()
so.user = request['user'][0]
# redirect to the home page
raise HTTP_REDIRECTION,"index.py"
