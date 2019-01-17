PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS 'Toys';
DROP TABLE IF EXISTS 'Children';


CREATE TABLE 'Children' (
    'ChildId' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'Name' TEXT NOT NULL
);

INSERT INTO 'Children'
VALUES (null, "Billy");

INSERT INTO 'Children'
VALUES (null, "Laney");

INSERT INTO 'Children'
VALUES (null, "Jesse");



CREATE TABLE 'Toys' (
    'ToyId' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'Name' TEXT NOT NULL,
    'ChildId' INTEGER NOT NULL,
    'Delivered' INTEGER NOT NULL DEFAULT 0 CHECK (Delivered BETWEEN 0 AND 1),
    FOREIGN KEY('ChildId')
    REFERENCES 'Children'('ChildId')
    ON DELETE CASCADE
);

INSERT INTO 'Toys'
VALUES (null, "Doll", 1, 0);

INSERT INTO 'Toys'
VALUES (null, "VR Headset", 2, 0);

INSERT INTO 'Toys'
VALUES (null, "Sharp Knife", 2, 0);

INSERT INTO 'Toys'
VALUES (null, "Woody Doll", 3, 0);

