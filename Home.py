import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home')

#image_path = "C:\\Users\\Guilherme\\Documents\\jupyter\\FTC_Python\\logo.png"
#image = Image.open( image_path + 'logo.png' )

#image_path = "C:\\Users\\Guilherme\\Documents\\jupyter\\FTC_Python\\logo.png"
#erro
image = Image.open( 'logo.png' )
st.sidebar.image(image, width=120)


st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.title( 'Curry Company Grouth Dashboard')

st.markdown(
    """
    Este Growth Dashboard foi construído para acompanhar as métricas de desempenho da Curry Company.
    
    ### Como utilizar esse dashboard?
    - Visão Empresa:
        - Visão Gerencial: métricas gerais de acompanhamento
        - Visão Tática: indicadores semanais de crescimento
        - Visão Geográfica: insights de localização
    - Visão Restaurantes:
        - indicadores semanais de crescimento dos restaurantes
    - Visão Entregadores:
        - Acompanhamento de indicadores semanais relacionados aos entregadores
    
    ### Ask for Help
    - Time de Data Science da Curry Company
        - @guicapra
    """ )
    





