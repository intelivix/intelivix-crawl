# -*- coding: utf-8 -*-

import tldextract
import time
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common import by
from selenium.common import exceptions
from scrapy_venom.steps.browser import utils


class Popup(object):

    def __init__(self, browser, element, timeout):
        self.browser = browser
        self._current = None
        self._element = element
        self._timeout = timeout

    def __enter__(self):
        old_windows = self.window_handles
        elapsed = 0
        self._previous = self.current_window
        self._element.click()

        while not self._current:
            current = [x for x in self.window_handles if x not in old_windows]
            if current:
                self._current = current[0]
            else:
                time.sleep(2)
                elapsed += 2
                if elapsed > self._timeout:
                    raise exceptions.TimeoutException()

        self.switch_to_window(self._current)
        return self.browser

    def __exit__(self, type, value, traceback):
        if self._current in self.window_handles:
            self.switch_to_window(self._current)
            self.browser._driver.close()
        self.switch_to_window(self._previous)

    @property
    def current_window(self):
        return self.browser._driver.current_window_handle

    @property
    def window_handles(self):
        return self.browser._driver.window_handles

    def switch_to_window(self, window):
        return self.browser._driver.switch_to_window(window)


class Browser(object):
    """
    Class which facilitates the use of selenium

    """

    def __init__(self, webdriver):
        self._driver = webdriver()

    def get(self, url):
        """
        Access an url with a GET request

        """
        return self._driver.get(url)

    def get_element(self, xpath, many=False):
        """
        Find an element or many elements in the html by xpath

        """

        if many:
            return self._driver.find_elements_by_xpath(xpath)
        else:
            return self._driver.find_element_by_xpath(xpath)

    def set_cookies(self, cookies, domain=None):
        """
        Set the cookies for the current domain

        """
        for key, value in cookies.iteritems():
            cookie = {}
            cookie['name'] = key
            cookie['value'] = value
            cookie['domain'] = domain or self.get_domain()
            self._driver.add_cookie(cookie)

    def get_domain(self):
        """
        Returns the domain of current url

        """
        extracted = tldextract.extract(self._driver.current_url)
        if extracted.subdomain:
            return '{0.subdomain}.{0.domain}.{0.suffix}'.format(extracted)
        else:
            return '.{0.domain}.{0.suffix}'.format(extracted)

    def write(self, value, xpath=None, element=None,
              verify_read_only=False, clear_before=True):
        """
        Write method, generally used in <input type="text">

        Attributes:

            value               The value that will fill the input
            ...
            verify_read_only    If is True, verify if it's readonly before fill
            clear_before        If is True, will clear the input before fill

        """

        # Handling unicode errors
        if isinstance(value, str):
            value = value.decode('utf-8')

        if xpath:
            element = self.get_element(xpath)

        if not verify_read_only:
            if clear_before:
                element.clear()
            element.send_keys(value)
            return True

        elif not element.get_attribute('readonly'):
            if clear_before:
                element.clear()
            element.send_keys(value)
            return True

        return False

    def select(self, value, xpath=None, element=None, by_value=True):
        """
        Handle's the <select> tags

        Attributes:

            ...
            by_value    If it's True, the comparator will be the attribute
            value in the <select> tag, else will be the element inner text.

        """
        if xpath:
            element = self.get_element(xpath)

        if by_value:

            # Iterate's the <option> tags and compare the value attribute
            for option in element.find_elements_by_tag_name('option'):
                if utils.compare_strings(option.get_attribute('value'), value):
                    option.click()
                    return option.get_attribute('value')
        else:
            # Iterate's the <option> tags and compare the inner text
            for option in element.find_elements_by_tag_name('option'):
                if utils.compare_strings(option.text, value):
                    option.click()
                    return option.get_attribute('value')

        return False

    def wait_for_element(self, xpath, timeout=10):
        """
        Wait's until the element appear in the html

        """
        return ui.WebDriverWait(self._driver, 10).until(
            ec.presence_of_element_located((by.By.XPATH, xpath))
        )

    def open_popup(self, element, timeout=10):
        """
        Open a poup by clicking in the element

        Usage:
            with browser.open_popup():
                # do stuff

        """
        return Popup(self, element, timeout=timeout)

    def quit(self):
        """
        Closes the browser

        """
        return self._driver.quit()

    def refresh(self):
        """
        Refresh the browser

        """
        return self._driver.refresh()


class BrowserManager(object):
    """
    Manager to ensure that browser will quit at end of operations

    Usage:

        with BrowserManager() as browser:
            browser.write('//input', 'owww, works!')

    """

    def __init__(self, driver=None, webdriver=webdriver.Firefox):
        self._driver = driver
        self._webdriver = webdriver

    def __enter__(self):
        if not self._driver:
            self._driver = Browser(self._webdriver)
        return self._driver

    def __exit__(self, type, value, traceback):
        self._driver.quit()
