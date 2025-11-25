from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Author(models.Model):
    """Модель автора"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])


class Genre(models.Model):
    """Модель жанра"""

    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель книги"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        help_text="Введите краткое описание книги", default="Описание отсутствует"
    )
    isbn = models.CharField("ISBN", max_length=13)
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр книги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    """Модель экземпляра книги (копия книги в библиотеке)"""

    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    STATUS_CHOICES = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        blank=True,
        default="m",
        help_text="Доступность книги",
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        # безопасный __str__: если book отсутствует — вернём id, иначе покажем title
        if self.book:
            return f"{self.id} ({self.book.title})"
        return f"{self.id} (No book)"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
