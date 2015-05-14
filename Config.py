# -*- coding: utf-8 -*-
from instagram import client
from instagram.client import InstagramAPI
from SearchTag import SearchTag


class Config:

	def __init__( self, search_tags, related_tags, ignored_tags, ignored_users, config_user, max_iterations ):

		#TODO: how deep in old search it should go

		self.search_tags 			= []
		self.related_tags 			= None
		self.ignored_users 			= None
		self.ignored_tags 			= None
		self.config_user 			= config_user
		self.max_iterations			= max_iterations
		self.api 					= None

		if related_tags is not None:
			self.related_tags = related_tags

		if ignored_tags is not None:
			self.ignored_tags = ignored_tags

		if ignored_users is not None:
		 	self.ignored_users = ignored_users


		for search_tag in search_tags:

			temp_tag = SearchTag( search_tag )

			self.search_tags.append( temp_tag )

		try:
			self.api = client.InstagramAPI( access_token = self.config_user.get_access_token(), client_secret = self.config_user.get_client_secret() )
			
		except Exception as e:
			
			print(e)


		print 'Config object created'
		print ''

	def get_search_tags ( self ):
		return self.search_tags

	def get_related_tags ( self ):
		return self.related_tags

	def get_ignored_tags ( self ):
		return self.ignored_tags

	def get_ignored_users ( self ):
		return self.ignored_users

	def get_config_user ( self ):
		return self.config_user

	def get_max_iterations ( self ):
		return self.max_iterations

	def get_api ( self ):
		return self.api

	def user_name_to_user_id( self, user_list, api ):

		users_ids = []

		try:

			for user in user_list:

				api = client.InstagramAPI( access_token = self.config_user.get_access_token(), client_secret = self.config_user.get_client_secret() )

				user_search_tags = api.user_search( q=user )

				users_ids.append( user_search_tags[0].id )

				print "Remaining API Calls = %s/%s" % ( api.x_ratelimit_remaining, api.x_ratelimit )

		except Exception as e:

			print(e)

		return users_ids










