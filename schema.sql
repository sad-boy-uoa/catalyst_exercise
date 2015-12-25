-- Basic schema
--
--
CREATE TABLE movies (
  id     INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name   VARCHAR(100) NOT NULL UNIQUE,
  length INTEGER
);


CREATE TABLE people (
  id     INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name   VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE votes (
  id        INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
  person_id INTEGER NOT NULL ,
  movie_id  INTEGER NOT NULL,
  CONSTRAINT person_fk FOREIGN KEY (person_id) REFERENCES people(id),
  CONSTRAINT movie_fk FOREIGN KEY (movie_id) REFERENCES movies(id),
  CONSTRAINT votes_once UNIQUE (person_id, movie_id)
);


-- Optional bits
-- movie categories
--
CREATE TABLE categories (
  id     INTEGER PRIMARY KEY AUTO_INCREMENT, 
  name   VARCHAR(30) NOT NULL UNIQUE
);


ALTER TABLE movies ADD 
   category_id INTEGER;


ALTER TABLE movies ADD 
  CONSTRAINT category_fk FOREIGN KEY (category_id) 
  REFERENCES categories(id);
