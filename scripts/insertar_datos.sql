use master;
create database constantec;

use constantec;

INSERT INTO constancia_tipos VALUES
('Constancia de Inscritos', 'Documento que certifica que un estudiante está actualmente inscrito en una institución educativa, indicando generalmente el semestre o ciclo escolar en curso.'),
('Constancia de Kardex', 'Documento que muestra el historial académico del estudiante, incluyendo todas las materias cursadas, calificaciones obtenidas y los periodos en los que se cursaron.'),
('Constancia para el Seguro Social', 'Documento requerido por el IMSS u otra institución de salud, que valida que el estudiante está inscrito y tiene derecho a recibir atención médica como parte del servicio social o como estudiante activo.'),
('Constancia con Calificaciones del Semestre Anterior', 'Documento que detalla las materias cursadas y calificaciones obtenidas en el semestre inmediatamente anterior al actual.'),
('Constancia con Calificaciones de Dos Semestres Anteriores', 'Similar a la anterior, pero incluye las materias y calificaciones de los dos semestres previos al actual.'),
('Constancia de Egreso', 'Documento que certifica que el estudiante ha concluido la totalidad de sus estudios académicos, aunque aún no haya recibido el título oficial.'),
('Constancia de Título en Trámite', 'Documento que indica que el egresado ya inició el proceso de titulación y que el título profesional está en trámite ante la autoridad educativa correspondiente.'),
('Constancia de Pago', 'Documento que acredita que el estudiante ha realizado el pago correspondiente a su inscripción o colegiatura. Incluye detalles como el monto pagado, la fecha de pago y el semestre o ciclo escolar al que corresponde dicho pago.'),
('Constancia Personalizada', 'Descripción personalizada ingresada por el estudiante desde la aplicación web.');

INSERT INTO solicitud_estatus VALUES 
('pendiente', 'La solicitud esta pendiente' ),
('revision', 'La solicitud esta en revision' ),
('completo', 'La constancia esta lista' );

INSERT INTO Trabajadores VALUES 
('THJ384', 'Jorge', 'Méndez Suárez', '1995-08-12', 30, 'Servicios escolares', '477 890 3463', 'jorge.mendez@leon.tecnm.mx', '2000-06-12'),
('TPO235', 'Jessica', 'Rosas Flores', '1989-03-25', 36, 'Servicios escolares', '477 349 1211', 'jessica.rosas@leon.tecnm.mx', '1990-07-20'),
('TFR093', 'Camilo', 'Salazar Godínez', '1998-07-05', 27, 'Servicios escolares', '477 571 9712', 'camilo.salazar@leon.tecnm.mx', '2001-05-11');

insert into [dbo].[estudiantes] ([apellidos], [password], [correo_institucional], [edad], [semestre], [carrera], [fecha_nacimiento], [fecha_registro], [municipio], [no_control], [nombre], [primer_ingreso]) values 
('Rocha', '$2b$12$71/Hi78TNE/eFLx.4j3UB.N5szktjHT0JJ1ArZL4ooDK79wPXa0dK', '123@leon.tecnm.mx', 21, 6, 'Sistemas', '2004-04-21', '2025-06-01', 'Leon', '123', 'Jeshua', 0)

insert into [dbo].[Usuarios_administradores] ([username], [password], [is_active], [is_superuser]) values 
('admin', '$2b$12$71/Hi78TNE/eFLx.4j3UB.N5szktjHT0JJ1ArZL4ooDK79wPXa0dK', 1, 1);


// para jeshua
insert into constancias values
('constancia para la universidad', NULL),
('constancia para cartilla militar', NULL);

INSERT INTO solicitudes VALUES
(1, 1, 1, '2025-05-28', NULL),
(1, 2, 1, '2025-05-28', NULL);


--- Consultas
select * from usuarios_administradores;
SELECT * FROM estudiantes
SELECT * FROM solicitudes
SELECT * FROM solicitud_estatus
SELECT * FROM constancia_tipos
SELECT * FROM constancia_opciones
SELECT * FROM encuesta_satisfaccion
SELECT * FROM constancias
SELECT * FROM trabajadores

delete from estudiantes where id=1;
delete from usuarios_administradores where id=1;