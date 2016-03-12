import webapp2

app = webapp2.WSGIApplication([], debug=True)
app.router.add(webapp2.Route(r'/user', 'user.User'))
app.router.add(webapp2.Route(r'/user/<id:[0-9]+><:/?>', 'user.User'))
app.router.add(webapp2.Route(r'/user/search', 'user.UserSearch'))
app.router.add(webapp2.Route(r'/edit', 'edit.Edit'))
app.router.add(webapp2.Route(r'/edit/<user_id:[0-9]+><:/?>', 'edit.Edit'))