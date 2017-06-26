# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import UserManager, User, Book, BookManager, Review, Author
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	if 'user' in request.session:
		return redirect(reverse('books'))
	else:
		return render(request, 'belt_app/index.html')

def login(request):
	if request.method == 'POST':
		login = User.objects.login(request.POST.copy())
		if isinstance(login, list):
			for item in login:
				messages.error(request, item)
			return redirect(reverse('index'))
		else:
			request.session['user'] = login.id
			return redirect(reverse('books'))
	else:
		return redirect(reverse('index'))

def register(request):
	if request.method == 'POST':
		register = User.objects.register(request.POST.copy())
		if isinstance(register, list):
			for item in register:
				messages.error(request, item)
			return redirect(reverse('index'))
		else:
			request.session['user'] = register.id
			return redirect(reverse('books'))
	else:
		return redirect(reverse('index'))

def books(request):
	if 'user' in request.session:
		user = User.objects.get(id = request.session['user'])
		recent_reviews = Review.objects.all().order_by('-updated_at')[:3]
		exclude_reviews = recent_reviews.values('book_reviewed')
		all_books = Book.objects.exclude(id__in=exclude_reviews).order_by('title')
		favorites = Book.objects.filter(favorites=user.id)
		context = {
			'name':user.alias,
			'recent':recent_reviews,
			'all_books':all_books,
			'favorites':favorites
		}
		return render(request, 'belt_app/books.html', context)
	else:
		messages.error(request, 'Log in or register first')
		return redirect(reverse('index'))

def new_review(request):
	authors = Author.objects.all().order_by('name')
	favorites = Book.objects.filter(favorites=request.session['user'])
	context = {
		'authors':authors,
		'favorites':favorites
	}
	return render(request, 'belt_app/add.html', context)

def add(request):
	if request.method == 'POST':
		new_book = Book.objects.add_book(request.POST.copy(), request.session['user'])
		if isinstance(new_book, list):
			for item in new_book:
				messages.error(request, item)
			return redirect(reverse('new_review'))
		else:
			authors = Author.objects.filter(books_written__id=new_book.id)
			reviews = Review.objects.filter(book_reviewed=new_book.id)
			context = {
				'book':new_book,
				'reviews':reviews,
				'authors':authors
			}
			return redirect('/books/'+str(new_book.id))

def book_review(request, book_id):
	book = Book.objects.get(id=book_id)
	reviews = Review.objects.filter(book_reviewed=book.id)
	authors = Author.objects.filter(books_written__id=book.id)
	favorites = Book.objects.filter(favorites=request.session['user'])
	context = {
		'book':book,
		'reviews':reviews,
		'authors':authors,
		'favorites':favorites
	}
	return render(request, 'belt_app/book_review.html', context)

def user(request, user_id):
	user = User.objects.get(id=user_id)
	friends = User.objects.filter(friends=user.id)
	myself = User.objects.get(id=request.session['user'])
	reviews = Review.objects.filter(reviewer=user.id)
	favorites = Book.objects.filter(favorites=user.id)
	unfavorites = Book.objects.exclude(favorites=user.id)
	context = {
		'user':user,
		'friends':friends,
		'myself':myself,
		'reviews':reviews,
		'favorites':favorites,
		'unfavorites':unfavorites
	}
	return render(request, 'belt_app/user.html', context)

def friend(request, friend_id):
	user = User.objects.get(id=request.session['user'])
	friend = User.objects.get(id=friend_id)
	user.friends.add(friend)
	origin = request.META['HTTP_REFERER']
	page = origin.replace('http://localhost:8000','')
	return redirect(page)

def remove_friend(request, friend_id):
	user = User.objects.get(id=request.session['user'])
	friend = User.objects.get(id=friend_id)
	user.friends.remove(friend)
	origin = request.META['HTTP_REFERER']
	page = origin.replace('http://localhost:8000','')
	return redirect(page)

def author(request, author_id):
	author = Author.objects.get(id=author_id)
	books_written = Book.objects.filter(written_by__id=author.id)
	other_authors = Author.objects.exclude(id=author_id)
	context = {
		'author':author,
		'books_written':books_written,
		'other_authors':other_authors
	}
	return render(request, 'belt_app/author.html', context)

def add_review(request, book_id):
	if request.method == 'POST':
		review = Review.objects.add_review(request.POST.copy(), request.session['user'], book_id)
		origin = request.META['HTTP_REFERER']
		page = origin.replace(request.META['HTTP_ORIGIN'], '')
		if isinstance(review,list):
			for item in review:
				messages.error(request,item)
			return redirect(page)
		else:
			return redirect(page)

def favorites(request, book_id):
	book = Book.objects.get(id=book_id)
	user = User.objects.get(id=request.session['user'])
	book.favorites.add(user)
	origin = request.META['HTTP_REFERER']
	page = origin.replace('http://localhost:8000','')
	return redirect(page)

def remove_favorite(request, book_id):
	book = Book.objects.get(id=book_id)
	user = User.objects.get(id=request.session['user'])
	book.favorites.remove(user)
	origin = request.META['HTTP_REFERER']
	page = origin.replace('http://localhost:8000','')
	return redirect(page)

def delete(request, review_id):
	review = Review.objects.get(id=review_id)
	review.delete()
	origin = request.META['HTTP_REFERER']
	page = origin.replace('http://localhost:8000','')
	return redirect(page)

def logout(request):
	request.session.pop('user')
	return redirect(reverse('index'))