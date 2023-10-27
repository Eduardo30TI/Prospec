import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from SQL import SQL
import time
import phonenumbers
from phonenumbers import geocoder

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


class Configuracoes:

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

            st.header('Configurações')
            st.markdown('----')

            tab1,tab2=st.tabs(['Template','Vendedores'])

            with tab1.container():

                temp_dict=dict()

                df=sql.DataFrame(querys)

                lista=['']
                
                for l in df['template']['TITLE'].unique().tolist():

                    lista.append(l)

                    pass

                selected=st.selectbox('Lista de Template',options=lista)
                
                temp_dict['titulo']=selected if selected!='' else ''
                temp_dict['mensagem']=df['template'].loc[df['template']['TITLE']==selected,'TEXTO'].unique().tolist()[-1] if selected!='' else ''
                
                temp_dict['titulo']=st.text_input('Título',value=temp_dict['titulo'],key='titulo').upper()
                temp_dict['mensagem']=st.text_area('Mensagem',value=temp_dict['mensagem'],key='mensagem')

                btn_template=st.button('Salvar',key='save_template',type='primary')

                if btn_template==True:

                    resp=self.ValidarCampos(temp_dict)

                    if 1 in resp.keys():

                        mensagem=st.warning(f'Preencher o campo {resp[1]}')
                        time.sleep(1)
                        mensagem.empty()

                        pass

                    else:

                        querys={

                            'INSERT':

                            """

                            INSERT INTO template(TITLE,TEXTO)VALUES('{0}','{1}')

                            """.format(temp_dict['titulo'],temp_dict['mensagem']),

                            'UPDATE':

                            """
                            
                            UPDATE template
                            SET TEXTO='{1}'
                            WHERE TITLE='{0}'

                            """.format(temp_dict['titulo'],temp_dict['mensagem'])
                        }

                        count=df['template'].loc[df['template']['TITLE']==temp_dict['titulo'],'TEXTO'].count()

                        tipo='INSERT' if count<=0 else 'UPDATE'

                        sql.Save(querys[tipo])

                        mensagem=st.success('Dados salvo com sucesso')
                        time.sleep(1)
                        mensagem.empty()
                        streamlit_js_eval(js_expressions='parent.window.location.reload()')

                        pass

                    pass             

                pass

            with tab2.container():

                temp_dict=dict()

                df=sql.DataFrame(querys)

                lista=['']

                for l in df['vendedor']['VENDEDOR'].unique().tolist():

                    lista.append(l)

                    pass

                selected=st.selectbox('Lista de Vendedores',options=lista)

                temp_dict['vendedor']=selected if selected!='' else ''
                temp_dict['telefone']=df['vendedor'].loc[df['vendedor']['VENDEDOR']==selected,'TELEFONE'].unique().tolist()[-1] if selected!='' else ''
                
                temp_dict['vendedor']=st.text_input('Vendedor',value=temp_dict['vendedor'],key='vendedor').title()
                temp_dict['telefone']=st.text_input('Telefone',placeholder='Inserir o ddd + telefone sem espaço',value=temp_dict['telefone'],key='telefone')

                btn_vend=st.button('Salvar',key='save_vend',type='primary')

                pass

            pass

        if btn_vend==True:

            resp=self.ValidarCampos(temp_dict)

            if 1 in resp.keys():

                mensagem=st.warning(f'Preencher o campo {resp[1]}')
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                telefone_ajustado=phonenumbers.parse(temp_dict['telefone'],'BR')
                local=geocoder.description_for_number(telefone_ajustado,'pt_br')

                if local=='':

                    mensagem=st.warning('Telefone invalido')
                    time.sleep(1)
                    mensagem.empty()

                    pass


                else:

                    querys={

                        'INSERT':

                        """

                        INSERT INTO vendedor(VENDEDOR,TELEFONE)VALUES('{0}','{1}')

                        """.format(temp_dict['vendedor'],temp_dict['telefone']),

                        'UPDATE':

                        """
                        
                        UPDATE vendedor
                        SET TELEFONE='{1}'
                        WHERE VENDEDOR='{0}'

                        """.format(temp_dict['vendedor'],temp_dict['telefone'])
                    }

                    count=df['vendedor'].loc[df['vendedor']['TELEFONE']==temp_dict['telefone'],'TELEFONE'].count()

                    tipo='INSERT' if count<=0 else 'UPDATE'

                    sql.Save(querys[tipo])

                    mensagem=st.success('Dados salvo com sucesso')
                    time.sleep(1)
                    mensagem.empty()
                    streamlit_js_eval(js_expressions='parent.window.location.reload()')

                    pass

                pass

            pass        

        pass

    def ValidarCampos(self,campos: dict):

        erro_dict=dict()

        for k,v in campos.items():

            if v=='':

                erro_dict[1]=k

                break

            pass
        
        return erro_dict
        
        pass

    pass