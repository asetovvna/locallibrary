from django.test import TestCase
from django.urls import reverse
from catalog.models import Author


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Author.objects.create(first_name=f"John{i}", last_name="Doe")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/authors/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("authors"))
        self.assertTemplateUsed(response, "catalog/author_list.html")
