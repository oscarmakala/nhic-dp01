
import pytest
import pandas as pd
from decimal import Decimal
from datetime import datetime
from src.processors.data_processor import DataProcessor

@pytest.fixture
def sample_data():
    """Create sample test data."""
    transactions = [
        {
            "transaction_id": "T1",
            "product_id": "P1",
            "quantity": 10,
            "sale_price": Decimal("100.00"),
            "transaction_date": datetime.now()
        }
    ]
    
    products = [
        {
            "product_id": "P1",
            "category": "Electronics",
            "cost_price": Decimal("80.00"),
            "name": "Test Product"
        }
    ]
    
    return {"transactions": transactions, "products": products}

def test_input_validation(sample_data):
    """Test input data validation."""
    processor = DataProcessor()
    assert processor.validate_input_data(
        sample_data['transactions'], 
        sample_data['products']
    ), "Valid data should pass validation"

def test_negative_values(sample_data):
    """Test handling of negative values."""
    processor = DataProcessor()
    sample_data['transactions'][0]['quantity'] = -1
    
    with pytest.raises(ValueError):
        processor.process(sample_data)

def test_margin_calculation(sample_data):
    """Test profit margin calculations."""
    processor = DataProcessor()
    result = processor.process(sample_data)
    
    assert 'daily_margins' in result
    assert 'monthly_margins' in result
    
    daily_margin = result['daily_margins'][0]
    assert daily_margin['profit_margin'] == 20  # (100-80)/100 * 100

def test_missing_data(sample_data):
    """Test handling of missing data."""
    processor = DataProcessor()
    del sample_data['transactions'][0]['product_id']
    
    with pytest.raises(ValueError):
        processor.process(sample_data)
