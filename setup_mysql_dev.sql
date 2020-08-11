-- Configuration database for work

-- Create database hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create user of database
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost';

-- set password to user
SET PASSWORD FOR 'hbnb_dev'@'localhost' = PASSWORD('hbnb_dev_pwd');

-- give all the user's properties to the database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Let the user see the perfomance data
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

FLUSH PRIVILEGES;
