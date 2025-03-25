#!/usr/bin/env
"""
Data Product Main Entry Point

This script serves as the entry point for the data product.
It initializes the API server and data processing components.
"""

import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import data processors
from processors.data_processor import DataProcessor
from models.data_models import DataProductInfo, ProcessingResult

# Create FastAPI application
app = FastAPI(title="Data Product API",
              description="API for the data product in data mesh architecture",
              version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data processor
data_processor = DataProcessor()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint returning basic information."""
    return {"message": "Data Product API is running"}


@app.get("/info", response_model=DataProductInfo)
async def get_info():
    """Return metadata information about this data product."""
    return DataProductInfo(name="example-data-product",
                           domain="domain-name",
                           version="0.1.0",
                           description="Description of your data product",
                           owner="your-team",
                           update_frequency="daily",
                           last_updated="2024-01-01T00:00:00Z")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


@app.post("/process", response_model=ProcessingResult)
async def process_data(parameters: Optional[Dict[str, Any]] = None):
    """Process data using the configured processor."""
    try:
        result = data_processor.process(parameters or {})
        return ProcessingResult(success=True,
                                message="Data processed successfully",
                                results=result)
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Return metrics about this data product."""
    return {
        "execution_count": data_processor.execution_count,
        "average_processing_time": data_processor.average_processing_time,
        "last_execution_time": data_processor.last_execution_time,
        "error_count": data_processor.error_count
    }


if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Run the API server
    logger.info(f"Starting data product API on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
