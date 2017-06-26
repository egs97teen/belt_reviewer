# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import datetime
import dateutil.relativedelta
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, userData):
		messages = []

		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'first_name':'First name',
					'last_name':'Last name',
					'alias':'Alias',
					'email':'Email',
					'password':'Password',
					'confirm_pw':'Confirmation password',
					'birthday':'Birthday'
				}
				messages.append(fields[field]+' must be filled in')

		if len(userData['first_name']) < 2:
			messages.append('First name must be at least two characters long')

		if len(userData['last_name']) < 2:
			messages.append('Last name must be at least two characters long')

		if userData['first_name'].isalpha() == False or userData['last_name'].isalpha() == False:
			messages.append('Name must only contain letters')

		if not EMAIL_REGEX.match(userData['email']):
			messages.append('Must enter a valid email')

		try:
			User.objects.get(email=userData['email'])
			messages.append('Email already registered')
		except:
			pass

		if len(userData['password']) < 8:
			messages.append('Password must be at least eight characters long')

		if re.search('[0-9]', userData['password']) is None:
			messages.append('Password must contain at least one number')

		if re.search('[A-Z]', userData['password']) is None:
			messages.append('Password must contain at least one capital letter')

		if userData['password'] != userData['confirm_pw']:
			messages.append('Password and confirmation password must match')

		if userData['birthday']:
			birthday = datetime.datetime.strptime(userData['birthday'], '%Y-%m-%d')
			now = datetime.datetime.now()
			age = dateutil.relativedelta.relativedelta(now, birthday)

			if birthday > now:
				messages.append('Pick a date in the past')
			if age.years < 18:
				messages.append('Must be at least 18 years old to register')

		if len(messages) > 0:
			return messages
		else:
			hashed_pw = bcrypt.hashpw(userData['password'].encode(), bcrypt.gensalt())
			new_user = User.objects.create(first_name=userData['first_name'], last_name=userData['last_name'], alias=userData['alias'], email=userData['email'], hashed_pw=hashed_pw, birthday=userData['birthday'])
			return new_user

	def login(self, userData):
		messages = []

		for field in userData:
			if len(userData[field]) == 0:
				fields = {
					'login_email':'Email',
					'login_password':'Password'
				}
				messages.append(fields[field]+' must be filled in')

		try:
			user = User.objects.get(email=userData['login_email'])
			encrypted_pw = bcrypt.hashpw(userData['login_password'].encode(), user.hashed_pw.encode())
			if encrypted_pw == user.hashed_pw:
				return user
			else:
				messages.append('Wrong password')
		except:
			messages.append('User not registered')

		if len(messages) > 0:
			return messages

class BookManager(models.Manager):
	def add_book(self, userData, user_id):
		messages = []

		if len(userData['title']) == 0:
			messages.append('Enter a title')

		try:
			test = userData['select_author']
			if len(userData['new_author']) != 0:
				messages.append('Either choose an author or enter a new one')
		except:
			if len(userData['new_author']) == 0:
				messages.append('Add an author')

		try:
			Author.objects.get(name=userData['new_author'])
			messages.append('Author already in database')
		except:
			pass

		try:
			Author.objects.get(name=userData['new_second'])
			messages.append('Author # 2 already in database')
		except:
			pass

		if len(userData['new_second']) != 0:
			if userData['new_second'] == userData['new_author']:
				messages.append('Do not enter the same author twice')

		try:
			first_author = userData['select_author']
			if first_author == userData['new_second']:
				messages.append('Do not enter the same author twice')
		except:
			pass
			
		try:
			second_author = userData['select_second']
			if second_author == userData['select_author']:
				messages.append('Do not enter the same author twice')
		except:
			pass

		try: 
			second_author = userData['select_second']
			if second_author == userData['new_author']:
				messages.append('Do not enter the same author twice')
		except:
			pass

		try:
			Book.objects.get(title=userData['title'])
			messages.append('Book already in database')
		except:
			pass

		if len(userData['review']) == 0:
			messages.append('Enter a review')

		if userData['rating'] == '':
			messages.append('Enter a rating')

		if len(messages) > 0:
			return messages
		else:
			user = User.objects.get(id=user_id)
			new_book = Book.objects.create(title=userData['title'])
			Review.objects.create(content=userData['review'], rating=userData['rating'], reviewer=user, book_reviewed=new_book)

			if len(userData['new_author']) != 0:
				author = Author.objects.create(name=userData['new_author'])
				author.books_written.add(new_book)
			else:
				author = Author.objects.get(name=userData['select_author'])
				author.books_written.add(new_book)

			if len(userData['new_second']) != 0:
				author2 = Author.objects.create(name=userData['new_second'])
				author2.books_written.add(new_book)

			try:
				test = userData['select_second']
				author2 = Author.objects.get(name=userData['select_second'])
				author2.books_written.add(new_book)
			except:
				pass

			return new_book

class ReviewManager(models.Manager):
	def add_review(self, userData, user_id, book_id):
		messages = []

		if len(userData['review']) == 0:
			messages.append('Enter an actual review')

		if userData['rating'] == '':
			messages.append('Enter a rating')

		user = User.objects.get(id=user_id)
		book = Book.objects.get(id=book_id)

		try:
			Review.objects.get(reviewer=user, book_reviewed=book)
			messages.append('You already reviewed this book')
		except:
			pass

		if len(messages) > 0:
			return messages
		else:
			user = User.objects.get(id=user_id)
			book = Book.objects.get(id=book_id)
			review = Review.objects.create(content=userData['review'], rating=userData['rating'], reviewer=user, book_reviewed=book)
			return review


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	hashed_pw = models.CharField(max_length=255)
	birthday = models.DateField()
	friends = models.ManyToManyField('self')
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Book(models.Model):
	title = models.CharField(max_length=255)
	favorites = models.ManyToManyField(User, related_name="favorited_by")
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BookManager()

class Review(models.Model):
	content = models.CharField(max_length=1000)
	rating = models.IntegerField()
	reviewer = models.ForeignKey(User)
	book_reviewed = models.ForeignKey(Book)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ReviewManager()

class Author(models.Model):
	name = models.CharField(max_length=255)
	books_written = models.ManyToManyField(Book, related_name="written_by")
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)