#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Andy Song'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

import logging

@get('/')
async def index(request):
	logging.info('[handlers.py][index]')
	summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	#users = await User.findAll()
	blogs = [
		Blog(id='1',name='Test Blog',summary = summary,created_at=time.time()-120),
		Blog(id='2',name='Something New',summary = summary,created_at=time.time()-3600),
		Blog(id='3',name='Learn Swift',summary = summary,created_at=time.time()-7200)
	]
	'''
	return {
		'__template__': 'test.html',
		'users': users
	}
	'''
	return {
		'__template__':'blogs.html',
		'blogs':blogs
	}

@get('/api/users')
async def api_get_users():
	users = await User.findAll(orderBy='created_at desc')
	for u in users:
		u.passwd = '********'
	logging.info('users= %s' % type(users))
	return dict(users)
	#return 'heheheh'