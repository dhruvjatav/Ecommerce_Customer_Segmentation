import pandas as pd
from datetime import datetime

# Load dataset
df = pd.read_csv('../data/ecommerce_data.csv')

# Clean data
df.dropna(subset=['CustomerID'], inplace=True)
df = df[df['Quantity'] > 0]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Reference date (to calculate Recency)
current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',  # Frequency
    'TotalAmount': 'sum'     # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Save RFM result file
rfm.to_csv('../data/rfm_results.csv', index=False)

print("✅ RFM Analysis complete! Results saved in /data/rfm_results.csv")
