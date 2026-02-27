from app.back_end.funções.funções_elogistic import valores_devolução_DELL, valores_devolução_HP, criar_etiquetas_devolução_dell
from app.front_end.screens.cores_botoes import estilo_botao_neon_branco, estilo_botao_neon_branco_superiores
from app.back_end.funções.funções_IOB import emitir_NF_dev_dell, emitir_NF_dev_hp, emitir_NF_dev_flex
from app.back_end.funções.funções_Gerais import navigate, resource_path
import flet as ft

def menu_devolução(current_view, views, page):

    page.title = 'Matec'
    page.padding = 0  
    page.margin = 0 
    page.spacing = 0
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False 
    page.window.maximizable = False

    logger = views['logger_devolução']

    voltar_e_visualizar = ft.Container(
        content = ft.Row(
            controls = [

                ft.Container(
                    content = ft.ElevatedButton(
                        text = 'Voltar',
                        style = estilo_botao_neon_branco_superiores,
                        width = 200,
                        height = 40,
                        on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Menu Principal'),
                    ),
                    width = 150
                ),
                
                ft.Container(
                    content = ft.ElevatedButton(
                        text = 'Progresso',
                        style = estilo_botao_neon_branco_superiores,
                        width = 200,
                        height = 40,
                        on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'logs e informações devolução'),
                    ),
                    width = 150
                )
                
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        margin = ft.margin.only(top = 15, left = 10),
        width = 965
    )

    texto_dell = ft.Container(
        content = ft.Text(
            'Dell',
            size = 25,
            weight = 'bold',
            color = 'white',
            text_align = ft.alignment.top_center
        ),
        margin = ft.margin.only(top = 10) 
    )
    
    texto_HP = ft.Container(
        content = ft.Text(
            'HP',
            size = 25,
            weight = 'bold',
            color = 'white',
            text_align = ft.alignment.top_center
        ),
        margin = ft.margin.only(top = 10) 
    )

    container_botoes_dell = ft.Container(
    content = ft.Column(
        controls = [

            ft.ElevatedButton(
                text = 'Valores Devolução',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: valores_devolução_DELL(page, logger, views = views, current_view = current_view)
            ),

            ft.ElevatedButton(
                text = 'Emitir NF',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: emitir_NF_dev_dell(logger, page = page, views = views, current_view = current_view)
            ),

            ft.ElevatedButton(
                text = 'Gerar Etiquetas',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: criar_etiquetas_devolução_dell(logger, page = page, views = views, current_view = current_view)
            ),

            ],
            scroll = ft.ScrollMode.AUTO,
        ),
        height = 300,  
    )

    container_botoes_HP = ft.Container(
    content = ft.Column(
        controls = [

            ft.ElevatedButton(
                text = 'Valores Devolução',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: valores_devolução_HP(page, logger, views = views, current_view = current_view)
            ),

            ft.ElevatedButton(
                text = 'Emitir NF',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: emitir_NF_dev_hp(logger, page = page, views = views, current_view = current_view)
            ),

            ft.ElevatedButton(
                text = 'Emitir NF flex',
                style = ft.ButtonStyle(text_style = ft.TextStyle(size = 18), overlay_color = 'purple'),
                color = 'black',
                width = 200,
                height = 40,
                on_click = lambda e: emitir_NF_dev_flex(logger, page = page, views = views, current_view = current_view)
            ),
            ],
            scroll = ft.ScrollMode.AUTO,
        ),
        height = 300,  
    )

    container_dell = ft.Container(
        content = ft.Container(
            content = ft.Column(
                controls = [
                    texto_dell,
                    ft.Divider(height = 1, thickness = 2, color = 'red'),
                    container_botoes_dell,
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 10,
            ),
            padding = 20,
            bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
            border_radius = 18,  
        ),
        width = 330,
        height = 400,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        margin = ft.margin.only(bottom = 120),
    )

    container_HP = ft.Container(
        content = ft.Container(
            content = ft.Column(
                controls = [
                    texto_HP,
                    ft.Divider(height = 1, thickness = 2, color = 'red'),
                    container_botoes_HP
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                spacing = 10,
            ),
            padding = 20,
            bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
            border_radius = 18,  
        ),
        width = 330,
        height = 400,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        margin = ft.margin.only(bottom = 120),
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
                                controls = [voltar_e_visualizar],
                                alignment = ft.MainAxisAlignment.START
                            ),

                            ft.Column(
                                controls = [
                                    ft.Container(
                                        content = ft.Row(
                                            controls = [container_dell, container_HP],
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 40,
                                        ),
                                        alignment = ft.alignment.center,
                                    ),
                                ],
                                alignment = ft.MainAxisAlignment.CENTER,
                                expand = True,
                            ),
                        ],
                    ),
                    alignment = ft.alignment.center,
                    width = 1000,
                    height = 800,
                    expand = True,
                )
            ]
        ),
        expand = True,
        height = 800,
    )

    return container_pai
