import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_mock_data(filename="raw_order_export.csv", num_rows=15000):
    np.random.seed(42)
    random.seed(42)
    
    regions = ['Telangana - Hyderabad', 'Telangana - Warangal', 
               'Andhra Pradesh - Vijayawada', 'Andhra Pradesh - Vizag', 
               'Karnataka - Bengaluru Hub']
    
    categories = ['Chronic Care', 'Acute Care', 'OTC & Wellness', 'Diagnostics']
    channels = ['App', 'Web', 'Partner Agent']
    
    start_date = datetime(2026, 1, 1)
    
    data = []
    for i in range(num_rows):
        order_id = f"PE-{2026}{random.randint(100000, 999999)}"
        
        # Inject structural anomalies (missing or corrupted text fields)
        reg = random.choice(regions) if random.random() > 0.02 else "  UNKNOWN_REG  "
        cat = random.choice(categories) if random.random() > 0.01 else None
        chan = random.choice(channels)
        
        # Timestamp generation spanning 6 months
        days_offset = random.randint(0, 180)
        timestamp = start_date + timedelta(days=days_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        # Base pricing modeling
        base_value = random.uniform(300, 4500)
        
        # Inject financial anomalies (negative values or structural outliers)
        if random.random() < 0.015:
            order_value = -float(np.round(base_value, 2))
        elif random.random() < 0.01:
            order_value = float(np.round(base_value * 15, 2)) # Extreme Outlier
        else:
            order_value = float(np.round(base_value, 2))
            
        # Delivery times & Statuses
        status = random.choices(['Delivered', 'Cancelled', 'Returned'], weights=[0.88, 0.08, 0.04])[0]
        tat = random.randint(12, 72) if status == 'Delivered' else None
        
        data.append([order_id, timestamp, reg, cat, order_value, status, tat, chan])
        
    df = pd.DataFrame(data, columns=['order_id', 'timestamp', 'region', 'category', 'order_value', 'status', 'turnaround_time_hours', 'channel'])
    df.to_csv(filename, index=False)
    print(f" Data generation complete! Saved {num_rows} records to {filename}")

if __name__ == "__main__":
    generate_mock_data()
