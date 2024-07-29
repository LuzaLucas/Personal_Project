from selenium.webdriver.common.by import By

from .test_functional_base import ProductBaseFunctionalTest


class ProductHomePageFunctionalTest(ProductBaseFunctionalTest):
    def test_product_home_page_without_products_message(self):
        self.browser.get(self.live_server_url)
        
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No products have been added yet.', body.text)
