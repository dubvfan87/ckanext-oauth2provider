from __future__ import unicode_literals

import logging
import oauth2

from ckan import plugins
from ckan.plugins import toolkit as tk

from ckanext.oauth2provider.model import access_token, client, grant, refresh_token

log = logging.getLogger(__name__)

class Oauth2ProviderPlugin(plugins.SingletonPlugin):
	plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.IConfigurable)
	plugins.implements(plugins.IRoutes)
	plugins.implements(plugins.IActions)
	plugins.implements(plugins.IAuthFunctions)

	# IConfigurable
	def configure(self, config):
		# Create the tables if they don't exist
		client.client_table.create(checkfirst=True)
		grant.grant_table.create(checkfirst=True)
		access_token.access_token_table.create(checkfirst=True)
		refresh_token.refresh_token_table.create(checkfirst=True)

		# Ensure that a secret key has been set
		secret_key = config.get('ckanext.oauth2provider.secret_key', '')
		if not secret_key:
			raise RuntimeError(
				'ckanext.oauth2provider.secret_key is not configured and it must'
				' have a value. Please amend your .ini file.')

	# IConfigurer
	def update_config(self, config):
		tk.add_template_directory(config, 'templates')
		tk.add_public_directory(config, 'public')
		tk.add_resource('fanstatic', 'oauth2provider')

		# Add a new admin tab to ckan-admin
		tk.add_ckan_admin_tab(config, 'ckanext_oauth2provider',
								   'OAuth2 Provider')

	# IRoutes
	def before_map(self, route_map):
		controller = 'ckanext.oauth2provider.controllers.view:OAuth2ProviderController'

		route_map.connect('/oauth2/authorize', controller=controller,
			action='authorize')

		return route_map

	def after_map(self, route_map):
			return route_map

	# IActions
	def get_actions(self):
		from ckanext.oauth2provider.logic.action import token_create
		return {
			'oauth2provider_token_create': token_create
		}

	# IAuthFunctions
	def get_auth_functions(self):
		from ckanext.oauth2provider.logic.auth import token_create
		return {
			'oauth2provider_token_create': token_create
		}
