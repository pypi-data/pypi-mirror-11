# coding: utf-8
from apps.app.view import  *
# from sites.daoerp.apps.app.view import  *
from core.union import route

# routes = [
route( '/',         page,				'GET', 'page' )
route( '/db',       test_db,			'GET', 'test_db' )

route( '/ws',       ws,					'GET', 'ws' )
route( '/wsh',      ws_handler,			'GET', 'ws_handler' )

# route( '/page',   page2,	'GET' )
# ]

# routes = {
	# 'old_doc_blog10':  		('/rss.xml',					        get_rss,			'GET'),
	# 'rss':					('/rss',						        get_rss,			'GET'),
	# 'scripts':				('/scripts/',						    get_list_informer,	'GET'),
	# 'scripts1':				('/scripts',						    get_list_informer,	'GET'),
# }



