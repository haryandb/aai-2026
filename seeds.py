import pandas as pd
import os
import click
from tqdm import tqdm


def seed_db_command(db_engine):
    """Mengimpor seluruh data OnlineRetail.csv dengan progress bar"""
    from sqlalchemy import text

    file_path = "OnlineRetail.csv"
    chunk_size = 10000

    if not os.path.exists(file_path):
        click.echo(f"Error: File {file_path} tidak ditemukan!")
        return

    click.echo("Membaca file CSV...")
    total_rows = sum(1 for row in open(file_path, "r", encoding="unicode_escape")) - 1

    try:
        reader = pd.read_csv(
            file_path,
            encoding="unicode_escape",
            chunksize=chunk_size,
            dtype={"InvoiceNo": str, "StockCode": str, "CustomerID": float},
        )

        click.echo("Mengoptimalkan SQLite...")
        with db_engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode = WAL;"))
            conn.execute(text("PRAGMA synchronous = NORMAL;"))
            conn.commit()

        with tqdm(total=total_rows, desc="Proses Impor", unit="baris") as pbar:
            for chunk in reader:
                chunk["InvoiceDate"] = pd.to_datetime(
                    chunk["InvoiceDate"], format="%m/%d/%Y %H:%M"
                )
                chunk.rename(
                    columns={
                        "InvoiceNo": "invoice_no",
                        "StockCode": "stock_code",
                        "Description": "description",
                        "Quantity": "quantity",
                        "InvoiceDate": "invoice_date",
                        "UnitPrice": "unit_price",
                        "CustomerID": "customer_id",
                        "Country": "country",
                    },
                    inplace=True,
                )

                chunk.to_sql(
                    "transaction", con=db_engine, if_exists="append", index=False
                )

                pbar.update(len(chunk))

        click.echo("\nSelesai! Seluruh data berhasil diimpor.")

    except Exception as e:
        click.echo(f"\nTerjadi kesalahan: {e}")


def register_commands(app, db):
    """Register seeder commands to Flask app."""

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with OnlineRetail.csv data."""
        seed_db_command(db.engine)
