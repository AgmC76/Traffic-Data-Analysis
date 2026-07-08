import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# The Stanford Open Policing ProjectLinks to an external site. is collecting and standardizing data on vehicle and pedestrian stops from law enforcement
# departments across the country. They've collected data from 31 US states. You will use the data from the state of Rhode Island.
# Download the datasets police.csv and weather.csv You will explore and analyze the impact of gender on police behavior.
# This will involve cleaning messy data, combining and reshaping datasets, and manipulating time series data.

# 2.1 Prepping data ---------------------------------------------------------------------

# setting up streamlit page
st.title('Violation Reports')

# Load police.csv and weather.csv datasets to pandas dataframes, outcomes and weather.
outcomes = pd.read_csv('police.csv')
police_shape_og = outcomes.shape
weather = pd.read_csv('weather.csv')
weather_shape_og = weather.shape


# Locate missing values

# Drop columns and rows (based on missing value counts) [HINT: .isnull().sum()]

def remove_missing(df):
    rows_drop = df.index[df.isnull().sum(axis=1) > 50]  # row, 5 empty values in the row
    columns_drop = df.columns[df.isnull().sum(axis=0) > 10000]  # column, more than 10000 empty values

    df = df.drop(columns=columns_drop)
    df = df.drop(index=rows_drop)
    return df


# weather = remove_missing(weather)
# outcomes = remove_missing(outcomes)

w_shape = remove_missing(weather).shape
p_shape = remove_missing(outcomes).shape


# Examine shape with fewer rows and columns [HINT: specify the rows/columns you have dropped)
def show_diff(df):
    columns_dropped = df.columns.difference(remove_missing(df).columns)
    print("Dropped columns:", columns_dropped)


print(f"The original shape of the police csv was {police_shape_og}, while the cleaned shape is {p_shape}")
print(f"The original shape of the weather csv was {weather_shape_og}, while the cleaned shape is {w_shape}")

show_diff(outcomes)
show_diff(weather)

"""
remove missing still cleans outcomes
but not weather
need to fix the range
"""
weather = remove_missing(weather)
outcomes = remove_missing(outcomes)

# Examine and fix incorrect data types
# print(weather.dtypes) # what would be an incorrect datatype??
weather['date'] = pd.to_datetime(weather['DATE'])
weather = weather.set_index('date')

# Combine date and time columns to create a Datetime index.
outcomes['datetime'] = pd.to_datetime(outcomes['stop_date'] + ' ' + outcomes['stop_time'])

outcomes = outcomes.set_index('datetime')  # have to set this or resampling won't work
# print(outcomes)
weather_text = st.text("Weather Dataset")
st.dataframe(weather, use_container_width=True)
outcomes_text = st.text("Outcomes Dataset")
st.dataframe(outcomes, use_container_width=True)


