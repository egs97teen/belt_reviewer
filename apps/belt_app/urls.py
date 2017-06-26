from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'register$', views.register, name="register"),
  url(r'login$', views.login, name="login"),
  url(r'logout$', views.logout, name="logout"),
  url(r'books$', views.books, name="books"),
  url(r'books/add$', views.new_review, name="new_review"),
  url(r'add$', views.add, name="add"),
  url(r'^books/(?P<book_id>\d+)$', views.book_review, name="book_review"),
  url(r'^user/(?P<user_id>\d+)$', views.user, name="user"),
  url(r'^add_friend/(?P<friend_id>\d+)$', views.friend, name="add_friend"),
  url(r'^remove_friend/(?P<friend_id>\d+)$', views.remove_friend, name="remove_friend"),
  url(r'^author/(?P<author_id>\d+)$', views.author, name="author"),
  url(r'^add_review/(?P<book_id>\d+)$', views.add_review, name="add_review"),
  url(r'^favorites/(?P<book_id>\d+)$', views.favorites, name="favorites"),
  url(r'^remove/(?P<book_id>\d+)$', views.remove_favorite, name="remove_favorite"),
  url(r'^delete/(?P<review_id>\d+)$', views.delete, name="delete")
]