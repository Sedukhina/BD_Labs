FROM postgres:latest

ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database
ENV PGDATA="/var/lib/postgresql/data/pgdata"

WORKDIR /db

COPY . .