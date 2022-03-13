import uuid
from django.db import models
from django.urls import reverse

# Create your models here.


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-details', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200, help_text='Enter a book genre(eg. Horror)')

    def __str__(self) -> str:
        """String for representing model object"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)"""
    title = models.CharField(
        max_length=200, help_text='Book Title (eg. The Alchemist)')
    # assuming for each book there is only one author.
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Enter brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genres = models.ManyToManyField(
        Genre, help_text='Select Genres for this book')

    def __str__(self) -> str:
        """String representation of Book object"""
        return self.title

    def get_absolute_url(self):
        return reverse('book-details', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=100)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availiblity'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self) -> str:
        return f'{self.id} {self.book.title}'
