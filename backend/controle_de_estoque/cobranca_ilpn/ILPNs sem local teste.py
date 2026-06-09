import pandas as pd
from datetime import datetime
import os
import re
import sys

# Importa as regras do arquivo Regras.py que deve estar na mesma pasta
try:
    from Regras import REGRAS_PIX_BASE
except ImportError:
    print("❌ ERRO CRÍTICO: Não foi possível encontrar o arquivo 'Regras.py'.")
    print("Certifique-se de que 'Regras.py' está na mesma pasta que este script.")
    sys.exit()

# =================================================================
# 1. CONFIGURAÇÃO DE CAMINHOS
# =================================================================
PATH_ILPNS   = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\War Room\7.03 - iLPNs Sem Local\7.03 - iLPNs Sem Local.csv"
PATH_COLAB   = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\War Room\Coordenador + Colaborador\Base colaborador + Gestão Nova.xlsx"
PATH_PIX     = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\War Room\9.05 - Relatório PIX\9.05 - Relatório PIX.csv"

PATH_SAIDA   = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\ILPNs_pendentes.xlsx"
PATH_LOG     = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\log_execucao.csv"

if not os.path.exists(r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes"):
    os.makedirs(r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes")

# =================================================================
# 2. FUNÇÕES DE APOIO
# =================================================================
def ler_csv_inteligente(caminho):
    for enc in ['utf-16', 'iso-8859-1', 'utf-8-sig', 'cp1252']:
        try:
            return pd.read_csv(caminho, sep=None, engine='python', encoding=enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise Exception(f"Erro ao ler {caminho}.")

def definir_etiqueta_atraso(dias):
    if 2 <= dias <= 5: return "Atraso de 2 a 5 dias"
    if 6 <= dias <= 10: return "Atraso de 6 a 10 dias"
    if dias > 10: return "Atrasado + de 10 dias"
    return "Recente"

def normalizar_email(email):
    if pd.isna(email): return ""
    return str(email).strip().lower().replace('@casasbahia.com.br', '@viavarejo.com.br')

def limpar_texto(texto):
    if pd.isna(texto): return ""
    return re.sub(r'\s+', ' ', str(texto).strip().upper())

def verificar_correspondencia_area(palavra_chave, ref_pix):
    if palavra_chave in ref_pix: return True
    if ' ' not in palavra_chave:
        if re.search(rf'\b{palavra_chave}\b', ref_pix):
            return True
    return False

def determinar_destinatario_linha(row):
    """Calcula o gestor e fluxo para UMA linha específica."""
    usuario_norm = normalizar_email(row['Activity Tracking User ID'])
    ref2_limpa = limpar_texto(row['Referencia 2'])
    
    gestor_padrao = str(row['GESTOR'])
    coord_padrao = str(row['COORDENADOR'])
    
    # --- LÓGICA DE REGRA ESPECIAL (Importada de Regras.py) ---
    gestor_alvo = None
    if usuario_norm in REGRAS_PIX_BASE:
        regras_usuario = REGRAS_PIX_BASE[usuario_norm]
        
        for gestor_nome, lista_palavras in regras_usuario.items():
            for palavra in lista_palavras:
                if verificar_correspondencia_area(palavra, ref2_limpa):
                    gestor_alvo = gestor_nome
                    break
            if gestor_alvo: break
    
    if gestor_alvo:
        fluxo = "Especial (PIX)"
        chave_agrupamento = gestor_alvo
        dest_principal = gestor_alvo 
        
        # NOVA LÓGICA SIMPLIFICADA:
        # Envia para TODOS os envolvidos, independente se é 2, 5 ou 10 dias.
        dests = [dest_principal, coord_padrao, "controledeestoquecd1200@viavarejo.com.br"]
        
    else:
        fluxo = "Normal"
        chave_agrupamento = gestor_padrao
        
        # NOVA LÓGICA SIMPLIFICADA:
        # Envia para a cadeia completa sempre.
        dests = [row['Activity Tracking User ID'], gestor_padrao, coord_padrao]

    return chave_agrupamento, dests, fluxo

# =================================================================
# 3. LÓGICA PRINCIPAL (RAIO-X LINHA A LINHA)
# =================================================================
def processar_automacao():
    print("🕒 A iniciar processamento com REGRAS EXTERNAS e ENVIO COMPLETO...")

    try:
        # Carregar
        df_ilpns = ler_csv_inteligente(PATH_ILPNS)
        df_pix   = ler_csv_inteligente(PATH_PIX)
        df_colab = pd.read_excel(PATH_COLAB)
        
        print("✅ Bases carregadas.")

        # Limpeza e Processamento
        df_pix = df_pix.drop_duplicates(subset=['LPN ID'], keep='last')
        df_ilpns['Data_Convertida'] = pd.to_datetime(df_ilpns['Data da Atividade'], errors='coerce')
        hoje = pd.to_datetime('today').normalize()
        df_ilpns['Dias_Aberto'] = (hoje - df_ilpns['Data_Convertida'].dt.normalize()).dt.days
        
        # Filtros
        df_validos = df_ilpns[df_ilpns['Activity Tracking User ID'].notna()].copy()
        contagem_total_por_usuario = df_validos['Activity Tracking User ID'].value_counts().to_dict()
        
        # ===================================================================
        # AQUI ESTAVA O SEGREDO! Mudei de > 2 para >= 2 
        # ===================================================================
        df_atrasados = df_validos[df_validos['Dias_Aberto'] >= 2].copy()
        
        # ===================================================================
        # O PULO DO GATO: CRIAR EXCEL VAZIO SE FOR UM "DIA PERFEITO"
        # ===================================================================
        if df_atrasados.empty:
            print("⚠️ Nenhuma pendência igual ou superior a 2 dias. Criando base de 'Dia Perfeito'...")
            
            # Cria um ficheiro apenas com os cabeçalhos para o Auditor poder ler
            colunas_ordem = [
                "Data ilpn´s", "Usuário", "Quantidade ILPNs", "Ilpn´s em atraso",
                "Tempo de atraso", "Fluxo aplicado", "Referencia 1", "Referencia 2", "Destinatários", 
                "LPN", "Setor", "Atributo item", "Inventory type"
            ]
            df_vazio = pd.DataFrame(columns=colunas_ordem)
            df_vazio.to_excel(PATH_SAIDA, index=False)
            print(f"📂 Base vazia guardada em: {PATH_SAIDA}")
            return
        # ===================================================================

        # Merges
        df_atrasados = df_atrasados.merge(
            df_colab, left_on='Activity Tracking User ID', right_on='EMAIL | MATRICULA', how='left'
        )
        df_atrasados = df_atrasados.merge(
            df_pix[['LPN ID', 'Referencia 2', 'Referencia 1']], left_on='LPN', right_on='LPN ID', how='left'
        )

        # Preenchimento
        df_atrasados['Setor'] = df_atrasados['Setor'].fillna("SEM SETOR")
        df_atrasados['Atributo Item'] = df_atrasados['Atributo Item'].fillna("-")
        df_atrasados['Data_Formatada'] = df_atrasados['Data_Convertida'].dt.strftime('%d/%m/%Y')

        # 1. Calcular Destinatário LINHA A LINHA
        print("⚙️ Aplicando regras e definindo destinatários...")
        temp_data = []
        for idx, row in df_atrasados.iterrows():
            chave_gestor, lista_emails, nome_fluxo = determinar_destinatario_linha(row)
            
            # Limpeza de lista de emails
            emails_limpos = [str(d).strip() for d in lista_emails if str(d).lower() not in ['nan', 'none', '']]
            # Remove duplicatas mantendo a ordem (caso o gestor e coordenador sejam a mesma pessoa)
            emails_unicos = list(dict.fromkeys(emails_limpos))
            emails_str = ", ".join(emails_unicos)
            
            etiqueta = definir_etiqueta_atraso(row['Dias_Aberto'])
            
            temp_data.append({
                'Index': idx,
                'Chave_Gestor': chave_gestor,
                'Destinatarios_Final': emails_str,
                'Fluxo_Final': nome_fluxo,
                'Etiqueta_Final': etiqueta
            })
            
        df_rotas = pd.DataFrame(temp_data)
        df_atrasados = df_atrasados.merge(df_rotas, left_index=True, right_on='Index')

        # 2. Contagem do Grupo
        grupo_cols = ['Activity Tracking User ID', 'Chave_Gestor', 'Setor']
        df_contagem_grupo = df_atrasados.groupby(grupo_cols).size().reset_index(name='Contagem_Grupo')
        df_atrasados = df_atrasados.merge(df_contagem_grupo, on=grupo_cols, how='left')

        # 3. Gerar Excel Detalhado
        print("📦 Gerando arquivo final...")
        analise_final = []
        
        for _, row in df_atrasados.iterrows():
            usuario = row['Activity Tracking User ID']
            analise_final.append({
                "Data ilpn´s": row['Data_Formatada'],
                "Usuário": usuario,
                "Quantidade ILPNs": contagem_total_por_usuario.get(usuario, 0),
                "Ilpn´s em atraso": row['Contagem_Grupo'],
                "Tempo de atraso": row['Etiqueta_Final'], 
                "Fluxo aplicado": row['Fluxo_Final'],
                "Referencia 1": str(row['Referencia 1']) if pd.notna(row['Referencia 1']) else "",
                "Referencia 2": str(row['Referencia 2']) if pd.notna(row['Referencia 2']) else "",
                "Destinatários": row['Destinatarios_Final'],
                "LPN": str(row['LPN']),
                "Setor": str(row['Setor']),
                "Atributo item": str(row['Atributo Item']),
                "Inventory type": str(row['Inventory Type ID']) if pd.notna(row['Inventory Type ID']) else ""
            })

        if analise_final:
            colunas_ordem = [
                "Data ilpn´s", "Usuário", "Quantidade ILPNs", "Ilpn´s em atraso",
                "Tempo de atraso", "Fluxo aplicado", "Referencia 1", "Referencia 2", "Destinatários", 
                "LPN", "Setor", "Atributo item", "Inventory type"
            ]
            
            df_final = pd.DataFrame(analise_final)
            df_final = df_final[colunas_ordem]
            df_final = df_final.sort_values(by=['Usuário', 'Setor', 'Tempo de atraso'], ascending=[True, True, False])
            
            df_final.to_excel(PATH_SAIDA, index=False)
            
            # Log Simplificado
            resumo_log = pd.DataFrame(analise_final).groupby('Usuário')['Ilpn´s em atraso'].max().reset_index()
            resumo_log['Data'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            resumo_log['Faixa'] = "Detalhado"
            resumo_log['Email'] = "Preview"
            resumo_log['Teams'] = "Preview"
            resumo_log = resumo_log.rename(columns={'Ilpn´s em atraso': 'Qtd_Cobranca'})
            
            modo_abertura = 'a' if os.path.exists(PATH_LOG) else 'w'
            resumo_log[['Data','Usuário','Qtd_Cobranca','Faixa','Email','Teams']].to_csv(
                PATH_LOG, index=False, mode=modo_abertura, header=not os.path.exists(PATH_LOG)
            )
            
            print(f"\n✅ Concluído! Relatório gerado (Lógica: Envio para todos os responsáveis).")
            print(f"📂 Verifique: {PATH_SAIDA}")
        
    except Exception as e:
        print(f"❌ Erro técnico: {e}")

if __name__ == "__main__":
    processar_automacao()