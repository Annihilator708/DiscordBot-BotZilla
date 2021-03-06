CREATE SCHEMA botzilla;
CREATE TABLE botzilla.users(
    ID bigint primary key,
    name varchar(1024)
);
-- INSERT INTO botzilla.users (ID, name) VALUES (456164513, 'test15');

CREATE TABLE botzilla.help(
    name varchar(200) primary key,
    cog varchar(200),
    info varchar(1500)
);

CREATE TABLE botzilla.mute(
    id varchar(200) primary key
);

CREATE TABLE botzilla.music(
    ID bigint primary key,
    channel_name varchar(508),
    server_name varchar(508),
    type_channel varchar(24)
);

CREATE TABLE botzilla.blacklist(
    ID bigint primary key,
    server_name varchar(508),
    reason varchar(2000),
    total_votes integer
);

CREATE TABLE botzilla.swearwords(
    swearword varchar(508) primary key,
    total bigserial
);

INSERT INTO botzilla.swearwords(swearword, total) VALUES ('shit', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('fuck', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('damn', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('questionmark', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('crap', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('pussy', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('wtf', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('fag', 0);
INSERT INTO botzilla.swearwords(swearword, total) VALUES ('gay', 0);