from app.back_end.funções.funções_Gerais import navigate, Log, resource_path
from app.front_end.screens.cores_botoes import estilo_botao_neon_branco_superiores
import flet as ft

def menu_log_difal(current_view, views, page):

    page.title = 'Matec'
    page.padding = 0  
    page.margin = 0 
    page.spacing = 0
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False 
    page.window.maximizable = False
    page.theme = ft.Theme(
        scrollbar_theme = ft.ScrollbarTheme(
            thickness = 15,               # Espessura da barra
            radius = 20,                  # Raio da borda da barra
            thumb_color = 'blue',         # Cor da barra de rolagem
            cross_axis_margin = -8
        )
    )

    log_text_field = ft.TextField(
        value = '', 
        color = 'white',
        multiline = True,
        read_only = True, 
        height = 780,
        width = page.width,
        text_style = ft.TextStyle(size = 20),
    )

    logger = Log(log_text_field)

    botao_voltar = ft.Container(
        content = ft.ElevatedButton(
            text = 'Voltar',
            style = estilo_botao_neon_branco_superiores,
            width = 200,
            height = 40,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Difal'),
        ),
        margin = ft.margin.only(top = 15, left = 10),
        width = 150
    )

    botao_limpar = ft.Container(
        content = ft.ElevatedButton(
            text = 'Limpar',
            style = estilo_botao_neon_branco_superiores,
            width = 200,
            height = 40,
            on_click = logger.limpar
        ),
        margin = ft.margin.only(top = 15, right = 10),
        width = 150
    )

    container_logs = ft.Container(
        content = ft.ListView(
            controls = [log_text_field],
            auto_scroll = True,
            expand = True
        ),
        width = 960,
        height = 680,
        bgcolor = 'black',
        border = ft.border.all(2, 'white'),
        border_radius = 10,
    )

    container_pai = ft.Container(
        content = ft.Stack(
            controls = [
                ft.Image(
                    src = resource_path('app/front_end/imagens/imagem_tela_login.png'),
                    width = float('inf'),
                    height = 800,
                    fit = ft.ImageFit.COVER
                ),
                ft.Container(
                    content = ft.Column(
                        controls = [

                            ft.Row(
                                controls = [botao_voltar, botao_limpar],
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                            ),

                            ft.Column(
                                controls = [
                                    ft.Container(
                                        content = ft.Row(
                                            controls = [container_logs],
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 40,
                                        ),
                                        alignment = ft.alignment.center,
                                    ),
                                ],
                                alignment = ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                    alignment = ft.alignment.center,
                    width = 1000,
                    height = 700,
                    expand = True,
                )
            ]
        ),
        expand = True,
        height = 800,
    )

    return container_pai, logger
