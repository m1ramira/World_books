from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import *
from django.views import generic
from django.shortcuts import render
from .models import Author, Book, BookInstance
from .form import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



def index(request):
    # count books and book instances
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    # count available books (status = 'in order')
    num_instance_available = BookInstance.objects.filter(status__exact=2).count()
    # count authors
    num_authors = Author.objects.all().count()

    # count of visit
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instance': num_instance,
            'num_instance_available': num_instance_available,
            'num_authors': num_authors,
            'num_visits': num_visits,
        }
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrowed=self.request.user).filter(status__exact='2').order_by('due_back')


def authors_add(request):
    author = Author.objects.all()
    authorform = AuthorsForm()
    return render(
        request,
        'catalog/authors_add.html',
        {'form': authorform, 'author': author}
    )


def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')


def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect('/authors_add/')
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Author isn't found</h2>")


def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add/')
    else:
        return render(request, 'edit1.html', {'author': author})


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
