import subprocess
import time
from datetime import datetime
import sys
import os

# =================================================================
# 1. PAINEL DE CONTROLE (A GRADE DE HORÁRIOS)
# =================================================================

# ⏱️ GRADE DE PREPARAÇÃO: Digite os horários exatos em que a fábrica deve "ligar os motores".
# DICA: Coloque sempre 5 minutos antes da hora cheia em que o e-mail deve cair.
HORARIOS_DE_PREPARACAO = ["08:55", "15:55", "20:55", "02:55"]

# 🐍 CAMINHO DO PYTHON: O "motor" do seu ambiente virtual (.venv)
PYTHON_EXE = r"C:\Users\2960006959\Desktop\project\RPA Gestao de CD\.venv\Scripts\python.exe"

# 📜 CAMINHOS DOS SCRIPTS: A "Linha de Montagem" na ordem exata
SCRIPT_FISCAL   = r"C:\Users\2960006959\Desktop\project\RPA Gestao de CD\projetos_passados\Cobranças war room\ILPNs sem local teste.py"
SCRIPT_AUDITOR  = r"C:\Users\2960006959\Desktop\project\RPA Gestao de CD\projetos_passados\Cobranças war room\Gerador_Indicadores.py"
SCRIPT_CARTEIRO = r"C:\Users\2960006959\Desktop\project\RPA Gestao de CD\projetos_passados\Cobranças war room\Disparo_Cobranca_Construção.py"

print("=" * 50)
print("VALIDAÇÃO DE CAMINHOS")
print("=" * 50)

print("Python:", os.path.exists(PYTHON_EXE))
print("Fiscal:", os.path.exists(SCRIPT_FISCAL))
print("Auditor:", os.path.exists(SCRIPT_AUDITOR))
print("Carteiro:", os.path.exists(SCRIPT_CARTEIRO))
print("=" * 50)

# =================================================================
# 2. AMBIENTE DE TRADUÇÃO (UTF-8)
# =================================================================
# Força todos os scripts filhos a falarem e entenderem emojis e acentos ("ç", "ã", etc.)
meu_ambiente = os.environ.copy()
meu_ambiente["PYTHONIOENCODING"] = "utf-8"

# =================================================================
# 3. FUNÇÕES DA FÁBRICA
# =================================================================
def rodar_script(nome_etapa, caminho_script):
    """Executa o script de forma invisível e mostra eventuais erros"""
    print(f"▶️ [{datetime.now().strftime('%H:%M:%S')}] Iniciando: {nome_etapa}")
    try:
        # Blindagem dupla: Ambiente forçado em UTF-8 e ignorando letras defeituosas do Windows
        resultado = subprocess.run(
            [PYTHON_EXE, caminho_script], 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='replace', 
            env=meu_ambiente
        )
        print(resultado.stdout)
        if resultado.stderr:
            print(f"⚠️ Alerta na etapa {nome_etapa}:\n{resultado.stderr}")
    except Exception as e:
        print(f"❌ Erro crítico ao abrir {nome_etapa}: {e}")

def iniciar_ciclo_de_cobranca():
    """Roda a extração, espera a hora cheia, e faz o disparo"""
    print(f"\n{'='*60}")
    print(f"🚀 INICIANDO PREPARAÇÃO DA COBRANÇA | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}")

    # --- FASE 1: PREPARAÇÃO (Minuto 55) ---
    rodar_script("1. FISCAL (Extração de Dados)", SCRIPT_FISCAL)
    rodar_script("2. AUDITOR (Cruzamento com RH)", SCRIPT_AUDITOR)
    
    # --- FASE 2: A PAUSA TÁTICA ---
    # O robô vai travar aqui e olhar para o relógio até o minuto virar "00" (Hora cheia)
    print("\n⏳ DADOS PRONTOS! Iniciando a Pausa Tática...")
    print("Aguardando o relógio bater na hora cheia (00 minutos) para disparar...")
    
    while datetime.now().minute != 0:
        time.sleep(1) # Checa o relógio a cada 1 segundo
        
    # --- FASE 3: DISPARO SINCRONIZADO (Minuto 00 em ponto) ---
    print(f"\n⏰ HORA CHEIA ATINGIDA! ({datetime.now().strftime('%H:%M:%S')}) - Liberando os envios!")
    rodar_script("3. CARTEIRO (Disparo de Outlook e Teams)", SCRIPT_CARTEIRO)

    print(f"\n✅ CICLO CONCLUÍDO COM SUCESSO!")
    print(f"{'='*60}\n")

# =================================================================
# 4. O RADAR 24 HORAS (LOOP INFINITO)
# =================================================================
if __name__ == "__main__":
    print("🤖 ORQUESTRADOR ATIVADO E MONITORANDO O RELÓGIO!")
    print(f"📋 Horários programados para iniciar preparação: {HORARIOS_DE_PREPARACAO}")
    print("Pode minimizar esta tela. A automação está a rodar em segundo plano...\n")
    
    while True:
        hora_atual = datetime.now().strftime("%H:%M")
        
        # Se o relógio do Windows bater exatamente com algum horário da nossa grade
        if hora_atual in HORARIOS_DE_PREPARACAO:
            iniciar_ciclo_de_cobranca()
            
            # Depois que terminar (já vai ser hora cheia, tipo 09:00), dorme por 60 segundos
            # Isso evita que ele tente rodar o script duplicado no mesmo minuto
            time.sleep(60) 
            
        else:
            # Se não for a hora, dorme por 30 segundos para não gastar a memória/CPU do computador
            time.sleep(30)