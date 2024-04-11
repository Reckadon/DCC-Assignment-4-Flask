USE electoralbonds;
LOAD DATA LOCAL INFILE 'D:/Web Dev/DCC-Assignment-4-Flask/bonds_encashed_by_parties.csv' 
INTO TABLE bonds_encashed_by_parties 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 5 ROWS;
