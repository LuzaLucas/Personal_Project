from rest_framework.test import APITestCase
from products.tests.test_products_base import ProductMixin
from django.urls import reverse


class ProductAPITestMixin(APITestCase, ProductMixin):
    def get_product_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('products:products-api-list')
        return api_url
    
    def get_product_api_list(self, reverse_result=None):
        api_url = self.get_product_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        userdata = {
            'username': username,
            'password': password
        }
        user = self.make_author(
            username=userdata.get('username'), # type: ignore
            password=userdata.get('password') # type: ignore
        )
        response = self.client.post(
            reverse('products:token_obtain_pair'), data={**userdata})
        
        return {
            'jwt_access_token': response.data.get('access'), # type: ignore
            'jwt_refresh_token': response.data.get('refresh'), # type: ignore
            'user': user,
        }
    
    def get_product_raw_data(self):
        category = self.make_category()
        return {
            'name': 'This is the name',
            'stock': 77,
            'price': '55',
            'description': 'This is the description',
            'category': category.id, # type: ignore
            'author': 1,
        }


class ProductAPITest(ProductAPITestMixin):    
    def test_product_api_list_return_status_code_200(self):
        response = self.get_product_api_list()
        self.assertEqual(response.status_code, 200)
    
    def test_product_api_list_loads_correct_number_of_products(self):
        wanted_number_of_products = 14
        self.make_product_in_batch(qtd=wanted_number_of_products)
        
        response_page1 = self.get_product_api_list()
        products_loaded1 = len(response_page1.data.get('results'))  # type: ignore
        self.assertEqual(products_loaded1, 10)
        
        response_page2 = self.get_product_api_list(
            f"{reverse('products:products-api-list')}?page=2")
        products_loaded2 = len(response_page2.data.get('results'))  # type: ignore
        self.assertEqual(products_loaded2, 4)
    
    def test_product_api_list_do_not_show_not_published_objects(self):
        products = self.make_product_in_batch(qtd=2)
        product_not_published = products[0]
        product_not_published.is_published = False
        product_not_published.save()
        
        response = self.get_product_api_list()
        self.assertEqual(len(response.data.get('results')), 1) # type: ignore
        
    def test_product_api_list_user_must_send_jwt_token_to_create_object(self):
        api_url = reverse('products:products-api-list')
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)
        
    def test_product_api_logged_user_can_create_a_product(self):
        product_raw_data = self.get_product_raw_data()
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        
        response = self.client.post(
            self.get_product_list_reverse_url(),
            data=product_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        self.assertEqual(response.status_code, 201)
        
        
        # # testing validation errors when creating a product (name field)
        # data = self.get_product_raw_data()
        # response = self.client.post(
        #     self.get_product_reverse_url(),
        #     data=data,
        #     HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        # )
        # data['name'] = ''
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(
        #     response.data.get('name')[0],
        #     'This field is required.'
        # )
        
    def test_product_api_logged_user_can_update_a_product(self):
        # arrange
        product = self.make_product()
        access_data = self.get_auth_data(username='test_patch')
        jwt_access_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        product.author = author # type: ignore
        product.save()
        
        # action
        wanted_new_name = f'New name, updated by {author.username}' # type: ignore
        response = self.client.patch(
            reverse('products:products-api-detail', args=(product.id,)), # type: ignore
            data={
                'name': wanted_new_name
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        
        # assertion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), wanted_new_name) # type: ignore
        