--- allow for SELECT FROM test
--- to facilitate column naming
DROP TABLE IF EXISTS test; 
CREATE TABLE test(id INTEGER PRIMARY KEY);


DROP TABLE IF EXISTS countries, users, user_country, stores, merchants, products, products_authors, store_stock, orders, order_items CASCADE;
DROP TYPE IF EXISTS continents, user_roles, order_states, product_types CASCADE;

CREATE TYPE continents AS ENUM(
  'Africa', 'Asia', 'Europe', 
  'North America', 'South America', 
  'Antarctica', 'Australia'
);

CREATE TYPE user_roles AS ENUM(
  'Artist', 'Editor', 'Writer'
);

CREATE TYPE order_states AS ENUM(
  'New', 'In Cart', 'Checkout', 'Paid', 'Shipped'
);

CREATE TYPE product_types AS ENUM(
	'Book', 'Magazine', 'Journal', 'Comic'
);

CREATE TABLE countries (
  country_id CHAR(2) NOT NULL,
  country_name VARCHAR NOT NULL,
  continent continents NOT NULL,
  PRIMARY KEY (country_id)
);

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_full_name VARCHAR NOT NULL,
  user_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE user_country (
  user_id INT NOT NULL REFERENCES users,
  country_id CHAR(2) NOT NULL REFERENCES countries,
  PRIMARY KEY ( user_id, country_id )
);


CREATE TABLE stores (
	store_id SERIAL PRIMARY KEY,
	store_name VARCHAR NOT NULL,
	store_country CHAR(2) NOT NULL REFERENCES countries,
	store_admin INT NOT NULL REFERENCES users,
	store_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE merchants (
	merchant_id SERIAL PRIMARY KEY,
	merchant_name VARCHAR NOT NULL,
	merchant_country CHAR(2) NOT NULL REFERENCES countries,
	merchant_admin_id INT NOT NULL REFERENCES users,
	merchant_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE products (
	product_id SERIAL PRIMARY KEY,
	product_name VARCHAR NOT NULL,
	product_price numeric NOT NULL,
	product_type product_types NOT NULL,
	product_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE products_authors (
  product_id INT REFERENCES products,
  product_author INT REFERENCES users,
  relation_type user_roles NOT NULL,
  PRIMARY KEY ( product_id, product_author, relation_type )
);

CREATE TABLE store_stock (
	store_id INT REFERENCES stores,
	merchant_id INT REFERENCES merchants,
	product_id INT REFERENCES products,
	current_stock INT NOT NULL CHECK ( current_stock > 0 ),
	PRIMARY KEY (store_id, merchant_id, product_id)
);

CREATE TABLE orders (
	order_id SERIAL PRIMARY KEY,
	order_store_id INT NOT NULL REFERENCES stores,
	order_user_id INT NOT NULL REFERENCES users,
	order_status order_states NOT NULL,
	order_created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
	order_id INT references orders,
	product_id INT references products,
	quantity INT DEFAULT 1 CHECK ( quantity > 0 ),
	PRIMARY KEY (order_id, product_id)
);

INSERT INTO countries VALUES ('de', 'Germany', 'Europe');
INSERT INTO countries VALUES ('fr', 'France', 'Europe');
INSERT INTO countries VALUES ('be', 'Belgium', 'Europe');
INSERT INTO countries VALUES ('nl', 'Netherlands', 'Europe');
INSERT INTO countries VALUES ('jp', 'Japan', 'Asia');
INSERT INTO countries VALUES ('us', 'USA', 'North America');


INSERT INTO users VALUES (1, 'Hedvig Madhu');
INSERT INTO users VALUES (2, 'Casandra Walton');
INSERT INTO users VALUES (3, 'Alexander Lovisa');
INSERT INTO users VALUES (4, 'Chiyoko Kenji');
INSERT INTO users VALUES (5, 'Rene Goscinny');
INSERT INTO users VALUES (6, 'Alfred Neuwald');

INSERT INTO user_country VALUES (1, 'be');
INSERT INTO user_country VALUES (2, 'fr');
INSERT INTO user_country VALUES (3, 'de');
INSERT INTO user_country VALUES (4, 'jp');
INSERT INTO user_country VALUES (5, 'fr');
INSERT INTO user_country VALUES (6, 'de');

INSERT INTO stores VALUES 
	(1, 'Comic Gallery', 'de', 4),
    (2, 'Atomik Stripwinkel', 'nl', 1),
    (3, 'Midtown Comics Times Square', 'us', 2 ),
	(4, 'Comic Toranoana Akihabara Shop', 'jp', 3 );

INSERT INTO merchants VALUES 
	(1, 'Carlsen Comics', 'de', 2),
	(2, 'Granus Verlag', 'de', 6);

INSERT INTO products VALUES 
	(1, 'Isnogud 50 Year Edition', 139, 'Comic'),
	(2, 'Karl der Kleine in der Klimahölle', 12.9, 'Comic'),
    (3, 'Karl der Kleine - Die Stadt der Printen', 11.9, 'Comic'),
    (4, 'Calvin und Hobbes 6: Wissenschaftlicher Fortschritt macht "Boing"', 12.9, 'Comic');

INSERT INTO products_authors VALUES 
	(1, 5, 'Writer'),
	(2, 6, 'Writer'),
	(2, 6, 'Artist');

INSERT INTO store_stock VALUES 
	(1, 1, 1, 154),
	(1, 2, 2, 108),
    (1, 1, 3, 37),
    (2, 1, 1, 54),
    (2, 2, 2, 48);
    

INSERT INTO orders VALUES
	(1,3,3,'In Cart','2019-8-26 4:58:11+01'),
	(2,4,2,'Paid','2019-1-2 19:33:55+01'),
	(3,3,4,'Paid','2019-9-16 3:42:7+01'),
	(4,2,3,'Paid','2019-1-14 10:22:26+01'),
	(5,2,2,'Shipped','2019-12-14 7:38:20+01'),
	(6,1,5,'Paid','2019-11-19 6:45:41+01'),
	(7,2,2,'Paid','2020-4-5 9:55:54+01'),
	(8,3,6,'Paid','2020-8-3 1:12:9+01'),
	(9,1,1,'In Cart','2020-3-7 6:40:37+01'),
	(10,4,4,'Shipped','2020-8-16 10:31:23+01'),
	(11,2,2,'Shipped','2020-6-2 16:59:10+01'),
	(12,2,2,'In Cart','2021-7-2 8:23:33+01'),
	(13,3,4,'Paid','2021-7-7 4:14:59+01'),
	(14,1,5,'Shipped','2021-9-16 5:22:52+01'),
	(15,4,3,'Paid','2021-9-5 20:45:29+01');


INSERT INTO order_items VALUES 
	(1,3,16),
	(2,1,6),
	(3,3,26),
	(4,2,63),
	(5,1,38),
	(6,2,32),
	(7,2,72),
	(8,3,15),
	(9,2,48),
	(10,1,70),
	(11,1,41),
	(12,1,80),
	(13,3,91),
	(14,2,20),
	(15,3,6);
