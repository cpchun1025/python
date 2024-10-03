from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import this

# FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MSSQL Database connection (local) with Windows Authentication
DATABASE_SERVER = "localhost"  # or use "ROG-G834JZ" if you prefer using the hostname
DATABASE_NAME = "WideWorldImporters"

# Connection string for MSSQL with Windows Authentication
DATABASE_URL = f"mssql+pyodbc://@{DATABASE_SERVER}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

# Create the SQLAlchemy engine for MSSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route using pandas.read_sql() to fetch orders
@app.get("/orders", response_model=List[dict])
def get_orders(db=Depends(get_db)):
    """
    Fetch all orders using pandas.read_sql().
    """
    query = """
        SELECT TOP 100 OrderID, OrderDate, ExpectedDeliveryDate, CustomerPurchaseOrderNumber, IsUndersupplyBackordered
        FROM sales.Orders
    """
    
    # Use pandas to execute the query and fetch the results into a DataFrame
    with engine.connect() as conn:
        orders_df = pd.read_sql(query, conn)

    # Convert DataFrame to a list of dictionaries to return as JSON
    orders = orders_df.to_dict(orient='records')
    return orders

# API route using pandas.read_sql_query() to fetch order lines by order ID
@app.get("/orders/{order_id}/lines", response_model=List[dict])
def get_order_lines(order_id: int, db=Depends(get_db)):
    """
    Fetch order lines for a specific order using pandas.read_sql_query().
    """
    query = f"""
        SELECT OrderLineID, OrderID, Description, Quantity, UnitPrice
        FROM sales.OrderLines
        WHERE OrderID = {order_id}
    """
    
    # Use pandas to execute the query and fetch the results into a DataFrame
    with engine.connect() as conn:
        order_lines_df = pd.read_sql_query(query, conn)

    if order_lines_df.empty:
        raise HTTPException(status_code=404, detail="Order lines not found")
    
    # Convert DataFrame to a list of dictionaries to return as JSON
    order_lines = order_lines_df.to_dict(orient='records')
    return order_lines