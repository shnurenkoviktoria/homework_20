from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from polls.models import Author, Book
from polls.serializers import AuthorSerializer, BookSerializer


class BookTests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Book 1",
            author=self.author,
            genre="Fiction",
            publication_date="2022-01-01",
        )

    def test_get_all_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_by_id(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book 1")

    def test_update_book(self):
        url = reverse("book-update", kwargs={"pk": self.book.pk})
        data = {
            "title": "Updated Book",
            "genre": "Mystery",
            "publication_date": "2022-01-01",
            "author": self.author.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk).title, "Updated Book")
        self.assertEqual(Book.objects.get(pk=self.book.pk).genre, "Mystery")

    def test_create_book(self):
        url = reverse("book-create")
        data = {
            "title": "Book 2",
            "author": self.author.id,
            "genre": "Fantasy",
            "publication_date": "2023-06-01",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(title="Book 2").genre, "Fantasy")

    def test_delete_book(self):
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_get_all_authors(self):
        url = reverse("author-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_author_by_id(self):
        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")
