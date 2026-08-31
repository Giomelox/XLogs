from app.back_end.funções.funções_conectar_email import aux_path_XML_destino, conectar_email_e_baixar_arquivos_Dell, conectar_email_e_baixar_arquivos_HP
from app.back_end.funções.funções_Gerais import obter_configs, PlanilhaManager, navigate
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as ET
from selenium import webdriver
import subprocess
import pandas as pd
import flet as ft
import time
import os

# ======= INFORMAÇÕES DE LOGIN IOB =======
# ========================================
url_login_iob = 'https://sso.iob.com.br/signin/?response_type=code&scope=&client_id=c17d4225-9d57-401b-b4fd-32503121f55b&redirect_uri=https://emissor.iob.com.br'
url_importacao_IOB = 'https://emissor2.iob.com.br/notafiscal/incoming_nfes'
xpath_reCAPTCHA_IOB = '/html/body/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/form/div[4]/div/div/div/iframe'
elemento_clicavel_reCAPTCHA_IOB = '//div[@class="recaptcha-checkbox-border"]'
# ========================================
# ========================================

# ======= VARIÁVEIS DE EMISSÃO IOB =======
# ========================================
xpath_ir_para_aba_campo_icms = "/html/body/div[4]/div[10]/div/form/div[3]/ul/li[3]/a"
xpath_botao_submit_aba_icms = "/html/body/div[4]/div[10]/div/form/div[4]/div/span[1]/button"
xpath_botao_emitir_nf = "/html/body/div[4]/div[13]/div[2]/span/button"
xpath_botao_baixar_xml = "/html/body/div[3]/section/div/div[4]/div/a[4]"
xpath_botao_ir_para_danfe = "/html/body/div[3]/section/div/div[4]/div/a[3]"
xpath_botao_baixar_pdf = "/html/body/div[3]/section/div/a[2]"
# ========================================
# ========================================

# ======= VARIAVEIS GLOBAIS DA PLANILHA =======
planilha_manager = PlanilhaManager()
# =============================================


# ======= INFORMAÇÕES DE CONFIGURAÇÕES DE ICMS PARA EMISSÃO =======
botao_switch_para_icms = obter_configs().get('botao_switch_para_icms')
# =================================================================


# ======= INFORMAÇÕES DE EMISSÃO PARA CIRCULAÇÃO IOB =======
# ==========================================================
usuario_IOB = obter_configs().get('usuario_IOB')
senha_IOB = obter_configs().get('senha_IOB')
cliente_circulacao_IOB = obter_configs().get('cliente_circulação')
natureza_circulacao_IOB = obter_configs().get('natureza_circulação')
# ==========================================================
# ==========================================================


# ======= INFORMAÇÕES DE EMISSÃO PARA ENTRADA DE TÉC. IOB =======
# ===============================================================
cliente_recebimento_IOB = obter_configs().get('cliente_recebimento')
natureza_recebimento_IOB_good = obter_configs().get('natureza_recebimento_good')
natureza_recebimento_IOB_defective = obter_configs().get('natureza_recebimento_defective')
# ===============================================================
# ===============================================================


# ======= INFORMAÇÕES DE EMISSÃO PARA DEVOLUÇÃO DELL IOB =======
# ==============================================================
cliente_devolucao_dell_IOB = obter_configs().get('cliente_devoluçãoDell')
natureza_devolucao_dell_good_IOB = obter_configs().get('natureza_devolução_good')
natureza_devolucao_dell_defective_IOB = obter_configs().get('natureza_devolução_defective')
transportadora_devolucao_dell_IOB = obter_configs().get('transportadora_dell')
# ==============================================================
# ==============================================================


# ======= INFORMAÇÕES DE EMISSÃO PARA DEVOLUÇÃO HP IOB =======
# ============================================================
cliente_devolucao_hp_IOB = obter_configs().get('cliente_devoluçãoHP')
natureza_devolucao_hp_good_IOB = obter_configs().get('natureza_devolução_good')
natureza_devolucao_hp_defective_IOB = obter_configs().get('natureza_devolução_defective')
transportadora_devolucao_hp_IOB = obter_configs().get('transportadora_hp')
# ============================================================
# ============================================================


# ======= INFORMAÇÕES DE EMISSÃO PARA DEVOLUÇÃO FLEX IOB =======
# ==============================================================
cliente_devolucao_flex_IOB = obter_configs().get('cliente_devolução_flex')
natureza_devolucao_flex_IOB = obter_configs().get('natureza_devolução_flex')
# ==============================================================
# ==============================================================


# Botoes_entrada_Dell
def importar_produtos(log_instance, page, views, current_view):

    navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações recebimento')

    botao_voltar = views['logs e informações recebimento'].content.controls[1].content.controls[0].controls[0]
    botao_voltar.disabled = True
    botao_voltar.content.color = ft.Colors.GREY_400
    page.update()

    driver = None

    #==============================================================================
    subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
    time.sleep(3)

    # Pasta vazia nova, sem copiar nada
    import os
    temp_dir = r"C:\ChromeSelenium"
    os.makedirs(temp_dir, exist_ok=True)

    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "--no-first-run",
        "--no-default-browser-check"
    ])

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    log_instance.log_message('Iniciando importação de arquivos...')

    driver.get(url_login_iob)

    time.sleep(4)
    #==============================================================================

    try:
        
        idx = 1

        # Acessa a página desejada
        driver.get(url_login_iob)

        log_instance.log_message('Iniciando importação de arquivos...')

    except Exception as e:
        log_instance.log_message(f'Erro ao iniciar o navegador. {e}')

    try:

        time.sleep(15) # tempo para carregar o reCAPTCHA

        element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
            EC.presence_of_element_located((By.ID, 'username'))
        )
        element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

        time.sleep(2.5)

        element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
            EC.presence_of_element_located((By.ID, 'password'))
        )
        element_senha_emitir.send_keys(senha_IOB) # Insere a senha

        """
        time.sleep(15) # tempo para carregar o reCAPTCHA

        element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
            EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
        )
        driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
        captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
        captcha_checkbox.click() # Clica no elemento captcha

        driver.switch_to.default_content() # Muda para o contexto padrão da página

        time.sleep(10)
        """

        element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
            EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
        )
        element_submit_emitir.click()  # Clica no elemento submit

        element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
        )

        try:
            element_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
            )
            element_form.click()
        except:
            pass
                
        if element_emissão_notas_emitir:
            driver.get(url_importacao_IOB) # Caso encontre o botão de notas, entra na página para emitir

        try:
            element_form.click()
        except:
            pass
    
        try:
            for x in os.listdir(aux_path_XML_destino):
                # Remover o overlay antes de qualquer clique
                try:
                    driver.execute_script("""
                        let overlay = document.getElementById('UIDialogLayer');
                        if (overlay) {
                            overlay.remove();  // Remove completamente o overlay da página
                        }
                    """)
                    time.sleep(1.5)  # Pequena pausa para garantir que o overlay seja removido

                except AssertionError:
                    pass

                except Exception as e:
                    botao_voltar.disabled = False
                    botao_voltar.content.color = ft.Colors.WHITE
                    page.update()
                    log_instance.log_message("Não foi possível remover o overlay:", e)
                    

                # Iniciar o processo de importação
                element_importar = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "UILink button pull-right")]'))
                )
                time.sleep(0.5)
                element_importar.click()

                # Aguardar e clicar no input de arquivo
                element_abrir_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="import_nfe_nfe_xml"]'))
                )
                caminho = os.path.join(aux_path_XML_destino, x)
                element_abrir_input.send_keys(caminho)

                # Aguardar o botão de "Confirmar" (ou similar) aparecer após o upload
                element_confirmar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "save button primary")]'))
                )

                if element_confirmar:
                    element_confirmar.click()

                    time.sleep(1)

                    # Navegar de volta para a página inicial (após enviar um arquivo)
                    driver.get(url_importacao_IOB)

                # Aguardar a página carregar e clicar novamente no botão "Importar"
                element_importar1 = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "UILink button pull-right")]'))
                )
                time.sleep(0.8)
                element_importar1.click()

                log_instance.log_message(f'{idx}: {x} importado com sucesso.')

                idx += 1

                # Aguardar um breve momento para garantir que a próxima iteração não aconteça muito rápido
                time.sleep(2.5)

        except AssertionError:
            pass

        except Exception as e:
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            log_instance.log_message(f'Erro encontrado: {e}')

    except AssertionError:
        pass

    except Exception as e:
        log_instance.log_message(f'Ocorreu um erro: {e}')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    finally:
        driver.close()

        log_instance.log_message('Importação de arquivos concluída.')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

def emitir_nf_circulação(log_instance, page, views, current_view):

    navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações recebimento')

    botao_voltar = views['logs e informações recebimento'].content.controls[1].content.controls[0].controls[0]
    botao_voltar.disabled = True
    botao_voltar.content.color = ft.Colors.GREY_400
    page.update()

    try:

        driver = None

        #==============================================================================
        subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
        time.sleep(3)

        # Pasta vazia nova, sem copiar nada
        import os
        temp_dir = r"C:\ChromeSelenium"
        os.makedirs(temp_dir, exist_ok=True)

        subprocess.Popen([
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--remote-debugging-port=9222",
            f"--user-data-dir={temp_dir}",
            "--no-first-run",
            "--no-default-browser-check"
        ])

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        log_instance.log_message('Iniciando importação de arquivos...')

        driver.get(url_login_iob)

        time.sleep(4)
        #==============================================================================

        actions = ActionChains(driver)

        log_instance.log_message("Iniciando emissão de NFe's...")

        # Acessa a página desejada
        driver.get(url_login_iob)

    except:

        log_instance.log_message("Erro ao iniciar o navegador.")

    
    try:
        
        time.sleep(15) # tempo para carregar o reCAPTCHA

        element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
            EC.presence_of_element_located((By.ID, 'username'))
        )
        element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

        time.sleep(2.5)

        element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
            EC.presence_of_element_located((By.ID, 'password'))
        )
        element_senha_emitir.send_keys(senha_IOB) # Insere a senha

        """
        time.sleep(2.5) # tempo para carregar o reCAPTCHA

        element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
            EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
        )
        driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
        captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
        captcha_checkbox.click() # Clica no elemento captcha

        driver.switch_to.default_content() # Muda para o contexto padrão da página

        time.sleep(20)
        """

        element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
            EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
        )
        element_submit_emitir.click()  # Clica no elemento submit

        element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
        )

        try:
            element_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
            )
            element_form.click()
        except:
            pass
                
        if element_emissão_notas_emitir:
            driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso encontre o botão de notas, entra na página para emitir

        try:
            element_form.click()
        except:
            pass

        element_nova_nota_emitir = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
        )
        element_nova_nota_emitir.click()

    except AssertionError:
        pass

    except Exception as e:
        log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada.')
        driver.quit()
        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    idx = 0

    if planilha_manager.is_planilha_atualizada():
        planilha_manager.recarregar_planilha()
    
    planilha_df = planilha_manager.get_planilha()

    try:
        planilha_df.ffill(inplace = True)
    except AttributeError:
        log_instance.log_message(f'Erro. Verifique se alguma planilha foi selecionada.')

        driver.quit()

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    ler_planilha_mesclada = planilha_df.groupby('CHAMADO', as_index = False, sort = False).agg({
        'NF OU XML PARA BAIXAR (PROGRAMA)': lambda x: ', '.join(map(str, filter(pd.notna, x))),
        'PN CAIXA.': lambda x: ', '.join(map(str, x)),
        'VALOR': lambda x: ', '.join(map(str, x)),
        'CST': lambda x: ', '.join(map(str, x)),
        'ICMS': lambda x: ', '.join(map(str, x)),
        'NCM': lambda x: ', '.join(map(str, x)),
        'QTD.': lambda x: ', '.join(map(str, x))
    })

    try:
        for index, row in ler_planilha_mesclada.iloc[:].iterrows(): # Lê todas as linhas da planilha com as colunas selecionadas
            CHAMADO = str(row['CHAMADO']).replace('.0', '').strip()
            nf_lista = str(row['NF OU XML PARA BAIXAR (PROGRAMA)']).replace('.0', '').strip().split(', ')
            pn_lista = str(row['PN CAIXA.']).strip().split(', ')
            valor_lista = str(row['VALOR']).replace('.', ',').strip().split(', ')
            cst_lista = str(row['CST']).split(', ')
            icms_lista = str(row['ICMS']).split(', ')
            ncm_lista = str(row['NCM']).strip().split(', ')
            qtd_lista = str(row['QTD.']).strip().split(', ')

            try:

                try:
                    element_contingencia = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                    )
                    element_contingencia.click()
                except:
                    pass

                # Encontra o campo de cliente
                element_cliente_emitir = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_client_id'))
                )
                element_cliente_emitir.send_keys(cliente_circulacao_IOB) # Insere no campo cliente

                element_results_client_emitir = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) # Lê as opções dadas pelo site com a lista de clientes
                )

                element_first_li_cliente_emitir = element_results_client_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona o primeiro cliente que aparece
                element_first_li_cliente_emitir.click()

                # Encontra o campo de natureza
                element_natureza_emitir = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_nature_id'))
                )
                element_natureza_emitir.clear() # Limpa o que estiver escrito no campo natureza

                element_natureza_emitir.send_keys(natureza_circulacao_IOB) # Insere no campo natureza

                element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                )

                element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                element_first_li_natureza_emitir.click()

                idx_element = 1

                idx_qtd = 0
                
                for pn, valor, cst, icms, ncm, qtd in zip(pn_lista, valor_lista, cst_lista, icms_lista, ncm_lista, qtd_lista):
                    
                    # Busca pelo campo para inserir o produto
                    element_produto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_product_id'))
                    )

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_produto)

                    # Insere o produto que está na planilha
                    element_produto.send_keys(pn) 

                    time.sleep(1)

                    # Encontra a lista de opções do produto
                    element_produto_results = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    # Seleciona o primeiro produto que aparece                                          
                    try:
                        element_first_li_produto_emitir = driver.find_element(
                            By.XPATH, 
                            '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/div[1]/div/div/div[1]/div/div[2]/div/span/div/ul/li[1]'
                        )
                        element_first_li_produto_emitir.click()
                    except:
                        # Fallback para CSS selector
                        element_first_li_produto_emitir = element_produto_results.find_element(By.CSS_SELECTOR, 'ul li:first-child')
                        element_first_li_produto_emitir.click()

                    time.sleep(1.5)
                    
                    try:

                        element_baixar_frete = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
                        )

                        # Dá o scroll para as observações para que o programa consiga encontrar o ultimo produto listado
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_baixar_frete)

                        time.sleep(1)

                        elemento_produto_selecionar = WebDriverWait(driver, 50).until( 
                            EC.element_to_be_clickable((
                                By.XPATH, 
                                f"(//input[contains(@id, '_product_name')])[{idx_element}]"
                            )) 
                        )
                        elemento_produto_selecionar.click()


                        # Encontra o elemento NCM do produto e envia os dados da planilha
                        element_NCM = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_product_ncm_id'))
                        )
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_NCM)
                        element_NCM.clear()

                        time.sleep(1.5)

                        for x in ncm:
                            element_NCM.send_keys(x)
                            time.sleep(0.8)

                        time.sleep(3)

                        # Lê as opções dadas pelo site com a lista de NCM
                        
                        element_NCM = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )
                        time.sleep(2)

                        # Seleciona o primeiro NCM que aparece
                        element_NCM_prod = element_NCM.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                        element_NCM_prod.click()
                        actions.send_keys(Keys.TAB).perform()

                        element_CFOP = Select(driver.find_element(By.ID, 'item_cfop'))
                
                        element_CFOP.select_by_value('5949')

                        # Altera o display da informação ''quantidade'' do produto para ser possível acessar pelo selenium
                        element_quantidade_comercial = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_quantity'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_comercial, qtd)
                        
                        element_quantidade_tributavel =  WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_taxable_amount'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_tributavel, qtd)

                        # Altera o display da informação ''valor unitário'' do produto para ser possível acessar pelo selenium
                        driver.execute_script("document.getElementById('item_unit_price').style.display = 'block';") 
                        element_valor_produto = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_unit_price'))
                        )

                        # Força a inserção do valor no site
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_valor_produto, valor)
                        actions.send_keys(Keys.TAB).perform()

                        element_valor_taxa = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_taxable_price'))
                        )
                        element_valor_taxa.clear()

                        time.sleep(0.5) # Tempo para salvar o valor do produto

                        # Encontra o campo de ICMS e clica nele
                        element_campo_ICMS = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.XPATH, xpath_ir_para_aba_campo_icms))
                        )
                        element_campo_ICMS.click()

                        # Encontra o campo ORIG e altera para o orig do produto
                        element_orig = Select(driver.find_element(By.XPATH, f'//*[@id="item_icms_origin"]'))

                        element_orig.select_by_value(f'{cst}')

                        if botao_switch_para_icms == 'False':

                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('400')

                            time.sleep(3)

                        elif botao_switch_para_icms == 'True':
                            
                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('00')

                            element_campo_cst_icms = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.ID, 'item_icms_tax_rate'))
                            )

                            element_campo_cst_icms.clear()

                            time.sleep(2)

                            driver.execute_script("""
                                arguments[0].value = arguments[1];
                                arguments[0].dispatchEvent(new Event('input'));
                                arguments[0].dispatchEvent(new Event('change'));
                            """, element_campo_cst_icms, icms)

                            time.sleep(3)

                        element_submit_produto = driver.find_element(By.XPATH, xpath_botao_submit_aba_icms) # Encontra o botão de salvar as informações do produto e clica
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_submit_produto)
                        driver.execute_script("arguments[0].click();", element_submit_produto)

                        idx_qtd += 1

                        idx_element += 1

                    except AssertionError:
                        pass
                
                    except Exception as e:
                        log_instance.log_message(f'{idx}: Erro ao tentar inserir um dado do produto {CHAMADO}/{pn}: {e}')

                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                        driver.refresh()

                        element_nova_nota_emitir1 = WebDriverWait(driver, 200).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                        )
                        element_nova_nota_emitir1.click()   

                        idx += 1

                        continue

                # Encontra e clica na modalidade de frete
                element_frete =  WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
                )
                time.sleep(0.5)
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_frete)
                time.sleep(0.5)
                element_frete.click()

                # Encontra dentro das opções, o frete do processo

                element_frete_terceiros = Select(driver.find_element(By.ID, 'nfe_carriage_modality'))
                
                element_frete_terceiros.select_by_value('9')

                # Encontra o bloco de quantidade de produtos e insere a quantidade 1
                element_quantidade = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_quantity')) 
                )
                element_quantidade.clear()
                element_quantidade.send_keys(idx_qtd)
                actions.send_keys(Keys.TAB).perform()

                # Encontra o bloco de espécie de produtos e insere 'volume'
                element_especie = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_kind'))
                )
                element_especie.send_keys('CAIXA')
                actions.send_keys(Keys.TAB).perform() 

                time.sleep(0.5) # Tempo para processar a especie

                PESO_BRUTO = 1

                element_peso_bruto = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_gross_weight')) 
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_peso_bruto, PESO_BRUTO)
                time.sleep(0.5)
                actions.send_keys(Keys.TAB).perform()

                time.sleep(0.5) # Tempo para processar o peso bruto

                element_peso_liquido = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_net_weight')) 
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_peso_liquido, PESO_BRUTO)
                time.sleep(0.5)
                actions.send_keys(Keys.TAB).perform()

                time.sleep(0.5) # Tempo para processar o peso liquido

                # Encontra o campo de observação e adiciona as informações de acordo com a planilha
                element_observação = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'nfe_notes'))
                )


                if botao_switch_para_icms == 'False':

                    element_observação.send_keys(f'@ENV ;@REF {CHAMADO} REF NF {', '.join(nf_lista)} PN {', '.join(pn_lista)}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".')
                
                elif botao_switch_para_icms == 'True':
                    
                    element_observação.send_keys(f'@ENV ;@REF {CHAMADO} REF NF {', '.join(nf_lista)} PN {', '.join(pn_lista)}')                  



                # Encontra o bloco de pagamento e seleciona o 90
                element_formaPagamento = Select(driver.find_element(By.ID, 'nfe_payment_method'))
                element_formaPagamento.select_by_value('90')

                # Encontra o bloco de valor total e zera
                element_pagamento_total = driver.find_element(By.ID, 'nfe_total_information_attributes_paid_total')
                element_pagamento_total.clear()
                actions.send_keys(Keys.TAB).perform() 

                time.sleep(1.5)

                # Encontra o elemento para emitir a nota e clica
                element_emitir_nota = driver.find_element(By.ID, 'save-and-submit-nfe')
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_emitir_nota)
                time.sleep(1)
                element_emitir_nota.click()

                time.sleep(1) # Aguarda até aparecer a contingencia ou confirmar a NF
            
                element_contingencia1 = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                )

                try:
                    element_contingencia1.click()
                except:
                    pass

                # Confirma a emissão da NF
                element_confirmar_emissão = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                )
                element_confirmar_emissão.click()

                element_carregar = WebDriverWait(driver, 100).until( # Aguarda o elemento do carregamento da NF desaparecer para continuar
                    EC.invisibility_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                )

                if element_carregar:

                    driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                driver.refresh()

                element_nova_nota_emitir2 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                )
                element_nova_nota_emitir2.click()

                idx += 1
                
                log_instance.log_message(f'{idx}: {CHAMADO}/{pn_lista} inseridos com sucesso no site.')

                time.sleep(2.5)

            except AssertionError:
                pass

            except Exception as e:
                idx += 1 

                log_instance.log_message(f'Não foi possível inserir os dados da planilha no site:\n{idx}: {CHAMADO}/{pn_lista}')

                driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                driver.refresh()

                element_nova_nota_emitir3 = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                )
                element_nova_nota_emitir3.click()       
                continue
    except:
        driver.quit()

        log_instance.log_message('Erro desconhecido.')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()
        
    time.sleep(5)

    driver.close()

    log_instance.log_message("Emissão de NFe's concluída.")

    botao_voltar.disabled = False
    botao_voltar.content.color = ft.Colors.WHITE
    page.update()

def emitir_nf_entrada_tec(log_instance, page, views, current_view):

    navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações recebimento')

    botao_voltar = views['logs e informações recebimento'].content.controls[1].content.controls[0].controls[0]
    botao_voltar.disabled = True
    botao_voltar.content.color = ft.Colors.GREY_400
    page.update()

    driver = None

    #==============================================================================
    subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
    time.sleep(3)

    # Pasta vazia nova, sem copiar nada
    import os
    temp_dir = r"C:\ChromeSelenium"
    os.makedirs(temp_dir, exist_ok=True)

    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "--no-first-run",
        "--no-default-browser-check"
    ])

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    log_instance.log_message('Iniciando importação de arquivos...')

    driver.get(url_login_iob)

    time.sleep(4)
    #==============================================================================

    actions = ActionChains(driver)

    log_instance.log_message("Iniciando emissão de NFe's...")

    # Acessa a página desejada
    driver.get(url_login_iob)
    
    try:
        time.sleep(15) # tempo para carregar o reCAPTCHA

        element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
            EC.presence_of_element_located((By.ID, 'username'))
        )
        element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

        time.sleep(2.5)

        element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
            EC.presence_of_element_located((By.ID, 'password'))
        )
        element_senha_emitir.send_keys(senha_IOB) # Insere a senha

        """
        time.sleep(2.5) # tempo para carregar o reCAPTCHA

        element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
            EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
        )
        driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
        captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
        captcha_checkbox.click() # Clica no elemento captcha

        driver.switch_to.default_content() # Muda para o contexto padrão da página

        time.sleep(20)
        """

        element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
            EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
        )
        element_submit_emitir.click()  # Clica no elemento submit

        element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
        )

        try:
            element_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
            )
            element_form.click()
        except:
            pass
                
        if element_emissão_notas_emitir:
            driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso encontre o botão de notas, entra na página para emitir

        try:
            element_form.click()
        except:
            pass

        element_nova_nota_emitir = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
        )
        element_nova_nota_emitir.click()

    except AssertionError:
            pass

    except Exception as e:
        log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada.')
        driver.quit()
        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    idx = 1

    if planilha_manager.is_planilha_atualizada():
        planilha_manager.recarregar_planilha()
    
    planilha_df = planilha_manager.get_planilha()


    planilha_df.ffill(inplace = True)

    ler_planilha_mesclada = planilha_df.groupby('CHAMADO', as_index = False, sort = False).agg({
        'NF OU XML PARA BAIXAR (PROGRAMA)': lambda x: ', '.join(map(str, filter(pd.notna, x))),
        'PN CAIXA.': lambda x: ', '.join(map(str, x)),
        'VALOR': lambda x: ', '.join(map(str, x)),
        'CST': lambda x: ', '.join(map(str, x)),
        'ICMS': lambda x: ', '.join(map(str, x)),
        'NCM': lambda x: ', '.join(map(str, x)),
        'QTD.': lambda x: ', '.join(map(str, x)),
        'STATUS': lambda x: ', '.join(map(str, x))
    })

    try:

        for index, row in ler_planilha_mesclada.iloc[:].iterrows(): # Lê todas as linhas da planilha com as colunas selecionadas
            CHAMADO = str(row['CHAMADO']).replace('.0', '').strip()
            nf_lista = str(row['NF OU XML PARA BAIXAR (PROGRAMA)']).replace('.0', '').strip().split(', ')
            pn_lista = str(row['PN CAIXA.']).strip().split(', ')
            valor_lista = str(row['VALOR']).replace('.', ',').strip().split(', ')
            cst_lista = str(row['CST']).split(', ')
            icms_lista = str(row['ICMS']).split(', ')
            ncm_lista = str(row['NCM']).strip().split(', ')
            qtd_lista = str(row['QTD.']).strip().split(', ')
            status_planilha = str(row['STATUS']).strip().split(', ')

            try:

                try:
                    element_contingencia = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                    )
                    element_contingencia.click()
                except:
                    pass

                # Encontra o campo de cliente
                element_cliente_emitir = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_client_id'))
                )
                element_cliente_emitir.send_keys(cliente_recebimento_IOB) # Insere no campo cliente

                element_results_client_emitir = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) # Lê as opções dadas pelo site com a lista de clientes
                )

                element_first_li_cliente_emitir = element_results_client_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona o primeiro cliente que aparece
                element_first_li_cliente_emitir.click()

                # Encontra o campo de natureza
                element_natureza_emitir = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_nature_id'))
                )
                element_natureza_emitir.clear() # Limpa o que estiver escrito no campo natureza

                if any(s.upper() == 'GOOD' or s.strip().lower() == 'nan' for s in status_planilha): # Se o produto for GOOD:
                    element_natureza_emitir.send_keys(natureza_recebimento_IOB_good) # Insere no campo natureza

                    time.sleep(1.5)

                    element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                    )

                    element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                    element_first_li_natureza_emitir.click()

                else:
                    element_natureza_emitir.send_keys(natureza_recebimento_IOB_defective) # Insere no campo natureza

                    element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                    element_first_li_natureza_emitir.click()

                idx_element = 1

                idx_qtd = 0
                
                for pn, valor, cst, icms, ncm, qtd in zip(pn_lista, valor_lista, cst_lista, icms_lista, ncm_lista, qtd_lista):
                    
                    # Busca pelo campo para inserir o produto
                    element_produto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_product_id'))
                    )

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_produto)

                    # Insere o produto que está na planilha
                    element_produto.send_keys(pn) 

                    time.sleep(1)

                    # Encontra a lista de opções do produto
                    element_produto_results = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    # Seleciona o primeiro produto que aparece                                          
                    element_first_li_produto_emitir = element_produto_results.find_element(By.CSS_SELECTOR, f'ul li:first-child') 
                    element_first_li_produto_emitir.click() 

                    time.sleep(1.5)
                    
                    try:

                        element_produto_selecionar = WebDriverWait(driver, 50).until( 
                            EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/section/div/div[3]/form/div[1]/div[9]/div/div[7]/div/div[1]/div/div/table/tbody/tr[{idx_element}]/td[4]/div/span/input')) 
                        )
                        driver.execute_script("""
                            arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                            window.scrollBy(0, 230);  // Ajusta o scroll um pouco para baixo (230px)
                        """, element_produto_selecionar)

                        element_produto_selecionar.click()

                        # Encontra o elemento NCM do produto e envia os dados da planilha
                        element_NCM = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_product_ncm_id'))
                        )
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_NCM)
                        element_NCM.clear()
                        time.sleep(1.5)

                        for x in ncm:
                            element_NCM.send_keys(f'{x}')
                            time.sleep(0.8)

                        time.sleep(3)

                        # Lê as opções dadas pelo site com a lista de NCM
                        
                        element_NCM = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )
                        time.sleep(2)

                        # Seleciona o primeiro NCM que aparece
                        element_NCM_prod = element_NCM.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                        element_NCM_prod.click()
                        actions.send_keys(Keys.TAB).perform()

                        element_CFOP = Select(driver.find_element(By.ID, 'item_cfop'))
                
                        element_CFOP.select_by_value('1949')

                        # Altera o display da informação ''quantidade'' do produto para ser possível acessar pelo selenium
                        element_quantidade_comercial = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_quantity'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_comercial, qtd)
                        
                        element_quantidade_tributavel =  WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_taxable_amount'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_tributavel, qtd)

                        # Altera o display da informação ''valor unitário'' do produto para ser possível acessar pelo selenium
                        driver.execute_script("document.getElementById('item_unit_price').style.display = 'block';") 
                        element_valor_produto = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_unit_price'))
                        )

                        # Força a inserção do valor no site
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_valor_produto, valor)
                        actions.send_keys(Keys.TAB).perform()

                        element_valor_taxa = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_taxable_price'))
                        )
                        element_valor_taxa.clear()

                        time.sleep(0.5) # Tempo para salvar o valor do produto

                        # Encontra o campo de ICMS e clica nele
                        element_campo_ICMS = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.XPATH, xpath_ir_para_aba_campo_icms))
                        )
                        element_campo_ICMS.click()

                        # Encontra o campo ORIG e altera para o orig do produto
                        element_orig = Select(driver.find_element(By.XPATH, f'//*[@id="item_icms_origin"]'))

                        element_orig.select_by_value(cst)

                        if botao_switch_para_icms == 'False':

                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('400')

                            time.sleep(3)

                        elif botao_switch_para_icms == 'True':
                            
                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('00')

                            element_campo_cst_icms = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.ID, 'item_icms_tax_rate'))
                            )

                            element_campo_cst_icms.clear()

                            time.sleep(1)

                            driver.execute_script("""
                                arguments[0].value = arguments[1];
                                arguments[0].dispatchEvent(new Event('input'));
                                arguments[0].dispatchEvent(new Event('change'));
                            """, element_campo_cst_icms, icms)

                            time.sleep(3)

                        element_submit_produto = driver.find_element(By.XPATH, xpath_botao_submit_aba_icms) # Encontra o botão de salvar as informações do produto e clica
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_submit_produto)
                        driver.execute_script("arguments[0].click();", element_submit_produto)

                        idx_qtd += 1

                        idx_element += 1

                    except AssertionError:
                        pass
                
                    except Exception as e:
                        log_instance.log_message(f'{idx}: Erro ao tentar inserir um dado do produto {CHAMADO}/{pn}')

                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                        driver.refresh()

                        element_nova_nota_emitir1 = WebDriverWait(driver, 200).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                        )
                        element_nova_nota_emitir1.click()   

                        idx += 1

                        continue

                # Encontra e clica na modalidade de frete
                element_frete =  WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
                )
                time.sleep(0.5)
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_frete)
                time.sleep(0.5)
                element_frete.click()

                # Encontra dentro das opções, o frete do processo

                element_frete_terceiros = Select(driver.find_element(By.ID, 'nfe_carriage_modality'))
                
                element_frete_terceiros.select_by_value('9')

                # Encontra o bloco de quantidade de produtos e insere a quantidade 1
                element_quantidade = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_quantity')) 
                )
                element_quantidade.clear()
                element_quantidade.send_keys(idx_qtd)
                actions.send_keys(Keys.TAB).perform()

                # Encontra o bloco de espécie de produtos e insere 'volume'
                element_especie = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_kind'))
                )
                element_especie.send_keys('CAIXA')
                actions.send_keys(Keys.TAB).perform() 

                time.sleep(0.5) # Tempo para processar a especie

                PESO_BRUTO = 1

                element_peso_bruto = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_gross_weight')) 
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_peso_bruto, PESO_BRUTO)
                time.sleep(0.5)
                actions.send_keys(Keys.TAB).perform()

                time.sleep(0.5) # Tempo para processar o peso bruto

                element_peso_liquido = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'nfe_carriage_net_weight')) 
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_peso_liquido, PESO_BRUTO)
                time.sleep(0.5)
                actions.send_keys(Keys.TAB).perform()

                time.sleep(0.5) # Tempo para processar o peso liquido

                # Encontra o campo de observação e adiciona as informações de acordo com a planilha
                element_observação = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'nfe_notes'))
                )

                if botao_switch_para_icms == 'False':

                    element_observação.send_keys(f'@ENV ;@REF {CHAMADO} REF NF {nf_lista} PN {pn_lista} STATUS {status_planilha}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".')
                
                elif botao_switch_para_icms == 'True':
                    
                    element_observação.send_keys(f'@ENV ;@REF {CHAMADO} REF NF {nf_lista} PN {pn_lista} STATUS {status_planilha}')


                # Encontra o bloco de pagamento e seleciona o 90
                element_formaPagamento = Select(driver.find_element(By.ID, 'nfe_payment_method'))
                element_formaPagamento.select_by_value('90')

                # Encontra o bloco de valor total e zera
                element_pagamento_total = driver.find_element(By.ID, 'nfe_total_information_attributes_paid_total')
                element_pagamento_total.clear()
                actions.send_keys(Keys.TAB).perform() 

                time.sleep(1.5)

                # Encontra o elemento para emitir a nota e clica
                element_emitir_nota = driver.find_element(By.ID, 'save-and-submit-nfe')
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_emitir_nota)
                time.sleep(1)
                element_emitir_nota.click()

                time.sleep(1) # Aguarda até aparecer a contingencia ou confirmar a NF
            
                element_contingencia1 = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                )

                try:
                    element_contingencia1.click()
                except:
                    pass

                # Confirma a emissão da NF
                element_confirmar_emissão = WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                )
                element_confirmar_emissão.click()

                element_carregar = WebDriverWait(driver, 100).until( # Aguarda o elemento do carregamento da NF desaparecer para continuar
                    EC.invisibility_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                )

                if element_carregar:
                    driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                driver.refresh()

                element_nova_nota_emitir2 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                )
                element_nova_nota_emitir2.click()

                idx += 1
                
                log_instance.log_message(f'{idx}: {CHAMADO}/{pn_lista} inseridos com sucesso no site.')

                time.sleep(2.5)

            except AssertionError:
                pass

            except Exception as e:
                log_instance.log_message(f'Não foi possível inserir os dados da planilha no site:\n{idx}: {CHAMADO}/{pn_lista}')

                driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                driver.refresh()

                element_nova_nota_emitir3 = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                )
                element_nova_nota_emitir3.click()       

                idx += 1 

                continue
    except:
        driver.quit()

        log_instance.log_message('Erro: Verifique se alguma planilha foi selecionada')

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()
        
    time.sleep(5)

    driver.close()

    log_instance.log_message("Emissão de NFe's concluída.")

    botao_voltar.disabled = False
    botao_voltar.content.color = ft.Colors.WHITE
    page.update()

def emitir_NF_dev_dell(log_instance, page, views, current_view):

    def mostrar_confirmacao(page):
        dialog.open = True
        page.update()

    def continuar(e):

        navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações devolução')

        botao_voltar = views['logs e informações devolução'].content.controls[1].content.controls[0].controls[0]
        botao_voltar.disabled = True
        botao_voltar.content.color = ft.Colors.GREY_400
        dialog.open = False
        page.update()

        try:
            conectar_email_e_baixar_arquivos_Dell(log_instance)
        except Exception as e:
            log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada. Feche o navegador\n{e}')
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            return

        idx = 0

        driver = None

        #==============================================================================
        subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
        time.sleep(3)

        # Pasta vazia nova, sem copiar nada
        import os
        temp_dir = r"C:\ChromeSelenium"
        os.makedirs(temp_dir, exist_ok=True)

        subprocess.Popen([
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--remote-debugging-port=9222",
            f"--user-data-dir={temp_dir}",
            "--no-first-run",
            "--no-default-browser-check"
        ])

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        log_instance.log_message('Iniciando importação de arquivos...')

        driver.get(url_login_iob)

        time.sleep(4)
        #==============================================================================

        actions = ActionChains(driver)

        log_instance.log_message("Iniciando emissão de NFe's...")

        # Acessa a página desejada
        driver.get(url_login_iob)

        try:

            time.sleep(15) # tempo para carregar o reCAPTCHA

            element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
                EC.presence_of_element_located((By.ID, 'username'))
            )
            element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

            time.sleep(2.5)

            element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
                EC.presence_of_element_located((By.ID, 'password'))
            )
            element_senha_emitir.send_keys(senha_IOB) # Insere a senha

            """
            time.sleep(2.5) # tempo para carregar o reCAPTCHA

            element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
                EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
            )
            driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
            captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
            captcha_checkbox.click() # Clica no elemento captcha

            driver.switch_to.default_content() # Muda para o contexto padrão da página

            time.sleep(20)
            """

            element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
                EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
            )
            element_submit_emitir.click()  # Clica no elemento submit

            element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
            )

            try:
                element_form = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
                )
                element_form.click()
            except:
                pass
                    
            if element_emissão_notas_emitir:
                driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso encontre o botão de notas, entra na página para emitir

            try:
                element_form.click()
            except:
                pass

            element_nova_nota_emitir = WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
            )
            element_nova_nota_emitir.click()

        except AssertionError:
            pass

        except Exception as e:
            log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada.')
            driver.quit()
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()

        if planilha_manager.is_planilha_atualizada():
            planilha_manager.recarregar_planilha()

        planilha_df = planilha_manager.get_planilha()


        resultados = {} 

        try:

            for index, row in planilha_df.iloc[:].iterrows(): # Lê todas as linhas da planilha com as colunas selecionadas
                CHAMADO = str(row[0]).strip()
                NF = str(row[1]).strip()
                PN = str(row[2]).strip()
                PN_CAIXA = str(row[3]).strip()
                VALOR = str(row[5]).strip().replace('.', ',')
                CST = row[6]
                ICMS = row[7]
                NCM = str(row[8]).strip() 
                QTD = str(row[9]).strip()
                STATUS_planilha = str(row[10]).strip()

                # Percorrer todos os arquivos XML na pasta
                for arquivo_xml in os.listdir(aux_path_XML_destino):

                    if arquivo_xml.endswith('.xml'):
                        caminho_arquivo = os.path.join(aux_path_XML_destino, arquivo_xml)
                        
                        # Parsear o arquivo XML
                        tree = ET.parse(caminho_arquivo)
                        root = tree.getroot()

                        # Namespace do XML (pode variar dependendo do arquivo)
                        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

                        # Extrair todos os valores de <cProd>
                        cProd_list = root.findall('.//nfe:cProd', ns)
                        for cProd in cProd_list:
                            if cProd.text == PN:
                                # Extrair o valor de <infCpl>
                                infCpl = root.find('.//nfe:infCpl', ns)
                                if infCpl is not None:
                                    infCpl_text = infCpl.text

                                    # Verificar se o CHAMADO e NF estão no <infCpl>
                                    if f'{CHAMADO}' in infCpl_text:
                                        # Extrair a chave NFe
                                        infNFe = root.find('.//nfe:infNFe', ns)
                                        if infNFe is not None:
                                            chaveNFe = infNFe.attrib.get('Id')
                                            if chaveNFe:
                                                # Armazenar o resultado
                                                resultados[arquivo_xml] = chaveNFe

                try:

                    element_contingencia = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                    )

                    try: 
                        element_contingencia.click()
                    except:
                        pass

                    element_referenciar = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/ul/li[3]/a')) 
                    )
                    element_referenciar.click()

                    time.sleep(1.5)

                    element_inserir_documento = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@class="add"]'))
                    )
                    driver.execute_script("arguments[0].click();", element_inserir_documento)

                    time.sleep(1)

                    element_inserir_nf_referenciada = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "nfe_documents_attributes_") and contains(@id, "_document_ref_nfe_access_key")]'))
                    )
                    element_inserir_nf_referenciada.send_keys(chaveNFe[3:])

                    time.sleep(2)

                    element_inserir_produtos = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/ul/li[1]/a')) 
                    )
                    element_inserir_produtos.click()

                    time.sleep(2)

                    # Encontra o campo de cliente
                    element_cliente_emitir = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_client_id'))
                    )
                    element_cliente_emitir.send_keys(cliente_devolucao_dell_IOB) # Insere no campo cliente

                    element_results_client_emitir = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) # Lê as opções dadas pelo site com a lista de clientes
                    )

                    element_first_li_cliente_emitir = element_results_client_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona o primeiro cliente que aparece
                    element_first_li_cliente_emitir.click()

                    # Encontra o campo de natureza
                    element_natureza_emitir = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_nature_id'))
                    )
                    element_natureza_emitir.clear() # Limpa o que estiver escrito no campo natureza

                    if STATUS_planilha.upper() == 'GOOD' or STATUS_planilha.lower() == 'nan': # Se o produto for GOOD:
                        element_natureza_emitir.send_keys(natureza_devolucao_dell_good_IOB) # Insere no campo natureza

                        element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )

                        element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                        element_first_li_natureza_emitir.click()

                    else:
                        element_natureza_emitir.send_keys(natureza_devolucao_dell_defective_IOB) # Insere no campo natureza

                        element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                        )

                        element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                        element_first_li_natureza_emitir.click()
                    
                    # Busca pelo campo para inserir o produto
                    element_produto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_product_id'))
                    )

                    # Insere o produto que está na planilha
                    element_produto.send_keys(f'{PN}') 

                    # Encontra a lista de opções do produto
                    element_produto_results = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    # Seleciona o primeiro produto que aparece
                    element_first_li_produto_emitir = element_produto_results.find_element(By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/div[1]/div/div/div[1]/div/div[2]/div/span/div/ul/li[1]') 
                    element_first_li_produto_emitir.click()

                    time.sleep(1.5)
                    
                    try:
                        
                        # Clica no produto para alterar as informações
                        element_produto_selecionar = WebDriverWait(driver, 50).until( 
                            EC.element_to_be_clickable((By.XPATH, "//input[contains(@id, '_product_name')]")) 
                        )
                        element_produto_selecionar.click()

                        # Encontra o elemento NCM do produto e envia os dados da planilha
                        element_NCM = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_product_ncm_id'))
                        )
                        element_NCM.clear()
                        time.sleep(0.5)

                        for x in NCM:
                            element_NCM.send_keys(f'{x}')
                            time.sleep(0.8)

                        time.sleep(3)

                        # Lê as opções dadas pelo site com a lista de NCM
                        
                        element_NCM = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )
                        time.sleep(0.5)

                        # Seleciona o primeiro NCM que aparece
                        element_NCM_prod = element_NCM.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                        element_NCM_prod.click()
                        actions.send_keys(Keys.TAB).perform()

                        element_CFOP = Select(driver.find_element(By.ID, 'item_cfop'))
                    
                        element_CFOP.select_by_value('6949')

                        # Altera o display da informação ''quantidade'' do produto para ser possível acessar pelo selenium
                        element_quantidade_comercial = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_quantity'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_comercial, QTD)
                        
                        element_quantidade_tributavel =  WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_taxable_amount'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_tributavel, QTD)

                        # Altera o display da informação ''valor unitário'' do produto para ser possível acessar pelo selenium
                        driver.execute_script("document.getElementById('item_unit_price').style.display = 'block';") 
                        element_valor_produto = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_unit_price'))
                        )

                        # Força a inserção do valor no site
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_valor_produto, VALOR)
                        actions.send_keys(Keys.TAB).perform()

                        element_valor_taxa = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_taxable_price'))
                        )
                        element_valor_taxa.clear()

                        time.sleep(0.5) # Tempo para salvar o valor do produto

                        # Encontra o campo de ICMS e clica nele
                        element_campo_ICMS = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.XPATH, xpath_ir_para_aba_campo_icms))
                        )
                        element_campo_ICMS.click()

                        # Encontra o campo ORIG e altera para o orig do produto
                        element_orig = Select(driver.find_element(By.XPATH, f'//*[@id="item_icms_origin"]'))

                        element_orig.select_by_value(f'{CST}')


                        if botao_switch_para_icms == 'False':

                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('400')

                            time.sleep(3)

                        elif botao_switch_para_icms == 'True':
                            
                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('00')

                            element_campo_cst_icms = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.ID, 'item_icms_tax_rate'))
                            )

                            element_campo_cst_icms.clear()

                            time.sleep(1)

                            driver.execute_script("""
                                arguments[0].value = arguments[1];
                                arguments[0].dispatchEvent(new Event('input'));
                                arguments[0].dispatchEvent(new Event('change'));
                            """, element_campo_cst_icms, ICMS)

                            time.sleep(3)

                        element_submit_produto = driver.find_element(By.XPATH, xpath_botao_submit_aba_icms) # Encontra o botão de salvar as informações do produto e clica
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_submit_produto)
                        driver.execute_script("arguments[0].click();", element_submit_produto)

                    except AssertionError:
                        pass
                    
                    except Exception as e:
                        log_instance.log_message(f'{idx}: Erro ao tentar inserir um dado do produto {CHAMADO}/{PN}')

                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                        driver.refresh()

                        element_nova_nota_emitir1 = WebDriverWait(driver, 200).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                        )
                        element_nova_nota_emitir1.click()   

                        continue

                    # Encontra e clica na modalidade de frete
                    element_frete =  WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_frete)
                    element_frete.click()
                    
                    element_frete_terceiros = Select(driver.find_element(By.ID, 'nfe_carriage_modality'))
                    
                    element_frete_terceiros.select_by_value('1')

                    # Encontra o bloco de selecionar a transportadora e insere no campo de transportadora
                    element_transportadora = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carrier_id'))
                    )
                    element_transportadora.send_keys(transportadora_devolucao_dell_IOB) 

                    time.sleep(1)

                    # Lê as opções dadas pelo site com a lista de transportadora
                    element_transportadora = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    time.sleep(1)

                    # Seleciona a primeira transportadora que aparece
                    element_transportadora_tnt = element_transportadora.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                    element_transportadora_tnt.click()

                    # Encontra o bloco de quantidade de produtos e insere a quantidade 1
                    element_quantidade = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'nfe_carriage_quantity')) 
                    )
                    element_quantidade.clear()
                    element_quantidade.send_keys('1')
                    actions.send_keys(Keys.TAB).perform()

                    # Encontra o bloco de espécie de produtos e insere 'volume'
                    element_especie = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'nfe_carriage_kind'))
                    )
                    element_especie.send_keys('VOLUME')
                    actions.send_keys(Keys.TAB).perform() 

                    time.sleep(0.5) # Tempo para processar o peso bruto

                    # Encontra o bloco de peso bruto de produtos e insere a quantidade 1
                    PESO_BRUTO = 1

                    element_peso_bruto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_gross_weight')) 
                    )
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input'));
                        arguments[0].dispatchEvent(new Event('change'));
                        """, element_peso_bruto, PESO_BRUTO)
                    time.sleep(0.5)
                    actions.send_keys(Keys.TAB).perform()

                    time.sleep(0.5) # Tempo para processar o peso bruto

                    element_peso_liquido = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_net_weight')) 
                    )
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input'));
                        arguments[0].dispatchEvent(new Event('change'));
                        """, element_peso_liquido, PESO_BRUTO)
                    time.sleep(0.5)
                    actions.send_keys(Keys.TAB).perform()

                    time.sleep(0.5) # Tempo para processar o peso liquido

                    # Encontra o campo de observação e adiciona as informações de acordo com a planilha
                    element_observação = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.ID, 'nfe_notes'))
                    )

                    if botao_switch_para_icms == 'False':
                        
                        if PN == PN_CAIXA:
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} {STATUS_planilha}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".')
                        else:
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} SOFREU ALTERAÇÃO PARA {PN_CAIXA} {STATUS_planilha}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".')
                        

                    elif botao_switch_para_icms == 'True':

                        if PN == PN_CAIXA:
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} {STATUS_planilha}')
                        else:
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} SOFREU ALTERAÇÃO PARA {PN_CAIXA} {STATUS_planilha}')

                    time.sleep(3)

                    # Encontra o bloco de pagamento e seleciona o 90
                    element_formaPagamento = Select(driver.find_element(By.ID, 'nfe_payment_method'))
                    element_formaPagamento.select_by_value('90')

                    # Encontra o bloco de valor total e zera
                    element_pagamento_total = driver.find_element(By.ID, 'nfe_total_information_attributes_paid_total')
                    element_pagamento_total.clear()
                    actions.send_keys(Keys.TAB).perform() 

                    time.sleep(0.5)

                    # Encontra o elemento para emitir a nota e clica
                    element_emitir_nota = driver.find_element(By.ID, 'save-and-submit-nfe')
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_emitir_nota)
                    time.sleep(1)
                    element_emitir_nota.click()

                    time.sleep(1) # Aguarda até aparecer a contingencia ou confirmar a NF

                    element_contingencia1 = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                        )
                    
                    try: 
                        element_contingencia1.click()

                        # Confirma a emissão da NF
                        element_confirmar_emissão = WebDriverWait(driver, 100).until(
                            EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                        )
                        element_confirmar_emissão.click()

                    except:
                        # Confirma a emissão da NF
                        element_confirmar_emissão = WebDriverWait(driver, 100).until(
                            EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                        )
                        element_confirmar_emissão.click()

                        pass

                    WebDriverWait(driver, 100).until( # Aguarda o elemento do carregamento da NF desaparecer para continuar
                        EC.invisibility_of_element_located((By.XPATH, '//*[@id="proxy-reserve"]/div[5]/div[2]/div/div/a'))
                    )

                    # Encontra o elemento para baixar o XML e clica
                    element_baixar_xml = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_botao_baixar_xml))
                    )
                    element_baixar_xml.click()

                    time.sleep(2.5) # Tempo para baixar o arquivo

                    # Encontra o elemento para ir para danfe e clica
                    element_ir_para_danfe = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_botao_ir_para_danfe))
                    )
                    element_ir_para_danfe.click()

                    # Encontra o elemento para baixar o PDF e clica
                    element_baixar_pdf = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_botao_baixar_pdf))
                    )
                    element_baixar_pdf.click()

                    time.sleep(2.5) # Tempo para baixar o arquivo

                    if element_baixar_pdf:
                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso baixe o pdf, entra na página para emitir novamente

                    element_nova_nota_emitir2 = WebDriverWait(driver, 200).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                    )
                    element_nova_nota_emitir2.click()

                    idx += 1
                    
                    log_instance.log_message(f'{idx}: {CHAMADO}/{PN} inseridos com sucesso no site.')

                    time.sleep(2.5)

                except AssertionError:
                    pass

                except Exception as e:
                    log_instance.log_message(f'{idx}: Não foi possível inserir os dados da planilha no site: {CHAMADO}/{PN}')

                    driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                    driver.refresh()

                    element_nova_nota_emitir3 = WebDriverWait(driver, 200).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                    )
                    element_nova_nota_emitir3.click()       

                    continue
        except:
            driver.quit()

            log_instance.log_message('Erro: Verifique se alguma planilha foi selecionada')

            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            
        time.sleep(5)

        driver.quit()

        log_instance.log_message("Emissão de NFe's concluída.")

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

def emitir_NF_dev_hp(log_instance, page, views, current_view):

    def mostrar_confirmacao(page):
        dialog.open = True
        page.update()

    def continuar(e):

        navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações devolução')

        botao_voltar = views['logs e informações devolução'].content.controls[1].content.controls[0].controls[0]
        botao_voltar.disabled = True
        botao_voltar.content.color = ft.Colors.GREY_400
        dialog.open = False
        page.update()

        try:
            conectar_email_e_baixar_arquivos_HP(log_instance)
        except Exception as e:
            log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada. Feche o navegador\n{e}')
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            return

        idx = 0

        driver = None

        #==============================================================================
        subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
        time.sleep(3)

        # Pasta vazia nova, sem copiar nada
        import os
        temp_dir = r"C:\ChromeSelenium"
        os.makedirs(temp_dir, exist_ok=True)

        subprocess.Popen([
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "--remote-debugging-port=9222",
            f"--user-data-dir={temp_dir}",
            "--no-first-run",
            "--no-default-browser-check"
        ])

        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        log_instance.log_message('Iniciando importação de arquivos...')

        driver.get(url_login_iob)

        time.sleep(4)
        #==============================================================================

        actions = ActionChains(driver)

        log_instance.log_message("Iniciando emissão de NFe's...")

        # Acessa a página desejada
        driver.get(url_login_iob)

        try:
            time.sleep(15) # tempo para carregar o reCAPTCHA

            element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
                EC.presence_of_element_located((By.ID, 'username'))
            )
            element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

            time.sleep(2.5)

            element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
                EC.presence_of_element_located((By.ID, 'password'))
            )
            element_senha_emitir.send_keys(senha_IOB) # Insere a senha

            """
            time.sleep(2.5) # tempo para carregar o reCAPTCHA

            element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
                EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
            )
            driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
            captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
            captcha_checkbox.click() # Clica no elemento captcha

            driver.switch_to.default_content() # Muda para o contexto padrão da página

            time.sleep(20)
            """

            element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
                EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
            )
            element_submit_emitir.click()  # Clica no elemento submit

            element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
            )

            try:
                element_form = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
                )
                element_form.click()
            except:
                pass
                    
            if element_emissão_notas_emitir:
                driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso encontre o botão de notas, entra na página para emitir

            try:
                element_form.click()
            except:
                pass

            element_nova_nota_emitir = WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
            )
            element_nova_nota_emitir.click()

        except AssertionError:
            pass

        except Exception as e:
            log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada.')
            driver.quit()
            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()

        if planilha_manager.is_planilha_atualizada():
            planilha_manager.recarregar_planilha()

        planilha_df = planilha_manager.get_planilha()

        resultados = {} 

        try:

            for index, row in planilha_df.iloc[:].iterrows(): # Lê todas as linhas da planilha com as colunas selecionadas
                CHAMADO = str(row[0]).strip()
                NF = str(row[1]).strip()
                PN = str(row[2]).strip()
                AWB = str(row[4]).strip()
                VALOR = str(row[5]).strip().replace('.', ',')
                CST = row[6]
                ICMS = row[7]
                NCM = str(row[8]).strip() 
                QTD = str(row[9]).strip()
                STATUS_planilha = str(row[10]).strip()

                # Percorrer todos os arquivos XML na pasta
                for arquivo_xml in os.listdir(aux_path_XML_destino):

                    if arquivo_xml.endswith('.xml'):
                        caminho_arquivo = os.path.join(aux_path_XML_destino, arquivo_xml)
                        
                        # Parsear o arquivo XML
                        tree = ET.parse(caminho_arquivo)
                        root = tree.getroot()

                        # Namespace do XML (pode variar dependendo do arquivo)
                        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

                        # Extrair todos os valores de <cProd>
                        cProd_list = root.findall('.//nfe:cProd', ns)
                        for cProd in cProd_list:
                            if cProd.text == PN:
                                # Extrair o valor de <infCpl>
                                infCpl = root.find('.//nfe:infCpl', ns)
                                if infCpl is not None:
                                    infCpl_text = infCpl.text

                                    # Verificar se o CHAMADO e NF estão no <infCpl>
                                    if f'{CHAMADO}' in infCpl_text:
                                        # Extrair a chave NFe
                                        infNFe = root.find('.//nfe:infNFe', ns)
                                        if infNFe is not None:
                                            chaveNFe = infNFe.attrib.get('Id')
                                            if chaveNFe:
                                                # Armazenar o resultado
                                                resultados[arquivo_xml] = chaveNFe

                try:

                    element_contingencia = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                    )

                    try: 
                        element_contingencia.click()
                    except:
                        pass

                    element_referenciar = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/ul/li[3]/a')) 
                    )
                    element_referenciar.click()

                    time.sleep(1.5)

                    element_inserir_documento = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[@class="add"]'))
                    )
                    driver.execute_script("arguments[0].click();", element_inserir_documento)

                    time.sleep(1)

                    element_inserir_nf_referenciada = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "nfe_documents_attributes_") and contains(@id, "_document_ref_nfe_access_key")]'))
                    )
                    element_inserir_nf_referenciada.send_keys(chaveNFe[3:])

                    time.sleep(2)

                    element_inserir_produtos = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/ul/li[1]/a')) 
                    )
                    element_inserir_produtos.click()

                    time.sleep(2)

                    # Encontra o campo de cliente
                    element_cliente_emitir = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_client_id'))
                    )
                    element_cliente_emitir.send_keys(cliente_devolucao_hp_IOB) # Insere no campo cliente

                    element_results_client_emitir = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) # Lê as opções dadas pelo site com a lista de clientes
                    )

                    element_first_li_cliente_emitir = element_results_client_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona o primeiro cliente que aparece
                    element_first_li_cliente_emitir.click()

                    # Encontra o campo de natureza
                    element_natureza_emitir = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_nature_id'))
                    )
                    element_natureza_emitir.clear() # Limpa o que estiver escrito no campo natureza

                    if STATUS_planilha.upper() == 'GOOD' or STATUS_planilha.lower() == 'nan': # Se o produto for GOOD:
                        element_natureza_emitir.send_keys(natureza_devolucao_hp_good_IOB) # Insere no campo natureza

                        element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )

                        element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                        element_first_li_natureza_emitir.click()

                    else:
                        element_natureza_emitir.send_keys(natureza_devolucao_hp_defective_IOB) # Insere no campo natureza

                        element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                        )

                        element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
                        element_first_li_natureza_emitir.click()
                    
                    # Busca pelo campo para inserir o produto
                    element_produto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_product_id'))
                    )

                    # Insere o produto que está na planilha
                    element_produto.send_keys(f'{PN}') 

                    # Encontra a lista de opções do produto
                    element_produto_results = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    # Seleciona o primeiro produto que aparece
                    element_first_li_produto_emitir = element_produto_results.find_element(By.XPATH, '//*[@id="new_nfe"]/div[1]/div[9]/div/div[7]/div/div[1]/div/div/div[1]/div/div[2]/div/span/div/ul/li[1]') 
                    element_first_li_produto_emitir.click()

                    time.sleep(1.5)
                    
                    try:
                        # Clica no produto para alterar as informações
                        element_produto_selecionar = WebDriverWait(driver, 50).until( 
                            EC.element_to_be_clickable((By.XPATH, "//input[contains(@id, '_product_name')]")) 
                        )
                        element_produto_selecionar.click()

                        # Encontra o elemento NCM do produto e envia os dados da planilha
                        element_NCM = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_product_ncm_id'))
                        )
                        element_NCM.clear()
                        time.sleep(0.5)

                        for x in NCM:
                            element_NCM.send_keys(f'{x}')
                            time.sleep(0.8)

                        time.sleep(3)

                        # Lê as opções dadas pelo site com a lista de NCM
                        
                        element_NCM = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
                        )
                        time.sleep(0.5)

                        # Seleciona o primeiro NCM que aparece
                        element_NCM_prod = element_NCM.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                        element_NCM_prod.click()
                        actions.send_keys(Keys.TAB).perform()

                        element_CFOP = Select(driver.find_element(By.ID, 'item_cfop'))
                    
                        element_CFOP.select_by_value('6949')

                        # Altera o display da informação ''quantidade'' do produto para ser possível acessar pelo selenium
                        element_quantidade_comercial = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_quantity'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_comercial, QTD)
                        
                        element_quantidade_tributavel =  WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.ID, 'item_taxable_amount'))
                        )
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_quantidade_tributavel, QTD)

                        # Altera o display da informação ''valor unitário'' do produto para ser possível acessar pelo selenium
                        driver.execute_script("document.getElementById('item_unit_price').style.display = 'block';") 
                        element_valor_produto = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_unit_price'))
                        )

                        # Força a inserção do valor no site
                        driver.execute_script("""
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input'));
                            arguments[0].dispatchEvent(new Event('change'));
                            """, element_valor_produto, VALOR)
                        actions.send_keys(Keys.TAB).perform()

                        element_valor_taxa = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'item_taxable_price'))
                        )
                        element_valor_taxa.clear()

                        time.sleep(0.5) # Tempo para salvar o valor do produto

                        # Encontra o campo de ICMS e clica nele
                        element_campo_ICMS = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.XPATH, xpath_ir_para_aba_campo_icms))
                        )
                        element_campo_ICMS.click()

                        # Encontra o campo ORIG e altera para o orig do produto
                        element_orig = Select(driver.find_element(By.XPATH, f'//*[@id="item_icms_origin"]'))

                        element_orig.select_by_value(f'{CST}')

                        if botao_switch_para_icms == 'False':

                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('400')

                            time.sleep(3)

                        elif botao_switch_para_icms == 'True':
                            
                            # Encontra o campo para alterar o CST do produto para 400
                            element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                            element_cst.select_by_value('00')

                            element_campo_cst_icms = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable((By.ID, 'item_icms_tax_rate'))
                            )

                            element_campo_cst_icms.clear()

                            time.sleep(1)

                            driver.execute_script("""
                                arguments[0].value = arguments[1];
                                arguments[0].dispatchEvent(new Event('input'));
                                arguments[0].dispatchEvent(new Event('change'));
                            """, element_campo_cst_icms, ICMS)

                            time.sleep(3)

                        element_submit_produto = driver.find_element(By.XPATH, xpath_botao_submit_aba_icms) # Encontra o botão de salvar as informações do produto e clica
                        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_submit_produto)
                        driver.execute_script("arguments[0].click();", element_submit_produto)

                    except AssertionError:
                        pass
                    
                    except Exception as e:
                        log_instance.log_message(f'{idx}: Erro ao tentar inserir um dado do produto {CHAMADO}/{PN}')

                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                        driver.refresh()

                        element_nova_nota_emitir1 = WebDriverWait(driver, 200).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                        )
                        element_nova_nota_emitir1.click()   

                        continue

                    # Encontra e clica na modalidade de frete
                    element_frete =  WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_frete)
                    element_frete.click()
                    
                    element_frete_terceiros = Select(driver.find_element(By.ID, 'nfe_carriage_modality'))
                    
                    element_frete_terceiros.select_by_value('1')

                    # Encontra o bloco de selecionar a transportadora e insere no campo de transportadora
                    element_transportadora = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carrier_id'))
                    )
                    element_transportadora.send_keys(transportadora_devolucao_hp_IOB) 

                    time.sleep(1)

                    # Lê as opções dadas pelo site com a lista de transportadora
                    element_transportadora = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
                    )

                    time.sleep(1)

                    # Seleciona a primeira transportadora que aparece
                    element_transportadora_tnt = element_transportadora.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
                    element_transportadora_tnt.click()

                    # Encontra o bloco de quantidade de produtos e insere a quantidade 1
                    element_quantidade = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'nfe_carriage_quantity')) 
                    )
                    element_quantidade.clear()
                    element_quantidade.send_keys('1')
                    actions.send_keys(Keys.TAB).perform()

                    # Encontra o bloco de espécie de produtos e insere 'volume'
                    element_especie = WebDriverWait(driver, 50).until( 
                            EC.presence_of_element_located((By.ID, 'nfe_carriage_kind'))
                    )
                    element_especie.send_keys('VOLUME')
                    actions.send_keys(Keys.TAB).perform() 

                    time.sleep(0.5) # Tempo para processar o volume

                    # Encontra o bloco de peso bruto de produtos e insere a quantidade 1
                    PESO_BRUTO = 1

                    element_peso_bruto = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_gross_weight')) 
                    )
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input'));
                        arguments[0].dispatchEvent(new Event('change'));
                        """, element_peso_bruto, PESO_BRUTO)
                    time.sleep(0.5)
                    actions.send_keys(Keys.TAB).perform()

                    time.sleep(0.5) # Tempo para processar o peso bruto

                    element_peso_liquido = WebDriverWait(driver, 50).until( 
                        EC.presence_of_element_located((By.ID, 'nfe_carriage_net_weight')) 
                    )
                    driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input'));
                        arguments[0].dispatchEvent(new Event('change'));
                        """, element_peso_liquido, PESO_BRUTO)
                    time.sleep(0.5)
                    actions.send_keys(Keys.TAB).perform()

                    time.sleep(0.5) # Tempo para processar o peso liquido

                    # Encontra o campo de observação e adiciona as informações de acordo com a planilha
                    element_observação = WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.ID, 'nfe_notes'))
                    )

                    if botao_switch_para_icms == 'False':
                        
                        if PN :
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} {STATUS_planilha}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".')                        

                    elif botao_switch_para_icms == 'True':

                        if PN:
                            element_observação.send_keys(f'@DEV ;@REF {CHAMADO} REF NF {NF} PN {PN} {STATUS_planilha}')

                    time.sleep(3)

                    # Encontra o bloco de pagamento e seleciona o 90
                    element_formaPagamento = Select(driver.find_element(By.ID, 'nfe_payment_method'))
                    element_formaPagamento.select_by_value('90')

                    # Encontra o bloco de valor total e zera
                    element_pagamento_total = driver.find_element(By.ID, 'nfe_total_information_attributes_paid_total')
                    element_pagamento_total.clear()
                    actions.send_keys(Keys.TAB).perform() 

                    time.sleep(0.5)

                    # Encontra o elemento para emitir a nota e clica
                    element_emitir_nota = driver.find_element(By.ID, 'save-and-submit-nfe')
                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_emitir_nota)
                    time.sleep(1)
                    element_emitir_nota.click()

                    time.sleep(1) # Aguarda até aparecer a contingencia ou confirmar a NF

                    element_contingencia1 = WebDriverWait(driver, 50).until(
                            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
                        )
                    
                    try: 
                        element_contingencia1.click()

                        # Confirma a emissão da NF
                        element_confirmar_emissão = WebDriverWait(driver, 100).until(
                            EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                        )
                        element_confirmar_emissão.click()

                    except:
                        # Confirma a emissão da NF
                        element_confirmar_emissão = WebDriverWait(driver, 100).until(
                            EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
                        )
                        element_confirmar_emissão.click()

                        pass

                    WebDriverWait(driver, 100).until( # Aguarda o elemento do carregamento da NF desaparecer para continuar
                        EC.invisibility_of_element_located((By.XPATH, '//*[@id="proxy-reserve"]/div[5]/div[2]/div/div/a'))
                    )

                    # Encontra o elemento para baixar o XML e clica
                    element_baixar_xml = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/section/div/div[4]/div/a[4]'))
                    )
                    element_baixar_xml.click()

                    time.sleep(2.5) # Tempo para baixar o arquivo

                    # Encontra o elemento para ir para danfe e clica
                    element_ir_para_danfe = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_botao_ir_para_danfe))
                    )
                    element_ir_para_danfe.click()

                    # Encontra o elemento para baixar o PDF e clica
                    element_baixar_pdf = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_botao_baixar_pdf))
                    )
                    element_baixar_pdf.click()

                    time.sleep(2.5) # Tempo para baixar o arquivo

                    if element_baixar_pdf:
                        driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso baixe o pdf, entra na página para emitir novamente

                    element_nova_nota_emitir2 = WebDriverWait(driver, 200).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                    )
                    element_nova_nota_emitir2.click()

                    idx += 1
                    
                    log_instance.log_message(f'{idx}: {CHAMADO}/{PN} inseridos com sucesso no site.')

                    time.sleep(2.5)

                except AssertionError:
                    pass

                except Exception as e:
                    log_instance.log_message(f'{idx}: Não foi possível inserir os dados da planilha no site: {CHAMADO}/{PN}')

                    driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

                    driver.refresh()

                    element_nova_nota_emitir3 = WebDriverWait(driver, 200).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
                    )
                    element_nova_nota_emitir3.click()       

                    continue
        except:
            driver.quit()

            log_instance.log_message('Erro: Verifique se alguma planilha foi selecionada')

            botao_voltar.disabled = False
            botao_voltar.content.color = ft.Colors.WHITE
            page.update()
            
        time.sleep(5)

        driver.quit()

        log_instance.log_message("Emissão de NFe's concluída.")

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

def emitir_NF_dev_flex(log_instance, page, views, current_view):

    navigate(current_view = current_view, page = page, views = views, view_name = 'logs e informações devolução')

    botao_voltar = views['logs e informações devolução'].content.controls[1].content.controls[0].controls[0]
    botao_voltar.disabled = True
    botao_voltar.content.color = ft.Colors.GREY_400
    page.update()

    driver = None

    #==============================================================================
    subprocess.run(["powershell", "-Command", "Stop-Process -Name chrome -Force"], capture_output=True)
    time.sleep(3)

    # Pasta vazia nova, sem copiar nada
    import os
    temp_dir = r"C:\ChromeSelenium"
    os.makedirs(temp_dir, exist_ok=True)

    subprocess.Popen([
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--remote-debugging-port=9222",
        f"--user-data-dir={temp_dir}",
        "--no-first-run",
        "--no-default-browser-check"
    ])

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    log_instance.log_message('Iniciando importação de arquivos...')

    driver.get(url_login_iob)

    time.sleep(4)
    #==============================================================================

    actions = ActionChains(driver)

    log_instance.log_message("Iniciando emissão de NFe's...")

    # Acessa a página desejada
    driver.get(url_login_iob)
    
    try:
        time.sleep(15) # tempo para carregar o reCAPTCHA

        element_usuario_emitir = WebDriverWait(driver, 200).until( # Busca pela página o campo de usuário
            EC.presence_of_element_located((By.ID, 'username'))
        )
        element_usuario_emitir.send_keys(usuario_IOB) # Insere o nome de usuário

        time.sleep(2.5)

        element_senha_emitir = WebDriverWait(driver, 50).until( # Busca pela página o campo de senha
            EC.presence_of_element_located((By.ID, 'password'))
        )
        element_senha_emitir.send_keys(senha_IOB) # Insere a senha

        """
        time.sleep(2.5) # tempo para carregar o reCAPTCHA

        element_reCAPTCHA_emitir = WebDriverWait(driver, 50).until( # Buscar o elemento reCAPTCHA na página
            EC.presence_of_element_located((By.XPATH, xpath_reCAPTCHA_IOB))
        )
        driver.switch_to.frame(element_reCAPTCHA_emitir) # Muda para o contexto do iframe onde o captcha está inserido
        captcha_checkbox = driver.find_element(By.XPATH, elemento_clicavel_reCAPTCHA_IOB) # Busca o elemento clicável do captcha
        captcha_checkbox.click() # Clica no elemento captcha

        driver.switch_to.default_content() # Muda para o contexto padrão da página

        time.sleep(20)
        """

        element_submit_emitir = WebDriverWait(driver, 50).until( # Busca pelo elemento submit na página
            EC.presence_of_element_located((By.XPATH, '//*[@id="formButton"]'))
        )
        element_submit_emitir.click()  # Clica no elemento submit

        element_emissão_notas_emitir = WebDriverWait(driver, 200).until( # Busca pelo botao de emissão de notas
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="Emissão de Notas"]'))
        )

        try:
            element_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn-2'))
            )
            element_form.click()
        except:
            pass
                
        if element_emissão_notas_emitir:
            driver.get('https://emissor2.iob.com.br/notafiscal/nfes') # Caso encontre o botão de notas, entra na página para emitir

        try:
            element_form.click()
        except:
            pass

        element_nova_nota_emitir = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
        )
        element_nova_nota_emitir.click()

    except AssertionError:
        pass

    except Exception as e:
        log_instance.log_message(f'Erro: Verifique se alguma planilha foi selecionada.')
        driver.quit()
        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    idx = 0

    if planilha_manager.is_planilha_atualizada():
        planilha_manager.recarregar_planilha()
    
    planilha_df = planilha_manager.get_planilha()

    try:
        planilha_df.ffill(inplace = True)
    except AttributeError:
        log_instance.log_message(f'Erro. Verifique se alguma planilha foi selecionada.')

        driver.quit()

        botao_voltar.disabled = False
        botao_voltar.content.color = ft.Colors.WHITE
        page.update()

    # NOVA LÓGICA: Coleta TODOS os dados da planilha
    todos_chamados = []
    todas_nfs = []
    todos_pns = []

    for index, row in planilha_df.iterrows():
        chamado = str(row['CHAMADO']).replace('.0', '').strip()
        nf = str(row['NF OU XML PARA BAIXAR (PROGRAMA)']).replace('.0', '').strip()
        pn = str(row['PN CAIXA.']).strip()
        
        todos_chamados.append(chamado)
        todas_nfs.append(nf)
        todos_pns.append(pn)

    try:
        # Processa UMA ÚNICA NF com todos os produtos
        try:
            element_contingencia = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
            )
            element_contingencia.click()
        except:
            pass

        # Encontra o campo de cliente
        element_cliente_emitir = WebDriverWait(driver, 50).until( 
            EC.presence_of_element_located((By.ID, 'nfe_client_id'))
        )
        element_cliente_emitir.send_keys(cliente_devolucao_flex_IOB) # Insere no campo cliente

        element_results_client_emitir = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) # Lê as opções dadas pelo site com a lista de clientes
        )

        element_first_li_cliente_emitir = element_results_client_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona o primeiro cliente que aparece
        element_first_li_cliente_emitir.click()

        # Encontra o campo de natureza
        element_natureza_emitir = WebDriverWait(driver, 50).until( 
            EC.presence_of_element_located((By.ID, 'nfe_nature_id'))
        )
        element_natureza_emitir.clear() # Limpa o que estiver escrito no campo natureza

        element_natureza_emitir.send_keys(natureza_devolucao_flex_IOB) # Insere no campo natureza

        element_results_natureza_emitir = WebDriverWait(driver, 50).until( # Lê as opções dadas pelo site com a lista de natureza
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results'))
        )

        element_first_li_natureza_emitir = element_results_natureza_emitir.find_element(By.CSS_SELECTOR, 'ul li:first-child') # Seleciona a primeira natureza que aparece
        element_first_li_natureza_emitir.click()

        idx_element = 1
        idx_qtd = 0
        
        # INSERE TODOS OS PRODUTOS da planilha
        for pn in todos_pns:

            # Busca pelo campo para inserir o produto
            element_produto = WebDriverWait(driver, 50).until( 
                EC.presence_of_element_located((By.ID, 'nfe_product_id'))
            )

            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_produto)

            pn_sem_ultimo = pn[:-1]
            # Insere o produto que está na planilha
            element_produto.send_keys(pn_sem_ultimo)

            time.sleep(1)

            # Encontra a lista de opções do produto (PRIMEIRA VEZ)
            element_produto_results = WebDriverWait(driver, 50).until( 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
            )

            time.sleep(1)

            # Insere o último caractere do PN
            ultimo_caractere = pn[-1]
            element_produto.send_keys(ultimo_caractere)

            # Aguarda a lista de produtos atualizar
            time.sleep(1.5)

            # CORREÇÃO: Busca a lista de resultados NOVAMENTE (elemento atualizado)
            element_produto_results_atualizado = WebDriverWait(driver, 50).until( 
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results')) 
            )
            
            # CORREÇÃO: Usa o elemento ATUALIZADO para clicar
            element_first_li_produto_emitir = element_produto_results_atualizado.find_element(By.CSS_SELECTOR, 'ul li:first-child') 
            element_first_li_produto_emitir.click() 

            time.sleep(1.5)
            
            try:

                element_observação = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'nfe_notes'))
                )

                # Dá o scroll para as observações para que o programa consiga encontrar o ultimo produto listado
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_observação)

                time.sleep(1)

                element_produto_selecionar = WebDriverWait(driver, 50).until( 
                    EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/section/div/div[3]/form/div[1]/div[9]/div/div[7]/div/div[1]/div/div/table/tbody/tr[{idx_element}]/td[2]/div/span/input')) 
                )

                element_produto_selecionar.click()

                time.sleep(3)

                element_CFOP = Select(driver.find_element(By.ID, 'item_cfop'))
        
                element_CFOP.select_by_value('6949')

                # Altera o display da informação ''quantidade'' do produto para ser possível acessar pelo selenium
                element_quantidade_comercial = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'item_quantity'))
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_quantidade_comercial, 1)
                
                element_quantidade_tributavel =  WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, 'item_taxable_amount'))
                )
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_quantidade_tributavel, 1)

                driver.execute_script("document.getElementById('item_unit_price').style.display = 'block';") 
                element_valor_produto = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'item_unit_price'))
                )

                # PRIMEIRO: Lê o valor atual do campo
                valor_atual = element_valor_produto.get_attribute('value')

                # Converte para float (tratando vírgula como separador decimal)
                if ',' in valor_atual:
                    valor_numerico = float(valor_atual.replace('.', '').replace(',', '.'))
                else:
                    valor_numerico = float(valor_atual)

                # Calcula 10% do valor atual
                valor_10_percent = valor_numerico * 0.10

                # Formata para o padrão brasileiro
                valor_formatado = f"{valor_10_percent:.2f}".replace('.', ',')

                # Força a inserção do novo valor no site
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input'));
                    arguments[0].dispatchEvent(new Event('change'));
                    """, element_valor_produto, valor_formatado)
                    
                actions.send_keys(Keys.TAB).perform()

                element_valor_taxa = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.ID, 'item_taxable_price'))
                )
                element_valor_taxa.clear()

                time.sleep(0.5) # Tempo para salvar o valor do produto

                # Encontra o campo de ICMS e clica nele
                element_campo_ICMS = WebDriverWait(driver, 50).until( 
                    EC.presence_of_element_located((By.XPATH, xpath_ir_para_aba_campo_icms))
                )
                element_campo_ICMS.click()

                # Encontra o campo para alterar o CST do produto para 400
                element_cst = Select(driver.find_element(By.ID, 'item_icms_cst'))

                element_cst.select_by_value('400')

                element_submit_produto = driver.find_element(By.XPATH, xpath_botao_submit_aba_icms) # Encontra o botão de salvar as informações do produto e clica
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_submit_produto)
                driver.execute_script("arguments[0].click();", element_submit_produto)

                idx_qtd += 1
                idx_element += 1

                log_instance.log_message(f'Produto {pn} adicionado à NF')

            except AssertionError:
                pass
        
            except Exception as e:
                log_instance.log_message(f'Erro ao tentar inserir o produto {pn}: {e}')
                idx_element += 1
                continue

        # CONFIGURA O RESTO E EMITE A NF
        element_frete =  WebDriverWait(driver, 50).until( 
            EC.presence_of_element_located((By.ID, 'nfe_carriage_modality'))
        )
        time.sleep(0.5)
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_frete)
        time.sleep(0.5)
        element_frete.click()

        element_frete_terceiros = Select(driver.find_element(By.ID, 'nfe_carriage_modality'))
        element_frete_terceiros.select_by_value('9')

        element_quantidade = WebDriverWait(driver, 50).until( 
                EC.presence_of_element_located((By.ID, 'nfe_carriage_quantity')) 
        )
        element_quantidade.clear()
        element_quantidade.send_keys(idx_qtd)
        actions.send_keys(Keys.TAB).perform()

        element_especie = WebDriverWait(driver, 50).until( 
                EC.presence_of_element_located((By.ID, 'nfe_carriage_kind'))
        )
        element_especie.send_keys('VOLUME')
        actions.send_keys(Keys.TAB).perform() 

        element_peso_bruto = WebDriverWait(driver, 50).until( 
            EC.presence_of_element_located((By.ID, 'nfe_carriage_gross_weight')) 
        )
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input'));
            arguments[0].dispatchEvent(new Event('change'));
            """, element_peso_bruto, idx_qtd)
        time.sleep(1)
        actions.send_keys(Keys.TAB).perform()

        time.sleep(1)

        element_peso_liquido = WebDriverWait(driver, 50).until( 
            EC.presence_of_element_located((By.ID, 'nfe_carriage_net_weight')) 
        )
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input'));
            arguments[0].dispatchEvent(new Event('change'));
            """, element_peso_liquido, idx_qtd)
        time.sleep(1)
        actions.send_keys(Keys.TAB).perform()

        time.sleep(1)

        element_observação = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, 'nfe_notes'))
        )

        # OBSERVAÇÕES com TODOS os dados da planilha
        texto_obs = f'@ENV ;@REF {", ".join(todos_chamados)} REF NF {", ".join(todas_nfs)} PN {", ".join(todos_pns)}\n I - "DOCUMENTO EMITIDO POR ME OU EPP OPTANTE PELO SIMPLES NACIONAL";II - "NÃO GERA DIREITO A CRÉDITO FISCAL DE ICMS, DE ISS E DE IPI".'
        texto_obs_icms = f'@ENV ;@REF {", ".join(todos_chamados)} REF NF {", ".join(todas_nfs)} PN {", ".join(todos_pns)}'

        if botao_switch_para_icms == 'False':

            element_observação.send_keys(texto_obs)              

        elif botao_switch_para_icms == 'True':

            element_observação.send_keys(texto_obs_icms)

        element_formaPagamento = Select(driver.find_element(By.ID, 'nfe_payment_method'))
        element_formaPagamento.select_by_value('90')

        element_pagamento_total = driver.find_element(By.ID, 'nfe_total_information_attributes_paid_total')
        element_pagamento_total.clear()
        actions.send_keys(Keys.TAB).perform() 

        time.sleep(1.5)

        element_emitir_nota = driver.find_element(By.ID, 'save-and-submit-nfe')
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element_emitir_nota)
        time.sleep(1)
        element_emitir_nota.click()

        time.sleep(1)
    
        element_contingencia1 = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Aguardar")]'))
        )

        try:
            element_contingencia1.click()
        except:
            pass

        element_confirmar_emissão = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, xpath_botao_emitir_nf))
        )
        element_confirmar_emissão.click()

        element_carregar = WebDriverWait(driver, 100).until(
            EC.invisibility_of_element_located((By.XPATH, xpath_botao_emitir_nf))
        )

        if element_carregar:
            driver.get('https://emissor2.iob.com.br/notafiscal/nfes')

        driver.refresh()

        element_nova_nota_emitir2 = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
        )
        element_nova_nota_emitir2.click()

        idx += 1
        
        log_instance.log_message(f'NF com {len(todos_pns)} produtos emitida com sucesso.')

        time.sleep(2.5)

    except AssertionError:
        pass

    except Exception as e:
        log_instance.log_message(f'Não foi possível emitir a NF: {e}')

        driver.get('https://emissor2.iob.com.br/notafiscal/nfes')
        driver.refresh()

        element_nova_nota_emitir3 = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="UIContainer button-grid"] a[class="UILink button primary with_margin"]'))
        )
        element_nova_nota_emitir3.click()       

    driver.quit()
    log_instance.log_message('Erro desconhecido.')
    botao_voltar.disabled = False
    botao_voltar.content.color = ft.Colors.WHITE
    page.update()
        
    time.sleep(5)
    driver.close()
    log_instance.log_message("Emissão de NFe's concluída.")
    botao_voltar.disabled = False
    botao_voltar.content.color = ft.Colors.WHITE
    page.update()
