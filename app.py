import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.title('Interact with Gapminder Data')

df = pd.read_csv('Data/gapminder_tidy.csv')

continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())

metric_labels = {'gdpPercap': 'GDP Per Capita',
                'lifeExp': 'Average Life Expectancy',
                'pop': 'Population'}

def format_metric(metric_raw):
    return metric_labels[metric_raw]

# set location of widget

with st.sidebar:

# user inputs 1: by continent
    continent = st.selectbox(label='Choose a continent', options = continent_list)

    metric = st.selectbox(label='Choose a metric', options = metric_list, format_func = format_metric)

    query = f"continent=='{continent}' & metric=='{metric}'"

    df_filtered = df.query(query)

    title = f'{metric_labels[metric]} of countries in {continent}'
    fig = px.line(df_filtered, x = 'year', y = 'value',
             color = 'country', title=title,
             labels = {'value': f'{metric_labels[metric]}'})

# like fig.show() except for streamlit
st.plotly_chart(fig, use_container_width = True)

# add a text description
st.markdown(f'This plot shows the {metric_labels[metric]} for countries in {continent}.', unsafe_allow_html=False)

with st.sidebar:
    show_data=st.checkbox(label = 'Show the data for this plot', value = False)

if show_data:
    st.dataframe(df_filtered)

# user inputs 2: by country

country_list = list(df['country'].unique())
country = st.selectbox('Would you like to look at country level data? If so, pick a coutry: ', country_list)

metric = st.selectbox('Choose a metric again', options = metric_list, format_func = format_metric)

query_1 = f"country=='{country}' & metric=='{metric}'"

df_filtered = df.query(query_1)
title = f'{metric_labels[metric]} of {country}'
fig = px.line(df_filtered, x = 'year', y = 'value', title=title, labels = {'value': f'{metric_labels[metric]}'})

st.plotly_chart(fig, use_container_width = True)

df_messy = px.data.gapminder()

st.markdown(f'See how GDP per capita has grown over time.', unsafe_allow_html=False)

fig = px.bar(df_messy, x="continent", y='gdpPercap', color="continent", animation_frame="year", animation_group="country", range_y=[0,1000000])

st.plotly_chart(fig, use_container_width = True)

st.markdown(f'See how population has grown over time.', unsafe_allow_html=False)

fig = px.scatter_geo(df_messy, locations="iso_alpha", color="continent", hover_name="country", size="pop",
               animation_frame="year", projection="natural earth")

st.plotly_chart(fig, use_container_width = True)

st.markdown(f'See how life expectancy has changed over time.', unsafe_allow_html=False)

fig = px.choropleth(df_messy, locations="iso_alpha", color="lifeExp", hover_name="country", animation_frame="year", range_color=[20,80])

st.plotly_chart(fig, use_container_width = True)
