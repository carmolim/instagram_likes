# -*- coding: utf-8 -*-
import time
import random

class Liker:
	
	def __init__ ( self, min_interval, max_interval, configs ):

		
		self.min_interval		= min_interval
		self.max_interval		= max_interval
		self.configs			= configs

		print 'Liker object created'


	def like_media ( self, config, media_id ):

		api = config.get_api()

		api.like_media( media_id = media_id )

		seconds = random.randint( self.min_interval, self.max_interval ) # sorteia o tempo para a proxima acao
		print 'Wait %s seconds until next like' % seconds
		print " " 
		time.sleep( seconds ) # TODO: agora ele acha uma para dar like, da o like e espera e procura a proxima, trocar para procura para dar o like, da o like, acha a proxima para dar o like e dai espera




	def results_verifications ( self, config, results, media_processed, media_liked ) :

		# run through all the results
		for result in results:

			# tags from the current media
			media_id 			= result.id
			media_tags 			= result.tags
			media_user 			= result.user.username
			media_link			= result.link
			has_ignored_user 	= False
			has_ignored_tag 	= False
			has_related_tag		= False

			
			print 'user: ' + media_user
			# print 'id: '   + str( media_id )
			print 'link: ' + media_link
			# print media_tags

			# se ainda nao dei like nessa foto e nao foi postada por mim e tiver se tiver alguma tagRelacionada para verificar
			if media_user is not config.get_config_user().get_client_user() and result.user_has_liked is False and len( media_tags ) > 1 :

				# if the config has a list of ignored users
				if config.get_ignored_users() is not None :
					print 'Starting ignored user verification'

					# run through all excluded users listed in the config
					for ignored_user in config.get_ignored_users():

						# if this media was posted by some excluded user
						if media_user == ignored_user:

							# has_ignored_user is set to true
							has_ignored_user = True
							print 'This media has an ignored user'
							print ''

					if has_ignored_user is False:
						print ' - No ignored user found'


				# if this media wasn't posted by an excluded user and the config has a list of ignored tags
				if has_ignored_user is False and config.get_ignored_tags() is not None :

					print 'Starting ignored tags verification'

					# run through all tags from this media
					for tag in media_tags :

						# run through all related tags from this config
						for ignored_tag in config.get_ignored_tags():

							# if the current tag is listed in the ignored tags
							if tag == ignored_tag:

								# has_ignored_tag is set to true
								has_ignored_tag = True

								print 'This media has the %s excluded tag' % ignored_tag

					if has_ignored_tag is False:
						print ' - No ignored tag found'

				# if this media has not a excluded user and if this media has not a excluded user and the config has a list of related tags
				if has_ignored_user is False and has_ignored_tag is False and config.get_related_tags() is not None :

					print 'Starting related tags verification'

					# print  config.get_related_tags()

					# run through all tags from this media
					for tag in media_tags :

						# run through all tags from this media
						for related_tag in config.get_related_tags():

							# if the current tag is listed in the related tags
							if tag.name == related_tag :
							
								has_related_tag = True

								print ' - This media has the "%s" related tag' % related_tag 
								# like this media
					
					if has_related_tag is True:

						self.like_media( config, media_id )
						media_liked += 1


					if has_related_tag is not True:
						print ' - No related tag found'


			else:
				print ''
				print 'Essa foto já foi curtida, ou foi postada por mim ou não tem mais nenhuma tag para ser comparada'

			media_processed += 1		
			
			return media_processed, media_liked



	def make_likes ( self ):

		results_verifications = None

		# run through all configs
		for config in self.configs:

			media_processed = 0
			media_liked		= 0

			print 'Running config from %s' % config.get_config_user().get_client_user()
			print ''

			api = config.get_api()

			# run through all tags that must be searched
			for search_tag in config.get_search_tags():
				print ''
				print 'Searching for tag: %s' % search_tag
				print ''

				#  try to request media with the current tag
				try:
					results, next = api.tag_recent_media( count = 20, max_tag_id = '', tag_name = search_tag )

					media_processed, media_liked = self.results_verifications( config = config, results = results, media_processed = media_processed, media_liked = media_liked )
					print 'Media processed: ' + str( media_processed )		
					print 'Media liked: ' + str( media_liked )	
					print''	


					while next:

						results, next = api.tag_recent_media( tag_name = search_tag, with_next_url = next )
						media_processed, media_liked  = self.results_verifications( config = config, results = results, media_processed = media_processed, media_liked = media_liked  )
						print 'Media processed: ' + str( media_processed )		
						print 'Media liked: ' + str( media_liked )	
						print''	


				except Exception as e:
					print ( e )
			print ''
			print "Remaining API Calls = %s/%s" % ( api.x_ratelimit_remaining, api.x_ratelimit )
			print ''



	