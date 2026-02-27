from app.front_end.screens.tela_logs_recebimento import menu_log_recebimento
from app.front_end.screens.tela_logs_devolução import menu_log_devolução
from app.front_end.screens.tela_configurações import menu_configurações
from app.front_end.screens.tela_recebimento import menu_recebimento
from app.front_end.screens.tela_logs_difal import menu_log_difal
from app.front_end.screens.menu_principal import menu_principal
from app.front_end.screens.tela_devolução import menu_devolução
from app.back_end.funções.funções_Gerais import navigate, resource_path
from app.front_end.screens.tela_difal import menu_difal
from app.front_end.screens.tela_login import login
import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False 
    page.window.maximizable = False

    current_view = ft.Column()

    # Dicionário de views
    views = {}

    tela_login = login(current_view, views, page)
    views['login'] = tela_login

    # Cria a tela de logs de recebimento e armazena a instância da classe Log
    tela_logs_recebimento, logger_recebimento = menu_log_recebimento(current_view, views, page)
    views['logs e informações recebimento'] = tela_logs_recebimento
    views['logger_recebimento'] = logger_recebimento  # Armazena a instância da classe Log

    tela_logs_devolução, logger_devolução = menu_log_devolução(current_view, views, page)
    views['logs e informações devolução'] = tela_logs_devolução
    views['logger_devolução'] = logger_devolução  # Armazena a instância da classe Log

    tela_logs_difal, logger_difal = menu_log_difal(current_view, views, page)
    views['logs e informações difal'] = tela_logs_difal
    views['logger_difal'] = logger_difal  # Armazena a instância da classe Log

    menu = menu_principal(current_view, views, page)
    views['Menu Principal'] = menu

    recebimento = menu_recebimento(current_view, views, page)
    views['Recebimento de peças'] = recebimento

    devolução = menu_devolução(current_view, views, page)
    views['Devolução de peças'] = devolução

    difal = menu_difal(current_view, views, page)
    views['Difal'] = difal

    configurações = menu_configurações(current_view, views, page)
    views['Configurações'] = configurações

    navigate(current_view = current_view, page = page, views = views, view_name = 'login')

    page.add(current_view)
    page.update()

ft.app(target = main, assets_dir = 'imagens')