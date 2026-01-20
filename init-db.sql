-- Créer la base de données auth_db
CREATE DATABASE auth_db;

-- Créer la base de données cancer_db
CREATE DATABASE cancer_db;

-- Accorder les permissions
GRANT ALL PRIVILEGES ON DATABASE auth_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE cancer_db TO "user";
