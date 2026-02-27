from app.back_end.funções.funções_Gerais import navigate, resource_path
from app.front_end.screens.cores_botoes import estilo_botao_neon_branco_login
import flet as ft

def login(current_view, views, page):

    page.title = 'Matec'
    page.padding = 0  
    page.margin = 0 
    page.spacing = 0
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False 
    page.window.maximizable = False

    snackbar = ft.SnackBar(content = ft.Text(""))
    page.snack_bar = snackbar 
    page.add(snackbar) 
    page.update() 

    def mostrar_snackbar(mensagem, cor):
        """Atualiza e exibe o SnackBar."""

        snackbar.content.value = mensagem 
        snackbar.bgcolor = cor 
        snackbar.open = True
        page.update() 

    def validar_usuario(e):
        """Valida o e-mail do usuário."""  
        mostrar_snackbar('Usuário autenticado com sucesso.', ft.Colors.GREEN)
        navigate(current_view, page, views, 'Menu Principal') 
        
        #email = input_usuario.value.strip()
        
        #if not email:  
            #mostrar_snackbar('Por favor, insira um usuário.', ft.Colors.RED)
        #elif email:
            #mostrar_snackbar('Usuário autenticado com sucesso.', ft.Colors.GREEN)
            #navigate(current_view, page, views, 'Menu Principal')

    imagem_logomarca = ft.Container(
        content = ft.Image(
            src = resource_path('app/front_end/imagens/LogoMarca.png'),
            fit = ft.ImageFit.CONTAIN,
            width = 70,
            height = 70,
            border_radius = 20
        ),
        alignment = ft.alignment.top_left,
        margin = ft.margin.only(top = -120)
    )

    texto_boas_vindas = ft.Text(
            'Boas vindas!',
            color = 'white',
            weight = 'bold',
            size = 55,
            font_family = 'Times New Roman', # Courier New; Times New Roman; Georgia
    )

    divisória = ft.Container(
        content = ft.Divider(
            height = 1,
            thickness = 2,
            color = ft.Colors.WHITE,
        ),
        width = 220
    )

    texto_apresentação = ft.Text(
        'Este é o XLogs, seu sistema de automação para processos logísticos. Ganhe eficiência, agilidade e controle total das operações.',
        color = 'white',
        size = 20
    )

    quadrante_boas_vindas = ft.Container(
        content = ft.Column(
            controls = [
                imagem_logomarca,
                texto_boas_vindas, 
                divisória,
                texto_apresentação
                ],
            spacing = 50,
            alignment = ft.MainAxisAlignment.CENTER,
            width = 480,
        ),
        margin = ft.margin.only(bottom = 150, left = -10)
    )

    input_usuario = ft.TextField(
        label = 'Usuário',
        border_radius = 15,
        color = ft.Colors.BLACK,
        bgcolor = ft.Colors.WHITE,
        border_color = ft.Colors.WHITE,
        label_style = ft.TextStyle(color = ft.Colors.BLACK38),
        prefix_icon = ft.Icon(ft.Icons.PERSON_SHARP, color = '#5A0B38'),
        width = 400
    )

    botao_entrar = ft.TextButton(
        text = 'Entrar',
        style = estilo_botao_neon_branco_login,
        width = 150,
        height = 50,
        on_click = validar_usuario
    )

    quadrante_principal = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text('Login', size = 30, weight = 'bold', color = ft.Colors.WHITE, text_align = ft.TextAlign.CENTER),
                input_usuario,
                ft.Divider(height = 1, thickness = 2, color = ft.Colors.WHITE),
                ft.Row(
                    controls = [
                        botao_entrar
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 50,
        ),
        border_radius = 20,
        padding = 20,
        width = 350,
        height = 400,
        border = ft.border.all(2, 'white'),
        bgcolor = ft.Colors.with_opacity(0.10, ft.Colors.BLACK),
        alignment = ft.alignment.center,
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
                    content = ft.Row(
                        controls = [quadrante_boas_vindas, quadrante_principal],
                        alignment = ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    alignment = ft.alignment.center,
                    expand = True,
                )
            ]
        ),
        expand = True,
        height = 800,
    )

    return container_pai
