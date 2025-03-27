
import logging
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any, List
from models.data_models import TransactionData, ProductData, ProfitMarginResult

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.execution_count = 0
        self.error_count = 0
        self.total_processing_time = 0
        self.last_execution_time = None
        
    def validate_input_data(self, transactions: List[Dict], products: List[Dict]) -> bool:
        """Validate input data completeness and correctness."""
        try:
            # Convert to DataFrames for validation
            tx_df = pd.DataFrame(transactions)
            prod_df = pd.DataFrame(products)
            
            # Check required columns
            required_tx_cols = ['transaction_id', 'product_id', 'quantity', 'sale_price', 'transaction_date']
            required_prod_cols = ['product_id', 'category', 'cost_price', 'name']
            
            if not all(col in tx_df.columns for col in required_tx_cols):
                raise ValueError("Missing required transaction columns")
                
            if not all(col in prod_df.columns for col in required_prod_cols):
                raise ValueError("Missing required product columns")
                
            # Validate data types and ranges
            if (tx_df['quantity'] <= 0).any():
                raise ValueError("Invalid quantity values")
                
            if (tx_df['sale_price'] <= 0).any() or (prod_df['cost_price'] <= 0).any():
                raise ValueError("Invalid price values")
                
            return True
            
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            return False

    def calculate_margins(self, df: pd.DataFrame, period: str) -> List[ProfitMarginResult]:
        """Calculate profit margins by category for given period."""
        results = []
        
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]
            
            total_revenue = cat_data['total_revenue'].sum()
            total_cost = cat_data['total_cost'].sum()
            profit_margin = ((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0
            
            # Calculate trend (simple period-over-period change)
            prev_period = cat_data['profit_margin'].shift(1).fillna(profit_margin)
            trend = (profit_margin - prev_period) / prev_period * 100 if prev_period != 0 else 0
            
            results.append(
                ProfitMarginResult(
                    category=category,
                    period=period,
                    total_revenue=Decimal(str(total_revenue)),
                    total_cost=Decimal(str(total_cost)),
                    profit_margin=Decimal(str(profit_margin)),
                    trend=float(trend)
                )
            )
            
        return results

    def process(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process transaction and product data to calculate profit margins."""
        try:
            # Validate input data
            if not self.validate_input_data(parameters.get('transactions', []), 
                                         parameters.get('products', [])):
                raise ValueError("Input data validation failed")

            # Convert to DataFrames
            transactions_df = pd.DataFrame(parameters['transactions'])
            products_df = pd.DataFrame(parameters['products'])

            # Merge transactions with product data
            merged_df = transactions_df.merge(products_df, on='product_id')
            
            # Calculate revenue and cost
            merged_df['total_revenue'] = merged_df['quantity'] * merged_df['sale_price']
            merged_df['total_cost'] = merged_df['quantity'] * merged_df['cost_price']

            # Calculate daily aggregations
            daily_df = merged_df.groupby(['category', 
                                        pd.Grouper(key='transaction_date', freq='D')]).sum()
            daily_results = self.calculate_margins(daily_df, 'daily')

            # Calculate monthly aggregations
            monthly_df = merged_df.groupby(['category', 
                                          pd.Grouper(key='transaction_date', freq='M')]).sum()
            monthly_results = self.calculate_margins(monthly_df, 'monthly')

            return {
                'daily_margins': [result.dict() for result in daily_results],
                'monthly_margins': [result.dict() for result in monthly_results]
            }

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            self.error_count += 1
            raise
