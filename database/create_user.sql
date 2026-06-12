-- Active: 1759954468303@@127.0.0.1@3306@tarea2_appweb
-- Crear el usuario si no existe
CREATE USER IF NOT EXISTS 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

-- Otorgar todos los privilegios sobre la base de datos específica
GRANT ALL PRIVILEGES ON tarea2_appweb.* TO 'cc5002'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;