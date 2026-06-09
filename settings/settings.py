

# Controle de Estoque -- Disparo de ILPNs voando via Email + Teams

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