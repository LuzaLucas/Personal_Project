# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from utils.browser import make_chrome_browser

import time


class ProductBaseFunctionalTest(LiveServerTestCase):
    def sleep(self, seconds=3):
        time.sleep(seconds)
        
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()