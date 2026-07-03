import pytest
from django.urls import reverse
from rest_framework import status
from apps.marketplace.models.product import Product, MarketplaceListing
from apps.authentication.models import User

@pytest.mark.django_db
class TestMarketplaceAPIs:
    def setup_method(self):
        self.trending_url = reverse('api_v1:tenant-marketplace-trending')
        self.featured_url = reverse('api_v1:tenant-marketplace-featured')
        
        self.product = Product.objects.create(name="CRM Pro", slug="crm-pro", code="crm-pro", status="PUBLISHED")
        self.listing = MarketplaceListing.objects.get(product=self.product)
        self.listing.is_trending = True
        self.listing.is_featured = True
        self.listing.save()

    def test_trending_products(self, client):
        response = client.get(self.trending_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) == 1
        assert data[0]["name"] == "CRM Pro"

    def test_featured_products(self, client):
        response = client.get(self.featured_url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert len(data) == 1
        assert data[0]["name"] == "CRM Pro"
