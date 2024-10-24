from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('books/',  views.BookListView.as_view(), name ='books'), #view is implemented as a class. This is the recommended way to implement views in Django.
   path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), # the pattern for this URL is useful for displaying detailed information about a particular book.
   path('authors/', views.AuthorListView.as_view(), name='authors'),
   path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
   path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
   path('loaned/', views.LibrariansView.as_view(), name='all-borrowed'),
   
   # Warning: The generic class-based detail view expects to be passed a parameter named pk. If you're writing your own function view you can use whatever parameter name you like, or indeed pass the information in an unnamed argument.
]
