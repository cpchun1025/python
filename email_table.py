import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Step 1: Create the DataFrame
data = {
    'Jan-24': [1, 2, 3, 2, 1, 2],
    'Feb-24': [1, 2, 3, 2, 2, 1],
    'Mar-24': [1, 2, 1, 1, 1, 1],
    'Apr-24': [0, 1, 1, 0, 0, 1],
    'May-24': [1, 1, 1, 1, 1, 1],
    'Jun-24': [1, 2, 2, 1, 1, 1],
    'Jul-24': [2, 2, 1, 2, 2, 2]
}

rows = [
    ('America', 'CTO'),
    ('America', 'HKQ'),
    ('Asia', 'HKGX'),
    ('Asia', 'HKGX'),
    ('Asia', 'CPBG'),
    ('Asia', 'TSE')
]

# Create a DataFrame
df = pd.DataFrame(data, index=pd.MultiIndex.from_tuples(rows, names=['Region', 'City']))

# Step 2: Calculate row-wise totals
df['Total'] = df.sum(axis=1)

# Step 3: Calculate column-wise totals (excluding the 'Total' column)
column_totals = df.sum(axis=0)  # Sum for each column

# Add the total row to the DataFrame
# df.loc[('Total', ''), :] = list(column_totals) + [column_totals.sum()]

# Step 4: Convert the DataFrame to an HTML table
def style_table(df):
    # Start HTML table
    html = '<table border="1" style="border-collapse: collapse; width: 100%;">'
    
    # Add headers
    html += '<thead><tr>'
    html += '<th style="padding: 8px; background-color: #4CAF50; color: white; text-align: center;">Region</th>'
    html += '<th style="padding: 8px; background-color: #4CAF50; color: white; text-align: center;">City</th>'
    
    for col in df.columns:
        html += f'<th style="padding: 8px; background-color: #4CAF50; color: white; text-align: center;">{col}</th>'
    
    html += '</tr></thead><tbody>'
    
    # Keep track of current region for merging cells
    current_region = None
    region_rowspan = 0
    rowspan_index = None
    
    # Iterate through the DataFrame
    for i, (index, row) in enumerate(df.iterrows()):
        region, city = index
        
        # Start a new row
        html += '<tr>'
        
        # Handle region column (with merged cells)
        if region != current_region:
            if current_region is not None:
                # Close the previous rowspan
                html = html.replace(f'ROWSPAN_{rowspan_index}', str(region_rowspan))
            
            # Start new rowspan for the new region
            current_region = region
            region_rowspan = 1
            rowspan_index = i
            html += f'<td rowspan="ROWSPAN_{i}" style="padding: 8px; text-align: center;">{region}</td>'
        else:
            region_rowspan += 1
        
        # Add city column and row data
        html += f'<td style="padding: 8px; text-align: center;">{city}</td>'
        
        for value in row:
            html += f'<td style="padding: 8px; text-align: center;">{value}</td>'
        
        # Close the row
        html += '</tr>'
    
    # Close the last rowspan
    html = html.replace(f'ROWSPAN_{rowspan_index}', str(region_rowspan))
    
    # Close the table
    html += '</tbody></table>'
    
    return html

# Step 5: Send the email with the HTML table
def send_email(html_content):
    # Email details
    sender_email = "your_email@gmail.com"
    receiver_email = "recipient_email@gmail.com"
    subject = "Styled Table Report"

    # Create a MIME message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))

    # Send the email via Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, "your_password")
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Generate styled HTML table
html_table = style_table(df)

# Send the email with the styled table
send_email(html_table)