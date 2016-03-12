import webapp2
from google.appengine.ext import ndb
import db_models

class Edit(webapp2.RequestHandler):
	def post(self):
		'''
		Edit user by ID

		POST Body Variables:
		username - String. username
		description - String. User's description
		State - User's US State
		'''

		user_id = self.request.get('user_id')

		user = db_models.User.get_by_id(int(user_id))

		updateUser = self.request.get('username')
		updateDescription = self.request.get('description')
		updateState = self.request.get('state')

		if updateUser:
			user.username = self.request.get('username')
		if updateDescription:
			user.description = self.request.get('description')
		if updateState:
			user.state = self.request.get('state')
		
		user.put()

		return

	def delete(self, **kwargs):
		# Only the description may be deleted
		if 'user_id' in kwargs:
			user_id = kwargs['user_id']

			user = db_models.User.get_by_id(int(user_id))

			user.description = ""

			user.put()

		return