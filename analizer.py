import numpy as np
import pandas as pd
import sys

# get argument
read_file_path = sys.argv[1]
split_path = read_file_path.split('/')
write_file_path = './mold_data/mold_' + split_path[-1]
print(write_file_path)

# read csv data
df = pd.read_csv(read_file_path, header=None, usecols=[0, 2, 4, 6, 8], dtype={'0':'float', '2':'float', '4':'float', '6':'float', '8':'float'})
df = df.rename(columns={0:'time', 2:'time_count', 4:'pump_state', 6:'flow', 8:'pressure'})

# modify missing values
df = df.dropna(how='any')
df = df.dropna(subset=['time'])
df = df.fillna(0)

# split datetime data
df['year'] = df['time'].str.split(pat='-', expand=True)[0]
df['month'] = df['time'].str.split(pat='-', expand=True)[1]
df['day'] = df['time'].str.split(pat='-', expand=True)[2]
df['hour'] = df['time'].str.split(pat='-', expand=True)[3]
df['minute'] = df['time'].str.split(pat='-', expand=True)[4]
df['second'] = df['time'].str.split(pat='-', expand=True)[5]
df.drop('time', axis=1)

# delete missing column
df['flow'] = pd.to_numeric(df['flow'], errors='coerce')
df['pressure'] = pd.to_numeric(df['pressure'], errors='coerce')
df = df.fillna(0)

# mold flow data (nl -> ml)
df['flow(ml)'] = df['flow']/1000

# grouping by minute
df_new = df.groupby(['year','month', 'day', 'hour', 'minute'], as_index=False).agg({'flow(ml)':'sum', 'pressure':'mean'})

df_new.to_csv(write_file_path)
