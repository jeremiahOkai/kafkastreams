#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE testdb;
	CREATE USER admin WITH PASSWORD 'admin';
	GRANT ALL PRIVILEGES ON DATABASE testdb TO admin;
	GRANT ALL ON SCHEMA public TO admin;
EOSQL
