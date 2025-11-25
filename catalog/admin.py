from django.contrib import admin
from .models import Genre, Book, Author, BookInstance


# Простая регистрация моделей
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")
    fieldsets = (
        (None, {"fields": ("book", "imprint")}),  # убрали 'id'
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )
