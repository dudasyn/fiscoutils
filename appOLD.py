import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_option('deprecation.showfileUploaderEncoding', False)
#df = pd.read_excel("/mnt/c/Users/lemmo/Google Drive/Auditoria Fiscal/Operacional/Análises/Reg.xlsx")
df = pd.read_excel("./Reg.xlsx")

df['CODIGO'] = df['CODIGO'].astype(str)
df['RETENÇÃO NA FONTE'] = df['RETENÇÃO NA FONTE'].replace(np.nan,'Completa a tabela com o pdf original')
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


# Interpretador de Relatórios da Equipe do Simples Nacional
st.sidebar.header('CARREGUE O RELATÓRIO')
uploaded_file = st.sidebar.file_uploader("Upload do relatório em xlsx", type=["xlsx"])

def render_notas_fiscais_emitidas():
    st.write('RELATÓRIO DE NOTAS FISCAIS EMITIDAS PELO PRESTADOR')
    input_df = pd.read_excel(uploaded_file)
    alvo = input_df
    st.write(input_df)
   
    filtro = ['Nº Sequencial', 'Cidade Tomador','Data Emissão','Valor Documento', 'Valor Tributável', 'Atividade',
          'ITEM LC 116/2003', 'Imposto Retido', 'TOTAL_IMPOSTO',
        'Tributado Município', 'Retido','Descrição dos Serviços']
    alvo = alvo[filtro]

    def loopa(data):
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
            
    loopa(alvo)

    atividades = alvo['Atividade'].unique()
    for atividade in atividades:
        code = str(float(atividade[0:5]))
        idx = df.loc[df['CODIGO'] == code].index.values[0]
        st.write(idx)
        st.write('\n')
        st.write('CÓDIGO: {}'.format(code))
        st.write(resultado(df,idx))

def render_agregados_por_item():
    st.write('Agregados úteis')
    input_df = pd.read_excel(uploaded_file)
    alvo = input_df

    st.write('TOTAL POR ITEM DA LEI COMPLEMENTAR:')
    st.write(alvo[ ['ITEM LC 116/2003','Valor Documento',  'Imposto Retido', 'TOTAL_IMPOSTO']].groupby('ITEM LC 116/2003').sum())
    st.write('TOTAL POR MUNICÍPIO TOMADOR:')
    st.write(alvo[ ['Cidade Tomador','Valor Documento', 'Imposto Retido', 'TOTAL_IMPOSTO']].groupby('Cidade Tomador').sum())
    st.write('TOTAL POR MÊS:')
    st.write(alvo[ ['Data Emissão','Valor Documento', 'Imposto Retido', 'TOTAL_IMPOSTO']].groupby([alvo['Data Emissão'].dt.month]).sum())

def render_analise_cancelamento():
    st.write('Análise de solicitação de cancelamento')
    input_df = pd.read_excel(uploaded_file)
    alvo = input_df
    st.write(alvo)
    
    '''
        ***Lorem*** ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et <br><br>
        dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Arquivos: Relatório de Notas Emitidas Pelo Prestador, Realatório de Análise de Solicitação de cancelamento

        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
        sunt in culpa qui officia deserunt mollit anim id est laborum."
    '''


#if st.button('RELATÓRIO DE NOTAS EMITIDAS'):
#    option = st.sidebar.selectbox('Relatório de Notas Emitidas pelo prestador',('Notas emitidas por ano','Agregados por item'))
option = st.sidebar.selectbox('Relatório de Notas Emitidas pelo prestador',('Notas emitidas por ano','Agregados por item'))


if option=='Notas emitidas por ano':
    if uploaded_file is not None:
        render_notas_fiscais_emitidas()
    else:
        st.write("""
                        # Interpretador de Relatórios da Equipe do Simples Nacional
                """)
        st.write('Carregue o arquivo - de relatório de {}'.format(option))
        #st.write(input_df)

if option =='Agregados por item':

    if uploaded_file is not None:
        render_agregados_por_item()
    else:
        st.write('Arquivo não carregado')
        #st.write(input_df)


