import sqlite3
import pandas as pd

class SQL:

    def __init__(self) -> None:
        pass

    def Conexao(self):

        try:
            
            conectando=sqlite3.connect('MOINHO.db')

            return conectando

            pass

        except Exception as erro:

            print('Sem conexão com o banco de dados')

            pass

        pass

    def Save(self,query):

        conectando=self.Conexao()

        cursor=conectando.cursor()
        cursor.execute(query)

        conectando.commit()
      
        
        pass

    def Code(self,query):

        conectando=self.Conexao()

        cursor=conectando.cursor()
        cursor.execute(query)

        codigo=[l for l in cursor.fetchone()]

        return codigo[-1]       

        pass

    def DataFrame(self,querys: dict):

        temp_dict=dict()

        conectando=self.Conexao()

        for tabela,query in querys.items():
            
            temp_dict[tabela]=pd.read_sql(query,conectando)

            pass

        return temp_dict

        pass

    def CreateTable(self,querys:dict):

        for query in querys.values():

            self.Save(query)

            pass

        pass

    pass