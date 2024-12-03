import psycopg2

class DBManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sicar_table (
            uf TEXT,
            municipio TEXT,
            codigo_ibge BIGINT,
            area_do_imovel DOUBLEPRECISION ,
            registro_car TEXT,
            situacao_cadastro TEXT,
            condicao_cadastro TEXT,
            area_liquida DOUBLE PRECISION,
            area_remanescente_vegetacao_nativa DOUBLE PRECISION,
            area_reserva_legal_proposta DOUBLE PRECISION,
            area_preservacao_permanente DOUBLE PRECISION, 
            area_nao_classificada DOUBLE PRECISION,
            solicitacao_adesao_pra TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            data_inscricao DATE,
            data_alteracao_condicao_cadastro DATE,
            area_rural_consolidada DOUBLE PRECISION,
            area_servidao_administrativa DOUBLE PRECISION,
            tipo_imovel_rural TEXT,
            modulos_fiscais DOUBLE PRECISION,
            area_uso_restrito DOUBLE PRECISION,
            area_reserva_legal_averbada DOUBLE PRECISION,
            area_reserva_legal_aprovada_nao_averbada DOUBLE PRECISION,
            area_pousio DOUBLE PRECISION,
            data_ultima_retificacao DATE
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Table created.")

    def create_extension(self):
        create_extension_query = """
        CREATE EXTENSION IF NOT EXISTS citus;
        """
        # CREATE EXTENSION IF NOT EXISTS postgis;
        self.cursor.execute(create_extension_query)
        self.connection.commit()
        print("Extension created.")

    def create_distributed_table(self):
        create_dist_query = """
        SELECT create_distributed_table('sicar_table', 'codigo_ibge');
        """
        self.cursor.execute(create_dist_query)
        self.connection.commit()
        print("Table distributed.")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")