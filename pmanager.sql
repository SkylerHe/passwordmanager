CREATE TABLE IF NOT EXISTS pmanager 
(
    time datetime default current_timestamp,
    website varchar(30),
    username varchar(30),
    password varchar(300)
);
