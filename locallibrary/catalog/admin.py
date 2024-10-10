from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(Genre)
# admin.site.register(BookInstance)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    
    # orients the fields,
    # vertically for the names and horizontally for the dates,
    # in the author's view on theadmin page
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model.
# Can't be moved outside the class' scope to top of admin.py.
admin.site.register(Author, AuthorAdmin)

# replace admin.TabularInline with admin.StackedInline for a vertical layout
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    # the attribute extra=0 removes the ability to add more instances as placeholders
    extra = 0

# Register the Admin classes for Book using the decorator.
# does the same thing as admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_status', 'display_expected_return_date', 'book')
    list_filter = ('status', 'due_back')

# Adds sections to the detail view of the book instance.
# First section has no title but second section is titled 'Availability'.
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
