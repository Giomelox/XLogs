import pandas as pd
import flet as ft
import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Quando empacotado
    except AttributeError:
        base_path = os.path.abspath(".")  # Quando em desenvolvimento
    return os.path.join(base_path, relative_path)

class Log:
    def __init__(self, text_field):
        self.text_field = text_field  # Armazena o TextField

    def log_message(self, message):
        try:
            # Atualiza o valor do TextField com a nova mensagem
            self.text_field.value += f"{message}\n{'-' * 109}"
            self.text_field.update()  # Atualiza o TextField na interface
        except AssertionError:
            pass

    def limpar(self, e = None):   
        self.text_field.value = ''
        self.text_field.update()

class PlanilhaManager:
    _instance = None
    planilha_df = None
    file_path = None
    last_modified = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PlanilhaManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_planilha(self, df, file_path):
        self.planilha_df = df
        self.file_path = file_path
        self.last_modified = os.path.getmtime(file_path)

    def get_planilha(self):
        return self.planilha_df

    def is_planilha_atualizada(self):
        if self.file_path and os.path.exists(self.file_path):
            current_mod_time = os.path.getmtime(self.file_path)
            return current_mod_time != self.last_modified
        return False

    def recarregar_planilha(self):
        if self.file_path:
            df = pd.read_excel(self.file_path, sheet_name = 'Processos devolução (programa)')
            self.set_planilha(df, self.file_path)

class SolicitarPlanilha:
    def __init__(self, page: ft.Page):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.escolher_planilha)
        self.page.overlay.append(self.file_picker)
        self.planilha_manager = PlanilhaManager()

    def abrir_seletor(self, e):
        """Abre o seletor de arquivos para o usuário escolher um arquivo Excel."""
        self.file_picker.pick_files(allowed_extensions=["xlsx", "xls"])

    def escolher_planilha(self, e: ft.FilePickerResultEvent):

        snackbar = ft.SnackBar(content=ft.Text(""))
        self.page.snack_bar = snackbar 
        self.page.add(snackbar) 
        self.page.update() 

        def mostrar_snackbar(mensagem, cor):
            """Atualiza e exibe o SnackBar."""

            snackbar.content.value = mensagem 
            snackbar.bgcolor = cor 
            snackbar.open = True
            self.page.update() 

        """Lida com o arquivo escolhido pelo usuário."""
        if not e.files:
            mostrar_snackbar("Nenhum arquivo selecionado.", ft.Colors.RED)
            return None

        file_path = e.files[0].path  # Caminho do arquivo selecionado
        try:
            with pd.ExcelFile(file_path) as excel_file:
                sheets = excel_file.sheet_names

                sheet_name = "Processos devolução (programa)" if "Processos devolução (programa)" in sheets else sheets[0]

                planilha_df = pd.read_excel(excel_file, sheet_name = sheet_name, header = 0 if sheet_name == "Processos devolução (programa)" else None)
                
            mostrar_snackbar(f"Planilha '{sheet_name}' carregada com sucesso!", ft.Colors.GREEN)

            # Armazena a planilha no gerenciador
            self.planilha_manager.set_planilha(planilha_df, file_path)

            return planilha_df

        except Exception as e:
            mostrar_snackbar(f"Erro ao carregar a planilha: {str(e)}", ft.Colors.RED)
            return None

@staticmethod
def obter_configs():
    """Carrega as configurações do arquivo e retorna como dicionário"""
    try:
        with open('Configurações de usuário.txt', 'r') as f:
            dados = f.read()
            dados = [item.strip() for item in dados.split(',')]
            return {
                'email': dados[0],
                'caixa_email': dados[1],
                'usuario_Elogistic': dados[2],
                'senha_Elogistic': dados[3],
                'usuario_IOB': dados[4],
                'senha_IOB': dados[5],
                'cliente_circulação': dados[6],
                'cliente_recebimento': dados[7],
                'natureza_circulação': dados[8],
                'natureza_recebimento_good': dados[9],
                'natureza_recebimento_defective': dados[10],
                'cliente_devoluçãoDell': dados[11],
                'cliente_devoluçãoHP': dados[12],
                'cliente_devolução_flex': dados [13],
                'natureza_devolução_flex': dados [14],
                'natureza_devolução_good': dados[15],
                'natureza_devolução_defective': dados[16],
                'transportadora_dell': dados[17],
                'transportadora_hp': dados[18],
                'nome_credenciada': dados[19],
                'cnpj_credenciada': dados[20],
                'aliquota_interna': dados[21],
                'botao_switch_para_icms': dados[22]
            }
    except FileNotFoundError:
        return {}

if obter_configs:
    conta_email = obter_configs().get('email')
    caixa_emails = obter_configs().get('caixa_emails')
    usuario_elogistica = obter_configs().get('usuario_Elogistic')
    senha_elogistica = obter_configs().get('senha_Elogistic')
    usuario_IOB = obter_configs().get('usuario_IOB')
    senha_IOB = obter_configs().get('senha_IOB')
    cliente_circulação = obter_configs().get('cliente_circulação')
    cliente_recebimento = obter_configs().get('cliente_recebimento')
    natureza_circulação = obter_configs().get('natureza_circulação')
    natureza_recebimento_good = obter_configs().get('natureza_recebimento_good')
    natureza_recebimento_defective = obter_configs().get('natureza_recebimento_defective')
    cliente_devolução_dell = obter_configs().get('cliente_devoluçãoDell')
    cliente_devolução_hp = obter_configs().get('cliente_devoluçãoHP')
    cliente_devolução_flex = obter_configs().get('cliente_devolução_flex'),
    natureza_devolução_flex = obter_configs().get('natureza_devolução_flex'),
    natureza_devolução_good = obter_configs().get('natureza_devolução_good')
    natureza_devolução_defective = obter_configs().get('natureza_devolução_defective')
    transportadora_dell = obter_configs().get('transportadora_dell')
    transportador_hp = obter_configs().get('transportador_hp')
    nome_credenciada = obter_configs().get('nome_credenciada')
    cnpj_credenciada = obter_configs().get('cnpj_credenciada')
    aliquota_credenciada = obter_configs().get('aliquota_interna')
    botao_switch_para_icms = obter_configs().get('botao_switch_para_icms')

def navigate(current_view, page, views, view_name):
    # Esconde todas as views
    for view in views.values():
        view.visible = False  # Torna todas as views invisíveis

    # Verifica se a view solicitada está no dicionário
    if view_name in views:
        # Torna a view visível
        views[view_name].visible = True

        # Limpa os controles do current_view (a "container" da página)
        current_view.controls.clear()
        
        # Adiciona a view solicitada ao current_view
        current_view.controls.append(views[view_name])
        
        # Atualiza a página para refletir as mudanças
        page.update()
