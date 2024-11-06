from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('books/',  views.BookListView.as_view(), name ='books'), #view is implemented as a class. This is the recommended way to implement views in Django.
   path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'), # the pattern for this URL is useful for displaying detailed information about a particular book.
   path('authors/', views.AuthorListView.as_view(), name='authors'),
   path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

# use the 'urlpattern +=' instead of just making one long list of url patterns. Better for readability
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('loaned/', views.LibrariansView.as_view(), name='all-borrowed'),  # Added for challenge
]

# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

# Add URLConf to create, update, and delete books
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

urlpatterns += [
    path('bookinstances/', views.BookInstanceDetailView.as_view(), name='book-instance-detail'),
]