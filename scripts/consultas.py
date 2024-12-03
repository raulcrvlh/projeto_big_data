import os
import dotenv
import psycopg2
import time

# Carregar variáveis de ambiente
dotenv.load_dotenv()

# Conectar ao banco de dados
conn = psycopg2.connect(
    database="postgres",
    user=os.environ.get("PGUSER"),
    host="localhost",
    password=os.environ.get("PGPASSWORD"),
    port=5432
)

cur = conn.cursor()

# CONSULTAS
query1 = """
CREATE TABLE IF NOT EXISTS area_total_mt_ms AS
SELECT 
    uf, 
    SUM(area_do_imovel) AS area_total
FROM 
    public.sicar_table
WHERE 
    uf IN ('MT', 'MS')
GROUP BY 
    uf
ORDER BY 
    area_total DESC
LIMIT 10;
"""

# tempo de execução da consulta
start_time_q1 = time.time()
cur.execute(query1)
conn.commit()
end_time_q1 = time.time()
print(f"\nConsulta 1 concluída. Tempo de execução: {end_time_q1 - start_time_q1:.3f} segundos")

query1_select = "SELECT * FROM area_total_mt_ms;"
cur.execute(query1_select)
results1 = cur.fetchall()

print("Resultados da consulta:")
for row in results1:
    print(row)

query2 = """
CREATE TABLE IF NOT EXISTS propriedades_sudestes AS
SELECT 
    * 
FROM 
    public.sicar_table
WHERE 
    uf IN ('SP', 'RJ', 'MG', 'ES');
"""

start_time_q2 = time.time()
cur.execute(query2)
conn.commit()
end_time_q2 = time.time()
print(f"\nConsulta 2 concluída. Tempo de execução: {end_time_q2 - start_time_q2:.3f} segundos")

query2_select = "SELECT * FROM propriedades_sudestes;"
cur.execute(query2_select)
results2 = cur.fetchall()

print("Resultados da consulta:")
for i, row in enumerate(results2[:10], start=1):
    print(f"{i}: {row}")

min_lon, max_lon = -53.8181518, -51.0495971
min_lat, max_lat = -19.4632582, -16.1924262
query3 = """
CREATE TABLE IF NOT EXISTS 
    propriedades_dentro_do_poligono AS
SELECT 
    *
FROM 
    public.sicar_table
WHERE 
    longitude 
BETWEEN %s AND %s
AND 
    latitude 
BETWEEN %s AND %s;
"""
start_time_q3 = time.time()
cur.execute(query3, (min_lon, max_lon, min_lat, max_lat))
conn.commit()
end_time_q3 = time.time()
print(f"\nConsulta 3 concluída. Tempo de execução: {end_time_q3 - start_time_q3:.3f} segundos")

query3_select = "SELECT * FROM propriedades_dentro_do_poligono;"
cur.execute(query3_select)
results3 = cur.fetchall()

print("Resultados da consulta:")
for i, row in enumerate(results3[:10], start=1):
    print(f"{i}: {row}")

query4 = """
CREATE TABLE IF NOT EXISTS 
    total_propriedades_por_ano AS
SELECT 
    DATE_PART('YEAR', data_inscricao) 
AS 
    ano_cadastro, COUNT(*) AS total_propriedades
FROM 
    sicar_table
GROUP BY 
    ano_cadastro
ORDER BY 
    ano_cadastro;
"""

start_time_q4 = time.time()
cur.execute(query4)
conn.commit()
end_time_q4 = time.time()
print(f"\nConsulta 4 concluída. Tempo de execução: {end_time_q4 - start_time_q4:.3f} segundos")

query4_select = "SELECT * FROM total_propriedades_por_ano;"
cur.execute(query4_select)
results4 = cur.fetchall()

print("Resultados da consulta:")
for row in results4:
    print(row)

# query5 = """
# CREATE TABLE IF NOT EXISTS 
#     percentual_medio_de_vegetacao 
# AS
# SELECT 
#     AVG(area_remanescente_vegetacao_nativa / area_do_imovel * 100) 
# AS 
#     percentual_medio_vegetacao
# FROM 
#     public.sicar_table;
# """

# start_time_q5 = time.time()
# cur.execute(query5)
# conn.commit()
# end_time_q5 = time.time()
# print(f"\nConsulta 5 concluída. Tempo de execução: {end_time_q5 - start_time_q5:.3f} segundos")

# query5_select = "SELECT * FROM percentual_medio_de_vegetacao;"
# cur.execute(query5_select)
# results5 = cur.fetchall()

# print("Resultados da consulta:")
# for row in results5:
#     print(row)

query6 = """
CREATE TABLE IF NOT EXISTS total_de_propriedades AS 
SELECT 
    uf, COUNT(*) AS total_propriedades
FROM 
    public.sicar_table
GROUP BY 
    uf
ORDER BY 
    total_propriedades DESC
"""

start_time_q6 = time.time()
cur.execute(query6)
conn.commit()
end_time_q6 = time.time()
print(f"\nConsulta 6 concluída. Tempo de execução: {end_time_q6 - start_time_q6:.3f} segundos")

query6_select = "SELECT * FROM total_de_propriedades;"
cur.execute(query6_select)
results6 = cur.fetchall()

print("Resultados da consulta:")
for row in results6:
    print(row)

# Fechar conexão com o banco de dados
cur.close()
conn.close()