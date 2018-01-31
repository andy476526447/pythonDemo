#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orm
from models import User,Blog,Comment
import asyncio

#获取EventLoop
loop = asyncio.get_event_loop()

#测试添加User
async def test_insert_user():
	await orm.create_pool(loop = loop ,user='www-data',password='www-data',db='awesome')
	u = User(admin = False,name = 'Test',email = 'test3@qq.com',passwd = '1234567890',image = 'about:blank')
	await u.save()

#执行异步io
loop.run_until_complete(test_insert_user())