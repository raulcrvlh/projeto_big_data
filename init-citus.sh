#!/bin/bash

# Aguarda o PostgreSQL iniciar completamente
echo "Aguardando o PostgreSQL iniciar..."
until pg_isready -h localhost -U raulfelipecarvalho -d postgres; do
  sleep 1
done

# Cria a extensão Citus
echo "Instalando a extensão Citus..."
psql -U postgres -c "CREATE EXTENSION citus;"
# psql -U postgres "CREATE EXTENSION postgis;"

# Verifica se a extensão foi criada
psql -U postgres -c "SELECT * FROM pg_extension WHERE extname = citus;"
psql -U postgres -c "SELECT * FROM pg_extension WHERE extname = postgis;"

# Qualquer outra inicialização que você queira fazer, como criação de tabelas
echo "Configuração concluída."
