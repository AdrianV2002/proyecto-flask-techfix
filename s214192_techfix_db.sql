-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 24-03-2026 a las 20:21:49
-- Versión del servidor: 11.8.6-MariaDB-0+deb13u1 from Debian
-- Versión de PHP: 8.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `s214192_techfix_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes_ticket`
--

CREATE TABLE `mensajes_ticket` (
  `id_mensaje` int(11) NOT NULL,
  `id_ticket` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `mensaje` text NOT NULL,
  `fecha` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mensajes_ticket`
--

INSERT INTO `mensajes_ticket` (`id_mensaje`, `id_ticket`, `id_usuario`, `mensaje`, `fecha`) VALUES
(1, 1, 2, 'Hola', '2026-03-21 19:44:46'),
(2, 1, 2, 'Hola', '2026-03-21 19:44:47'),
(3, 1, 1, 'Hola Prueba', '2026-03-21 19:45:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descripcion` text NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `cantidad`, `precio`, `descripcion`, `imagen`) VALUES
(1, 'MinEc', 1, 50.00, '1', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlT4asR85sj8rF4AnWOeQ3epaUE2K6ryCIQg&s');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tickets`
--

CREATE TABLE `tickets` (
  `id_ticket` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `equipo` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente',
  `fecha` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tickets`
--

INSERT INTO `tickets` (`id_ticket`, `id_usuario`, `equipo`, `descripcion`, `estado`, `fecha`) VALUES
(1, 2, 'Instalación de Sistema Operativo', 'Ayudaaaa', 'En Proceso', '2026-03-21 19:44:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `mail` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `mail`, `password`, `rol`) VALUES
(1, 'Administrador', 'admin@admin.com', 'scrypt:32768:8:1$tdPCOmVEyizTaecd$a505dbf92b380b9ceab8300ca8606333664c58a7070ab73665ba618cc3c3015cf79db33fd92066bba1fd7d31795bde81088c40c5f18d7c98b661569a095ba6d8', 'admin'),
(2, 'Adrian Villegas', 'ajvc.2002.24@gmail.com', 'scrypt:32768:8:1$OcbPgZvPJioTUlUF$7c31d2b9540f4ae21c13c2c0cb005f80c64da0fc2dc34ea5e1141f614b1f3541d49c60eee252687d792f6e1ba3ead47c92921d9f21259d67d2fac51d63003cfd', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `mensajes_ticket`
--
ALTER TABLE `mensajes_ticket`
  ADD PRIMARY KEY (`id_mensaje`),
  ADD KEY `id_ticket` (`id_ticket`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id_ticket`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `mensajes_ticket`
--
ALTER TABLE `mensajes_ticket`
  MODIFY `id_mensaje` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id_ticket` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `mensajes_ticket`
--
ALTER TABLE `mensajes_ticket`
  ADD CONSTRAINT `mensajes_ticket_ibfk_1` FOREIGN KEY (`id_ticket`) REFERENCES `tickets` (`id_ticket`) ON DELETE CASCADE,
  ADD CONSTRAINT `mensajes_ticket_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
