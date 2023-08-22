#Libraries
import pandas as pd
import numpy as np
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config( page_title='Visão Entregadores', layout='wide')

#==========================
#Funções
#==========================

def top_delivers(df1, top_asc):
#6 Os 10 entregadores mais rápidos por cidade
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City', 'Delivery_person_ID'])
              .min()
              .sort_values(['City', 'Time_taken(min)'], ascending=top_asc )
              .reset_index() )

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat ( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True )
    return df3

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
st.header( 'Marketplace - Visão Entregadores' )

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

weather_options = ( st.sidebar.multiselect('Quais as condições de clima?', 
                                           ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy','conditions Fog', 'conditions Windy'],
                                           default=['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy', 'conditions Fog', 'conditions Windy']) )

st.sidebar.markdown("""---""") #39min Aula 47

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :] 

#Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de clima  
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas, :]
                                        
                                        
#===============================
#LAYOUT STREAMLIT
#===============================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_ ', '_ '])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='medium')
        
        with col1:
            maior_idade = df_aux2 = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior Idade', maior_idade)
                    
        with col2:
            menor_idade = df_aux1 = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
        
        with col3:
            melhor_veiculo = df_aux2 = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor Condição Veículo', melhor_veiculo)
                     
        with col4:
            pior_veiculo = df_aux1 = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior Condição Veículo', pior_veiculo)
                  
            
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Avaliação Média por Entregador')
            #3 A avaliação média por entregador
            df_aux = ( df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                      .groupby('Delivery_person_ID')
                      .mean()
                      .reset_index() )
            st.dataframe (df_aux)
            
            
        
        with col2:
            st.subheader('Avaliação Média por Trânsito')
            df_avg_std = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                             .groupby('Road_traffic_density')
                             .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            
            #mudança de nome das colunas
            df_avg_std.columns = ['delivery_mean', 'delivery_std']
            df_avg_std.reset_index()
            st.dataframe(df_avg_std)


            st.subheader('Avaliação Média por Clima')
            df_avg_std = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                             .groupby('Weatherconditions')
                             .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            df_avg_std.columns = ['delivery_mean', 'delivery_std']
            df_avg_std.reset_index()
            st.dataframe(df_avg_std)

            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Top Entregadores Mais Rápidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
            
        with col2:
            st.subheader('Top Entregadores Mais Lentos')
            df3 = top_delivers(df1, top_asc=False)            
            st.dataframe(df3)


    
            
            
        
        


























