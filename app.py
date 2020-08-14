import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")
#st.set_option('deprecation.showfileUploaderEncoding', False)
#df = pd.read_excel("/mnt/c/Users/lemmo/Google Drive/Auditoria Fiscal/Operacional/Análises/Reg.xlsx")

def gera_titulo(titulo):
    return st.markdown(f"<br><div><span class='titulo bold'>{titulo}</span></div><br>",unsafe_allow_html=True)
def gera_subitem(titulo):
    return st.markdown(f"<div><span class=' bold'>{titulo}</span></div>",unsafe_allow_html=True)
 
st.sidebar.header('CARREGUE O RELATÓRIO')

uploaded_file = st.sidebar.file_uploader("Upload do relatório em xlsx", type=["xlsx"])

def notas_fiscais_emitidas(alvo):
    filtro = ['Nº Sequencial', 'Cidade Tomador','Data Emissão','Valor Documento', 'Valor Tributável', 'Atividade','ITEM LC 116/2003', 'Imposto Retido', 'TOTAL_IMPOSTO',
            'Tributado Município', 'Retido','Descrição dos Serviços']
    alvo = alvo[filtro]
    for mes in range(1,13):
                
        alvo_mensal = alvo[alvo['Data Emissão'].dt.month == mes]
                
        if alvo_mensal.empty == False:
            st.write('No mês {} o contribuinte emitiu {}  nota(s) relativa(s) a {} código(s) de atividade(s):'.format(mes,len(alvo_mensal['Nº Sequencial']),alvo_mensal['Atividade'].nunique()))
            #atividades = alvo['Atividade'].unique()
            atividades = alvo_mensal['Atividade'].unique()
            for atividade in atividades:
                st.write('{}'.format(atividade[0:5]),end='\n\n')

            st.write(alvo_mensal[['Atividade','Valor Tributável']].groupby('Atividade').sum())
            st.write('############################################################################\n\n')
                
def agregados_uteis(alvo):

    input_df = pd.read_excel(uploaded_file)
    alvo = input_df

    gera_subitem('TOTAL POR ITEM DA LEI COMPLEMENTAR:')
    st.write(alvo[ ['ITEM LC 116/2003','Valor Documento',  'Imposto Retido', 'TOTAL_IMPOSTO']].groupby('ITEM LC 116/2003').sum())
    gera_subitem('TOTAL POR MUNICÍPIO TOMADOR:')

    st.write(alvo[ ['Cidade Tomador','Valor Documento', 'Imposto Retido', 'TOTAL_IMPOSTO']].groupby('Cidade Tomador').sum())
    gera_subitem('TOTAL POR MÊS:')
    st.write(alvo[ ['Data Emissão','Valor Documento', 'Imposto Retido', 'TOTAL_IMPOSTO']].groupby([alvo['Data Emissão'].dt.month]).sum())

def detalhamento_servico(alvo):

    def resultado(df1, idx):    
        string = ''
        if len(df1.index)!= 0:
            string += '\nServiço: ' + df1['TITULO'].iloc[idx]
            string += '\n\nExceção na LC 116?: ' + df1['EXCECAO'].iloc[idx]
            string += '\n\nLocal da Prestação: ' + df1['LOCALDAPRESTACAOPJ'].iloc[idx]
            string += '\n\nBase de Cálculo: ' + df1['BASEDECALCULO'].iloc[idx]
            string += '\n\nDedução da Base de Cálculo: ' + df1['DEDUCAODABASEDECALCULO'].iloc[idx]
            string += '\n\nRetenção na Fonte: ' + df1['RETENÇÃO NA FONTE'].iloc[idx]
        else:
            return 'Codigo não encontrado'
        return string

    df = pd.read_excel("./Reg.xlsx")
    df['CODIGO'] = df['CODIGO'].astype(str)
    df['RETENÇÃO NA FONTE'] = df['RETENÇÃO NA FONTE'].replace(np.nan,'Completa a tabela com o pdf original')

    atividades = alvo['Atividade'].unique()
    for atividade in atividades:
        code = str(float(atividade[0:5]))
        idx = df.loc[df['CODIGO'] == code].index.values[0]
        st.write('CÓDIGO: {}'.format(code)) 
        st.write(resultado(df,idx))

def  gera_notebook():

    input_df = pd.read_excel(uploaded_file)
    alvo = input_df

    gera_titulo('NOTAS FISCAIS EMITIDAS E SEUS RESPECTIVOS CÓDIGOS DE SERVIÇO')   
    notas_fiscais_emitidas(alvo)

    gera_titulo('DESCRIÇÃO DETALHADA DOS SERVIÇOS PRESTADOS PELO CONTRIBUINTE')
    detalhamento_servico(alvo)        
    
    gera_titulo('AGREGADOS ÚTEIS')
    agregados_uteis(alvo)
    

if uploaded_file is not None:
    gera_notebook()
else:
    
   
    st.write("""
                # Interpretador de Relatórios da Equipe do Simples Nacional
            """)
    st.write('Carregue o relatório de notas fiscais emitidas pelo prestador')
    image = Image.open('img_rel.jpg')
    st.image(image, caption='ISS.Net', use_column_width=True)
    st.image(image, caption='ISS.Net', width=1024)


