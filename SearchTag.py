# -*- coding: utf-8 -*-
from instagram import client
from instagram.client import InstagramAPI


class SearchTag:

	def __init__( self, tag ):

		self.likes			= 0
		self.processed		= 0
		self.search_tag		= tag
		self.next_page		= None
		self.search_older	= False

		print 'SearchTag object created'
		print ''


	def set_next_page ( next_page ):
		self.next_page = next_page

	def set_search_older ( boolean ):
		self.search_older = boolean

	def set_likes( n ):
		self.likes = n

	def set_processed( n ):
		self.processed = n




	def get_tag_name ( self ):
		return self.search_tag

	def get_next_page ( self ):
		return self.next_page

	def get_search_older ( self ):
		return self.search_older

	def get_likes ( self ):
		return self.likes
	
	def get_processed ( self ):
		return self.processed


	def processed(self):
		self.processed = self.processed + 1






