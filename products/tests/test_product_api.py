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
    
    def get_product_raw_data(self, author_id):
        category = self.make_category()
        return {
            'name': 'This is the name',
            'stock': 77,
            'price': '55',
            'description': 'This is the description',
            'category': category.id, # type: ignore
            'author': author_id,
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
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')
        user = auth_data.get('user')
        product_raw_data = self.get_product_raw_data(author_id=user.id) # type: ignore
        
        response = self.client.post(
            self.get_product_list_reverse_url(),
            data=product_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )
        
        if response.status_code != 201:
            print(response.data)  # type: ignore
        
        self.assertEqual(response.status_code, 201)
        
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
        
    def test_product_api_logged_user_cant_update_a_product_he_doesnt_own(self):
        product = self.make_product()
        # creating a user that does not own the product
        another_user = self.get_auth_data(username='not_the_owner')
        jwt_another_user = another_user.get('jwt_access_token')
        
        # this is the user who owns the product
        owner_user = self.get_auth_data(username='test_patch')
        author = owner_user.get('user')
        product.author = author # type: ignore
        product.save()
        
        # "another_user" tries to update the product he doesn't owns
        response = self.client.patch(
            reverse('products:products-api-detail', args=(product.id,)), # type: ignore
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_another_user}'
        )
        
        # "another_user" is forbidden to update the product
        self.assertEqual(response.status_code, 403)
        
    # def test_validation_errors_when_creating_a_product(self):
    #     auth_data = self.get_auth_data()
    #     jwt_access_token = auth_data.get('jwt_access_token')
    #     user = auth_data.get('user')
    #     product_raw_data = self.get_product_raw_data(author_id=user.id) # type: ignore
        
    #     response = self.client.post(
    #         self.get_product_list_reverse_url(),
    #         data=product_raw_data,
    #         HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
    #     )
    #     product_raw_data['name'] = ''
        
    #     self.assertEqual(
    #         response.data.get('name')[0],
    #         'This field is required.'
    #     )
    

class LoggedInUserAPITest(ProductAPITestMixin, APITestCase):
    def test_logged_in_user_api_view(self):
        auth_data = self.get_auth_data()
        jwt_access_token = auth_data.get('jwt_access_token')

        response = self.client.get(
            reverse('products:products_api_me'),
            HTTP_AUTHORIZATION=f'Bearer {jwt_access_token}'
        )

        self.assertEqual(response.status_code, 200)

        expected_data = {
            "username": auth_data['user'].username,
            "first_name": auth_data['user'].first_name,
            "last_name": auth_data['user'].last_name,
            "email": auth_data['user'].email,
        }
        self.assertEqual(response.data, expected_data) # type: ignore
        