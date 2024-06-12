# Importing Libraries
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open(r"C:\Users\91916\Desktop\ICN.png")
st.set_page_config(page_title= "Airbnb Data Visualization",
                   page_icon= icon,
                   layout= "wide")
st.title(':red[Airbnb Data Visualization]')

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Overview","Explore"], 
                           icons=["graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )


# READING THE CLEANED DATAFRAME
df = pd.read_csv(r'C:\Users\91916\GUVI_DS\Airbnb_data.csv')
    
# OVERVIEW PAGE
if selected == "Overview":
    tab1,tab2 = st.tabs(["HOTELS", "DATA ANALYSIS"])
    
    # RAW DATA TAB
    with tab1:
        st.write('### List of Hotels available')
        st.dataframe(df, hide_index = True, column_order = ('Name', 'Property_type', 'Review_scores', 'Country'))
        # DATAFRAME FORMAT
        
       
    # INSIGHTS TAB
    with tab2:
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
        
 
        # TOP 10 PROPERTY TYPES BAR CHART
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Property_type',
                         y='Listings',
                         color='Property_type',
                         pattern_shape_sequence=["."],
                         text = 'Listings')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # TOP 10 HOSTS BAR CHART
        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
        fig1 = px.bar(df2,
                         title='Top 10 Hosts with highest number of listings',
                         x='Host_name',
                         y='Listings',
                         color='Host_name',
                         pattern_shape_sequence=["."],
                         text = 'Listings')
        fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1,use_container_width=True)
        
            
        # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
        df3 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig3 = px.bar(df3,
                         title='Total Listings in Room types',
                         x='Room_type',
                         y='counts',
                         color='Room_type',
                         pattern_shape_sequence=["."],
                         text = 'counts')
        fig3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3,use_container_width=False)

        
# EXPLORE PAGE
if selected == "Explore":
    st.markdown("### Explore Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("### Price Analysis")
    
    # AVG PRICE BY ROOM TYPE BARCHART
    pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
    fig4 = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Average Price in Room type',
                     text = 'Price',
                     color_continuous_scale=px.colors.sequential.Viridis
                    )
    fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    st.plotly_chart(fig4,use_container_width=True)
        
    # HEADING 2
    st.markdown("### Availability Analysis")
        
    # AVAILABILITY BY ROOM TYPE BOX PLOT
    fig5 = px.bar(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room type',
                     color_continuous_scale=px.colors.sequential.Viridis
                    )
    st.plotly_chart(fig5,use_container_width=True)
        
    
        
    # AVG PRICE IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
    fig6 = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Average Price in a Country',
                                       color_continuous_scale=px.colors.sequential.Viridis
                            )
    st.plotly_chart(fig6,use_container_width=True)
        

        
    # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
    country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
    country_df.Availability_365 = country_df.Availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Average availability in each Country',
                                       color_continuous_scale=px.colors.sequential.Viridis
                            )
    st.plotly_chart(fig,use_container_width=True)
