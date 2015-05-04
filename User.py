class User( object ):


	def __init__( self, client_user, client_id, access_token, client_secret ):
	
		self.client_user	= client_user
		self.client_id		= client_id
		self.access_token	= access_token
		self.client_secret	= client_secret

		print 'User %s created' % self.client_user
		print ''

	def get_client_user ( self ):
		return self.client_user

	def get_client_id ( self ):
		return self.client_id

	def get_access_token( self ):
		return self.access_token

	def get_client_secret ( self ):
		return self.client_secret

	def get_user_redirect_uri ( self ):
		return self.redirect_uri





