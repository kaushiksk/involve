CREATE TABLE candidates(
	c_id INT NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	party VARCHAR(50) NOT NULL,	
	constituency VARCHAR(50) NOT NULL,
	thumb VARCHAR(500) NOT NULL,
	votes INT NOT NULL DEFAULT 0
	);
	
CREATE TABLE voters(
	u_id VARCHAR(12) PRIMARY KEY,
	voted BOOL NOT NULL
	);	
	
CREATE TABLE transactions(
	t_id VARCHAR(200) PRIMARY KEY,
	stamp TIMESTAMP NOT NULL
	);
	
ALTER TABLE transactions ADD c_id INT NOT NULL;	
ALTER TABLE transactions ADD FOREIGN KEY (c_id) REFERENCES candidates(c_id);
	

