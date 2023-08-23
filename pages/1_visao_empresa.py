#pip install streamlit-folium
#pip install plotly

#Libraries
import pandas as pd
import numpy as np
#from haversine import haversine
#import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config( page_title='Visão Empresa', layout='wide')

#========================
#Funções
#========================

def country_maps(df1):
    """ Essa função desenha no mapa a localização das cidades conforme os pedidos
        utilizando a densidade de tráfego"""    
    
    #6 Localização central de cada cidade por tipo de tráfego
    columns = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    columns_groupby = ['City', 'Road_traffic_density']
    data_plot = df1.loc[:, columns].groupby( columns_groupby ).median().reset_index()
    data_plot = data_plot[data_plot['City'] != 'NaN']
    data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']
    # Desenhar o mapa
    mapa = folium.Map( zoom_start=12 )
    for index, location_info in data_plot.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( mapa )
    
    folium_static ( mapa, width=1024, height=600 )

def orders_by_delivery_and_week(df1):
    """ Essa função gera gráfico de barras da quantidade de pedidos por semana"""

    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()

    #juntar dois dataframes:
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' ) #how é o como juntar duas coisas - mais explicações no curso de SQL
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig

def order_by_week(df1):
        
    #2 Quantidade de pedidos por Semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    # gráfico
    fig = px.bar( df_aux, x='week_of_year', y='ID' )
    return fig
      

def traffic_order_city(df1):
    #4 Comparacao do volume de pedidos por cidade e por tráfego
    columns = ['ID', 'City', 'Road_traffic_density']
    df_aux = df.loc[:, columns].groupby( ['City', 'Road_traffic_density'] ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    fig = px.bar( df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group')
    return fig

def traffic_order_share(df1):
    #3 Distribuição dos pedidos por tipo de tráfego
    columns = ['ID', 'Road_traffic_density']
    df_aux = df1.loc[:, columns].groupby( 'Road_traffic_density' ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    # gráfico
    fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )
                
    return fig

def orders_by_day(df1):
    #1 Quantidade de pedidos por dia
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
    df_aux.columns = ['order_date', 'qtde_entregas']
    # gráfico
    fig = px.bar( df_aux, x='order_date', y='qtde_entregas' )
        
    return fig

def clean_code( df1 ):
    """ Esta função tem a resposabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. remoção dos dados Nan
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da data
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
    
        Imput: dataframe
        Output: dataframe    """
    
    #1. Convertendo a coluna Age de texto para número 
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    #2 Convertendo a coluna Ratings de texto para número decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #3 convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    #4 convertendo multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #5 Removendo espaços de maneira mais simples
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    #6 limpando a coluna Time Taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

#====================================
#Início da Estrtura Lógica do Código
#====================================

#Impor dataset
df = pd.read_csv( 'dataset/train.csv' )

#Limpeza dos dados
df1 = clean_code(df)

#===============================
#Barra lateral
#===============================
st.header( 'Marketplace - Visão Cliente' )

image = Image.open( 'logo.png' )
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione a data limite')
date_slider = (st.sidebar.slider('Até qual data?', 
                value=pd.datetime(2022, 4, 13), 
                min_value=pd.datetime(2022, 2, 11), 
                max_value=pd.datetime(2022, 4, 6), 
                format='DD-MM-YYYY' ) )

st.sidebar.markdown("""---""")
traffic_options = st.sidebar.multiselect('Quais as condições de trânsito?',
                       ['Low', 'Medium', 'High', 'Jam'],
                        default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown("""---""") #39min Aula 47

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :] 

#Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#===============================
#LAYOUT STREAMLIT
#===============================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        fig = orders_by_day(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart( fig, use_container_width=True)
        
    with st.container():
        col1, col2 = st.columns(2) 
        with col1:
            fig = traffic_order_share(df1)
            st.header('Pedidos por Densidade de Trânsito:')
            st.plotly_chart(fig, use_container_width=True)
                       
        with col2:
            st.header('Pedidos por Cidade e Trânsito:')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        st.header('Pedidos por Semana:')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)

        
        
    with st.container():
        st.header('Pedidos por Entregador e por Semana:')
        fig = orders_by_delivery_and_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
with tab3:
    st.header('Distribuição dos pedidos no Mapa:')
    country_maps(df1)
    
    
    
    

   









