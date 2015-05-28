# -*- coding: utf-8 -*-
import time
import random
from SearchTag import SearchTag

class Liker:
	
	def __init__ ( self, min_interval, max_interval, configs ):

		
		self.min_interval		= min_interval
		self.max_interval		= max_interval
		self.configs			= configs

		print 'Liker object created'

	def str_to_boolean( self, s ):

		s = str( s )

		if s == 'True':
			# print 'True'
			return True

		elif s == 'False':
			# print 'False'
			return False

		else:
			raise ValueError # evil ValueError that doesn't tell you what the wrong value was

	# Like a media based in the media ID	
	def like_media ( self, config, media_id ):

		api = config.get_api() 
		api.like_media( media_id = media_id )

		seconds = random.randint( self.min_interval, self.max_interval ) # sorteia o tempo para a proxima acao

		# seconds = random.randint( 1, 2 ) # sorteia o tempo para a proxima acao
		print 'Wait %s seconds until next like' % seconds

		# Waits random time
		time.sleep( seconds )

	#
	def results_verifications ( self, search_tag, config, results ) :
	
		# print results
		# run through all the results
		for result in results:

			# checks if this result has tags
			if hasattr( result , 'tags' ):			
				
				# print getattr(result, 'tags', [])

				# tags from the current media
				media_id 			= result.id
				media_tags 			= result.tags
				media_user 			= str( result.user.username )
				media_link			= result.link

				is_from_client		= False
				has_liked 			= self.str_to_boolean( result.user_has_liked )
				has_ignored_user 	= False
				has_ignored_tag 	= False
				has_related_tag		= False

				print ''
				print 'tag: ' + search_tag.get_tag_name()
				print media_tags
				print 'user: ' + media_user
				# print 'liked: ' + str( has_liked )
				# print 'id: '  + str( media_id )
				print 'link: ' + media_link
				# print media_tags

				#TODO: try to find the related tags in the media description

				#TODO: translate se ainda nao dei like nessa foto e nao foi postada por mim e tiver se tiver alguma tagRelacionada para verificar
				# failed verification of the user... make some tests
				
				if media_user == config.get_config_user().get_client_user():
					# print 'is from client'
					is_from_client = True

				else: 
					# print 'isnt from client'
					is_from_client = False

				if is_from_client is False and has_liked is False and len( media_tags ) > 1 :

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
								if tag.name == ignored_tag:

									# has_ignored_tag is set to true
									has_ignored_tag = True

									print ' - This media has the %s excluded tag' % ignored_tag

						if has_ignored_tag is False:
							print ' - No ignored tag found'

					# if this media has not a excluded user and if this media has not a excluded user and the config has a list of related tags
					if has_ignored_user is False and has_ignored_tag is False and config.get_related_tags() is not None :

						print 'Starting related tags verification'

						# print config.get_related_tags()

						# run through all tags from this media
						for tag in media_tags :

							# run through all tags from this media
							for related_tag in config.get_related_tags():

								# checks if this string starts with an * 
								if related_tag[0] == '*':
									# print ' - Searching for substring'

									# remove the '*' from string to make the right commparison
									related_tag = related_tag[ 1 : len( related_tag ) ]

									# if the current related tag is a sub-string of the tag...
									# convert the tag to lower case to improve comparison
									if tag.name.lower().find( related_tag ) != -1:

										has_related_tag = True

										print ' - This media has the substring "%s" related tag' % related_tag 
										# break with this break things are supossed to go faster, but I think that wont be noticeble


								# if the current tag is listed in the related tags
								# convert the tag to lower case to improve comparison

								elif tag.name.lower() == related_tag :
								
									has_related_tag = True

									print ' - This media has the "%s" related tag' % related_tag 
									# break with this break things are supossed to go faster, but I think that wont be noticeble
						
						if has_related_tag is True:

							self.like_media( config, media_id )
							search_tag.likes = search_tag.likes + 1 


						if has_related_tag is not True:
							print ' - No related tag found'

					# if no related tag is defined, like all the media that has the current SearchTag and pass all other verifications
					elif has_ignored_user is False and has_ignored_tag is False:

						self.like_media( config, media_id )

						search_tag.likes = search_tag.likes + 1
					

				else:
					print "This media have already been liked, or was posted for me, or doesn't have more than 1 tag to bem compared"

			else:
				print "This media doesn't have any tags"

			search_tag.processed = search_tag.processed + 1
			

			# print 'Media processed: ' + str( media_processed )		
			print 'Media processed: ' + str( search_tag.processed )	

			# print 'Media liked: ' + str( media_liked )	
			print 'Media liked: ' + str( search_tag.likes )	

			print ''


	def make_likes ( self ):

		results_verifications = None

		# run through all configs
		for config in self.configs:
			
			print ''
			print 'Running config from %s' % config.get_config_user().get_client_user()
			print ''

			api = config.get_api()

			# run through all tags that must be searched
			for search_tag in config.get_search_tags():

				media_processed = 0
				media_liked		= 0	

				print ''
				print 'Searching for tag: %s ' % search_tag.get_tag_name()
				print '========================================================================================================='
				print ''

				# try to request media with the current tag
				# try:

				next_page = ''


				if search_tag.get_search_older() is True :

					print 'Searching for older results'
					print ''

					results, next_page = api.tag_recent_media( tag_name = search_tag.get_tag_name(), with_next_url = search_tag.get_next_page() )
					self.results_verifications( search_tag = search_tag, config = config, results = results )				
				
				else : 
					results, next_page = api.tag_recent_media( count = 20, max_tag_id = '', tag_name = search_tag.get_tag_name() )
					self.results_verifications( search_tag = search_tag, config = config, results = results )	


				while next_page and media_processed < config.get_max_iterations() :

					if search_tag.get_search_older() is True :

						results, next_page = api.tag_recent_media( tag_name = search_tag.get_tag_name(), with_next_url = search_tag.get_next_page() )
						self.results_verifications( search_tag = search_tag, config = config, results = results )				

					else:
						results, next_page = api.tag_recent_media( tag_name = search_tag.get_tag_name(), with_next_url = next_page )
						self.results_verifications( search_tag = search_tag, config = config, results = results )
					
					# print results
					print ''
					print "Remaining API Calls = %s/%s" % ( api.x_ratelimit_remaining, api.x_ratelimit )
					print ''

					


					search_tag.next_page = next_page

					print search_tag.next_page

						
					if media_liked == 0 :
						search_tag.search_older = True
						print ''
						print 'Searching for older tags next time'
						print ''

					else :
						search_tag.search_older = False



				# except Exception as e:
				# 	print ( e )
		
		while True:
			# TODO: salvar o último next_url de cada config para iniciar a próxima interação da última parada, mas isso só pode rolar se...
			# não der nenhum like nas últimas x iterações
			self.make_likes()



	