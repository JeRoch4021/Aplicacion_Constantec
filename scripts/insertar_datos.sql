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

insert into [dbo].[estudiantes] ([apellidos], [contrasena], [correo_institucional], [edad], [fecha_nacimiento], [fecha_registro], [municipio], [no_control], [nombre], [primer_ingreso]) 
values ('Rocha Sainez', '$2b$12$.tAxA1EUOoReYtXpthDCIOhGr7s6TzayAPy.yPWgwY/OjmPIcw8Jy', '22240302@leon.tecnm.mx', 18, '1983-07-04T00:00:00.000Z', '2025-05-29T00:00:00.000Z', 'Justinfurt', '22240302', 'Jeshua', 0)

insert into [dbo].[estudiantes] ([apellidos], [contrasena], [correo_institucional], [edad], [fecha_nacimiento], [fecha_registro], [municipio], [no_control], [nombre], [primer_ingreso]) 
values ('Martinez Sanchez', '$2b$12$.tAxA1EUOoReYtXpthDCIOhGr7s6TzayAPy.yPWgwY/OjmPIcw8Jy', '33340302@leon.tecnm.mx', 18, '1983-07-04T00:00:00.000Z', '2025-05-29T00:00:00.000Z', 'Leon', '33340302', 'Oscar', 0)

INSERT INTO solicitud_estatus VALUES 
('pendiente', 'La solicitud esta pendiente' ),
('revisión', 'La solicitud esta en revision' ),
('completo', 'La constancia esta lista' );

// para jeshua
insert into constancias values
('constancia para la universidad', NULL),
('constancia para cartilla militar', NULL);

INSERT INTO solicitudes VALUES
(1, 1, 1, '2025-05-28', NULL),
(1, 2, 1, '2025-05-28', NULL);

// para oscar
insert into constancias values
('constancia para la maestria', NULL),
('constancia para creditos complementarios', NULL);

INSERT INTO solicitudes VALUES
(2, 3, 1, '2025-05-28', NULL),
(2, 4, 1, '2025-05-28', NULL);
