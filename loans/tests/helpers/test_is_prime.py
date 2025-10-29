from django.test import TestCase
from parameterized import parameterized

from loans.helpers import is_prime

class IsPrimeTestCase(TestCase):
	@parameterized.expand([
			("incorrect input type"),
			(-4),
			(0),
		])
	def test_is_prime_with_invalid_values(self, value):
		error_message = f"is_prime failed to raise a ValueError when called with input: {str(input)}"
		with self.assertRaises(ValueError, msg=f"is_prime failed to raise a ValueError when called with input: {input}"):
			is_prime(value)

	@parameterized.expand([
			(1, False),
			(2, True),
			(3, True),
			(4, False),
			(5, True),
			(7, True),
			(9, False),
			(11, True),
			(15, False),
			(27, False),
			(2017, True),
			(2117, False)
		])
	def test_is_prime_with_positive_integer(self, number, expected_result):
		actual_result = is_prime(number)
		self.assertEqual(expected_result, actual_result)
