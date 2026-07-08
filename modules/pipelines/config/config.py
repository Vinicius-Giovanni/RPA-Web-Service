PIPELINE_CONFIG = {
        'pendencia_asn' :{
        'remove_columns': [
            'Filial destino',
            'Tipo ASN',
            'Companhia',
            'Inventory Type',
            'Status'
        ],
        'rename_columns': {
            'ASN':'asn',
            'Descrição':'descricao',
            'Filial origem':'filial_origem',
            'Descrição recebimento':'desc_recebimento',
            'Nota Fiscal':'nota_fiscal',
            'Data integração WMS':'data_integracao_wms',
            'Data inicio recebimento':'data_inicio_recebimento',
            'Item':'item',
            'Descrição item':'desc_item',
            'Setor':'setor',
            'Status do produto':'status_produto',
            'Qtde original':'qtd_original',
            'Qtde recebida':'qtd_recebida'
        },
        'column_types': {
            'asn':'Int64',
            'descricao':'string',
            'filial_origem':'string',
            'desc_recebimento':'string',
            'nota_fiscal':'string',
            'item':'Int64',
            'desc_item':'string',
            'setor':'string',
            'status_produto':'string',
            'qtd_original':'Int64',
            'qtd_recebida':'Int64'
        },
        'datetime_columns': [
            'data_integracao_wms',
            'data_inicio_recebimento'
        ],
        'encoding':'utf-16',
        'sep':'\t'
        },
        'bottleneck_salao': {
        'read_columns_packed': [
            'olpn',
            'data_hora_fim_olpn'
        ],
        'read_columns_putaway': [
            'olpn',
            'data_hora_putaway'
        ],
        'datetime_columns': [
            'data_hora_fim_olpn',
            'data_hora_putaway'
        ],
        'column_type': {
            'olpn': 'string'
        }
    },
        'bottleneck_box': {
        'read_columns_load': [
                'olpn',
                'data_hora_load'
                ],
        'read_columns_putaway': [
                'olpn',
                'data_hora_putaway'
                ],
        'datetime_columns': [
            'data_hora_putaway',
            'data_hora_load'
        ],
        'column_type': {
            'olpn': 'string'
        }

    },
        'time_lead_olpn': {
        'read_columns': [
            'olpn',
            'data_hora_load',
            'data_pedido'
        ],
        'datetime_columns': [
            'data_hora_load',
            'data_pedido'
        ],
        'column_types': {
            'olpn': 'string'
        },
    },
        'expedicoes':{
        'remove_columns': [
                'data_integração_wms',
                'inventory_type_id',
                'wave',
                'pedido_de_venda',
                'bandeira',
                'status_do_pedido',
                'destinatário',
                'cep_destinatário',
                'cidade',
                'estado',
                'item',
                'descrição_do_item',
                'código_do_setor',
                'empresa',
                'status_da_nota_fiscal',
                'shipment',
                'marcação_de_ead',
                'ship_via',
                'descrição',
                'uf',
                'data_prometida',
                'data_prevista_entrega',
                'data_limite_expedição'
        ],
        'rename_columns': {
                'data_ultima_movimentação':'dt_ultima_movimentacao',
                'filial':'filial',
                'pedido':'pedido',
                'box':'box',
                'tipo_do_pedido':'tipo_de_pedido',
                'descrição':'descricao',
                'setor_do_item':'setor_item',
                'status':'status',
                'qtde._original':'qtd_pcs_solicitada',
                'qtde._expedida':'qtd_pcs_expedida'
        },
        'column_types': {
            'filial':'string',
            'pedido':'string',
            'box':'Int64',
            'tipo_de_pedido':'string',
            'descricao':'string',
            'setor_item':'string',
            'status':'string',
            'qtd_pcs_solicitada':'Int64',
            'qtd_pcs_expedida':'Int64'
        },
        'datetime_columns': [
            'dt_ultima_movimentacao'
        ],
        'encoding':'utf-16',
        'sep':'\t'
        },
        'olpn': {
        'remove_columns': [
                'cod_setor_item',
                'inventory_type_id',
                'data_limite_expedição',
                'data_prevista_entrega',
                'marcação_de_ead',
                'numero_da_gaiola',
                'tarefa_status',
                'data_do_pedido',
                'shipment',
                'filial_destino',
                'status_pedido',
                'wave',
                'descrição'
        ],
        'rename_columns': {
                'filial': 'filial',
                'status_olpn': 'status_olpn',
                'data_locação_pedido': 'data_locacao_pedido',
                'audit_status': 'audit_status',
                'último_update_olpn': 'data_hora_ultimo_update_olpn',
                'tote': 'tote',
                'tarefa': 'tarefa',
                'grupo_de_tarefa': 'grupo_de_tarefa',
                'item': 'item',
                'local_de_picking': 'local_de_picking',
                'qtde._peças_item': 'qt_pecas',
                'volume': 'volume',
                'box': 'box',
                'desc_setor_item': 'desc_setor_item',
                'tipo_de_pedido': 'tipo_de_pedido',
                'pedido': 'pedido',
                'olpn': 'olpn'
        },
        'column_types': {
                'status_olpn': 'string',
                'audit_status': 'string',
                'tote': 'string',
                'tarefa': 'string',
                'grupo_de_tarefa': 'string',
                'item': 'Int64',
                'descricao': 'string',
                'local_de_picking': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'pedido': 'string',
                'olpn': 'string'
        },
        'datetime_columns':  [
                'data_locacao_pedido',
                'data_hora_ultimo_update_olpn'
        ],
        'encoding': 'utf-16',
        'sep' : '\t'
    },
        'picking': {
        'remove_columns': [
                'status_tarefa',
                'tipo_de_transação',
                'qtde_alocada',
                'task_moviment',
                'pull_location_for_task_detail',
                'destination_location_for_task_detail',
                'wave',
                'nome',
                'data_da_tarefa_(create)',
                'data_e_hora_da_assinatura_da_tarefa',
                'descrição',
                'local_destino',
                'inventory_type',
                'status_detalhe_da_tarefa'
        ],
        'rename_columns': {
                'filial':'filial',
                'tarefa':'tarefa',
                'qtde_requerida':'qt_requerida',
                'qtde_separada':'qt_separada',
                'usuário':'usuario',
                'data_do_inicio_da_tarefa':'data_hora_inicio_tarefa',
                'data_de_finalização_da_tarefa':'data_hora_fim_tarefa',
                'data_de_finalização_da_olpn':'data_hora_fim_olpn',
                'order_id':'pedido',
                'olpn':'olpn',
                'item':'item',
                'setor':'desc_setor_item',
                'tipo_de_pedido':'tipo_de_pedido',
                'local_de_coleta':'local_de_picking',
                'box':'box'
        },
        'column_types': {
                'tarefa': 'string',
                'qt_requerida': 'Int64',
                'qt_separada': 'Int64',
                'usuario': 'string',
                'pedido': 'Int64',
                'olpn': 'string',
                'item': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'local_de_picking': 'string',
                'box': 'Int64'
                        },
        'datetime_columns':  [
                'data_hora_inicio_tarefa',
                'data_hora_fim_tarefa',
                'data_hora_fim_olpn'
        ],
        'encoding': 'utf-16',
        'sep' : '\t'
    },
        'cancel' : {
        'remove_columns': [
                'inventory_type_id',
                'pedido_de_venda',
                'carga',
                'destinatário',
                'descrição_do_item',
                'qtde_original',
                'qtde_expedida',
                'data_integração_wms',
                'código_reference_text'
        ],
        'rename_columns': {
                'filial':'filial',
                'pedido': 'pedido',
                'tipo_da_ordem': 'tipo_de_pedido',
                'qtde_ajustada': 'qt_pecas',
                'data_do_cancelamento': 'data_cancelamento',
                'usuário': 'usuario',
                'motivo_secondary_reference_text': 'motivo_cancelamento'
        },
        'column_types': {
                'pedido': 'string',
                'tipo_de_pedido': 'string',
                'qt_pecas': 'Int64',
                'usuario': 'string',
                'motivo_cancelamento': 'string',
                'item': 'Int64'
        },
        'datetime_columns': [
                'data_cancelamento'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'packing' : {
        'remove_columns': [
                'inventory_type_id',
                'pallet',
                'descrição_item',
                'data_pedido',
                'nome_do_usuário',
                'shipment',
                'pedido_venda',
                'nota_fiscal',
                'embala',
                'facility_id',
                'tipo_de_pedido',
                'data_load',
                'pedido_de_venda',
                'descrição_do_item'
        ],
        'rename_columns': {
                'filial':'filial',
                'olpn':'olpn',
                'pedido':'pedido',
                'item':'item',
                'setor':'desc_setor_item',
                'tipo_pedido':'tipo_de_pedido',
                'data_packed':'data_hora_packed',
                'usuário':'usuario',
                'quantidade':'qt_pecas',
                'box':'box'
        },
        'column_types': {
                'olpn': 'string',
                'pedido': 'string',
                'item': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'usuario': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64'
        },
        'datetime_columns': [
                'data_hora_packed'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'loading' : {
        'remove_columns': [
                'facility_id',
                'inventory_type_id',
                'nome_do_usuário',
                'shipment',
                'pedido_de_venda',
                'nota_fiscal',
                'descrição_do_item'
        ],
        'rename_columns': {
                'olpn':'olpn',
                'pedido':'pedido',
                'tipo_de_pedido':'tipo_de_pedido',
                'data_load':'data_hora_load',
                'usuário':'usuario',
                'quantidade':'qt_pecas',
                'box':'box',
                'item':'item',
                'data_pedido':'data_pedido'
        },
        'column_types': {
                'olpn': 'string',
                'pedido': 'string',
                'tipo_de_pedido': 'string',
                'usuario': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64',
                'Item': 'Int64'
        },
        'datetime_columns': [
                'data_hora_load',
                'data_pedido'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'putaway' : {
        'remove_columns': [
                'data',
                'status',
                'descrição_item',
                'item_attribute1',
                'transaction_type',
                'inventory_type_id'
        ],
        'rename_columns': {
                'filial':'filial',
                'order': 'pedido',
                'olpn': 'olpn',
                'item': 'item',
                'qt': 'qt_pecas',
                'setor': 'desc_setor_item',
                'tipo_de_pedido': 'tipo_de_pedido',
                'box': 'box',
                'data_do_evento': 'data_hora_putaway',
                'usuário': 'usuario'
        },
        'column_types': {
                'pedido': 'string',
                'olpn': 'string',
                'item': 'Int64',
                'qt_pecas': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'box': 'Int64',
                'usuario': 'string'
        },
        'datetime_columns': [
                'data_hora_putaway'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'jornada' : {
        'remove_columns': [],
        'rename_columns': {
                'dia': 'data',
                'matricula': 'matricula',
                'cod': 'cod',
                'hora': 'hora'
        },
        'column_types': {
                'matricula': 'Int64',
                'cod': 'string',
        },
        'datetime_columns': [
                'data'
        ],
        'encoding': 'ascii',
        'sep': ';'
    },
        'padrao' : {
        'remove_columns': [],
        'rename_columns': {},
        'column_types': {},
        'datetime_columns': [],
        'encoding': 'utf-16',
        'sep': '\t'
    },
}