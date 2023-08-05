SELECT pg_terminate_backend(pid) from pg_stat_activity where datname='arches_my_hip_app';

DROP DATABASE IF EXISTS arches_my_hip_app;

CREATE DATABASE arches_my_hip_app
  WITH ENCODING='UTF8'
       OWNER=postgres
       TEMPLATE=template_postgis_20
       CONNECTION LIMIT=-1;

