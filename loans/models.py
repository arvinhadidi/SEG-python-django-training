from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

class Book(models.Model):
	authors = models.CharField(
		max_length=255,
		validators=[MinLengthValidator(4)]
	)
	title = models.CharField(max_length=255)
	publication_date = models.DateField()
	isbn = models.CharField(
		max_length=13,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'^\d{10}(\d{3})?$', 
				message="An ISBN number must consist of either 10 or 13 digits."
			)
		]
	)

	def __str__(self):
		return(f"{self.authors}  ({self.publication_date.year})  \"{self.title}\"  ISBN {self.isbn}.")
