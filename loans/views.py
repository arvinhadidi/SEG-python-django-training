from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import View
from django.views.generic.edit import FormView
import random

from loans.models import Book
from loans.forms import BookForm

ITEMS_PER_PAGE = 25

SLOGAN_LIST = [
	"Having fun isn't hard when you've got a library card.",
	"Libraries make shhh happen.",
	"Believe in your shelf.",
	"Need a good read? We’ve got you cover to covered.",
	"Check us out. And maybe one of our books too.",
	"Get a better read on the world.",
]

def welcome(request):
	context = {'slogan': random.choice(SLOGAN_LIST)}
	return render(request, 'welcome.html', context)

def list_books(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    context = {'page_object': page_object}
    return render(request, 'books.html', context)

def get_book(request, book_id):
	try:
		context = {'book': Book.objects.get(id=book_id)}
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 
	else:
		return render(request, 'book.html', context)

def update_book(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 

	if request.method == "POST":
		form = BookForm(request.POST, instance=book)
		if form.is_valid():
			try:
				book = form.save()
			except:
				form.add_error(None, "It was not possible to save this book to the database.  Check the ISBN number.")
			else:
				messages.info(request, f"Updated book record to: {book}")
				path = reverse('list_books')
				return HttpResponseRedirect(path)
	else:
		form = BookForm(instance=book)
	return render(request, 'update_book.html', {'book_id': book_id, 'form': form})

def delete_book(request, book_id):
	try:
		book = Book.objects.get(id=book_id)
	except Book.DoesNotExist:
		raise Http404(f"Could not find book with primary key {book_id}") 

	if request.method == "POST":
		book.delete()
		path = reverse('list_books')
		return HttpResponseRedirect(path)
	else:
		return render(request, 'delete_book.html', {'book': book})
	
class CreateBookView(FormView):
    form_class = BookForm
    template_name = 'create_book.html'
    
    def form_valid(self, form):
        try:
            form.save()
        except:
            form.add_error(None, "It was not possible to save this book to the database.  Check the ISBN number.")
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('list_books')
