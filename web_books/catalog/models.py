from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Write book's genre",
        verbose_name="Book's genre",
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=20,
        help_text="Write book's language",
        verbose_name="Book's language",
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        help_text="Write author's name",
        verbose_name="Author's name",
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Write author's lastname",
        verbose_name="Author's lastname",
    )
    date_of_birth = models.DateField(
        help_text="Write author's date of birth",
        verbose_name="Author's date of birth",
        null=True,
        blank=True,
    )
    date_of_death = models.DateField(
        help_text="Write author's date of death",
        verbose_name="Author's date of death",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Write title",
        verbose_name="Book's title",
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.CASCADE,
        help_text="Write book's genre",
        verbose_name="Book's genre",
        null=True,
    )
    language = models.ForeignKey(
        "Language",
        on_delete=models.CASCADE,
        help_text="Write book's language",
        verbose_name="Book's language",
        null=True,
    )
    author = models.ManyToManyField(
        "Author",
        help_text="Write book's author",
        verbose_name="Book's author",
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Write book's summary",
        verbose_name="Annotation",
    )
    isbn = models.CharField(
        max_length=13,
        help_text="Should write 13 characters",
        verbose_name="ISBN",
    )

    def __str__(self):
        return self.title

    def absolute_url(self):
        """
        Function return URL to access a copy of a book
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Authors'


class Status(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Write status",
        verbose_name="Status",
    )

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        null=True,
    )
    inv_number = models.CharField(
        max_length=20,
        help_text="Write inventory number",
        verbose_name="Inventory number",
        null=True,
    )
    imprint = models.CharField(
        max_length=200,
        help_text="Write publisher and year of publishing",
        verbose_name="Publisher and year of publishing",
    )
    status = models.ForeignKey(
        'Status',
        on_delete=models.CASCADE,
        help_text="Change book's status",
        verbose_name="Status",
        null=True,
    )
    due_back = models.DateField(
        help_text="Write status end date ",
        verbose_name="Status end date",
        null=True,
        blank=True,
    )
    borrowed = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Customer',
        help_text='Choose customer'
    )

    def __str__(self):
        return '%s %s %s' % (self.inv_number, self.book, self.status)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
