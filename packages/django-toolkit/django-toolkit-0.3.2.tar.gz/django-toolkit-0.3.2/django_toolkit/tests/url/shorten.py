from django.utils import unittest
from django_toolkit.url.shorten import shorten_url, netloc_no_www


class ShortenUrlTestCase(unittest.TestCase):

    @property
    def shorten_url(self):
        """
        Allow alternative method to be used so we can use the same tests for the templatetags.

        :return: shorten_url
        """
        return shorten_url

    def test_get_shorten_url(self):
        url = 'example012345678901234.com.au'
        url = self.shorten_url(url, 28)
        self.assertEquals(url, 'example012345...01234.com.au')

    def test_does_not_shorten_if_match_length(self):
        self.assertEquals(self.shorten_url('exampleasdf5678901234.com.au', 32), 'exampleasdf5678901234.com.au')

    def test_does_not_shorten_if_less_length(self):
        self.assertEquals(self.shorten_url('example.com.au', 32), 'example.com.au')

    def test_large(self):
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexample.com.au', 16), 'areally...com.au')
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexample.com.au/path/to/strip/', 16), 'areally...com.au')

    def test_large_even(self):
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexamplee.com.au', 16), 'areally...com.au')

    def test_large_odd_length(self):
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexamplee.com.au', 17), 'areally....com.au')

    def test_tld(self):
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexamplee.com', 32), 'areallylongsubd...ngexamplee.com')

    def test_no_tld(self):
        self.assertEquals(self.shorten_url('areallylongsubdomain.areallylongexampleecom12', 32), 'areallylongsubd...gexampleecom12')

    def test_no_www(self):
        self.assertEquals(self.shorten_url('www.example.com', 16), 'example.com')

    def test_www(self):
        self.assertEquals(self.shorten_url('www.example.com', 16, strip_www=False), 'www.example.com')

    def test_with_path(self):
        self.assertEquals(self.shorten_url('www.example.com/au', 32, strip_www=False, strip_path=False), 'www.example.com/au')
        self.assertEquals(self.shorten_url('www.example.com/au', 16, strip_path=False), 'example.com/au')
        self.assertEquals(self.shorten_url('www.example.com/au', 16, strip_www=False, strip_path=False), 'www.exa...com/au')
        self.assertEquals(self.shorten_url('www.example.com/au/page/n/', 16, strip_www=False, strip_path=False), 'www.exa...age/n/')
        self.assertEquals(self.shorten_url('www.example.com.au/au/page/n/', 16, strip_www=False, strip_path=False), 'www.exa...age/n/')
        self.assertEquals(self.shorten_url('http://www.example.com.au/au/page/n/', 32, strip_www=False, strip_path=False), 'www.example.com.au/au/page/n/')
        self.assertEquals(self.shorten_url('http://www.example.com.au/au/page/n/', 24, strip_www=False, strip_path=False), 'www.example...au/page/n/')

    def test_ellipsis(self):
        self.assertEquals(self.shorten_url('www.example.com/au', 32, strip_www=False, strip_path=False, ellipsis=True), 'www.example.com/au')
        self.assertEquals(self.shorten_url('www.example.com/au', 16, strip_path=False, ellipsis=True), 'example.com/au')
        self.assertEquals(self.shorten_url('www.example.com/au', 16, strip_www=False, strip_path=False, ellipsis=True), u'www.exa\u2026com/au')
        self.assertEquals(self.shorten_url('www.example.com/au/page/n/', 16, strip_www=False, strip_path=False, ellipsis=True), u'www.exa\u2026age/n/')
        self.assertEquals(self.shorten_url('www.example.com.au/au/page/n/', 16, strip_www=False, strip_path=False, ellipsis=True), u'www.exa\u2026age/n/')
        self.assertEquals(self.shorten_url('http://www.example.com.au/au/page/n/', 32, strip_www=False, strip_path=False, ellipsis=True), u'www.example.com.au/au/page/n/')
        self.assertEquals(self.shorten_url('http://www.example.com.au/au/page/n/', 24, strip_www=False, strip_path=False, ellipsis=True), u'www.example\u2026au/page/n/')


class NetlocNoWwwTestCase(unittest.TestCase):

    @property
    def netloc_no_www(self):
        """
        Allow alternative method to be used so we can use the same tests for the templatetags.

        :return: netloc_no_www
        """
        return netloc_no_www

    def test_netloc_no_www(self):
        self.assertEqual(
            self.netloc_no_www('http://example.com'),
            'example.com'
        )
        self.assertEqual(
            self.netloc_no_www('http://www.example.com'),
            'example.com'
        )
        self.assertEqual(
            self.netloc_no_www('http://www.example.com/asdf'),
            'example.com'
        )
        self.assertEqual(
            self.netloc_no_www('http://wwwjd.example.com/asdf'),
            'wwwjd.example.com'
        )
