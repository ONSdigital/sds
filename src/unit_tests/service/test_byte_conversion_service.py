from unittest import TestCase
from unittest.mock import MagicMock
import pytest
import json
from services.shared.byte_conversion_service import ByteConversionService

class TestByteConversionService:
    
    def test_get_serialized_size(self):
        input = "cat"
        expected_size = 5
        assert expected_size == ByteConversionService.get_serialized_size(input) 

        
        input = {"key": "cat"}
        expected_size = 14
        assert expected_size == ByteConversionService.get_serialized_size(input) 

    def test_get_serialized_size_empty(self):
        input = {}
        expected_size = 2
        assert expected_size == ByteConversionService.get_serialized_size(input) 
