from rest_framework import status


class TestDownload:
    URL_DOWNLOAD_SH_CART = '/api/recipes/download_shopping_cart/'

    def test_00_download_unauth(self, client):
        response = client.get(self.URL_DOWNLOAD_SH_CART)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_01_download_empty_cart(self, user_client):
        response = user_client.get(self.URL_DOWNLOAD_SH_CART)
        assert response.status_code == status.HTTP_204_NO_CONTENT
