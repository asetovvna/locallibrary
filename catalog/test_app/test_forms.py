from django.test import TestCase
from catalog.forms import AuthorForm, RenewBookForm
import datetime
from django.utils import timezone


class AuthorFormTest(TestCase):

    def test_form_valid_data(self):
        form = AuthorForm(data={"first_name": "John", "last_name": "Doe"})
        self.assertTrue(form.is_valid())

    def test_first_name_label(self):
        form = AuthorForm()
        self.assertTrue(
            form.fields["first_name"].label == "First name"
            or form.fields["first_name"].label is None
        )


class RenewBookFormTest(TestCase):

    def test_renew_book_form_valid_date(self):
        valid_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookForm(data={"renewal_date": valid_date})
        self.assertTrue(form.is_valid())

    def test_renew_book_form_invalid_past_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={"renewal_date": past_date})
        self.assertFalse(form.is_valid())

    def test_renew_book_form_invalid_future_date(self):
        future_date = datetime.date.today() + datetime.timedelta(weeks=5)
        form = RenewBookForm(data={"renewal_date": future_date})
        self.assertFalse(form.is_valid())
