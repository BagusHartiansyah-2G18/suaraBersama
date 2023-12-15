# streamlit run dashboard.py
# conda activate main-ds
# pip freeze > requirements.txt



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
 



    #  st.write(st.session_state['place']) # see *

st.set_page_config(page_title="Code of Cosmos", layout="wide")


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn-icons-png.flaticon.com/512/2857/2857309.png")
    
    st.markdown("<h1 style='text-align: center; color: grey;'>Visualisasi Data</h1>", unsafe_allow_html=True)


# read data 
allData = pd.read_excel("https://docs.google.com/spreadsheets/d/e/2PACX-1vRrTVLo9EUE9eGc6sAw-WsLIDDUaAVBVmGvaKQjTz7696busOoh32mXD0RDIVs_TqJnVwJBEoT-qbzi/pub?output=xlsx")

# get daftar Desa dan jumlah nya 
# desaC = allData.groupby(by=['desa']).desa.count() 
desaC = allData.groupby(by=['DESA']).agg( 
    total=('DESA','count')
)

st.header('Data Desa / Kelurahan ('+str(desaC.values.size)+') :sparkles:')
st.text("Dengan Total Suara: "+str(desaC.values.sum())+' orang')

col1, col2 = st.columns(2)
# col1.write("This is column 1")
# col2.write("This is column 2")
with col1:
    # st.table(pd.DataFrame([desaC.index,desaC.values],columns=["Desa","Total Suara"]))
    st.dataframe(desaC,use_container_width=True)
with col2:
    st.bar_chart(desaC)

# batas 
if 'viewTabel' not in st.session_state:
    st.session_state['viewTabel'] = 1
if 'nmDesa' not in st.session_state: 
    st.session_state['nmDesa'] = desaC.index[0] 

def changeDesa(): 
    st.session_state.viewTabel = 1
    st.session_state.nmDesa= st.session_state['place']
    st.session_state.place1 = None

if 'nmLing' not in st.session_state: 
    st.session_state['nmLing'] = ''

if st.session_state.viewTabel:
    pemilih=allData.query("DESA == '"+st.session_state.nmDesa+"'")  
    gpemilih = pemilih.groupby(by="LINGKUNGAN").agg(
        total=("NAMA","count")
    )
    # tpemilih =st.table(gpemilih) 
    st.session_state.nmLing = gpemilih.index[0]

# batas 
if 'viewTabel1' not in st.session_state:
    st.session_state['viewTabel1'] = 1


def changeLingkungan(): 
    # st.session_state.viewTabel1 = 1
    st.session_state.nmLing= st.session_state['place1']
# digunakan untuk memastikan perubahan desa sehingga memperbarui data lingkungannnya 
glingkungan = pemilih.query("LINGKUNGAN == '"+st.session_state.nmLing+"' ")
if 'place1' in st.session_state:
    if st.session_state.place1 is not None:
        glingkungan = pemilih.query("LINGKUNGAN == '"+st.session_state.place1+"' ")
    else :
        # untuk menetapkan Lingkungan tetap ada jika kosong
        st.session_state.place1 = st.session_state.nmLing
# batas 
with st.container(border=True):
    st.header('Perhitungan Pemilih Berdasarkan Lingkungan')   
    sdesa = st.selectbox("Pilih Desa / Kelurahan ", options=desaC.index, key="place",on_change=changeDesa)
    col11, col22 = st.columns(2)
    with col11:
        ttpemilih =st.dataframe(gpemilih,use_container_width=True)  
    with col22:
        st.bar_chart(gpemilih)
# batas 
with st.container(border=True):
    st.header('Data Pemilih Berdasarkan Lingkungan')   
    sdesa = st.selectbox("Pilih Lingkungan di "+st.session_state.nmDesa, options=gpemilih.index, key="place1",on_change=changeLingkungan)
    tlingkungan =st.dataframe(glingkungan,hide_index=True,use_container_width=True)

# batas 
with st.container(border=True):
    st.header('Data Full')
    st.text("Semua data yang terdaftar") 
    allData.index += 1
    st.dataframe(allData,use_container_width=True)
