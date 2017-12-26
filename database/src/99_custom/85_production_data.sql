--=============================================
--Insert CSV Data into temporary staging tables
--=============================================

--------------
--antennes.csv
--------------


CREATE DATABASE bot;
\c database bot
CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigserial primary key,
    name varchar(254),
    date_added timestamp default NULL
);