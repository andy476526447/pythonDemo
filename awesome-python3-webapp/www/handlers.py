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
	users = await User.findAll()
	return {
		'__template__': 'test.html',
		'users': users
	}