import pandas as pd
import os
from datetime import datetime

# =================================================================
# 1. CONFIGURAÇÕES FÁCEIS E CAMINHOS
# =================================================================

# --- CAMINHOS DOS ARQUIVOS ---
PATH_FOTO_HOJE = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\ILPNs_pendentes.xlsx"
PATH_COLABORADORES = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\War Room\Coordenador + Colaborador\Base colaborador + Gestão Nova.xlsx"

# --- CAMINHOS DOS NOVOS ARQUIVOS QUE ESTE SCRIPT VAI CRIAR ---
PATH_HISTORICO_PBI = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\Base_Indicadores_Historico.xlsx"
PATH_PRONTO_ENVIO = r"C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\SOLICITAÇÕES DE AJUSTES CD 1200 - BASE INDICADORES\ILPNs pendentes\ILPNs_pendentes_pronta_para_envio.xlsx"

# =================================================================
# 2. FUNÇÕES DE APOIO (RH E LIMPEZA)
# =================================================================
def normalizar_email(email):
    if pd.isna(email): return ""
    return str(email).strip().lower().replace('@casasbahia.com.br', '@viavarejo.com.br')

def carregar_bases_rh():
    """Lê a base de RH com a blindagem ativada contra linhas vazias."""
    dict_email, dict_nome = {}, {}
    try:
        df_colab = pd.read_excel(PATH_COLABORADORES)
        
        if 'EMAIL | MATRICULA' in df_colab.columns:
            df_colab['CHAVE_BUSCA'] = df_colab['EMAIL | MATRICULA'].apply(normalizar_email)
            df_email = df_colab[df_colab['CHAVE_BUSCA'] != ""].drop_duplicates(subset=['CHAVE_BUSCA'], keep='first')
            dict_email = df_email.set_index('CHAVE_BUSCA').to_dict('index')
            
        col_nome = next((c for c in df_colab.columns if 'NOME' in str(c).upper()), None)
        if col_nome:
            df_colab['NOME_BUSCA'] = df_colab[col_nome].astype(str).str.strip().str.upper()
            df_nome = df_colab[(df_colab['NOME_BUSCA'] != "") & (df_colab['NOME_BUSCA'] != "NAN")].drop_duplicates(subset=['NOME_BUSCA'], keep='first')
            dict_nome = df_nome.set_index('NOME_BUSCA').to_dict('index')
            
        return dict_email, dict_nome
    except Exception as e:
        print(f"⚠️ Aviso: Falha ao carregar a base de colaboradores. Erro: {e}")
        return {}, {}

def buscar_dados_rh(alvo, dict_email, dict_nome):
    """Procura o 'alvo' na base de RH."""
    alvo_str = str(alvo).strip()
    if '@' in alvo_str:
        return dict_email.get(normalizar_email(alvo_str), {})
    return dict_nome.get(alvo_str.upper(), {})

# =================================================================
# 3. O CÉREBRO DA OPERAÇÃO (GERADOR DE INDICADORES)
# =================================================================
def processar_indicadores():
    print("\n" + "="*50)
    print("🧠 INICIANDO O AUDITOR DE INDICADORES E RH")
    print("="*50)

    # 1. VERIFICA SE EXISTEM DADOS DE HOJE
    if not os.path.exists(PATH_FOTO_HOJE):
        print(f"❌ Erro: Relatório de hoje não encontrado em: {PATH_FOTO_HOJE}")
        return

    df_hoje = pd.read_excel(PATH_FOTO_HOJE)
    if df_hoje.empty:
        print("⚠️ A extração de hoje está vazia. Processando resoluções de pendências anteriores...")
    else:
        df_hoje['LPN'] = df_hoje['LPN'].astype(str).str.strip()

    # 2. FASE A: ENRIQUECIMENTO COM DADOS DO RH
    print("🔍 Consultando a Base de Colaboradores do RH...")
    dict_email, dict_nome = carregar_bases_rh()
    
    coordenadores, gestores, setores_rh = [], [], []

    if not df_hoje.empty:
        for index, row in df_hoje.iterrows():
            fluxo = str(row.get('Fluxo aplicado', ''))
            destinatarios = str(row.get('Destinatários', ''))
            usuario = str(row.get('Usuário', ''))
            setor_original = str(row.get('Setor', ''))

            # Lógica Especial vs Normal
            if "Especial" in fluxo:
                alvo = destinatarios.split(',')[0].strip()
            else:
                alvo = usuario.strip()
                
            dados_rh = buscar_dados_rh(alvo, dict_email, dict_nome)
            
            # Preenche as listas com o que achou no RH
            coordenadores.append(dados_rh.get('COORDENADOR', 'Não Localizado'))
            gestores.append(dados_rh.get('GESTOR', 'Não Localizado'))
            setores_rh.append(dados_rh.get('SETOR', setor_original))

        # Adiciona as colunas novas na Foto de Hoje
        df_hoje['COORDENADOR'] = coordenadores
        df_hoje['GESTOR'] = gestores
        df_hoje['SETOR_RH'] = setores_rh

    # Salva o arquivo pronto para o Carteiro (Script 3)
    df_hoje.to_excel(PATH_PRONTO_ENVIO, index=False)
    print(f"✅ Arquivo para envio mastigado gerado: COBRANCA_PRONTA_PARA_ENVIO.xlsx")

    # =========================================================
    # 3. FASE B: ATUALIZAÇÃO DO HISTÓRICO PARA O POWER BI
    # =========================================================
    print("📊 Atualizando a Base de Indicadores (Histórico)...")
    data_hoje_str = datetime.now().strftime("%d/%m/%Y")
    hora_agora_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    colunas_historico = [
        "DATA_FOTO", "ILPN", "STATUS_SISTEMA", "DATA_CRIACAO_ILPN", 
        "DATA_HORA_RESOLUCAO", "FAIXA_DE_ATRASO", "USUARIO_CRIADOR", 
        "REFERENCIA_1", "REFERENCIA_2", "PALAVRA_CHAVE", 
        "SETOR_RESPONSAVEL", "GESTOR", "COORDENADOR"
    ]

    # Verifica se o Histórico existe. Se não existir, cria do zero.
    if not os.path.exists(PATH_HISTORICO_PBI):
        print("⚠️ Arquivo de Histórico não encontrado. Criando base 'Dia Zero'...")
        df_historico = pd.DataFrame(columns=colunas_historico)
    else:
        df_historico = pd.read_excel(PATH_HISTORICO_PBI)
        
    # BLINDAGEM: Força a tabela inteira a aceitar texto (object) para evitar o erro float64
    df_historico = df_historico.astype(object)
    
    if not df_historico.empty:
        df_historico['ILPN'] = df_historico['ILPN'].astype(str).str.strip()

    novas_linhas = []
    lista_lpns_hoje = df_hoje['LPN'].tolist() if not df_hoje.empty else []

    # PASSO B1: Procurar quem foi RESOLVIDO
    resolvidas = 0
    if not df_historico.empty:
        for index, row in df_historico.iterrows():
            if row['STATUS_SISTEMA'] == 'Pendente':
                # Se estava pendente e não está mais na lista de hoje = Resolvido!
                if row['ILPN'] not in lista_lpns_hoje:
                    df_historico.at[index, 'STATUS_SISTEMA'] = 'Resolvido'
                    df_historico.at[index, 'DATA_HORA_RESOLUCAO'] = hora_agora_str
                    resolvidas += 1
    
    # PASSO B2: Adicionar NOVOS e atualizar ENVELHECIDOS
    novas = 0
    atualizadas = 0
    
    if not df_hoje.empty:
        for index, row in df_hoje.iterrows():
            ilpn_atual = row['LPN']
            
            # Verifica se essa ILPN já está no Histórico
            mascara_existente = df_historico['ILPN'] == ilpn_atual
            
            if not df_historico.empty and mascara_existente.any():
                # Envelhecido: Já existe, então só atualiza a FAIXA_DE_ATRASO
                idx_hist = df_historico.index[mascara_existente][0]
                df_historico.at[idx_hist, 'FAIXA_DE_ATRASO'] = row.get('Tempo de atraso', '')
                df_historico.at[idx_hist, 'STATUS_SISTEMA'] = 'Pendente' # Garante q continua pendente
                atualizadas += 1
            else:
                # Novo: Cria uma linha nova para o Histórico
                nova_linha = {
                    "DATA_FOTO": data_hoje_str,
                    "ILPN": ilpn_atual,
                    "STATUS_SISTEMA": "Pendente",
                    "DATA_CRIACAO_ILPN": row.get('Data ilpn´s', ''),
                    "DATA_HORA_RESOLUCAO": "",
                    "FAIXA_DE_ATRASO": row.get('Tempo de atraso', ''),
                    "USUARIO_CRIADOR": row.get('Usuário', ''),
                    "REFERENCIA_1": row.get('Referencia 1', ''),
                    "REFERENCIA_2": row.get('Referencia 2', ''),
                    "PALAVRA_CHAVE": str(row.get('Destinatários', '')).split(',')[0], # O focal point
                    "SETOR_RESPONSAVEL": row.get('SETOR_RH', ''),
                    "GESTOR": row.get('GESTOR', ''),
                    "COORDENADOR": row.get('COORDENADOR', '')
                }
                novas_linhas.append(nova_linha)
                novas += 1

    # Anexa as novas linhas no final do Histórico
    if novas_linhas:
        df_historico = pd.concat([df_historico, pd.DataFrame(novas_linhas)], ignore_index=True)

    # Guarda o Histórico no Excel
    df_historico.to_excel(PATH_HISTORICO_PBI, index=False)
    print(f"✅ Histórico do Power BI atualizado com sucesso!")
    
    print("\n📊 --- RESUMO DA OPERAÇÃO DE HOJE ---")
    print(f"🔹 ILPNs Resolvidas pelo time (D-1): {resolvidas}")
    print(f"🔹 ILPNs Novas mapeadas: {novas}")
    print(f"🔹 ILPNs Envelhecidas (Continuam pendentes): {atualizadas}")
    print("==================================================")

if __name__ == "__main__":
    processar_indicadores()