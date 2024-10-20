from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Book, Author, BookInstance, Genre

# view written as a function
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    books_titles_containing = Book.objects.filter(title__icontains='the').count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres = Genre.objects.all().count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'books_titles_containing': books_titles_containing,
    }



    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# view written as a class
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'   # template variable that will represent the list of books in the template file book_list.html

    # Get 5 books containing the word'the' in the title
    # queryset = Book.objects.filter(title__icontains='the')[:5]

    #  A more flexible way to filter the books is to override the get_queryset(). No real benefit tho.
    def get_queryset(self):
        return Book.objects.filter(title__icontains='a')[:5]

    template_name = 'book_list.html'  # the template name/location

class BookDetailView(generic.DetailView):
    model = Book
    
# a class based view as a function if you don't want tp use the generic class-based view
# Version 1
# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})

# Version 2
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    paginate_10 = 10
    context_object_name = 'author_list'
    queryset = Author.objects.all().order_by('last_name')
    template_name = 'author_list.html'
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author})