import psycopg2
import os
from dotenv import load_dotenv
import time

from docker_manager import DockerManager
from db_manager import DBManager
from data_ingestion import DataIngestion

def main():
    # Leitura do arquivo .env
    load_dotenv()
    # Iniciar o Docker
    DockerManager.run_docker_compose()

    # Caminho para o arquivo
    file_path = "data/temas_ambientais.csv"

    # Conectar ao banco de dados
    connection = psycopg2.connect(
        dbname="postgres", 
        user=os.getenv("PGUSER"), 
        password=os.getenv("PGPASSWORD"), 
        host="localhost", 
        port="5432"
    )
    try:

        db_manager = DBManager(connection)
        inicio1 = time.time()
        db_manager.create_extension()
        fim1 = time.time()

        print("Tempo extensões: ", fim1 - inicio1)
        inicio2 = time.time()
        db_manager.create_table()
        fim2 = time.time()

        print("Tempo de criação da tabela: ", fim2 - inicio2)
        inicio3 = time.time()
        db_manager.create_distributed_table()
        fim3 = time.time()
        print("tempo de criação de tabela distribuida: ", fim3 - inicio3)
        
        inicio_ingestao = time.time()
        DataIngestion.ingest_csv(db_manager.cursor, file_path, batch_size=1000)
        fim_ingestao = time.time()
        print(f"Tempo total para ingestão de dados: {fim_ingestao - inicio_ingestao}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    main()
