from django.test import TestCase
from django.urls import reverse

import datetime

from loans.forms import BookForm
from loans.models import Book

INVALID_BOOK_ID = 0

class DeleteBookTestCase(TestCase):
	def setUp(self):
		self.book = Book.objects.create(
			authors="Doe, J.",
			title="A title",
			publication_date=datetime.datetime(2024,9,1),
			isbn="1234567890123",
		)
		self.url = reverse('delete_book', kwargs={'book_id': self.book.id})

	def test_delete_book_url(self):
		self.assertEqual(self.url, f'/delete_book/{self.book.id}')

	def test_get_delete_book(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'delete_book.html')

	def test_get_delete_book_with_invalid_pk(self):
		invalid_url = reverse('delete_book', kwargs={'book_id': INVALID_BOOK_ID})
		response = self.client.get(invalid_url)
		self.assertEqual(response.status_code, 404)

	def test_post_with_valid_id(self):
		book_id = self.book.id
		before_count = Book.objects.count()
		response = self.client.post(self.url, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count-1)
		expected_redirect_url = reverse('list_books')
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		try:
			book = Book.objects.get(pk=book_id)
		except Book.DoesNotExist:
			pass
		else:
			self.fail("Book should have been removed after deletion.")

	def test_post_with_invalid_pk(self):
		invalid_url = reverse('delete_book', kwargs={'book_id': INVALID_BOOK_ID})
		before_count = Book.objects.count()
		response = self.client.post(invalid_url, follow=True)
		after_count = Book.objects.count()
		self.assertEqual(after_count, before_count)
		self.assertEqual(response.status_code, 404)