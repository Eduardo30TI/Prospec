from csv import excel
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from SQL import SQL
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains 
import urllib
import time
import os
import socket as s

sql=SQL()

tabelas={

    'template':

    """
    
    CREATE TABLE IF NOT EXISTS template(
    
        TITLE VARCHAR(250) NOT NULL,
        TEXTO TEXT NOT NULL

    )

    """,

    'vendedor':

    """

    CREATE TABLE IF NOT EXISTS vendedor(
    
        VENDEDOR VARCHAR(250) NOT NULL,
        TELEFONE VARCHAR(250) NOT NULL

    )

    """
}

class Mensagem:

    def main(self):

        sql.CreateTable(tabelas)

        querys={
            
            'template':

            """

            SELECT * FROM template

            """,

            'vendedor':

            """

            SELECT * FROM vendedor

            """
        } 

        placeholder=st.empty()

        with placeholder.container():

            st.header('Mensagens')
            st.markdown('----')

            df=sql.DataFrame(querys)

            lista=['']
                
            for l in df['template']['TITLE'].unique().tolist():

                lista.append(l)

                pass    

            selected=st.selectbox('Template',options=lista)
            mensagem=df['template'].loc[df['template']['TITLE']==selected,'TEXTO'].max()

            lista=['']
                
            for l in df['vendedor']['VENDEDOR'].unique().tolist():

                lista.append(l)

                pass

            selected=st.selectbox('Vendedor',options=lista)
            vendedor=selected
            telefone=df['vendedor'].loc[df['vendedor']['VENDEDOR']==selected,'TELEFONE'].max()

            arquivos=st.file_uploader('Arquivo',type=['.xlsx'],accept_multiple_files=False)

            excel_df=pd.DataFrame()

            try:

                excel_df=pd.read_excel(arquivos)
                col_leach=st.multiselect('Telefone',options=excel_df.columns.tolist(),max_selections=1)
                col_leach=col_leach[-1]
                excel_df[col_leach]=excel_df[col_leach].astype(str)
                excel_df[col_leach]=excel_df[col_leach].apply(self.FormatarNumero)
                cliente=st.multiselect('Cliente',options=excel_df.columns.tolist(),max_selections=1)
         
                st.dataframe(excel_df,hide_index=True)
                
                pass

            except:

                pass

            btn_send=st.button('Whatsapp',key='send',type='primary')
            
            pass

        if btn_send==True:

            whatsapp_df=pd.DataFrame(columns=['Vendedor','DDD','Telefone','Mensagens','Path'])

            for i in excel_df.index.tolist():

                nome=str(excel_df.loc[i,cliente].max())
                telefone=str(excel_df.loc[i,col_leach])

                if not str(telefone).isnumeric():

                    continue

                ddd=telefone[:2]
                telefone=telefone[len(ddd):]

                msg=str(mensagem).replace('cliente',nome)

                whatsapp_df.loc[len(whatsapp_df)]=[nome,ddd,telefone,msg,'']

                pass

            self.Whatsapp(whatsapp_df)
            
            mensagem=st.success('Mensagens enviadas')
            time.sleep(1)
            mensagem.empty()
            time.sleep(1)
            streamlit_js_eval(js_expressions='parent.window.location.reload()')

            pass

        pass


    def FormatarNumero(self,val):

        val=str(val)
        
        if val.find('+55')>=0:

            val=val[len('+55'):].strip()

            pass

        for r in ['(',')','-']:

            val=val.replace(r,'')

            pass

        val=val.strip()
        val=''.join([l for l in val.split()])

        return val

        pass

    def Whatsapp(self,excel):

        link='https://web.whatsapp.com/'

        opc=['DIARIO','SEMANAL']
        
        #service=Service(GeckoDriverManager().install())
        service=Service()
        IP=s.gethostbyname(s.gethostname())
        dir_path=os.path.join(os.getcwd(),IP)
        opcao=Options()
        opcao.add_argument(r'user-data-dir='+dir_path+'profile/zap')        
        options=Options()

        with webdriver.Chrome(service=service,options=opcao) as driver:
            driver.maximize_window()
            driver.get(link)

            for i in range(0,len(excel)):
                    
                ddd=excel['DDD'].loc[excel.index==i].tolist()[-1]

                telefone=excel['Telefone'].loc[excel.index==i].tolist()[-1]

                mensagem=str(excel['Mensagens'].loc[excel.index==i].tolist()[-1]).strip()

                paths=excel['Path'].loc[(excel.index==i)&(~excel['Path'].isnull())].tolist()

                tel_format=f'55{ddd}{telefone}'

                text_format=urllib.parse.quote(mensagem)

                link_api=f'{link}send?phone={tel_format}&text={text_format}'

                driver.get(link_api)

                time.sleep(2)
                    
                if len(paths)<=0:

                    try:

                        while True:

                            contagem=len(driver.find_elements(By.ID,'side'))
                            time.sleep(1)

                            if contagem>0:

                                break
                                
                            pass                        
                            
                        send=driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
                        send.click()

                        time.sleep(5)

                        pass

                    except:

                        continue

                    continue

                contagem=len(driver.find_elements(By.CSS_SELECTOR,'p.selectable-text.copyable-text'))
                tempo=0

                while contagem==0:
                    contagem=len(driver.find_elements(By.CSS_SELECTOR,'p.selectable-text.copyable-text'))
                    time.sleep(1)
                            
                    erro=len(driver.find_elements(By.CLASS_NAME,'_3J6wB'))

                    block=len(driver.find_elements(By.XPATH,'//*[@id="main"]/footer/div'))

                    if(erro>0 or block>0):

                        break
                            
                    pass
                    
                try:

                    if(len(paths)>0):

                        click=driver.find_element(By.CSS_SELECTOR,'span[data-icon="attach-menu-plus"]')
                        click.click()
                        #inserir arquivo
                        anexo=driver.find_element(By.CSS_SELECTOR,'input[type="file"]')
                        time.sleep(2)
                        anexo.send_keys(paths[-1])
                        time.sleep(3)
                        #driver.switch_to.window(driver.window_handles[-1])                

                        pass
                        

                    #iq0m558w
                    contagem=len(driver.find_elements(By.CSS_SELECTOR,'p.selectable-text.copyable-text'))
                    tempo=0

                    while contagem==0:

                        contagem=len(driver.find_elements(By.CSS_SELECTOR,'p.selectable-text.copyable-text'))
                        time.sleep(1)

                        erro=len(driver.find_elements(By.CLASS_NAME,'_3J6wB'))

                        block=len(driver.find_elements(By.XPATH,'//*[@id="main"]/footer/div'))

                        if(erro>0 or block>0):

                            break                        

                        pass

                    campo=driver.find_element(By.CSS_SELECTOR,'p.selectable-text.copyable-text')
                    time.sleep(1)
                    #campo.send_keys(Keys.ENTER)

                    time.sleep(3)

                    pass

                except:

                    continue
                            
                pass

            pass
        
        pass

    pass