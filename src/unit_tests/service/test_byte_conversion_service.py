from unittest import TestCase
from unittest.mock import MagicMock
import pytest
import json
from services.shared.byte_conversion_service import ByteConversionService
from src.test_data import dataset_test_data

class TestByteConversionService:
    
    def test_get_serialized_size(self):
        assert dataset_test_data.string_byte_size_cat == ByteConversionService.get_serialized_size(dataset_test_data.string_cat) 

    def test_get_serialized_size_empty(self):
        assert dataset_test_data.empty_dict_byte_size == ByteConversionService.get_serialized_size(dataset_test_data.empty_dict) 
