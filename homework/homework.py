"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
from pathlib import Path

def clean_campaign_data():
    # Rutas de entrada y salida
    input_dir = Path("files/input")
    output_dir = Path("files/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Columnas esperadas en los datos
    columns = [
        "client_id", "age", "job", "marital", "education", "credit_default",
        "mortgage", "month", "day", "contact_duration", "number_contacts",
        "previous_campaign_contacts", "previous_outcome", "cons_price_idx",
        "euribor_three_months", "campaign_outcome"
    ]

    # Crear DataFrame vacío con columnas correctas
    data = pd.DataFrame(columns=columns)

    # Leer y concatenar los archivos ZIP
    for archive in input_dir.iterdir():
        df = pd.read_csv(archive, compression="zip", index_col=False)
        data = pd.concat([data, df], ignore_index=True)

    # Limpieza y transformación de datos
    data["job"] = data["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    data["education"] = data["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    data["credit_default"] = data["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    data["mortgage"] = data["mortgage"].map(lambda x: 1 if x == "yes" else 0)

    # DataFrame de clientes
    client_df = data[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]]

    # Transformación de campaña
    data["previous_outcome"] = data["previous_outcome"].map(lambda x: 1 if x == "success" else 0)
    data["campaign_outcome"] = data["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)
    data["last_contact_date"] = pd.to_datetime(data["day"].astype(str) + "-" + data["month"] + "-2022", format="%d-%b-%Y")

    # DataFrame de campaña
    campaign_df = data[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "last_contact_date"]]

    # DataFrame de economía
    economics_df = data[["client_id", "cons_price_idx", "euribor_three_months"]]

    # Guardar archivos en CSV sin índice de client_id
    client_df.set_index("client_id").to_csv(output_dir / "client.csv")
    campaign_df.set_index("client_id").to_csv(output_dir / "campaign.csv")
    economics_df.set_index("client_id").to_csv(output_dir / "economics.csv")

if __name__ == "__main__":
    clean_campaign_data()