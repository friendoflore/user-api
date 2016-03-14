import webapp2
from google.appengine.ext import ndb
import db_models
import json

class User(webapp2.RequestHandler):
	def post(self):
		"""
		Creates a User entity

		POST variables:
		username - Required. State name
		password - Required. User password
		description - Not required. Short user description (editable)
		state - Not required. User's state
		"""

		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return
		
		# Create a new user entity
		new_user = db_models.User()

		# Get all of the attribute values passed with the request
		username = self.request.get('username')
		password = self.request.get('password')
		description = self.request.get('description')

		# Store the attribute values in the new entity
		if username and password:
			new_user.username = username
			new_user.password = password
			new_user.description = description
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
			self.response.write(self.response.status_message)
			return

		# Store the new user entity
		key = new_user.put()

		# Output the new user that was stored in JSON
		out = new_user.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.state = 406
			self.response.status_message = "API only supports JSON"
			return

		# If an ID was provided in the request, get that single entity
		if 'id' in kwargs:

			# Get the user entity and store it in a variable as a JSON object
			out = ndb.Key(db_models.User, int(kwargs['id'])).get().to_dict()
			
			# Write the user entity identified by the ID
			self.response.write(json.dumps(out))
		
		# Else get all of the user entities and display their keys
		else:

			# Get all user entities
			q = db_models.User.query()

			# Store all of their keys as a list
			keys = q.fetch(keys_only=True)

			# Store all of the key IDs as a dictionary
			results = { 'keys' : [x.id() for x in keys]}

			# Write the list of keys
			self.response.write(json.dumps(results))

	def delete(self, **kwargs):
		# Limit to JSON support only
		if 'application/json' not in self.request.accept:
			self.response.state = 406
			self.response.status_message = "API only supports JSON"
			return

		# An ID is required in order to delete an entity
		if 'id' in kwargs:
			
			# Get the user entities by the ID provided
			del_key = ndb.Key(db_models.User, int(kwargs['id'])).get()
			
			# Delete the user entity
			del_key.key.delete()
			
			return
		else:
			self.response.state = 400
			self.response.status_message = "Invalid request"
			return

class UserSearch(webapp2.RequestHandler):
	def post(self):
		'''
		Search for users

		POST Body Variables:
		username - String. username
		password - String. User's password
		'''

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports JSON"
			return

		q = db_models.User.query()
		if self.request.get('username', None):
			q = q.filter(db_models.User.username == self.request.get('username'))

		userattempt = q.fetch()
		results = {}
		for x in userattempt:
			if (x.password == self.request.get('password')):
				results = {'key' : x.key.id()}

		self.response.write(json.dumps(results))


