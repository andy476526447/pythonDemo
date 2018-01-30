#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
class Hello(object):
	def hello(self,name = 'word'):
		print('Hello,%s.' % name)
'''

'''
#利用metaclass动态创建类
def fn(self,name='world'):
	print('Hello, %s.' % name)
#使用type创建类的三个参数
#1.类名
#2.父类组成的tuple
#3.将类的方法名与函数绑定
Hello = type('Hello',(object,),dict(hello=fn))

h = Hello()
h.hello()
print(type(Hello))
print(type(h))
'''

'''
#利用metaclass动态修改类功能
class ListMetaclass(type):
	def __new__(cls,name,bases,attrs):
		attrs['add'] = lambda self,value:self.append(value)
		return type.__new__(cls,name,bases,attrs)

class MyList(list,metaclass=ListMetaclass):
	pass

L = MyList()
L.add(1)
print(L)
'''

#用metaclass创建出类，再由类创建实例。可以把类看成是metaclass创建出来的实例
#如下为一个ORM框架
class Field(object):
	
	def __init__(self,name,column_type):
		self.name = name
		self.column_type = column_type
	
	def __str__(self):
		return '<%s:%s>' % (self.__class__.__name__,self.name)
	
class StringField(Field):
	def __init__(self,name):
		super(StringField,self).__init__(name,'varchar(100)')

class IntegerField(Field):
	def __init__(self,name):
		super(IntegerField,self).__init__(name,'bigint')

class ModelMetaclass(type):
	#cls 当前准备创建的类的对象
	#name 类的名字
	#类继承的父类集合
	#类的方法和属性集合
	def __new__(cls,name,bases,attrs):
		print('[ModelMetaclass][__new__]=========================')
		print('cls=',cls)
		print('name=',name)
		print('bases =',bases)
		print('arrts=',attrs)
		if name == 'Model':
			return type.__new__(cls,name,bases,attrs)
		print('Found model: %s' % name)
		mappings = dict()
		for k,v in attrs.items():
			if isinstance(v,Field):
				print('Found mapping: %s ==> %s' % (k,v))
				mappings[k] = v
		#清空attrs
		for k in mappings.keys():
			attrs.pop(k)
		attrs['__mappings__'] = mappings #保存属性和列的映射关系
		attrs['__table__'] = name #假设表明和类名一致
		return type.__new__(cls,name,bases,attrs)

class Model(dict,metaclass=ModelMetaclass):
	def __init__(self,**kw):
		super(Model,self).__init__(**kw)
		print('[Model][__init__] kw',kw)
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute `%s`" % key)
	def __setattr__(self,key,value):
		self[key] = value
	
	def save(self):
		fields = []
		params = []
		args = []
		for k,v in self.__mappings__.items():
			print('[Model][save]',k,v)
			fields.append(v.name)
			params.append('?')
			args.append(getattr(self,k,None))
		sql = 'insert into %s (%s) values (%s)' % (self.__table__,','.join(fields),','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % str(args))
		
class User(Model):
	# 定义类的属性到列的映射
	id = IntegerField('id')
	name = StringField('username')
	email = StringField('email')
	password = StringField('password')
	def __str__(self):
		return '[User]id=%s,name=%s,email=%s,password=%s' % (self.id,self.name,self.email,self.password)

#创建一个实例:
u = User(id=12345,name ='Andy',email = 'test@qq.com',password='hahaha')
print(u)
u.save()