from models.schemas.invoices_schema import InvoiceModel
from infrastructure.dataframes.dataframe_manager import DataframeManager
from pathlib import Path



data = DataframeManager()

df = data.load_csv(
    caminho=Path(r'C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\Sala PCP - Online_A.B.S - Data Lakehouse\Bronze (Raw Layer)\pcom_validade_invoices'),
    encoding='latin1',
    sep='\t'
)

print(df.head())

InvoiceModel.update_history(
        bronze_df=df,
        gold_path=Path(r'C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\Sala PCP - Online_A.B.S - Data Lakehouse\Gold (Business Layer)\pcom_validade_invoices'),
        nf_column='nota_fiscal',
        status_column='status_pcom'
    )