import pytest

from .models import Products

from datetime import date

from django.urls import reverse

@pytest.mark.django_db
def test_book_creation():
    """Test that the Products model works correctly."""
    book = Products.objects.create(
        name="Test Products", 
        description="Test Author", 
        price=223,
        inventory_count = 45,
        category =  "book"
    )
    name="Test Products", 
    description="Test Author", 
    price=223,
    inventory_count = 45,
    category =  "book"

@pytest.mark.django_db
def test_book_list_view(client):
    """Test the book list view."""
    book1 = Products.objects.create(name="Products 1", description="Author 1", price=55,inventory_count=44,category="pen")
    book2 = Products.objects.create(name="Products 2", description="Author 2", price=55,inventory_count=44,category="pen")
    
    url = reverse('get_product')  # Assuming URL is named 'book_list'
    response = client.get(url)
    
    assert response.status_code == 200
    assert "Products 1" in response.content.decode()
    assert "Products 2" in response.content.decode()
