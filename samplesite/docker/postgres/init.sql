CREATE USER djangouser WITH PASSWORD 'rootroot';

CREATE DATABASE djangodb;
GRANT ALL PRIVILEGES ON DATABASE djangodb TO djangouser;