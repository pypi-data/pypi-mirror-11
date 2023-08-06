#!/usr/bin/env python
# coding: utf-8


import sys, os
assert sys.version >= '3.3', 'Please use Python 3.4 or higher.'

import asyncio
from aiohttp import web


import settings
sys.path.append(settings.root)
os.environ['TAO_PATH_ROOT'] = settings.root
path = os.path.dirname( __file__ )
sys.path.append( path )
# print (sys.path)
# os.chdir(path)

from tao1.core.union import init


loop = asyncio.get_event_loop()
loop.run_until_complete( init( loop ) )
try: loop.run_forever()
except KeyboardInterrupt:  pass 




