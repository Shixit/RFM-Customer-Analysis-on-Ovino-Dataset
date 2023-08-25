 #importing necessary libraries

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

 

# importing the data

df = pd.read_excel(r"C:\Users\shikha\Desktop\OVINO\Output_Report\customer_life_cycle_report2023_08_24_09_49_17.xls")

df.head()

 

# Recency

df_recency = df.groupby(by='Customer Phone Number', as_index=False)['No. of Days of Last Order'].max()

df_recency.columns = ['CustomerPhone', 'Recency']

df_recency.head()

 

# Frequency

frequency_df = df.groupby(by='Customer Phone Number', as_index=False)['Order Count'].sum()

frequency_df.columns = ['CustomerPhone', 'Frequency']

frequency_df.head()

 

# Monetary

df['Total'] = df['Total Order Amount']

monetary_df = df.groupby(by='Customer Phone Number', as_index=False)['Total'].sum()

monetary_df.columns = ['CustomerPhone', 'Monetary']

monetary_df.head()

 

# Merging all three columns into one dataframe

rf_df = df_recency.merge(frequency_df, on='CustomerPhone')

rfm_df = rf_df.merge(monetary_df, on='CustomerPhone')

rfm_df.head()

 

# Adding additional columns

rfm_df['S.No.'] = range(1, len(rfm_df) + 1)

rfm_df['Customer ID'] = df['Customer ID']  # Assuming 'Customer ID' is the correct column containing Customer ID

rfm_df['Customer Name'] = df['Customer Name']

rfm_df['Customer Email'] = df['Customer Email']

rfm_df['Hub Name'] = df['Hub Name']

rfm_df['Customer Phone Number'] = df['Customer Phone Number']

rfm_df['Customer Address'] = df['Customer Address']

 

# Calculating ranks and normalizing the rank of the customers

rfm_df['R_rank'] = rfm_df['Recency'].rank(ascending=False)

rfm_df['F_rank'] = rfm_df['Frequency'].rank(ascending=True)

rfm_df['M_rank'] = rfm_df['Monetary'].rank(ascending=True)

rfm_df['R_rank_norm'] = (rfm_df['R_rank'] / rfm_df['R_rank'].max()) * 100

rfm_df['F_rank_norm'] = (rfm_df['F_rank'] / rfm_df['F_rank'].max()) * 100

rfm_df['M_rank_norm'] = (rfm_df['M_rank'] / rfm_df['M_rank'].max()) * 100

rfm_df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)

rfm_df.head()

 

# Calculating RFM Score

rfm_df['RFM_Score'] = 0.2 * rfm_df['R_rank_norm'] + 0.4 * rfm_df['F_rank_norm'] + 0.4 * rfm_df['M_rank_norm']

rfm_df['RFM_Score'] *= 0.1

rfm_df = rfm_df.round(2)

rfm_df[['CustomerPhone', 'RFM_Score']].head()

 

# Assigning customer segments based on RFM Score

rfm_df["Customer_segment"] = np.where(rfm_df['RFM_Score'] > 8, "Premium Customers",

                                      np.where(rfm_df['RFM_Score'] > 6, "Medium Value Customer",

                                               np.where(rfm_df['RFM_Score'] > 4, 'Low Value Customers',

                                                        'Lost Customers')))

rfm_df[['CustomerPhone', 'RFM_Score', 'Customer_segment']].head()

 

# Dropping rows with missing values

rfm_df_result = rfm_df.dropna(axis=0)

 

 

# Move 'S.No.' column to the first position in the DataFrame

sno_column = rfm_df_result.pop('S.No.')

rfm_df_result.insert(0, 'S.No.', sno_column)

 

# Saving the modified DataFrame to the output Excel file

file_name = r"C:\Users\sanlakshya\Desktop\OVINO\Output_Report\RFM_Output.xlsx"

rfm_df_result.to_excel(file_name, index=False)

 

# Plotting the customer segment distribution

plt.pie(rfm_df_result.Customer_segment.value_counts(),

        labels=rfm_df_result.Customer_segment.value_counts().index,

        autopct='%.0f%%')
