from django import forms
from django.test import TestCase

import datetime

from loans.forms import BookForm
from loans.models import Book

class BookFormTestCase(TestCase):
	def setUp(self):
		self.form_input = {
			'authors': "Doe, J.",
			'title': "A title",
			'publication_date': datetime.datetime(2024,9,1),
			'isbn': "1234567890123",
		}

	def test_form_has_the_necessary_fields(self):
		form = BookForm()
		self.assertIn('authors', form.fields)
		self.assertIn('title', form.fields)
		self.assertIn('publication_date', form.fields)
		publication_date_field = form.fields['publication_date']
		self.assertTrue(isinstance(publication_date_field, forms.DateField))
		self.assertIn('isbn', form.fields)

	def test_valid_form(self):
		form = BookForm(data=self.form_input)
		self.assertTrue(form.is_valid())

	def test_blank_author_is_invalid(self):
		self.form_input['authors'] = ''
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_overlong_author_is_invalid(self):
		self.form_input['authors'] = 'x' * 256
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_overly_short_author_is_invalid(self):
		self.form_input['authors'] = "abc"
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_blank_title_is_invalid(self):
		self.form_input['title'] = ''
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_overlong_title_is_invalid(self):
		self.form_input['title'] = 'x' * 256
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_blank_publication_date_is_invalid(self):
		self.form_input['publication_date'] = None
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_non_date_publication_date_is_invalid(self):
		self.form_input['publication_date'] = 'invalid'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_blank_isbn_is_invalid(self):
		self.form_input['isbn'] = ''
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_overlong_isbn_is_invalid(self):
		self.form_input['isbn'] = "12345678901234"
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_10_digit_isbn_is_valid(self):
		self.form_input['isbn'] = '1234567890'
		form = BookForm(data=self.form_input)
		self.assertTrue(form.is_valid())

	def test_9_digit_isbn_is_invalid(self):
		self.form_input['isbn'] = '123456789'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_11_digit_isbn_is_invalid(self):
		self.form_input['isbn'] = '12345678901'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_12_digit_isbn_is_invalid(self):
		self.form_input['isbn'] = '123456789012'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_10_character_isbn_with_non_digit_is_invalid(self):
		self.form_input['isbn'] = '12345b7890'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_13_character_isbn_with_non_digit_is_invalid(self):
		self.form_input['isbn'] = '12345b7890123'
		form = BookForm(data=self.form_input)
		self.assertFalse(form.is_valid())

	def test_valid_form_can_be_saved(self):
		form = BookForm(data=self.form_input)
		before_count = Book.objects.count()
		form.save()
		after_count = Book.objects.count()
		self.assertEqual(before_count+1, after_count)