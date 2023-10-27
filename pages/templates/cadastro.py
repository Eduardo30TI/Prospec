import streamlit as st
import os
from glob import glob
import socket as s
from streamlit_js_eval import streamlit_js_eval
import time
from SQL import SQL, query

path_img=os.path.join(os.getcwd(),'Logo','*.*')
img=glob(path_img)

sql=SQL()

tabelas={

    'user':

    """

    CREATE TABLE IF NOT EXISTS login(
    
        EMAIL TEXT NOT NULL,
        TELEFONE NOT NULL,
        SENHA VARCHAR NOT NULL,
        CONECTADO BOOL

    )

    """
}

class CadastroUser:

    def querySQL(self,campos: dict):

        querys={

            'validar':

            """

            SELECT COUNT(*) FROM login WHERE EMAIL='{0}'

            """.format(campos['email']),

            'INSERT':

            """

            INSERT INTO login (EMAIL,TELEFONE,SENHA,CONECTADO)VALUES('{0}','{1}','{2}',{3})

            """.format(campos['email'],campos['celular'],campos['senha'],False),

            'UPDATE':

            """

            UPDATE login
            SET TELEFONE='{1}',
            SENHA='{2}',
            CONECTADO={3}
            WHERE EMAIL='{0}'

            """.format(campos['email'],campos['celular'],campos['senha'],False)

        }

        return querys

        pass

    def main(self):

        sql.CreateTable(tabelas)
        
        IP=s.gethostbyname(s.gethostname())
        path_dir=os.path.join(os.getcwd(),IP)
        temp_path=os.path.join(path_dir,'cadastro.txt')
        arq=glob(temp_path)

        placeholder=st.empty()

        path_css=os.path.join(os.getcwd(),'CSS','*.*')
        style_css=glob(path_css)

        with open(style_css[-1]) as file:

            st.markdown(f'<style>{file.read()}</style>',unsafe_allow_html=True)

            pass        

        with placeholder.container():
            
            if len(img)>0:

                with open(img[-1],'rb') as file:

                    st.image(file.read(),width=250)

                    pass

                st.markdown('----')

                pass

            temp_dict=dict()

            st.markdown('<h3>Cadastro de usuário</h3>',unsafe_allow_html=True)
            temp_dict['email']=st.text_input('E-mail',key='email')
            temp_dict['celular']=st.text_input('Celular',key='celular')
            col1,col2=st.columns(2)

            temp_dict['senha']=col1.text_input('Senha',key='senha',type='password')
            temp_dict['validar']=col2.text_input('Validar Senha',key='validarsenha',type='password')

            btn_save=st.button('Salvar',use_container_width=True,type='primary')
            btn_voltar=st.button('Voltar',use_container_width=True,type='secondary')

            pass

        if btn_save==True:

            resp=self.ValidarCampos(temp_dict)

            if 1 in resp.keys():

                mensagem=st.warning(f'Preencher o campo {resp[1]}')
                time.sleep(1)
                mensagem.empty()

                pass

            else:
                
                if temp_dict['senha']!=temp_dict['validar']:

                    mensagem=st.warning('Senha de confirmação não confere')
                    time.sleep(1)
                    mensagem.empty()

                    pass

                else:

                    querys=self.querySQL(temp_dict)
                    validar=sql.Code(querys['validar'])

                    tipo='INSERT' if validar<=0 else 'UPDATE'

                    sql.Save(querys[tipo])

                    mensagem=st.success('Dados salvo com sucesso')
                    time.sleep(1)
                    mensagem.empty()
                    time.sleep(1)

                    os.remove(arq[-1])
                    streamlit_js_eval(js_expressions='parent.window.location.reload()')

                    pass

                pass
                        
            pass

        if btn_voltar==True:
            
            os.remove(arq[-1])
            streamlit_js_eval(js_expressions='parent.window.location.reload()')

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