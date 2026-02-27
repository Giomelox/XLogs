from app.back_end.funções.funções_Gerais import navigate, resource_path
from app.front_end.screens.cores_botoes import estilo_botao_neon_branco, estilo_botao_neon_branco_superiores, estilo_botao_neon_branco_cancelar, estilo_botao_neon_branco_salvar
import flet as ft

def menu_configurações(current_view, views, page):

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
            thickness = 7,               # Espessura da barra
            radius = 20,                  # Raio da borda da barra
            thumb_color = 'white',          # Cor da barra de rolagem
            cross_axis_margin = -11
        )
    )

    def fechar_dialogo():
        if expandir.alerta:
            expandir.alerta.open = False

        expandir.expandido = False
        page.update()

    def carregar_configs():
        try:
            with open('Configurações de usuário.txt', 'r') as f:
                dados = f.read()

                # Divide a string lida nos campos usando a vírgula como separador
                dados = [item.strip() for item in dados.split(',')]

                # Atribui os valores lidos para os campos de texto
                armazenar_email.value = dados[0]
                armazenar_caixa_email.value = dados[1]
                armazenar_usuario_elogistc.value = dados[2]
                armazenar_senha_elogistc.value = dados[3]
                armazenar_usuario_iob.value = dados[4]
                armazenar_senha_IOB.value = dados[5]
                armazenar_cliente_circulação_IOB.value = dados[6]
                armazenar_cliente_recebimento_IOB.value = dados[7]
                armazenar_natureza_circulação_IOB.value = dados[8]
                armazenar_natureza_recebimento_GOOD_IOB.value = dados[9]
                armazenar_natureza_recebimento_DEFECTIVE_IOB.value = dados[10]
                armazenar_cliente_devolução_dell_IOB.value = dados[11]
                armazenar_cliente_devolução_hp_IOB.value = dados[12]
                armazenar_cliente_devolução_flex_IOB.value = dados[13]
                armazenar_natureza_devolução_flex_IOB.value = dados[14]
                armazenar_natureza_devolução_good_IOB.value = dados[15]
                armazenar_natureza_devolução_defective_IOB.value = dados[16]
                armazenar_transporadora_dell_IOB.value = dados[17]
                armazenar_transporadora_hp_IOB.value = dados[18]
                armazenar_nome_credenciada.value = dados[19]
                armazenar_cnpj_credenciada.value = dados[20]
                armazenar_aliquota_interna.value = dados[21]
                switch_icms.value = dados[22]

        except FileNotFoundError:
            pass  # Caso o arquivo não exista, não faz nada
        except ValueError:
            pass  # Caso os dados estejam no formato incorreto

    def salvar_configs(e = None):
        email = armazenar_email.value
        caixa_email = armazenar_caixa_email.value
        usuario_Elogistica = armazenar_usuario_elogistc.value
        senha_Elogistica = armazenar_senha_elogistc.value
        usuario_IOB = armazenar_usuario_iob.value
        senha_IOB = armazenar_senha_IOB.value
        cliente_circulacao = armazenar_cliente_circulação_IOB.value
        cliente_recebimento = armazenar_cliente_recebimento_IOB.value
        natureza_circulacao = armazenar_natureza_circulação_IOB.value
        natureza_recebimento_good = armazenar_natureza_recebimento_GOOD_IOB.value
        natureza_recebimento_defective = armazenar_natureza_recebimento_DEFECTIVE_IOB.value
        cliente_devolucao_dell = armazenar_cliente_devolução_dell_IOB.value
        cliente_devolucao_hp = armazenar_cliente_devolução_hp_IOB.value
        cliente_devolução_flex = armazenar_cliente_devolução_flex_IOB.value
        natureza_devolução_flex = armazenar_natureza_devolução_flex_IOB.value
        natureza_devolucao_good = armazenar_natureza_devolução_good_IOB.value
        natureza_devolucao_defective = armazenar_natureza_devolução_defective_IOB.value
        transportadora_dell = armazenar_transporadora_dell_IOB.value
        transportadora_hp = armazenar_transporadora_hp_IOB.value
        nome_credenciada = armazenar_nome_credenciada.value
        cnpj_credenciada = armazenar_cnpj_credenciada.value
        aliquota_interna = armazenar_aliquota_interna.value
        botao_switch_para_icms = switch_icms.value

        try:
            with open('Configurações de usuário.txt', 'w') as f:
                f.write(f'{email}, {caixa_email}, {usuario_Elogistica}, {senha_Elogistica}, {usuario_IOB}, {senha_IOB},'
                        f'{cliente_circulacao}, {cliente_recebimento}, {natureza_circulacao}, {natureza_recebimento_good}, {natureza_recebimento_defective}, {cliente_devolucao_dell},'
                        f'{cliente_devolucao_hp}, {cliente_devolução_flex}, {natureza_devolução_flex}, {natureza_devolucao_good}, {natureza_devolucao_defective}, {transportadora_dell}, {transportadora_hp},'
                        f'{nome_credenciada}, {cnpj_credenciada}, {aliquota_interna}, {botao_switch_para_icms}')

            fechar_dialogo()
            snackbar = ft.SnackBar(content = ft.Text('Alterações salvas com sucesso.'), bgcolor = ft.Colors.GREEN)

            page.snack_bar = snackbar
            page.snack_bar.open = True
            page.update()
        
        except Exception as e:
            snackbar = ft.SnackBar(content = ft.Text(f'Erro ao salvar: {e}'), bgcolor = ft.Colors.RED)

            page.snack_bar = snackbar
            page.snack_bar.open = True
            page.update()  

    def cancelar_e_obter_configs(e):
        carregar_configs()
        fechar_dialogo()
        
    class alert_dialog:

        @staticmethod
        def alerta_email(e):

            container_armazenar_email = ft.Container(
                content = armazenar_email,
                width = 620,
                height = 70
            )

            container_armazenar_caixa_email = ft.Container(
                content = armazenar_caixa_email,
                width = 620,
                height = 70
            )

            email_expandido_alerta = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Container(),
                        container_armazenar_email,
                        container_armazenar_caixa_email
                    ],
                    scroll = ft.ScrollMode.AUTO,
                ),
                height = 530,
                margin = ft.margin.only(top = 10),
            )
       
            return ft.AlertDialog(
                title = ft.Text(
                    'Editar informações de Email',
                    color = 'white'
                ),
                content = ft.Column( 
                    controls = [ 
                        email_expandido_alerta, 
                    ], 
                    width = 610, 
                    height = 700 
                ),
                actions = [
                    ft.Container(
                        content = ft.Row(
                            controls = [

                                ft.ElevatedButton(
                                    'Cancelar', 
                                    on_click = cancelar_e_obter_configs,
                                    width = 200,
                                    height = 50,
                                    style = estilo_botao_neon_branco_cancelar
                                ),

                                salvar_email
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )    
                ],
                bgcolor = 'black',
            )

        def alerta_elogistic(e):

            container_armazenar_usuario_elogistic = ft.Container(
                content = armazenar_usuario_elogistc,
                width = 620,
                height = 70
            )

            container_armazenar_senha_elogistic = ft.Container(
                content = armazenar_senha_elogistc,
                width = 620,
                height = 70
            )

            elogistic_expandido_alerta = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Container(),
                        container_armazenar_usuario_elogistic,
                        container_armazenar_senha_elogistic
                    ],
                    scroll = ft.ScrollMode.AUTO,
                ),
                height = 530,
                margin = ft.margin.only(top = 10),
            )

            return ft.AlertDialog(
                title = ft.Text(
                    'Editar informações do E-logistic',
                    color = 'white'
                ),
                content = ft.Column(
                    controls = [
                        elogistic_expandido_alerta,
                    ],
                    width = 610,
                    height = 700
                ),

                actions = [
                    ft.Container(
                        content = ft.Row(
                            controls = [

                                ft.ElevatedButton(
                                    'Cancelar', 
                                    on_click = cancelar_e_obter_configs,
                                    width = 200,
                                    height = 50,
                                    style = estilo_botao_neon_branco_cancelar
                                ),

                                salvar_elogistic
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )    
                ],
                bgcolor = 'black',
            )
        
        def alerta_IOB(e):

            container_armazenar_usuario_iob = ft.Container(
                content = armazenar_usuario_iob,
                width = 620,
                height = 70
            )

            container_armazenar_senha_IOB = ft.Container(
                content = armazenar_senha_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_cliente_circulação_IOB = ft.Container(
                content = armazenar_cliente_circulação_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_cliente_recebimento_IOB = ft.Container(
                content = armazenar_cliente_recebimento_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_circulação_IOB = ft.Container(
                content = armazenar_natureza_circulação_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_recebimento_GOOD_IOB = ft.Container(
                content = armazenar_natureza_recebimento_GOOD_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_recebimento_DEFECTIVE_IOB = ft.Container(
                content = armazenar_natureza_recebimento_DEFECTIVE_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_cliente_devolução_dell_IOB = ft.Container(
                content = armazenar_cliente_devolução_dell_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_cliente_devolução_hp_IOB = ft.Container(
                content = armazenar_cliente_devolução_hp_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_cliente_devolução_hp_flex_IOB = ft.Container(
                content = armazenar_cliente_devolução_flex_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_devolução_hp_flex_IOB = ft.Container(
                content = armazenar_natureza_devolução_flex_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_devolução_good_IOB = ft.Container(
                content = armazenar_natureza_devolução_good_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_natureza_devolução_defective_IOB = ft.Container(
                content = armazenar_natureza_devolução_defective_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_transporadora_dell_IOB = ft.Container(
                content = armazenar_transporadora_dell_IOB,
                width = 620,
                height = 70
            )

            container_armazenar_transporadora_hp_IOB = ft.Container(
                content = armazenar_transporadora_hp_IOB,
                width = 620,
                height = 70
            )
 
            IOB_expandido_alerta = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Container(),
                        container_armazenar_usuario_iob,
                        container_armazenar_senha_IOB,
                        container_armazenar_cliente_circulação_IOB,
                        container_armazenar_cliente_recebimento_IOB,
                        container_armazenar_natureza_circulação_IOB,
                        container_armazenar_natureza_recebimento_GOOD_IOB,
                        container_armazenar_natureza_recebimento_DEFECTIVE_IOB,
                        container_armazenar_cliente_devolução_dell_IOB,
                        container_armazenar_cliente_devolução_hp_IOB,
                        container_armazenar_cliente_devolução_hp_flex_IOB,
                        container_armazenar_natureza_devolução_hp_flex_IOB,
                        container_armazenar_natureza_devolução_good_IOB,
                        container_armazenar_natureza_devolução_defective_IOB,
                        container_armazenar_transporadora_dell_IOB,
                        container_armazenar_transporadora_hp_IOB

                    ],
                    scroll = ft.ScrollMode.AUTO,
                ),
                height = 530,
                margin = ft.margin.only(top = 10),
            )

            return ft.AlertDialog(
                title = ft.Text(
                    'Editar informações do IOB',
                    color = 'white'
                ),
                content = ft.Column(
                    controls = [
                        IOB_expandido_alerta
                    ],
                    width = 610,
                    height = 700,
                ),
                actions = [
                    ft.Container(
                        content = ft.Row(
                            controls = [

                                ft.ElevatedButton(
                                    'Cancelar', 
                                    on_click = cancelar_e_obter_configs,
                                    width = 200,
                                    height = 50,
                                    style = estilo_botao_neon_branco_cancelar
                                ),

                                salvar_IOB
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )    
                ],
                bgcolor = 'black',
            )
        
        def alerta_difal(e):

            container_armazenar_nome_credenciada = ft.Container(
                content = armazenar_nome_credenciada,
                width = 620,
                height = 70
            )

            container_armazenar_cnpj_credenciada = ft.Container(
                content = armazenar_cnpj_credenciada,
                width = 620,
                height = 70
            )

            container_armazenar_aliquota_interna = ft.Container(
                content = armazenar_aliquota_interna,
                width = 620,
                height = 70
            )

            elogistic_expandido_alerta = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Container(),
                        container_armazenar_nome_credenciada,
                        container_armazenar_cnpj_credenciada,
                        container_armazenar_aliquota_interna
                    ],
                    scroll = ft.ScrollMode.AUTO,
                ),
                height = 530,
                margin = ft.margin.only(top = 10),
            )

            return ft.AlertDialog(
                title = ft.Text(
                    'Editar informações do Difal',
                    color = 'white'
                ),
                content = ft.Column(
                    controls = [
                        elogistic_expandido_alerta
                    ],
                    width = 610,
                    height = 700,
                ),
                actions = [
                    ft.Container(
                        content = ft.Row(
                            controls = [

                                ft.ElevatedButton(
                                    'Cancelar', 
                                    on_click = cancelar_e_obter_configs,
                                    width = 200,
                                    height = 50,
                                    style = estilo_botao_neon_branco_cancelar
                                ),

                                salvar_difal
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )    
                ],
                bgcolor = 'black',
            )

    class expandir:
        expandido = False

        alerta = None
        
        @staticmethod
        def expandir_container_email(e):

            expandir.expandido = not expandir.expandido

            if expandir.expandido:
                
                expandir.alerta = alert_dialog.alerta_email(e)

                if expandir.alerta not in page.overlay:
                
                    page.overlay.append(expandir.alerta)
                    expandir.alerta.open = True

            else:
                fechar_dialogo()
                botao_expandir_email.icon = ft.Icons.LIST
            
            page.update()
        
        @staticmethod
        def expandir_container_elogistic(e):

            expandir.expandido = not expandir.expandido

            if expandir.expandido:
                
                expandir.alerta = alert_dialog.alerta_elogistic(e)

                if expandir.alerta not in page.overlay:
                
                    page.overlay.append(expandir.alerta)
                    expandir.alerta.open = True

            else:
                fechar_dialogo()
                botao_expandir_email.icon = ft.Icons.LIST
            
            page.update()

        @staticmethod
        def expandir_container_IOB(e):

            expandir.expandido = not expandir.expandido

            if expandir.expandido:
                
                expandir.alerta = alert_dialog.alerta_IOB(e)

                if expandir.alerta not in page.overlay:
                
                    page.overlay.append(expandir.alerta)
                    expandir.alerta.open = True

            else:
                fechar_dialogo()
                botao_expandir_email.icon = ft.Icons.LIST
            
            page.update()

        @staticmethod
        def expandir_container_difal(e):

            expandir.expandido = not expandir.expandido

            if expandir.expandido:
                
                expandir.alerta = alert_dialog.alerta_difal(e)

                if expandir.alerta not in page.overlay:
                
                    page.overlay.append(expandir.alerta)
                    expandir.alerta.open = True

            else:
                fechar_dialogo()
                botao_expandir_email.icon = ft.Icons.LIST
            
            page.update()

    """
    serve de alternativa para quando eu quiser adicionar um botão de senha, para alterar a visibilidade das mesmas.
    porém precisa saber ajustar a legenda do text label

    senhas_visiveis = {
        'Senha E-logistic': False,
        'Senha IOB': False
    }
    
    def visualizar_senha(e, nome_senha, campo):
        senhas_visiveis[nome_senha] = not senhas_visiveis[nome_senha]
        campo.password = not senhas_visiveis[nome_senha]
        campo.suffix_icon = ft.IconButton(
            icon = ft.Icons.VISIBILITY if senhas_visiveis[nome_senha] else ft.Icons.VISIBILITY_OFF,
            on_click = lambda e: visualizar_senha(e, nome_senha, campo)
        )
        campo.update()
    """

    botao_voltar = ft.Container(
        content = ft.ElevatedButton(
            text = 'Voltar',
            style = estilo_botao_neon_branco_superiores,
            width = 200,
            height = 40,
            on_click = lambda e: navigate(current_view = page.controls[1], page = page, views = views, view_name = 'Menu Principal'),
        ),
        margin = ft.margin.only(top = 15, left = 10),
        width = 150
    )

    switch_icms = ft.Switch(
        label='Configurações de ICMS',
        width = 200,
        height = 40,
        on_change = salvar_configs
    )

    botao_switch_para_icms = ft.Container(
        content = switch_icms,
        margin = ft.margin.only(top = 15, left = 10),
        width = 250,
        height = 40
    )

    botao_expandir_email = ft.Container(
        content = ft.IconButton(
            icon = ft.Icons.LIST,
            on_click = expandir.expandir_container_email,
            tooltip = 'Expandir/Recolher',
            icon_color = ft.Colors.ORANGE
        ),
        alignment = ft.alignment.center_right
    )

    texto_email = ft.Container(
        content = ft.Row(
            controls = [

                ft.Container(width = 50),
                
                ft.Container(
                    content = ft.Text(
                        'Email',
                        size = 25,
                        weight = 'bold',
                        color = 'white',
                        
                        text_align = ft.TextAlign.CENTER,
                    ),
                    margin = ft.margin.only(top = 6.5),
                    alignment = ft.alignment.center,
                ),

                ft.Container(
                    content = ft.Row(
                        controls = [botao_expandir_email],
                    ),
                    alignment = ft.alignment.center_right,
                    margin = ft.margin.only(top = 6.5),
                    width = 50
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN, 
        ),
    )

    armazenar_email = ft.TextField(
        label = 'Email Matec',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center',
    )

    armazenar_caixa_email = ft.TextField(
        label = 'Caixa de entrada Matec',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    salvar_email = ft.Container(
       content = ft.ElevatedButton(
            text = 'Salvar',
            style = estilo_botao_neon_branco_salvar,
            width = 200,
            height = 50,
            on_click = salvar_configs,
       )
    )

    container_botoes_email = ft.Container(
        content = ft.Column(
            controls = [

                armazenar_email,

                armazenar_caixa_email

                ],
                scroll = ft.ScrollMode.AUTO,
            ),
            height = 150,  
            margin = ft.margin.only(top = 10),
    )

    container_email = ft.Container(
        content = ft.Column(
            controls = [

                texto_email,

                ft.Divider(height = 0.1, thickness = 2, color = 'red'),

                container_botoes_email,

                salvar_email

            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 10
        ),
        width = 330,
        height = 300,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
    )

    botao_expandir_elogistic = ft.Container(
        content = ft.IconButton(
            icon = ft.Icons.LIST,
            on_click = expandir.expandir_container_elogistic,
            tooltip = 'Expandir/Recolher',
            icon_color = ft.Colors.ORANGE
        ),
        alignment = ft.alignment.center_right
    )

    texto_Elogistic = ft.Container(
        content = ft.Row(
            controls = [

                ft.Container(width = 50),
                
                ft.Container(
                    content = ft.Text(
                        'E-logistic',
                        size = 25,
                        weight = 'bold',
                        color = 'white',
                        
                        text_align = ft.TextAlign.CENTER,
                    ),
                    margin = ft.margin.only(top = 6.5, left = 5),
                    alignment = ft.alignment.center,
                ),

                ft.Container(
                    content = ft.Row(
                        controls = [botao_expandir_elogistic],
                    ),
                    alignment = ft.alignment.center_right,
                    margin = ft.margin.only(top = 6.5),
                    width = 50
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,   
        ),
    )

    armazenar_usuario_elogistc = ft.TextField(
        label = 'Usuário E-logistic',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_senha_elogistc = ft.TextField(
        label = 'Senha E-logistic',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center',
        #password = True,
        #suffix_icon = ft.IconButton(icon = ft.Icons.VISIBILITY_OFF, 
                                    #on_click = lambda e: visualizar_senha(e, 'Senha E-logistic', armazenar_senha_elogistc))
    )

    salvar_elogistic = ft.Container(
       content = ft.ElevatedButton(
            text = 'Salvar',
            width = 200,
            height = 50,
            on_click = salvar_configs,
            style = estilo_botao_neon_branco_salvar,
       )
    )

    container_botoes_elogistc = ft.Container(
        content = ft.Column(
            controls = [

                armazenar_usuario_elogistc,

                armazenar_senha_elogistc
    
                ],
                scroll = ft.ScrollMode.AUTO,
            ),
            height = 150, 
            margin = ft.margin.only(top = 10), 
    )

    container_elogistc = ft.Container(
        content = ft.Column(
            controls = [

                texto_Elogistic,

                ft.Divider(height = 1, thickness = 2, color = 'red'),

                container_botoes_elogistc,

                salvar_elogistic

            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        width = 330,
        height = 300,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK)
    )

    botao_expandir_IOB = ft.Container(
        content = ft.IconButton(
            icon = ft.Icons.LIST,
            on_click = expandir.expandir_container_IOB,
            tooltip = 'Expandir/Recolher',
            icon_color = ft.Colors.ORANGE
        ),
        alignment = ft.alignment.center_right
    )

    texto_IOB = ft.Container(
        content = ft.Row(
            controls = [

                ft.Container(width = 50),
                
                ft.Container(
                    content = ft.Text(
                        'IOB',
                        size = 25,
                        weight = 'bold',
                        color = 'white',
                        
                        text_align = ft.TextAlign.CENTER,
                    ),
                    margin = ft.margin.only(top = 6.5),
                    alignment = ft.alignment.center,
                ),

                ft.Container(
                    content = ft.Row(
                        controls = [botao_expandir_IOB],
                    ),
                    alignment = ft.alignment.center_right,
                    margin = ft.margin.only(top = 6.5),
                    width = 50
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,   
        ),
    )

    armazenar_usuario_iob = ft.TextField(
        label = 'Usuário IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_senha_IOB = ft.TextField(
        label = 'Senha IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center',
        #password = True,
        #suffix_icon = ft.IconButton(icon = ft.Icons.VISIBILITY_OFF, 
                                    #on_click = lambda e: visualizar_senha(e, 'Senha IOB', armazenar_senha_IOB))
    )

    armazenar_cliente_circulação_IOB = ft.TextField(
        label = 'Cliente Circulação IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_cliente_recebimento_IOB = ft.TextField(
        label = 'Cliente recebimento téc. IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_circulação_IOB = ft.TextField(
        label = 'Natureza Circulação IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_recebimento_GOOD_IOB = ft.TextField(
        label = 'Natureza Recebimento téc. GOOD IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_recebimento_DEFECTIVE_IOB = ft.TextField(
        label = 'Natureza Recebimento téc. DEFECTIVE IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_cliente_devolução_dell_IOB = ft.TextField(
        label = 'Cliente devolução Dell IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_cliente_devolução_hp_IOB = ft.TextField(
        label = 'Cliente devolução HP IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_cliente_devolução_flex_IOB = ft.TextField(
        label = 'Cliente devolução HP FLEX IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_devolução_flex_IOB = ft.TextField(
        label = 'Natureza devolução HP FLEX IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_devolução_good_IOB = ft.TextField(
        label = 'Natureza devolução GOOD IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_natureza_devolução_defective_IOB = ft.TextField(
        label = 'Natureza devolução DEFECTIVE IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_transporadora_dell_IOB = ft.TextField(
        label = 'Transportadora devolução dell IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_transporadora_hp_IOB = ft.TextField(
        label = 'Transportadora devolução hp IOB',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    salvar_IOB = ft.Container(
       content = ft.ElevatedButton(
            text = 'Salvar',
            width = 200,
            height = 50,
            on_click = salvar_configs,
            style = estilo_botao_neon_branco_salvar,
       )
    )

    container_botoes_IOB = ft.Container(
        content = ft.Column(
            controls = [

                armazenar_usuario_iob,

                armazenar_senha_IOB,

                armazenar_cliente_circulação_IOB,

                armazenar_cliente_recebimento_IOB,

                armazenar_natureza_circulação_IOB,

                armazenar_natureza_recebimento_GOOD_IOB,

                armazenar_natureza_recebimento_DEFECTIVE_IOB,

                armazenar_cliente_devolução_dell_IOB,

                armazenar_cliente_devolução_hp_IOB,

                armazenar_cliente_devolução_flex_IOB,

                armazenar_natureza_devolução_flex_IOB,

                armazenar_natureza_devolução_good_IOB,

                armazenar_natureza_devolução_defective_IOB,

                armazenar_transporadora_dell_IOB,

                armazenar_transporadora_hp_IOB
    
                ],
                scroll = ft.ScrollMode.AUTO,
            ),
            height = 150, 
            margin = ft.margin.only(top = 10), 
    )

    container_IOB = ft.Container(
        content = ft.Column(
            controls = [

                texto_IOB,

                ft.Divider(height = 1, thickness = 2, color = 'red'),

                container_botoes_IOB,

                salvar_IOB

            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        width = 330,
        height = 300,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK)
    )

    botao_expandir_difal = ft.Container(
        content = ft.IconButton(
            icon = ft.Icons.LIST,
            on_click = expandir.expandir_container_difal,
            tooltip = 'Expandir/Recolher',
            icon_color = ft.Colors.ORANGE
        ),
        alignment = ft.alignment.center_right
    )

    texto_difal = ft.Container(
        content = ft.Row(
            controls = [

                ft.Container(width = 50),
                
                ft.Container(
                    content = ft.Text(
                        'Difal',
                        size = 25,
                        weight = 'bold',
                        color = 'white',
                        
                        text_align = ft.TextAlign.CENTER,
                    ),
                    margin = ft.margin.only(top = 6.5),
                    alignment = ft.alignment.center,
                ),

                ft.Container(
                    content = ft.Row(
                        controls = [botao_expandir_difal],
                    ),
                    alignment = ft.alignment.center_right,
                    margin = ft.margin.only(top = 6.5),
                    width = 50
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,   
        ),
    )

    armazenar_nome_credenciada = ft.TextField(
        label = 'Nome Credenciada Difal',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_cnpj_credenciada = ft.TextField(
        label = 'CNPJ Credenciada Difal',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    armazenar_aliquota_interna = ft.TextField(
        label = 'Alíquota interna Difal',
        bgcolor = 'white',
        width = 290,
        height = 60,
        border_radius = 5,
        label_style = ft.TextStyle(color = ft.Colors.BLACK54),
        border_color = 'black',
        text_align = 'center'
    )

    salvar_difal = ft.Container(
       content = ft.ElevatedButton(
            text = 'Salvar',
            width = 200,
            height = 50,
            on_click = salvar_configs,
            style = estilo_botao_neon_branco_salvar,
       )
    )

    container_botoes_difal = ft.Container(
        content = ft.Column(
            controls = [

                armazenar_nome_credenciada,

                armazenar_cnpj_credenciada,

                armazenar_aliquota_interna,

                ],
                scroll = ft.ScrollMode.AUTO,
            ),
            height = 150, 
            margin = ft.margin.only(top = 10), 
    )

    container_difal = ft.Container(
        content = ft.Column(
            controls = [

                texto_difal,

                ft.Divider(height = 1, thickness = 2, color = 'red'),

                container_botoes_difal,

                salvar_difal

            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        width = 330,
        height = 300,
        border = ft.border.all(2, 'white'),
        border_radius = 20,
        bgcolor = ft.Colors.with_opacity(0.20, ft.Colors.BLACK),
        #gradient = ft.LinearGradient(  Caso queira adicionar efeito de gradiente color nos containers
            #begin = ft.alignment.top_left,
            #end = ft.alignment.bottom_right,
            #colors = ["#FF0000", "#0000FF"]
        #),
    )

    carregar_configs()

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
                                controls = [botao_voltar, botao_switch_para_icms],
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                            ),

                            ft.Column(
                                controls = [
                                    ft.Container(
                                        content = ft.Row(
                                            controls = [container_email, container_elogistc],
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 40,
                                        ),
                                        alignment = ft.alignment.center,
                                    ),

                                    ft.Container(
                                        content = ft.Row(
                                            controls = [container_IOB, container_difal],
                                            alignment = ft.MainAxisAlignment.CENTER,
                                            spacing = 40,
                                        ),
                                        alignment = ft.alignment.center,
                                        margin = ft.margin.only(bottom = 40)
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
