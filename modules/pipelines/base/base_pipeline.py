"""
modules/
└── pipelines/
    │
    ├── base/
    │   ├── __init__.py
    │   ├── base_pipeline.py          # Classe abstrata das pipelines
    │   ├── pipeline_context.py       # Contexto compartilhado
    │   └── pipeline_result.py        # Resultado da execução
    │
    ├── domain/
    │   ├── __init__.py
    │   │
    │   ├── constants/
    │   │   ├── columns.py
    │   │   ├── dtypes.py
    │   │   └── dates.py
    │   │
    │   └── validators/
    │       ├── dataframe_validator.py
    │       └── required_columns.py
    │
    ├── services/
    │   ├── __init__.py
    │   │
    │   ├── dataframe_service.py
    │   ├── datetime_service.py
    │   ├── duration_service.py
    │   ├── merge_service.py
    │   ├── sector_service.py
    │   ├── location_service.py
    │   ├── export_service.py
    │   ├── reader_service.py
    │   ├── duckdb_service.py
    │   └── parquet_service.py
    │
    ├── use_cases/
    │   ├── cancel_pipeline.py
    │   ├── loading_pipeline.py
    │   ├── olpn_pipeline.py
    │   ├── packing_pipeline.py
    │   ├── picking_pipeline.py
    │   └── putaway_pipeline.py
    │
    ├── sql/
    │   ├── packing.sql
    │   ├── loading.sql
    │   ├── olpn.sql
    │   └── ...
    │
    └── pipeline_factory.py
"""