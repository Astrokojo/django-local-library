import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse ,reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# view written as a function.
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
    
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'books_titles_containing': books_titles_containing,
        'num_visits': num_visits,
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
        return Book.objects.all().order_by('title')

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
    paginate_by = 10
    context_object_name = 'author_list'
    queryset = Author.objects.all().order_by('last_name')
    template_name = 'author_list.html'
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author': author})
    

    
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

class LibrariansView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan."""
    model = BookInstance
    template_name = 'catalog/librarian_view.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    

# form view written as a function.
    # if you just need a form to map the fields of a single model
    # it is easier to use the ModelForm helper class to create the form from your model
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
        
        # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
            
    context = {
        'form': form,
        'book_instance': book_instance,
        }
            
    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # fields = '__all__' is not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.add_book'
    
class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'
    
class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )
            
class BookInstanceDetailView(generic.DetailView):
    model = BookInstance
    
    def book_instance_detail_view(request, primary_key):
        book_instance = get_object_or_404(BookInstance, pk=primary_key)
        return render(request, 'catalog/book_instance_detail.html', context={'book_instance': book_instance})
    
import uuid

from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.


