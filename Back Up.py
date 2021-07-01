import PySimpleGUIWeb as sg
import sqlite3
import pandas as pd
import datetime
import matplotlib.pyplot as pl
import numpy as np


class webproject():
    def __init__(self):
        self.texto_arrumado = ''
        # Cor da Janela
        sg.ChangeLookAndFeel('black')
        # Inicioando o banco de dados
        self.iniciar_sql()
        # Criando a tabela caso ela não exista
        self.criando_tabela()
        # Lendo todos itens da tabela para amostragem
        self.itens_registro()
        # Estastisticas da tabela
        self.Estastisticas()
        # Abrindo variavel da janela
        self.layout()
        self.janela = sg.Window('Site', self.componentes, background_color='black', size=(1080, 600))
        while True:
            # Retorna a KEY e o VALOR dos elementos
            key, valor = self.janela.read()
            print(key, valor)

            if key == sg.WINDOW_CLOSED:
                # Para garantir que será possivel encerrar a aba
                break

            if key == '-ADICIONAR-':
                self.janela_adicionar()
            # Atualização para tela de adicionar registros

            if key == '-VOLTAR-':
                self.voltar_geral()
            # Voltando para tela principal

            if key == '-CONFIRMAR-':
                # Definindo variaveis que receberam os valores da respectiva leva de informações
                cor_da_linha = valor['-CORES-']
                tamanho_da_linha = valor['-TAMANHOS-']
                unidades_vendidas = valor['-QUANTIDADES-']
                valor_unitario = valor['-VALORES-']

                # Chamando comando def para adicionar as informações ao banco de dados
                self.adicionar_itens_tabela(CL=cor_da_linha, TR=tamanho_da_linha,
                                            UV=unidades_vendidas, VU=valor_unitario)

                # Voltando para a tela inicial após o cadastros no banco de dados das informações
                self.voltar_geral()

            if key == '-VER-':
                # Para ver os registros
                self.janela_registros()

            if key == '-ESTATISTICAS-':
                self.janela_de_estatisticas()


    def layout(self):
        self.componentes = [
            # Titulo
            [sg.Text('Menu', size=(192, 4), font=['calibri', 40], justification='center', key='-TITULO-')],

            # Tela de adicionar registros
            [sg.Text('Cor da Linha:', font=['calibri', 40], text_color='white', background_color='black', visible=False,
                     key='-TEXT_COR-'),
             sg.Combo(values=['Nenhum', 'Branco', 'Preto', 'Vermelho', 'Verde', 'Azul', 'Amarelo', 'Rosa'],
                      text_color='white', background_color='black', size=(25, 2), font=['calibri', 40],
                      visible=False, disabled=True, default_value='Nenhum', key='-CORES-')],
            [sg.Text('Tamanho do Rolo:', font=['calibri', 40], text_color='white', background_color='black',
                     visible=False,
                     key='-TEXT_TAMANHO-'),
             sg.Combo(values=['Nenhum', 'Grande', 'Medio', 'Pequeno'], size=(25, 2), font=['calibri', 40],
                      text_color='white', background_color='black', visible=False,
                      disabled=True, default_value='Nenhum', key='-TAMANHOS-')],
            [sg.Text('Unidades Vendidas:', font=['calibri', 40], text_color='white', background_color='black',
                     visible=False,
                     key='-TEXT_QUANTIDADE-'),
             sg.Spin(values=[0, 1, 2, 3], size=(20, 2), font=['calibri', 35], text_color='white',
                     background_color='black',
                     visible=False, key='-QUANTIDADES-')],
            [sg.Text('Valor Unitario:  R$', font=['calibri', 40], text_color='white', background_color='black',
                     visible=False,
                     key='-TEXT_VALOR-', size=(30, 2)),
             sg.Multiline('', key='-VALORES-', visible=False, text_color='white', background_color='black',
                          font=['calibri', 40], size=(20, 2))],
            [sg.Button('Voltar', key='-VOLTAR-', size=(20, 2), font=['calibri', 30], visible=False),
             # Botão de voltar universal
             sg.Button('Confirmar', key='-CONFIRMAR-', size=(20, 2), font=['calibri', 30], visible=False)],

            # Tela de visualização de cadastros
            [sg.MultilineOutput(F'{self.texto_arrumado}', font=['calibri', 30], key='-LISTA_CADASTROS-',
                                visible=False, text_color='white', background_color='black',
                                size_px=(1500, 1500), disabled=True)],
            # [sg.Button('Voltar',font=['calibri', 30], size=(20, 2), visible=False, key='-VOLTAR-')],
            # Menu Principal
            [sg.Button('Adicionar Cadastro', size=(40, 3), font=['calibri', 40], visible=True, key='-ADICIONAR-')],
            [sg.Button('Ver Historico de Vendas', size=(40, 3), font=['calibri', 40], visible=True, key='-VER-')],
            [sg.Button('Ver Estatísticas', size=(40, 3), font=['calibri', 40], visible=True, key='-ESTATISTICAS-')]]

    def voltar_geral(self):
        self.janela['-ADICIONAR-'].update(visible=True)
        self.janela['-VER-'].update(visible=True)
        self.janela['-ESTATISTICAS-'].update(visible=True)
        self.janela['-TITULO-'].update('Menu')
        self.janela['-TEXT_COR-'].update(visible=False)
        self.janela['-CORES-'].update(visible=False, disabled=True)
        self.janela['-TEXT_TAMANHO-'].update(visible=False)
        self.janela['-TAMANHOS-'].update(visible=False, disabled=True)
        self.janela['-TEXT_QUANTIDADE-'].update(visible=False)
        self.janela['-QUANTIDADES-'].update(visible=False)
        self.janela['-TEXT_VALOR-'].update(visible=False)
        self.janela['-VALORES-'].update(visible=False)
        self.janela['-VOLTAR-'].update(visible=False)
        self.janela['-CONFIRMAR-'].update(visible=False)
        self.janela['-LISTA_CADASTROS-'].update(visible=False)

    def janela_adicionar(self):
        self.janela['-ADICIONAR-'].update(visible=False)
        self.janela['-VER-'].update(visible=False)
        self.janela['-ESTATISTICAS-'].update(visible=False)
        self.janela['-TITULO-'].update('Adicionando Cadastro')
        self.janela['-TEXT_COR-'].update(visible=True)
        self.janela['-CORES-'].update(visible=True, disabled=False)
        self.janela['-TEXT_TAMANHO-'].update(visible=True)
        self.janela['-TAMANHOS-'].update(visible=True, disabled=False)
        self.janela['-TEXT_QUANTIDADE-'].update(visible=True)
        self.janela['-QUANTIDADES-'].update(visible=True)
        self.janela['-TEXT_VALOR-'].update(visible=True)
        self.janela['-VALORES-'].update(visible=True)
        self.janela['-VOLTAR-'].update(visible=True)
        self.janela['-CONFIRMAR-'].update(visible=True)

    def janela_registros(self):
        self.janela['-ADICIONAR-'].update(visible=False)
        self.janela['-VER-'].update(visible=False)
        self.janela['-ESTATISTICAS-'].update(visible=False)
        self.janela['-LISTA_CADASTROS-'].update(visible=True)
        self.janela['-VOLTAR-'].update(visible=True)
        self.janela['-VALORES-'].update(visible=False)

    def iniciar_sql(self):
        # Iniciando Banco de dados em sql como BDD e abrindo cursor como mouse
        self.BDD = sqlite3.connect('Registros.db')
        self.mouse = self.BDD.cursor()

    def criando_tabela(self):
        # Criando tabela com variaveis corretas
        self.mouse.execute('CREATE TABLE IF NOT EXISTS produtos_infos(CL TEXT, TR TEXT, ' \
                           'UV REAL, VU TEXT, DATA TEXT)')
        # Abreviações CL -> Cor do rolo. TR -> Tamanho do rolo. UV -> Unidades vendidas. VU -> Valor unitario.

    def adicionar_itens_tabela(self, CL, TR, UV, VU):
        data = str(datetime.datetime.now())
        data = data[:16]
        self.mouse.execute('INSERT INTO produtos_infos VALUES(?, ?, ?, ?, ?)', (CL, TR, UV, VU, data))
        self.BDD.commit()

    def itens_registro(self):
        # Criação da variavel que mostrará os dados já existentes na tabela
        self.mouse.execute('SELECT * FROM produtos_infos')
        lista_de_valores = self.mouse.fetchall()
        cl = []
        tr = []
        uv = []
        vu = []
        data = []
        for linha in range(0, len(lista_de_valores)):
            cl.append(lista_de_valores[linha][0])
            tr.append(lista_de_valores[linha][1])
            uv.append(lista_de_valores[linha][2])
            vu.append(lista_de_valores[linha][3])
            data.append(lista_de_valores[linha][4])
        dicionario = {'Cor da Linha': cl,
                      'Tamanho do Rolo': tr,
                      'Unidades Vendidas': uv,
                      'Valor da unidade': vu,
                      'Data da Venda': data}

        dataframe = pd.DataFrame(dicionario)
        # Opção para que não mostre o resumo da tabela e sim ela inteira
        pd.options.display.max_columns = 5
        pd.set_option('display.width', 200)
        pd.set_option('max_rows', dataframe.index.size)
        self.texto_arrumado = dataframe

    def Estastisticas(self):
        # Definição que coleta dados para uso estastistico
        vendas_por_tamanho = []
        # Retirando
        self.mouse.execute('SELECT UV FROM produtos_infos WHERE TR="Grande"')
        grandes_vendidos = self.mouse.fetchall()
        self.mouse.execute('SELECT UV FROM produtos_infos WHERE TR="Medio"')
        medios_vendidos = self.mouse.fetchall()
        self.mouse.execute('SELECT UV FROM produtos_infos WHERE TR="Pequeno"')
        pequenos_vendidos = self.mouse.fetchall()
        vendas_por_tamanho.append(np.cumsum(grandes_vendidos))
        vendas_por_tamanho.append(np.cumsum(medios_vendidos))
        vendas_por_tamanho.append(np.cumsum(pequenos_vendidos))
        self.grande_total = vendas_por_tamanho[0][-1]
        self.medio_total = vendas_por_tamanho[1][-1]
        self.pequeno_total = vendas_por_tamanho[2][-1]
        venda_total = self.grande_total+self.medio_total+self.pequeno_total


    def janela_de_estatisticas(self):
        self.janela['-VOLTAR-'].update(visible=True)
        self.janela['-ADICIONAR-'].update(visible=False)
        self.janela['-VER-'].update(visible=False)
        self.janela['-ESTATISTICAS-'].update(visible=False)
        pl.bar('Grande', self.grande_total, label='Rolos grandes vendidos', color='b')
        pl.bar('Medio', self.medio_total, label='Rolos medios vendidos', color='r')
        pl.bar('Pequeno', self.pequeno_total, label='Rolos pequenos vendidos', color='g')
        pl.legend()
        pl.show()



iniciar = webproject()