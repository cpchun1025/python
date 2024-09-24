
import pandas as pd

# Create a DataFrame from your table
data = {
    'lvl1': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],
    'lvl2': [' ', 'B', 'B', 'B', 'B', 'C', 'C', 'D'],
    'lvl3': [' ', ' ', 'B1', 'B1', ' ', ' ', ' ', ' '],
    'Gross': [10, 10, 20, 30, 40, 50, 60, 70],
    'Net': [10, 10, 20, 30, 40, 50, 60, 70]
}
df = pd.DataFrame(data)

# Melt the DataFrame to create a single column for levels
df_melted = pd.melt(df, id_vars=['Gross', 'Net'], value_vars=['lvl1', 'lvl2', 'lvl3'], var_name='Level', value_name='Row Labels')

# Remove empty strings
df_melted = df_melted[df_melted['Row Labels'] != ' ']

# Pivot the DataFrame to get the desired output
df_pivoted = df_melted.pivot_table(index='Row Labels', values=['Gross', 'Net'], aggfunc='sum')

# Reset the index to get the 'Row Labels' as a column
df_pivoted = df_pivoted.reset_index()

# Rename the columns
df_pivoted.columns = ['Row Labels', 'Sum of Gross', 'Sum of Net']

# Sort the DataFrame to get the desired order
df_pivoted['Row Labels'] = pd.Categorical(df_pivoted['Row Labels'], categories=df_pivoted['Row Labels'].tolist(), ordered=True)
df_pivoted = df_pivoted.sort_values(by='Row Labels', na_position='first')

# Add the missing rows with blank labels
missing_rows = df[df['lvl2'] == ' '][['Gross', 'Net']].sum()
df_pivoted.loc[len(df_pivoted)] = [' ', missing_rows['Gross'], missing_rows['Net']]

missing_rows = df[df['lvl3'] == ' '][['Gross', 'Net']].sum()
df_pivoted.loc[len(df_pivoted)] = [' ', missing_rows['Gross'], missing_rows['Net']]

# Print the final DataFrame
print(df_pivoted)