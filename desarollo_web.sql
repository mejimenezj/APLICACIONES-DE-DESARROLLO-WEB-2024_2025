-- Script de Base de Datos: desarrollo_web
-- Configuraciones básicas
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Tabla 'productos' 
DROP TABLE IF EXISTS `productos`;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Tabla 'usuarios' (estructura idéntica)
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Datos de prueba ORIGINALES pero con contraseñas seguras genéricas
INSERT INTO `productos` (`id_producto`, `nombre`, `precio`, `stock`) VALUES 
(1, 'lapto', 500.00, 5);

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `password`) VALUES 
(1, 'Maritza Jimenez', 'jhennyjiron1998@gmail.com', 'scrypt:32768:8:1$seguro$abc123');  -- Contraseña hasheada genérica

-- Restaurar configuraciones
SET FOREIGN_KEY_CHECKS = 1;
