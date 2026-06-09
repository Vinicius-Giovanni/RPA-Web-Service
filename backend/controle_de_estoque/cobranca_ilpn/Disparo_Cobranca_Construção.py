import pandas as pd
import win32com.client as win32
import os
import requests
import time  # <--- NOVO: Biblioteca para dar as pausas do Teams

# =================================================================
# 1. CONFIGURAÇÕES FÁCEIS E CAMINHOS
# =================================================================

# --- O CARTEIRO AGORA LÊ A PLANILHA MASTIGADA PELO AUDITOR ---
PATH_PRONTO_ENVIO = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\ILPNs_pendentes_pronta_para_envio.xlsx"

# --- CONFIGURAÇÕES DE DISPARO ---
MODO_TESTE = False  # True = Salva e-mail em Rascunho / False = Dispara E-mail de verdade

EMAIL_DEPARTAMENTO = "controleestoque1200@casasbahia.com.br"
# Removi os nomes sem '@' daqui para evitar erros de servidor. Coloque apenas emails válidos!
EMAILS_GESTORES = ["edinaide.silva@casasbahia.com.br", "vinicius.barbosa@casasbahia.com.br"]

WEBHOOK_TEAMS = "https://default5a86b3fb421349cdb4d6be91482ad3.c0.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/3e265c94215f4e818cf6d3796af1cdd1/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=vvKvFBL4OOiHjoLFlyplwcfdHxNoFgvUB_mZ4ZhbxSA" 

MENSAGEM_TEAMS_CABECALHO = "🚨 **ILPNs sem local, que ainda temos pendências em atraso crítico.**\n\nPeço, por favor, que verifiquem com o time e avancem nas tratativas das que ainda estão abertas. **Obrigado pelo apoio de todos!**"

# =================================================================
# 2. FUNÇÕES DE APOIO
# =================================================================
def obter_pior_atraso(df_grupo):
    atrasos = df_grupo['Tempo de atraso'].unique()
    if "Atrasado + de 10 dias" in atrasos: return "Atrasado + de 10 dias"
    if "Atraso de 6 a 10 dias" in atrasos: return "Atraso de 6 a 10 dias"
    if "Atraso de 2 a 5 dias" in atrasos: return "Atraso de 2 a 5 dias"
    return "Atraso Recente"

def limpar_nan(valor):
    """Garante que palavras como 'nan' ou células vazias virem um traço '-'"""
    if pd.isna(valor) or str(valor).strip().lower() in ['nan', 'nat', 'none', '']:
        return '-'
    return str(valor)

def formatar_tabela_html(df_grupo):
    estilo_tabela = """
    <style>
        table { border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 12px; }
        th { background-color: #004b87; color: white; text-align: left; padding: 8px; border: 1px solid #ddd; }
        td { padding: 8px; border: 1px solid #ddd; text-align: left; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .atraso-critico { color: red; font-weight: bold; }
    </style>
    """
    linhas_html = ""
    for _, row in df_grupo.iterrows():
        atraso = row['Tempo de atraso']
        if "6 a 10" in atraso or "+ de 10" in atraso:
            atraso = f"<span class='atraso-critico'>{atraso}</span>"
        
        ref1 = limpar_nan(row.get('Referencia 1'))
        ref2 = limpar_nan(row.get('Referencia 2'))
        
        linhas_html += f"<tr><td>{row['LPN']}</td><td>{row['Setor']}</td><td>{row['Atributo item']}</td><td>{row['Data ilpn´s']}</td><td>{atraso}</td><td>{ref1}</td><td>{ref2}</td></tr>"
        
    return f"{estilo_tabela}<table><thead><tr><th>LPN</th><th>Setor</th><th>Atributo Item</th><th>Data Atividade</th><th>Tempo de Atraso</th><th>Referência 1</th><th>Referência 2</th></tr></thead><tbody>{linhas_html}</tbody></table>"

def enviar_card_separado_teams(coordenador, gestor, setor, detalhes_lpns):
    """Dispara um card isolado no canal do Teams para o grupo atual."""
    if not WEBHOOK_TEAMS:
        return 
        
    texto_bloco_gestao = (
        "================================================\n\n"
        f"👔 **COORDENADOR:** {coordenador}\n\n"
        f"👤 **GESTOR:** {gestor}\n\n"
        f"🏢 **SETOR:** {setor}\n\n"
        "================================================"
    )

    mensagem = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {"type": "TextBlock", "text": MENSAGEM_TEAMS_CABECALHO, "wrap": True},
                        {"type": "TextBlock", "text": texto_bloco_gestao, "wrap": True, "weight": "Bolder", "color": "Accent"},
                        {"type": "TextBlock", "text": detalhes_lpns, "wrap": True}
                    ]
                }
            }
        ]
    }
    
    try:
        response = requests.post(WEBHOOK_TEAMS, json=mensagem)
        if response.status_code not in [200, 202]:
            print(f"⚠️ Erro ao enviar cartão para o Teams: {response.status_code}")
    except Exception as e:
        print(f"❌ Falha de conexão com o Teams: {e}")

# =================================================================
# 3. LÓGICA DE DISPARO (E-MAIL + TEAMS)
# =================================================================
def enviar_cobrancas():
    print("🕒 Lendo a planilha mastigada pelo Auditor e iniciando envios...")

    if not os.path.exists(PATH_PRONTO_ENVIO):
        print(f"❌ Erro: Planilha de envio não encontrada em: {PATH_PRONTO_ENVIO}")
        return

    df = pd.read_excel(PATH_PRONTO_ENVIO)
    if df.empty:
        print("⚠️ O relatório está vazio. Nenhuma cobrança a enviar.")
        return

    outlook = win32.Dispatch('outlook.application')
    
    grupos = df.groupby(['Usuário', 'Destinatários'])
    print(f"📦 Preparando {len(grupos)} blocos de mensagens distintos.")

    for (usuario_origem, destinatarios), df_grupo in grupos:
        try: # <--- ESCUDO: Se este envio falhar, ele pula para o próximo sem desligar o robô!
            
            qtd_pendencias = len(df_grupo)
            pior_atraso = obter_pior_atraso(df_grupo)
            fluxo_deste_bloco = str(df_grupo['Fluxo aplicado'].iloc[0])
            
            # =========================================================
            # O PULO DO GATO: AS INFORMAÇÕES JÁ VÊM PRONTAS DO AUDITOR!
            # =========================================================
            nome_coordenador = str(df_grupo['COORDENADOR'].iloc[0])
            nome_gestor = str(df_grupo['GESTOR'].iloc[0])
            nome_setor = str(df_grupo['SETOR_RH'].iloc[0])

            # =========================================================
            # PARTE 1: GERAÇÃO DO CARD DO TEAMS
            # =========================================================
            texto_lpns_teams = ""
            for _, row in df_grupo.iterrows():
                ref1 = limpar_nan(row.get('Referencia 1'))
                ref2 = limpar_nan(row.get('Referencia 2'))
                
                texto_lpns_teams += f"🔹 **DATA:** {row['Data ilpn´s']}\n\n"
                texto_lpns_teams += f"🔹 **USUÁRIO:** {row['Usuário']}\n\n"
                texto_lpns_teams += f"🔹 **ILPN:** {row['LPN']} | ⏳ **ATRASO:** {row['Tempo de atraso']}\n\n"
                texto_lpns_teams += f"🔹 **REF 1:** {ref1}\n\n"
                texto_lpns_teams += f"🔹 **REF 2:** {ref2}\n\n"
                texto_lpns_teams += "------------------------------------------------\n\n"
            
            # NOVO: Adiciona a menção visual ao Coordenador e Gestor no final do texto do card
            texto_lpns_teams += f"📌 **@{nome_coordenador}** (Coord.)\n\n📌 **@{nome_gestor}** (Gest.)\n\n"
                
            enviar_card_separado_teams(nome_coordenador, nome_gestor, nome_setor, texto_lpns_teams)

            # AMORTECEDOR: Espera 2 segundos antes de enviar para o próximo, para o Teams não achar que é Spam
            time.sleep(2)

            # =========================================================
            # PARTE 2: GERAÇÃO DO E-MAIL (OUTLOOK)
            # =========================================================
            lista_para = str(destinatarios).replace(',', ';')
            
            # FILTRO ANTI-ERRO: Limpa nomes soltos da lista de cópias para o Outlook não travar
            emails_validos = [
                usuario_origem,
                EMAIL_DEPARTAMENTO,
                *EMAILS_GESTORES
            ]

            emails_validos = [
                email.strip()
                for email in emails_validos
                if pd.notna(email) and '@' in str(email)
            ]

            lista_cc = ";".join(emails_validos)
  
            mail = outlook.CreateItem(0)

            """
            Desabilitado temporariamente
            o envio usando a caixa compartilhada 'controledeestoque1200' estava sendo registrado em 'itens enviados',
            po´rem os destinatários não recebiam as mensagens.
            Necessário validar permissões 'Send As' ou 'Send on Behalf' com o time de M365
            """   
            # mail.SentOnBehalfOfName = EMAIL_DEPARTAMENTO 

       
            mail.To = lista_para
            mail.CC = lista_cc

            # Validacao de destinatario
            if not mail.Recipients.ResolveAll():
                print(f"Destinatário inválido: {lista_para}")
                continue

            mail.Subject = f"🚨 Ação Requerida: ILPNs Pendentes ({pior_atraso}) | Setores: {nome_setor}"
            
            if "Especial" in fluxo_deste_bloco:
                texto_dinamico = f"Foram identificadas <b>{qtd_pendencias}</b> ILPN(s) com <b>{pior_atraso}</b> que requerem a vossa ação imediata."
            else:
                texto_dinamico = f"Foram identificadas <b>{qtd_pendencias}</b> ILPN(s) geradas pelo(a) colaborador(a) <b>{usuario_origem}</b> com <b>{pior_atraso}</b> que requerem a vossa ação imediata."

            corpo_html = f'<p style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">Olá,<br><br>{texto_dinamico}<br>Abaixo encontra-se a lista detalhada para análise e regularização sistémica:</p><br>'
            assinatura = '<br><br><p style="font-family: Arial, sans-serif; font-size: 12px; color: #777;"><i>Este é um e-mail automático gerado pela automação do Controle de Estoque CD 1200.</i><br>Por favor, não responda diretamente a esta mensagem sem manter os envolvidos em cópia.</p>'
            
            mail.HTMLBody = corpo_html + formatar_tabela_html(df_grupo) + assinatura

            print("=" * 100)
            print("TO: ", lista_para)
            print("CC: ", lista_cc)
            print("ASSUNTO", mail.Subject)
            print("=" * 100)
            
            if MODO_TESTE:
                mail.Save() 
            else:
                mail.Send()
                
            print(f"✔️ Enviado com sucesso para: {nome_setor} ({nome_gestor})")
            
        except Exception as erro:
            print(f"⚠️ Erro ao enviar para {nome_setor} ({nome_gestor}). Pulando para o próximo! Detalhe: {erro}")
            continue # O "continue" é a magia que faz ele ignorar o erro e ir para o próximo envio

    print(f"\n✅ CONCLUÍDO! Cartões e E-mails processados.")

if __name__ == "__main__":
    enviar_cobrancas()