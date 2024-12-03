import pandas as pd

class DataIngestion:
    @staticmethod
    def ingest_csv(cursor, file_path, batch_size=1000):
        try:
            # Ler o arquivo CSV em chunks
            for chunk in pd.read_csv(file_path, chunksize=batch_size, delimiter=';', on_bad_lines='error'):
                print("Colunas do chunk:", chunk.columns.tolist())
                print("Número de colunas no chunk:", len(chunk.columns))

                expected_columns = 26
                if len(chunk.columns) != expected_columns:
                    print(f"Número inesperado de colunas: {len(chunk.columns)}")
                    continue  # Ignorar este chunk se o número de colunas não for o esperado

                date_columns = [
                    "data_inscricao",
                    "data_alteracao_condicao_cadastro",
                    "data_ultima_retificacao"
                ]

                # Converter colunas de data para datetime
                for date_col in date_columns:
                    if date_col in chunk.columns:
                        chunk[date_col] = pd.to_datetime(chunk[date_col], errors='coerce')
                        if chunk[date_col].isna().any():
                            print(f"Valores ausentes encontrados na coluna {date_col}")
                            # Preencher NaT com a data padrão
                            chunk[date_col] = chunk[date_col].fillna(pd.Timestamp('1900-01-01'))

                # Inserir dados no banco
                for _, row in chunk.iterrows():
                    if len(row) == expected_columns:
                        cursor.execute("""
                            INSERT INTO sicar_table (
                                uf, municipio, codigo_ibge, area_do_imovel, registro_car, 
                                situacao_cadastro, condicao_cadastro, area_liquida, 
                                area_remanescente_vegetacao_nativa, area_reserva_legal_proposta, 
                                area_preservacao_permanente, area_nao_classificada, 
                                solicitacao_adesao_pra, latitude, longitude, data_inscricao, 
                                data_alteracao_condicao_cadastro, area_rural_consolidada, 
                                area_servidao_administrativa, tipo_imovel_rural, modulos_fiscais, 
                                area_uso_restrito, area_reserva_legal_averbada, 
                                area_reserva_legal_aprovada_nao_averbada, area_pousio, 
                                data_ultima_retificacao
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            )
                        """, tuple(row))
                    else:
                        print(f"Row has unexpected number of columns: {len(row)}")
                cursor.connection.commit()
            print("Data ingestion completed.")
        except Exception as e:
            print(f"Error during ingestion: {e}")