CREATE DATABASE IF NOT EXISTS ibli;
USE ibli;

CREATE TABLE IF NOT EXISTS Object (
	ObjectID int auto_increment,
    PosX int,
    PosY int,
    Width int,
    Height int,
    Collide bool,
    PRIMARY KEY(ObjectID)
);

CREATE TABLE IF NOT EXISTS Item (
	ItemID int auto_increment,
    ItemDamage int,
    ItemOffset int,
    primary key (ItemID)
);

SELECT * FROM ITEM;