CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

-- Crear tabla 'libros'
CREATE TABLE IF NOT EXISTS libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(256) NOT NULL,
    autor VARCHAR(256) NOT NULL,
    genero VARCHAR(256) NOT NULL,
    estatus INT NOT NULL,
    archivo LONGBLOB NOT NULL
);

-- Crear tabla 'usuarios'
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);
