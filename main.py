import streamlit as st
import os
from glob import glob
import time
from pages.templates import *
import socket as s
from SQL import SQL
from streamlit_js_eval import streamlit_js_eval

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

def querySQL(campos:dict):

    querys={

        'log':

        """
        
        SELECT COUNT(*) FROM login WHERE EMAIL='{0}' AND SENHA='{1}'

        """.format(campos['email'],campos['senha'])
    }

    return querys

    pass

def main():

    sql.CreateTable(tabelas)
    
    IP=s.gethostbyname(s.gethostname())
    path_dir=os.path.join(os.getcwd(),IP)
    os.makedirs(path_dir,exist_ok=True)
    temp_path=os.path.join(path_dir,'*.txt*')
    arq=glob(temp_path)

    page_dict={'cadastro.txt':'CadastroUser','menu.txt':'Menu'}

    if len(arq)<=0:

        placeholder=st.empty()

        temp_dict=dict()

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

            st.markdown('<h3>Login</h3>',unsafe_allow_html=True)
            temp_dict['email']=st.text_input('Usuário',label_visibility='visible',key='user').lower()
            temp_dict['senha']=st.text_input('Senha',label_visibility='visible',key='password').lower()
            btn_entrar=st.button('Entrar',use_container_width=True,type='primary')
            btn_cad=st.button('Cadastro',use_container_width=True)

            pass

        if btn_entrar==True:

            resp=ValidarCampos(temp_dict)

            if 1 in resp.keys():

                mensagem=st.warning(f'Preencher o campo {resp[1]}')
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                querys=querySQL(temp_dict)                
                validar=sql.Code(querys['log'])

                if validar>0:

                    mensagem=st.success('Seja bem vindo')
                    time.sleep(1)
                    mensagem.empty()
                    time.sleep(1)

                    temp_path=os.path.join(path_dir,'menu.txt')
                    with open(temp_path,'w') as file:

                        file.write(temp_dict['email'])

                        pass

                    placeholder.empty()
                    time.sleep(1)
                    tela=Menu()
                    tela.main()

                    pass

                else:

                    mensagem=st.warning('Usuário ou senha não confere')
                    time.sleep(1)
                    mensagem.empty()
                    
                    pass

                pass      
            
            pass

        if btn_cad==True:
            
            placeholder.empty()

            temp_path=os.path.join(path_dir,'cadastro.txt')
            with open(temp_path,'w') as file:

                file.write('cadastro')

                pass

            tela=CadastroUser()
            tela.main()

            pass

        pass

    else:

        arq=os.path.basename(arq[-1])

        tela=globals().get(page_dict[arq])()
        tela.main()  

        pass

    pass


def ValidarCampos(campos: dict):

    erro_dict=dict()

    for k,v in campos.items():

        if v=='':

            erro_dict[1]=k

            break

        pass
    
    return erro_dict
    
    pass


if __name__=='__main__':

    main()

    pass