from app.back_end.funções.funções_Gerais import PlanilhaManager, obter_configs, navigate, resource_path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path
import flet as ft
import shutil
import imaplib
import pickle
import email
import json
import os

if os.name == 'nt':  # Para Windows
    download_dir = Path(os.getenv('USERPROFILE')) / 'Downloads'
else:  # Para macOS e Linux
    download_dir = Path.home() / 'Downloads'

current_dir = Path(__file__).parent

aux_path_credentials = resource_path('credenciais_e_tokens/credentials.json')

with open(aux_path_credentials, 'r') as f:
    aux_path_credentials = json.load(f)

creds_installed = aux_path_credentials.get('installed', {})

config_dict = {
    "installed": {
        "client_id": creds_installed.get("client_id"),
        "client_secret": creds_installed.get("client_secret"),
        "auth_uri": creds_installed.get("auth_uri"),
        "token_uri": creds_installed.get("token_uri"),
        "auth_provider_x509_cert_url": creds_installed.get("auth_provider_x509_cert_url"),
        "redirect_uris": creds_installed.get("redirect_uris")
    }
}

aux_path_XML_destino = download_dir / 'XML_DELL'

aux_path_XML_destino.mkdir(parents = True, exist_ok = True)

# Baixar arquivos HP e valores devolução HP
def conectar_email_e_baixar_arquivos_HP(log_instance):

    conta_email = obter_configs().get('email')
    caixa_emails = obter_configs().get('caixa_email')

    planilha_manager = PlanilhaManager()

    if planilha_manager.is_planilha_atualizada():
        planilha_manager.recarregar_planilha()
    
    planilha_df = planilha_manager.get_planilha()

    planilha_df.ffill(inplace = True)

    substrings_hp = []

    for index, row in planilha_df.iterrows():
        cell_hp = row[1]

        if isinstance(cell_hp, str) and len(cell_hp) >= 34:
            # Extrai a substring e adiciona à lista
            substring_hp = cell_hp[28:34]
            substrings_hp.append(substring_hp)
        elif isinstance(cell_hp, float):
            cell_int = int(cell_hp)
            substrings_hp.append(cell_int)
        else:
            substrings_hp.append(cell_hp)

    def get_gmail_service():
        """Realiza a autenticação OAuth2 e retorna o serviço do Gmail."""
        
        creds = None
        # Carrega as credenciais do arquivo 'token.pickle' se ele existir
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        SCOPES = ['https://mail.google.com/']

        # Verifica se as credenciais são válidas, e se não, tenta atualizar ou obter novas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())  # Tenta atualizar o token
                except Exception as e:
                    log_instance.log_message(f'Erro ao atualizar as credenciais: {e}')
                    # Se falhar, precisa obter novas credenciais
                
                    flow = InstalledAppFlow.from_client_config(config_dict, scopes = SCOPES)
                    creds = flow.run_local_server(port = 0)  # Inicia o fluxo de autenticação
            else:
                # Se não houver credenciais, inicia o fluxo de autenticação
                
                flow = InstalledAppFlow.from_client_config(config_dict, scopes = SCOPES)
                creds = flow.run_local_server(port = 0)

            # Salva as credenciais para futuras execuções
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def generate_oauth2_string(username, access_token):
        """Gera a string de autenticação OAuth2 no formato necessário para IMAP."""
        auth_string = f'user={username}\1auth=Bearer {access_token}\1\1'
        return auth_string.encode('ascii')

    def connect_to_gmail_imap(creds, conta_email):
        """Conecta ao Gmail via IMAP usando OAuth2."""
        imap_host = 'imap.gmail.com'
        mail = imaplib.IMAP4_SSL(imap_host)
        
        # Gera a string de autenticação OAuth2
        auth_string = generate_oauth2_string(conta_email, creds.token)
        
        # Autentica no servidor IMAP usando OAuth2
        try:
            mail.authenticate('XOAUTH2', lambda x: auth_string)
            log_instance.log_message('Autenticação bem sucedida, seguindo para baixar emails')

        except AssertionError:
            pass

        except Exception as e:
            log_instance.log_message(f'Ocorreu um erro durante a autenticação com servidor: {e}')
            return None
        
        return mail

    # Inicie a autenticação
    creds = get_gmail_service()

    # Conecte ao Gmail via IMAP usando as credenciais OAuth2
    mail = connect_to_gmail_imap(creds, conta_email)

    processed_files = []

    if mail:
        # Selecionar a caixa de entrada ou outro rótulo
        mail.select(f'"{caixa_emails}"')

        try:
        
            idx = 1

            for xml in substrings_hp:
                status, email_ids = mail.search(None, f'(SUBJECT "{xml}")')
                log_instance.log_message(f'{idx} - Buscando emails com assunto: "{xml}"')

                for email_id in email_ids[0].split():
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = email_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    # Processar o e-mail e anexos
                    for part in message.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        file_name = part.get_filename()

                        # Verificar se o anexo já foi processado
                        if file_name and file_name.endswith('-nfe.xml') and file_name not in processed_files:
                            log_instance.log_message(f'{idx} - Anexo baixado: {file_name}')

                            try:
                                save_path = os.path.join(aux_path_XML_destino, file_name)
                                os.makedirs(aux_path_XML_destino, exist_ok = True)

                                # Salvar o arquivo
                                with open(save_path, 'wb') as f:
                                    f.write(part.get_payload(decode = True))

                                if os.path.exists(save_path):
                                    destino_path = os.path.join(aux_path_XML_destino, file_name)
                                    shutil.move(save_path, destino_path)

                                    # Adicionar o arquivo processado na lista
                                    processed_files.append(file_name)

                                else:
                                    log_instance.log_message(f'{idx} - O arquivo de origem não foi encontrado: {save_path}')

                                    idx += 1

                            except AssertionError:
                                pass

                            except Exception as e:
                                log_instance.log_message(f'{idx} - Ocorreu um erro ao processar o anexo "{file_name}": {e}')

                                idx += 1

                idx += 1

        except AssertionError:
            pass

        except Exception as e:
            log_instance.log_message(f'Não foi possível prosseguir com a busca no email: {e}')
    else:
        log_instance.log_message(f'A conexão IMAP falhou.')

    substrings_hp.clear()

# Baixar arquivos Dell e Valores devolução Dell
def conectar_email_e_baixar_arquivos_Dell(log_instance):

    conta_email = obter_configs().get('email')
    caixa_emails = obter_configs().get('caixa_email')

    planilha_manager = PlanilhaManager()

    if planilha_manager.is_planilha_atualizada():
        planilha_manager.recarregar_planilha()
    
    planilha_df = planilha_manager.get_planilha()

    planilha_df.ffill(inplace = True)
    
    substrings_Dell = []
    
    for index, row in planilha_df.iterrows():

        cell_Dell = row[1]

        if isinstance(cell_Dell, str) and len(cell_Dell) >= 34:
            # Extrai a substring e adiciona à lista
            substring_Dell = cell_Dell[27:34]
            substrings_Dell.append(substring_Dell)
        elif isinstance(cell_Dell, float):
            cell_int = int(cell_Dell)
            substrings_Dell.append(cell_int)
        else:
            substrings_Dell.append(cell_Dell)

    def get_gmail_service():
        """Realiza a autenticação OAuth2 e retorna o serviço do Gmail."""
        
        creds = None
        # Carrega as credenciais do arquivo 'token.pickle' se ele existir
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        SCOPES = ['https://mail.google.com/']
        
        # Verifica se as credenciais são válidas, e se não, tenta atualizar ou obter novas
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())  # Tenta atualizar o token
                
                except AssertionError:
                    pass
                except Exception as e:
                    log_instance.log_message(f'Erro ao atualizar as credenciais: {e}')
                    # Se falhar, precisa obter novas credenciais
                    flow = InstalledAppFlow.from_client_config(config_dict, scopes = SCOPES)
                    creds = flow.run_local_server(port = 0)  # Inicia o fluxo de autenticação
            else:
                # Se não houver credenciais, inicia o fluxo de autenticação
                
                flow = InstalledAppFlow.from_client_config(config_dict, scopes = SCOPES)
                creds = flow.run_local_server(port = 0)

            # Salva as credenciais para futuras execuções
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def generate_oauth2_string(username, access_token):
        """Gera a string de autenticação OAuth2 no formato necessário para IMAP."""
        auth_string = f'user={username}\1auth=Bearer {access_token}\1\1'
        return auth_string.encode('ascii')

    def connect_to_gmail_imap(creds, conta_email):
        """Conecta ao Gmail via IMAP usando OAuth2."""
        try:
            imap_host = 'imap.gmail.com'
            mail = imaplib.IMAP4_SSL(imap_host)
            
            # Gera a string de autenticação OAuth2
            auth_string = generate_oauth2_string(conta_email, creds.token)
            
            # Autentica no servidor IMAP usando OAuth2
        
            mail.authenticate('XOAUTH2', lambda x: auth_string)
            log_instance.log_message('Autenticação bem sucedida, seguindo para baixar emails')

        except AssertionError:
            pass
        
        except Exception as e:
            log_instance.log_message(f'Ocorreu um erro durante a autenticação com servidor: {e}')
            return None
        
        return mail

    # Inicie a autenticação
    creds_devolução = get_gmail_service()

    # Conecte ao Gmail via IMAP usando as credenciais OAuth2
    mail = connect_to_gmail_imap(creds_devolução, conta_email)

    if mail:
        # Selecionar a caixa de entrada ou outro rótulo
        mail.select(f'"{caixa_emails}"')

        try:
            processed_files = []

            idx = 1

            for xml in substrings_Dell:
                status, email_ids = mail.search(None, f'(SUBJECT "{xml}")')
                log_instance.log_message(f'{idx} - Buscando emails com assunto: "{xml}"')

                for email_id in email_ids[0].split():
                    status, email_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = email_data[0][1]
                    message = email.message_from_bytes(raw_email)

                    # Processar o e-mail e anexos
                    for part in message.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        file_name = part.get_filename()

                        # Verificar se o anexo já foi processado
                        if file_name and file_name.endswith('-procNFe.xml') and file_name not in processed_files:

                            try:
                                save_path = os.path.join(aux_path_XML_destino, file_name)
                                os.makedirs(aux_path_XML_destino, exist_ok = True)

                                # Salvar o arquivo
                                with open(save_path, 'wb') as f:
                                    f.write(part.get_payload(decode = True))

                                if os.path.exists(save_path):
                                    destino_path = os.path.join(aux_path_XML_destino, file_name)
                                    shutil.move(save_path, destino_path)

                                    # Adicionar o arquivo processado na lista
                                    processed_files.append(file_name)

                                    log_instance.log_message(f'{idx} - Anexo baixado: {file_name}\n')
                                else:
                                    log_instance.log_message(f'{idx} - O arquivo de origem não foi encontrado: {save_path}')

                                    idx += 1

                            except AssertionError:
                                pass

                            except Exception as e:
                                log_instance.log_message(f'{idx} - Ocorreu um erro ao processar o anexo "{file_name}": {e}')

                                idx += 1
                idx += 1

        except AssertionError:
            pass

        except Exception as e:
            log_instance.log_message(f'Não foi possível prosseguir com a busca no email: {e}')
    else:
        log_instance.log_message(f'A conexão IMAP falhou.')

    substrings_Dell.clear()

# Botoes_entrada_Dell
def baixar_arquivosXML_DELL(page: ft.Page, log_instance, views, current_view):

    def mostrar_confirmacao(page):
        dialog.open = True
        page.update()

    def continuar(e):
        
        navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações recebimento')

        botao_voltar = views['logs e informações recebimento'].content.controls[1].content.controls[0].controls[0]
        botao_voltar.disabled = True
        botao_voltar.content.color = ft.Colors.GREY_400
        page.update()

        # Lista todos os arquivos na pasta
        arquivos_excluir = os.listdir(aux_path_XML_destino)

        for arquivo_excluir in arquivos_excluir:
            caminho_arquivo_excluir = os.path.join(aux_path_XML_destino, arquivo_excluir)
            if os.path.isfile(caminho_arquivo_excluir):
                os.remove(caminho_arquivo_excluir)

        dialog.open = False
        page.update()

        try:
            log_instance.log_message('Iniciando download de arquivos...')
            conectar_email_e_baixar_arquivos_Dell(log_instance)
        except Exception as e:
            log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada:\n {e}')
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            return
        
        log_instance.log_message('Download de arquivos concluído.')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    def parar(e):
        dialog.open = False
        page.update()
        return
    
    container_aviso = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(f'Caso existam arquivos na pasta abaixo, serão excluídos: \n\n{aux_path_XML_destino}\n\n Deseja continuar?', text_align = ft.TextAlign.CENTER, color = 'white', size = 15)
            ],
            scroll = ft.ScrollMode.AUTO,
        ),
        margin = ft.margin.only(top = 10),
        height = 180,
        width = 450,
        alignment = ft.alignment.center
    )

    dialog = ft.AlertDialog(
        title = ft.Container(
            content = ft.Row(
                controls = [
                    ft.Icon(ft.Icons.WARNING, color = 'red', size = 30),
                    ft.Text('Aviso', color = 'white', size = 30),
                    ft.Icon(ft.Icons.WARNING, color = 'red', size = 30)],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ),
        content = ft.Column(
            [
                container_aviso,
                ft.Row(
                    [
                        ft.ElevatedButton('Sim', on_click = continuar, bgcolor = 'red', color = 'white', width = 100),
                        ft.ElevatedButton('Não', on_click = parar, bgcolor = 'red', color = 'white', width = 100)
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing = 20,
            width = 450,
            height = 250,
            scroll = ft.ScrollMode.AUTO,
        ),
        bgcolor = 'black',
        actions = [],
    )

    # Adiciona o AlertDialog à página
    page.dialog = dialog

    page.add(dialog)
    dialog.open = True

    # Chama a função de exibir o popup
    mostrar_confirmacao(page)

# Botoes_entrada_HP
def baixar_arquivosXML_HP(page: ft.Page, log_instance, views, current_view):

    def mostrar_confirmacao(page):
        dialog.open = True
        page.update()
        

    def continuar(e):

        navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações recebimento')

        botao_voltar = views['logs e informações recebimento'].content.controls[1].content.controls[0].controls[0]
        botao_voltar.disabled = True
        botao_voltar.content.color = ft.Colors.GREY_400
        page.update()

        # Lista todos os arquivos na pasta
        arquivos_excluir = os.listdir(aux_path_XML_destino)

        for arquivo_excluir in arquivos_excluir:
            caminho_arquivo_excluir = os.path.join(aux_path_XML_destino, arquivo_excluir)
            if os.path.isfile(caminho_arquivo_excluir):
                os.remove(caminho_arquivo_excluir)

        dialog.open = False
        page.update()

        try:
            log_instance.log_message('Iniciando download de arquivos...')
            conectar_email_e_baixar_arquivos_HP(log_instance)
        except:
            log_instance.log_message('Erro: Verifique se alguma planilha foi selecionada')
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            return
        
        log_instance.log_message('Download de arquivos concluído.')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    def parar(e):
        dialog.open = False
        page.update()
        return
    
    container_aviso = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(f'Caso existam arquivos na pasta abaixo, serão excluídos: \n\n{aux_path_XML_destino}\n\n Deseja continuar?', text_align = ft.TextAlign.CENTER, color = 'white', size = 15)
            ],
            scroll = ft.ScrollMode.AUTO,
        ),
        margin = ft.margin.only(top = 10),
        height = 180,
        width = 450,
        alignment = ft.alignment.center
    )

    dialog = ft.AlertDialog(
        title = ft.Container(
            content = ft.Row(
                controls = [
                    ft.Icon(ft.Icons.WARNING, color = 'red', size = 30),
                    ft.Text('Aviso', color = 'white', size = 30),
                    ft.Icon(ft.Icons.WARNING, color = 'red', size = 30)],
                alignment = ft.MainAxisAlignment.CENTER
            )
        ),
        content = ft.Column(
            [
                container_aviso,
                ft.Row(
                    [
                        ft.ElevatedButton('Sim', on_click = continuar, bgcolor = 'red', color = 'white', width = 100),
                        ft.ElevatedButton('Não', on_click = parar, bgcolor = 'red', color = 'white', width = 100)
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing = 20,
            width = 450,
            height = 250,
            scroll = ft.ScrollMode.AUTO,
        ),
        bgcolor = 'black',
        actions = [],
    )

    # Adiciona o AlertDialog à página
    page.dialog = dialog

    page.add(dialog)
    dialog.open = True

    # Chama a função de exibir o popup
    mostrar_confirmacao(page)
