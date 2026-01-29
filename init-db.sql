-- Créer la base de données auth_db si elle n'existe pas
-- Note: PostgreSQL ne supporte pas CREATE DATABASE IF NOT EXISTS directement dans un script simple
-- Mais comme le script ne tourne qu'à l'initialisation, c'est correct.

CREATE DATABASE auth_db;

-- Accorder les permissions
GRANT ALL PRIVILEGES ON DATABASE auth_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE cancer_db TO "user";
