import streamlit as st
from streamlit_option_menu import option_menu
import os
from glob import glob
import socket as s
from datetime import datetime
from .configuracao import Configuracoes
from .mensagens import Mensagem

class Menu:

    def main(self):

        placeholder=st.empty()

        IP=s.gethostbyname(s.gethostname())
        path_dir=os.path.join(os.getcwd(),IP)
        os.makedirs(path_dir,exist_ok=True)
        temp_path=os.path.join(path_dir,'menu.txt')
        arq=glob(temp_path)

        with open(arq[-1],'r') as file:

            user=file.read()

            pass
        
        dt_now=datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M:%S')

        with placeholder.container():

            with st.sidebar:

                st.write(f'Usuário Logado: {user}')
                st.write(f'Data e Hora: {dt_now}')
                st.markdown('----')

                selected = option_menu(f'Opções', ["Mensagens", 'Configurações','Sair'], 
                    icons=['house', 'gear','box-arrow-left'], menu_icon="cast", default_index=0)

                page_dict={'Configurações':'Configuracoes','Mensagens':'Mensagem'}

                pass

            if selected in page_dict.keys():

                tela=globals().get(page_dict[selected])()
                tela.main()

                pass            

            pass

        pass

    pass