from django.test import TestCase
from catalog.models import Author, Book


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name="John", last_name="Doe")

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        author = Author.objects.create(first_name="John", last_name="Doe")
        Book.objects.create(title="Test Book", author=author)

    def test_book_title(self):
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.title, "Test Book")
