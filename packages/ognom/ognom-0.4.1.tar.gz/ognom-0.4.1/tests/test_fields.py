import unittest
from decimal import Decimal

import pytest

from ognom.fields import (
    DocumentField, URLField, ValidationError, HTTPField, DecimalField)
from tests.common import BaseDoc


class TestDocumentField(unittest.TestCase):
    def test_should_accept_document_class_as_model_class(self):
        field = DocumentField(BaseDoc)
        assert field.model_class == BaseDoc

    def test_should_accept_string_as_model_class(self):
        field = DocumentField('tests.common.BaseDoc')
        assert field.model_class == BaseDoc


class TestURLField(unittest.TestCase):

    def setUp(self):
        self.field = URLField()

    def test_validate_wrong_urls(self):
        wrong_urls = [
            'aaaaaaaa',
            'some.url.domain',
            '://somestring'
        ]
        for url in wrong_urls:
            self.assertRaises(ValidationError, self.field.validate, url)

    def test_validate_regular_url(self):
        valid_urls = [
            'http://some.domain.ru',
            'ftp://some.domain.ru',
            'http://some.domain.ru:8080',
            'http://some.domain.ru:8011/path',
            'http://some.domain.ru:9001/path&param1=value1',
        ]
        for url in valid_urls:
            self.assertIsNone(self.field.validate(url))


class TestHTTPField(unittest.TestCase):

    def setUp(self):
        self.field = HTTPField()

    def test_validate_wrong_urls(self):
        wrong_urls = [
            'aaaaaaaa',
            'some.url.domain',
            '://somestring',
            'ftp://some.domain.ru',
            'ftps://some.domain.ru'
        ]
        for url in wrong_urls:
            self.assertRaises(ValidationError, self.field.validate, url)

    def test_validate_regular_url(self):
        valid_urls = [
            'http://some.domain.ru',
            'https://some.domain.ru:8080',
            'http://some.domain.ru:8011/path',
            'https://some.domain.ru:9001/path&param1=value1',
        ]
        for url in valid_urls:
            self.assertIsNone(self.field.validate(url))


class TestDecimalField(unittest.TestCase):
    def setUp(self):
        self.field = DecimalField()

    def test_should_convert_to_string_when_storing(self):
        value = self.field.to_mongo(Decimal('3.14'))
        assert value == '3.14'
        value = self.field.to_mongo(Decimal('3.1415926535897932384'))
        assert value == '3.1415926535897932384'

    def test_should_restore_to_decimal(self):
        value = self.field.from_mongo('3.14')
        assert value == Decimal('3.14')
        value = self.field.from_mongo('3.1415926535897932384')
        assert value == Decimal('3.1415926535897932384')

    def test_should_accept_only_decimal(self):
        with pytest.raises(ValidationError):
            self.field.validate(10)
