from unittest import TestCase
from unittest.mock import MagicMock
import pytest
import json
from services.shared.byte_conversion_service import ByteConversionService

class TestByteConversionService:
    
    def test_get_serialized_size(self):
        obj = {"key": "value", "number": 123}
        expected_size = len(json.dumps(obj).encode('utf-8'))
        assert ByteConversionService.get_serialized_size(obj) == expected_size

        #
        obj = ["item1", "item2", "item3"]
        expected_size = len(json.dumps(obj).encode('utf-8'))
        assert ByteConversionService.get_serialized_size(obj) == expected_size

    def test_get_serialized_size_empty(self):
        obj = {}
        expected_size = len(json.dumps(obj).encode('utf-8'))
        assert ByteConversionService.get_serialized_size(obj) == expected_size

        obj = []
        expected_size = len(json.dumps(obj).encode('utf-8'))
        assert ByteConversionService.get_serialized_size(obj) == expected_size
