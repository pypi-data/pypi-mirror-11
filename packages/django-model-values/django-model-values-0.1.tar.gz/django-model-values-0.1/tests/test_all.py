from django.db import models
from django.utils import timezone
from django_dynamic_fixture import G
import pytest
from .models import Book

pytestmark = pytest.mark.django_db


@pytest.fixture
def books():
    for quantity in (10, 10):
        G(Book, author='A', quantity=quantity)
    for quantity in (2, 1, 2):
        G(Book, author='B', quantity=quantity)
    return Book.objects.all()


def test_queryset(books):
    assert books.filter(id__ne=None).exists(5)
    assert set(books['author']) == {'A', 'B'}
    assert dict(books['id', 'author']) == {1: 'A', 2: 'A', 3: 'B', 4: 'B', 5: 'B'}

    assert len(books['quantity'] < 2) == 1
    assert len(books['quantity'] <= 2) == 3
    assert len(books['quantity'] > 2) == 2
    assert len(books['quantity'] >= 2) == 4
    assert len(books['quantity'] == 2) == 2
    assert len(books['quantity'] != 2) == 3

    quant = books['quantity']
    assert 10 in quant
    assert quant
    assert 10 in quant
    assert books[0] in books.all()
    assert ('A', 10) in books['author', 'quantity']

    now = timezone.now()
    assert books.filter(author='B').modify({'last_modified': now}, quantity=2) == 1
    assert len(books['last_modified'] == now) == 1
    assert books.filter(author='B').modify({'last_modified': timezone.now()}, quantity=2) == 0
    assert len(books['last_modified'] == now) == 1
    assert books.remove() == 5
    assert not books


def test_manager(books):
    assert 1 in Book.objects
    assert Book.objects[1]['id'][0] == 1
    assert Book.objects.update_rows(dict.fromkeys([3, 4, 5], {'quantity': 2})) == {4}
    assert 4 in (books['quantity'] == 2)['id']
    assert Book.objects.update_columns('quantity', dict.fromkeys([3, 4, 5], 1)) == {1: 3}
    assert len(books['quantity'] == 1) == 3


def test_aggregation(books):
    assert set(books['author',].annotate()) == {('A',), ('B',)}
    assert dict(books['author'].annotate(models.Max('quantity'))) == {'A': 10, 'B': 2}
    assert dict(books['author'].value_counts()) == {'A': 2, 'B': 3}

    assert books['author', 'quantity'].reduce(models.Max, models.Min) == ('B', 1)
    assert books['author', 'quantity'].min() == ('A', 1)
    assert books['quantity'].min() == 1
    assert books['quantity'].max() == 10
    assert books['quantity'].sum() == 25
    assert books['quantity'].mean() == 5.0


def test_functions(books):
    book = Book.objects[1]
    assert book['quantity'].first() == 10
    book['quantity'] += 1
    assert book['quantity'].first() == 11
    book['quantity'] -= 1
    assert book['quantity'].first() == 10
    book['quantity'] *= 2
    assert book['quantity'].first() == 20
    book['quantity'] /= 2
    assert book['quantity'].first() == 10
    book['quantity'] %= 7
    assert book['quantity'].first() == 3
    book['quantity'] **= 2
    assert book['quantity'].first() == 9
