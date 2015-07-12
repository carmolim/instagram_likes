# -*- coding: utf-8 -*-
import datetime
import time
import random
import langid



class Liker:
	
	def __init__ ( self, min_interval, max_interval, configs ):

		
		self.min_interval		= min_interval
		self.max_interval		= max_interval
		self.configs			= configs

		print 'Liker object created'

	def time_ago ( self, timestamp ):

		print 'date: ' + str( timestamp )
		timestamp = time.mktime(timestamp.timetuple())


		
		difference = 0.0

		day = 86400 # 24 * 60 * 60
		hour = 360 #60 * 60 
		now = int( time.time() )
		difference = now - timestamp
		# print 'timestamp: ' + str( timestamp )
		# print 'now: ' + str( now )
		# print 'difference: ' + str( difference )
		

		if difference >= day :

			days_ago  = difference / day

			if days_ago > 1 :
				return '%s days ago' % str( days_ago )

			else:
				return '1 day ago'


		else: 

			hours_ago = difference / hour

			if hours_ago > 1 :
				return '%s hours ago' % str( hours_ago )

			else:
				return '%s hour ago' % str( hours_ago )



		# difeference = now time stamp - timestamp
		# if difference > 1 day


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

		# try to like, sometimes I get a 429 api return (too many api requests), need to wait before do the like
		api.like_media( media_id = media_id )

		seconds = random.randint( self.min_interval, self.max_interval ) # sorteia o tempo para a proxima acao

		# seconds = random.randint( 1, 2 ) # sorteia o tempo para a proxima acao
		print 'Wait %s seconds until next like' % seconds

		# Waits random time
		time.sleep( seconds )


	def user_info ( self, config, user_id ) :

		api = config.get_api() 

		user_info = api.user( user_id )

		return user_info


	# checks if the passed text is from the language specified in the config object
	def media_lang ( self, config, text ):

		# find in wich language the text is written
		language = langid.classify( text )

		print language

		# runs through the listed langs in the config langs 
		for lang in config.get_langs() : 

			# checks if the resulted languangage is listed in the langs from config
			if lang == language[0] :
				
				# adds this threshold to the config
				if language[1] >= .8:
					
					return True

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
				media_user_id		= result.user.id 
				media_link			= result.link
				media_created		= result.created_time
				is_from_client		= False
				has_liked 			= self.str_to_boolean( result.user_has_liked )
				has_ignored_user 	= False
				has_ignored_tag 	= False
				has_related_tag		= False
				is_correct_lang		= False

				print ''
				print 'tag: ' + search_tag.get_tag_name()
				print media_tags
				print 'user: ' + media_user
				# print 'when: ' + self.time_ago( media_created )
				print 'when: ' + str( media_created )

				# print 'liked: ' + str( has_liked )
				# print 'id: '  + str( media_id )
				print 'link: ' + media_link
				# print media_tags

				#TODO: try to find the related tags in the media description
				
				if media_user == config.get_config_user().get_client_user():
					# print 'is from client'
					is_from_client = True

				else: 
					# print 'isnt from client'
					is_from_client = False

				# if this media is not form this client, and haven't been liked yet, and there is more than 1 #hashtag...
				if is_from_client is False and has_liked is False and len( media_tags ) > 1 :

					# if the config has a list of ignored users
					if config.get_ignored_users() is not None :
						print 'Starting ignored user verification'

						# run through all excluded users listed in the config
						for ignored_user in config.get_ignored_users():

							# checks if this string starts with an * 
							if ignored_user[0] == '*':
								# print ' - Searching for substring'

								# remove the '*' from string to make the right commparison
								ignored_user = ignored_user[ 1 : len( ignored_user ) ]

								# if the current related tag is a sub-string of the tag...
								# convert the tag to lower case to improve comparison
								if media_user.lower().find( ignored_user ) != -1:

									has_ignored_user = True

									print ' - This user has the substring "%s"' % ( ignored_user )
									#break # with this break things are supossed to go faster, but I think that wont be noticeble

							# if this media was posted by some excluded user
							elif media_user == ignored_user:

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

								# checks if this string starts with an * 
								if ignored_tag[0] == '*':
									# print ' - Searching for substring'

									# remove the '*' from string to make the right commparison
									ignored_tag = ignored_tag[ 1 : len( ignored_tag ) ]

									# if the current related tag is a sub-string of the tag...
									# convert the tag to lower case to improve comparison
									if tag.name.lower().find( ignored_tag ) != -1:

										has_ignored_tag = True

										print ' - This media has the substring "%s" in the tag: "%s" ' % ( ignored_tag, tag.name )
										#break # with this break things are supossed to go faster, but I think that wont be noticeble

								# if the current tag is listed in the ignored tags
								elif tag.name == ignored_tag:

									# has_ignored_tag is set to true
									has_ignored_tag = True

									print ' - This media has the %s excluded tag' % ignored_tag

						if has_ignored_tag is False:
							print ' - No ignored tag found'


					# if this media has not a excluded user and if this media has not a ignored tag and the config has a list of languages, and the media has a description
					if has_ignored_user is False and has_ignored_tag is False and config.get_langs() is not None and hasattr( result.caption, 'text' ) :

						media_description = result.caption.text
							
						print 'caption: ' + media_description
							
						is_correct_lang = self.media_lang( config, media_description )

						if is_correct_lang:
							print 'media is from correct language'

						else:
							print 'media isnt from correct language'

						
					# if this media has not a excluded user and if this media has not a ignored tag and the config has a list of related tags
					if has_ignored_user is False and has_ignored_tag is False and config.get_related_tags() is not None and is_correct_lang is True:

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

										print ' - This media has the substring "%s" in the tag: "%s" ' % ( related_tag, tag.name )
										#break # with this break things are supossed to go faster, but I think that wont be noticeble


								# if the current tag is listed in the related tags
								# convert the tag to lower case to improve comparison

								elif tag.name.lower() == related_tag :
								
									has_related_tag = True

									print ' - This media has the "%s" related tag' % related_tag 
									# break with this break things are supossed to go faster, but I think that wont be noticeble
						
						if has_related_tag is True:

							media_user_info = self.user_info( config, media_user_id )
							user_followers = media_user_info.counts['followed_by']
							print 'user followers: ' + str( user_followers )

							self.like_media( config, media_id )
							search_tag.likes = search_tag.likes + 1 

						if has_related_tag is not True:
							print ' - No related tag found'

					# if no related tag is defined, like all the media that has the current SearchTag and pass all other verifications
					elif has_ignored_user is False and has_ignored_tag is False and is_correct_lang is True:

						self.like_media( config, media_id )

						search_tag.likes = search_tag.likes + 1
					

				else:
					print "This media have already been liked, or was posted by me, or doesn't have more than 1 tag to bem compared"

			else:
				print "This media doesn't have any tags"


			search_tag.processed = search_tag.processed + 1
			

			print 'Media processed: ' + str( search_tag.processed )	

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


				while next_page and search_tag.processed < config.get_max_iterations() :

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

						
					if search_tag.processed == config.get_max_iterations() and search_tag.likes == 0:


						search_tag.search_older = True

						# reset the max iterations to search for older posts
						config.max_iterations = 0
						
						print ''
						print 'Searching for older tags next time'
						print ''

					else :
						search_tag.search_older = False

				# except Exception as e:
				# 	print ( e )
		
		while True:
			self.make_likes()



	