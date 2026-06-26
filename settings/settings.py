

# Controle de Estoque -- Disparo de ILPNs voando via Email + Teams =======================================

SCHEDULE_DISPARO = ['08:55', '15:55', '20:55', '02:55']

MODO = False # False para disparar emails e True para testes
EMAIL_DEPARTAMENTO = "controleestoque1200@casasbahia.com.br"
EMAILS_GESTORES = [
    #"edinaide.silva@casasbahia.com.br",
    "vinicius.barbosa@casasbahia.com.br",
    #"edvaldo.fiqueredo@casasbahia.com.br"
]

WEBHOOK_TEAMS = (
    "https://default5a86b3fb421349cdb4d6be91482ad3.c0.environment.api.powerplatform.com:443/"
    "powerautomate/automations/direct/workflows/3e265c94215f4e818cf6d3796af1cdd1/triggers/manual/"
    "paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig="
    "vvKvFBL4OOiHjoLFlyplwcfdHxNoFgvUB_mZ4ZhbxSA"
)

MENSAGEM_TEAMS_CABECALHO = (
    "🚨 **ILPNs sem local, que ainda temos pendências em atraso crítico.**\n\n"
    "Peço, por favor, que verifiquem com o time e avancem nas tratativas das que ainda estão abertas. "
    "**Obrigado pelo apoio de todos!**"
)
# =======================================================================================================


# Tratativa de Nota Fiscal Pendente =====================================================================

FILIAIS_CD = {
    '14', '125', '1200', '1400', '1401', '1445', '1475',
    '1500', '1522', '1600', '1624', '1635', '1640',
    '1668', '1673', '1736', '1760', '1792', '1850',
    '1875', '1876', '1877', '1882', '1887', '1888',
    '1895', '1999', '2241', '2600', '3600', '3601',
    '3602', '1454', '1778'
}

async def get_type_filial(filial: str) -> str:
    return "CD" if filial in FILIAIS_CD else "LOJA"

DELIMITADOR_TXT_MANAGER = ";"

# ======================================================================================================