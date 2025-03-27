import pytest
import pandas as pd
from src.processors.data_processor import DataProcessor


def test_completeness():
    """Test that data has no missing values."""
    processor = DataProcessor()
    result = processor.process({})

    # Convert to DataFrame for easier testing
    df = pd.DataFrame(result['records'])

    # Check for missing values
    assert df.isnull().sum().sum() == 0, "Data should not have missing values"


def test_value_ranges():
    """Test that values are within expected ranges."""
    processor = DataProcessor()
    result = processor.process({})

    # Convert to DataFrame for easier testing
    df = pd.DataFrame(result['records'])

    # Check value ranges
    assert df['value'].min() >= 10, "Values should be at least 10"
    assert df['value'].max() < 20, "Values should be less than 20"


def test_category_values():
    """Test that categories are valid."""
    processor = DataProcessor()
    result = processor.process({})

    # Convert to DataFrame for easier testing
    df = pd.DataFrame(result['records'])

    # Check categories
    valid_categories = {'A', 'B', 'C'}
    assert set(df['category'].unique()).issubset(
        valid_categories), "Categories should be valid"
