import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Load your CSV files here
df_evanmiya = pd.read_csv('EvanMiya24.csv')
df_vegas = pd.read_csv('Vegas24.csv')

df_evanmiya['To Win Tournament'] = df_evanmiya['To Win Tournament'].str.rstrip('%').astype('float')
df_vegas['To Win Tournament'] = df_vegas['To Win Tournament'].str.rstrip('%').astype('float')

df_evanmiya['Odds To Make Round of 32'] = df_evanmiya['Odds To Make Round of 32'].str.rstrip('%').astype('float')
df_vegas['Odds To Make Round of 32'] = df_vegas['Odds To Make Round of 32'].str.rstrip('%').astype('float')

df_evanmiya['Odds To Make Sweet 16'] = df_evanmiya['Odds To Make Sweet 16'].str.rstrip('%').astype('float')
df_vegas['Odds To Make Sweet 16'] = df_vegas['Odds To Make Sweet 16'].str.rstrip('%').astype('float')

df_evanmiya['Odds To Make Elite 8'] = df_evanmiya['Odds To Make Elite 8'].str.rstrip('%').astype('float')
df_vegas['Odds To Make Elite 8'] = df_vegas['Odds To Make Elite 8'].str.rstrip('%').astype('float')

df_evanmiya['Odds To Make Final 4'] = df_evanmiya['Odds To Make Final 4'].str.rstrip('%').astype('float')
df_vegas['Odds To Make Final 4'] = df_vegas['Odds To Make Final 4'].str.rstrip('%').astype('float')

df_evanmiya['Odds To Make Championship'] = df_evanmiya['Odds To Make Championship'].str.rstrip('%').astype('float')
df_vegas['Odds To Make Championship'] = df_vegas['Odds To Make Championship'].str.rstrip('%').astype('float')



# region separation
regions = list(set(df_evanmiya['Region']).union(set(df_vegas['Region'])))
regions.sort()
regions.insert(0, 'All')

# Application title
st.title('March Madness 2024 Bracket Data')

# Region selection
selected_region = st.selectbox('Select a Region', regions)

# Function to filter DataFrame by region
def filter_by_region(df, region):
    if region == 'All':
        return df
    else:
        return df[df['Region'] == region]

# filter the data based on the selected region
filtered_df_evanmiya = filter_by_region(df_evanmiya, selected_region)
filtered_df_vegas = filter_by_region(df_vegas, selected_region)

def percentage_color_scale(val):
    """
    Takes a float and returns a color scale from red to green,
    with 50% as the midpoint.
    """
    red = int(255 * (1 - val))
    green = int(255 * val)
    return f'background-color: rgba({red}, {green}, 0, 0.6); color: white;'


# display DataFrame with a pinned column in an AG Grid
def display_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("Team", pinned="left")
    gb.configure_column("To Win Tournament", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2, aggFunc='sum')
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, fit_columns_on_grid_load=False, allow_unsafe_jscode=True)

# data in tabs
tab1, tab2 = st.tabs(["EvanMiya's Predictions", "Vegas Predictions"])

with tab1:
    st.header(f"2024 March Madness Optimal Bracket - EvanMiya ({selected_region} Region)")
    display_aggrid(filtered_df_evanmiya)

with tab2:
    st.header(f"2024 March Madness Optimal Bracket - Vegas ({selected_region} Region)")
    display_aggrid(filtered_df_vegas)