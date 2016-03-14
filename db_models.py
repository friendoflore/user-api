from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class User(Model):
	username = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	description = ndb.StringProperty()
	state = ndb.StringProperty()