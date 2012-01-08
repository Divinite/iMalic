print "<h3>Simple portal</h3>"

so = Session()
if hasattr(so,'user'):
    print "User :", so.user
    print '<br><a href="logout.py">Logout</a>'
else:
    print '<a href="login.html">Login</a>'

print "<p>Your content here..."
