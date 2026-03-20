## BACKLOG DE PRODUCTO

### Historias de Usuario para Configuración del Entorno Docker y Servicios

#### Historia de Usuario 1: Configuración Inicial del Entorno Docker
*   **Título:** Configurar Entorno Docker con NestJS, Angular, PostgreSQL y Redis
*   **Descripción:** Como desarrollador, quiero un entorno de desarrollo local configurado con Docker que incluya NestJS, Angular, PostgreSQL y Redis, para poder empezar a desarrollar y probar la aplicación de la quiniela de manera aislada y reproducible.
*   **Criterios de Aceptación:**
    *   El archivo `docker-compose.yml` está creado y permite levantar todos los servicios (NestJS, Angular, PostgreSQL, Redis).
    *   Cada servicio se ejecuta en su propio contenedor Docker.
    *   La base de datos PostgreSQL es accesible desde el servicio NestJS.
    *   Redis es accesible desde el servicio NestJS.
    *   La aplicación Angular se levanta y se puede acceder a ella en el navegador.
    *   Se puede realizar una migración de base de datos inicial a través del contenedor NestJS.
*   **Puntos de Historia:** 5

#### Historia de Usuario 2: Integración de ORM en NestJS y Conexión a DB
*   **Título:** Integrar TypeORM/Prisma en NestJS y establecer conexión con PostgreSQL
*   **Descripción:** Como desarrollador backend, quiero tener un ORM (TypeORM o Prisma) configurado en el servicio NestJS y conectado a la base de datos PostgreSQL, para poder definir modelos de datos y realizar operaciones CRUD de manera eficiente.
*   **Criterios de Aceptación:**
    *   El ORM elegido está instalado y configurado en el proyecto NestJS.
    *   Existe un módulo de conexión a la base de datos en NestJS que utiliza el ORM.
    *   Se puede realizar una operación de prueba (ej. insertar un registro simple) en la base de datos a través del ORM.
    *   La configuración de la base de datos se gestiona mediante variables de entorno en Docker.
*   **Puntos de Historia:** 3

### Historias de Usuario para Implementación del Servicio de Validación de Tiempo

#### Historia de Usuario 3: Sincronización de Servidores con NTP
*   **Título:** Configurar servidores para sincronización horaria con NTP
*   **Descripción:** Como administrador de sistemas, quiero que todos los contenedores de la aplicación estén sincronizados con servidores NTP externos de alta precisión, para garantizar que la referencia temporal sea consistente en todo el sistema y evitar problemas de validación de pronósticos.
*   **Criterios de Aceptación:**
    *   Los contenedores de NestJS y cualquier otro servicio relevante (ej. Workers) están configurados para usar NTP.
    *   Se verifica que la hora del sistema dentro de los contenedores coincide con la hora de los servidores NTP.
    *   Existe un mecanismo para monitorear la sincronización NTP.
*   **Puntos de Historia:** 2

#### Historia de Usuario 4: Servicio de Validación de Tiempo de Pronósticos
*   **Título:** Implementar servicio de validación de pronósticos basado en tiempo
*   **Descripción:** Como usuario del sistema, quiero que mi pronóstico sea validado automáticamente contra la hora de inicio oficial del partido, para asegurar que no se acepten pronósticos después del límite de tiempo establecido (5 minutos antes del inicio del partido).
*   **Criterios de Aceptación:**
    *   El backend de NestJS tiene un endpoint para recibir pronósticos de partidos.
    *   Antes de guardar el pronóstico, se verifica que la hora actual del servidor (sincronizada vía NTP) sea al menos 5 minutos antes de la hora de inicio oficial del partido.
    *   Si el pronóstico está fuera de tiempo, se devuelve un error indicando que no se puede enviar.
    *   Cada pronóstico guardado incluye un `timestamp` exacto en la base de datos.
    *   Los pronósticos para el primer clasificado de grupo y campeón del torneo se validan para ser enviados antes del inicio del primer partido del torneo.
*   **Puntos de Historia:** 5

### Historias de Usuario para Desarrollo de la Lógica de Puntos y Persistencia

#### Historia de Usuario 5: Almacenamiento de Pronósticos y Resultados
*   **Título:** Persistir pronósticos de jugadores y resultados de partidos en la base de datos
*   **Descripción:** Como sistema, quiero almacenar de forma estructurada los pronósticos de los jugadores para cada partido, así como los resultados oficiales de los partidos, para poder realizar los cálculos de puntuación y mantener un registro histórico.
*   **Criterios de Aceptación:**
    *   Existe un modelo de base de datos para `Pronostico` que incluye `id_jugador`, `id_partido`, `marcador_local`, `marcador_visitante`, `timestamp_envio`.
    *   Existe un modelo de base de datos para `Partido` que incluye `id_partido`, `equipo_local`, `equipo_visitante`, `fecha_hora_inicio`, `marcador_final_local`, `marcador_final_visitante`, `estado` (ej. pendiente, jugado, suspendido).
    *   Se pueden guardar y recuperar pronósticos de jugadores y resultados de partidos.
*   **Puntos de Historia:** 3

#### Historia de Usuario 6: Cálculo de Puntos por Acierto Exacto
*   **Título:** Implementar cálculo de puntos por acierto exacto de resultado
*   **Descripción:** Como sistema de puntuación, quiero calcular y asignar 5 puntos a un jugador cuando acierta el resultado exacto de un partido (marcador y ganador/empate), para recompensar la precisión en sus pronósticos.
*   **Criterios de Aceptación:**
    *   Existe una función en el backend que toma un pronóstico y un resultado oficial y determina si hay un acierto exacto.
    *   Si hay acierto exacto, se asignan 5 puntos al jugador para ese partido.
    *   Los puntos se persisten en la base de datos asociados al jugador y al partido.
    *   La función considera resultados como 2-1 vs 2-1.
*   **Puntos de Historia:** 3

#### Historia de Usuario 7: Cálculo de Puntos por Acierto de Ganador/Empate
*   **Título:** Implementar cálculo de puntos por acierto de ganador o empate (sin marcador exacto)
*   **Descripción:** Como sistema de puntuación, quiero calcular y asignar 3 puntos a un jugador cuando acierta el ganador de un partido o si el resultado es un empate (sin acertar el marcador exacto), para recompensar el acierto direccional.
*   **Criterios de Aceptación:**
    *   Existe una función en el backend que toma un pronóstico y un resultado oficial y determina si hay un acierto de ganador o empate (sin ser exacto).
    *   Si hay acierto de ganador/empate, se asignan 3 puntos al jugador para ese partido.
    *   Los puntos se persisten en la base de datos asociados al jugador y al partido.
    *   La función considera resultados como 2-1 pronosticado vs 3-1 real (acierto de ganador) o 1-1 pronosticado vs 0-0 real (acierto de empate).
*   **Puntos de Historia:** 3

#### Historia de Usuario 8: Cálculo de Puntos por Bono de Primer Clasificado de Grupo
*   **Título:** Implementar cálculo de puntos por bono de primer clasificado de grupo
*   **Descripción:** Como sistema de puntuación, quiero calcular y asignar 10 puntos a un jugador por cada grupo en el que acierte el equipo que terminará en la primera posición, para recompensar la visión estratégica en la fase de grupos.
*   **Criterios de Aceptación:**
    *   Existe un modelo de base de datos para `PronosticoClasificadoGrupo` que incluye `id_jugador`, `id_grupo`, `equipo_pronosticado`.
    *   Existe un modelo de base de datos para `Grupo` que incluye `id_grupo`, `equipo_primer_clasificado_oficial`.
    *   Al finalizar la fase de grupos, se ejecuta un proceso que compara los pronósticos con los resultados oficiales.
    *   Por cada acierto, se asignan 10 puntos al jugador y se persisten en la base de datos.
*   **Puntos de Historia:** 5

#### Historia de Usuario 9: Cálculo de Puntos por Bono de Campeón del Torneo
*   **Título:** Implementar cálculo de puntos por bono de campeón del torneo
*   **Descripción:** Como sistema de puntuación, quiero calcular y asignar 25 puntos a un jugador que acierta al equipo que se coronará campeón del torneo, para premiar la predicción más ambiciosa.
*   **Criterios de Aceptación:**
    *   Existe un modelo de base de datos para `PronosticoCampeon` que incluye `id_jugador`, `equipo_pronosticado`.
    *   Al finalizar el torneo, se ejecuta un proceso que compara el pronóstico con el resultado oficial del campeón.
    *   Si hay acierto, se asignan 25 puntos al jugador y se persisten en la base de datos.
*   **Puntos de Historia:** 3

#### Historia de Usuario 10: Persistencia de Puntuación Total del Jugador
*   **Título:** Persistir la puntuación total acumulada de cada jugador
*   **Descripción:** Como sistema, quiero mantener un registro actualizado de la puntuación total de cada jugador en la base de datos, para poder mostrar la clasificación general de la quiniela.
*   **Criterios de Aceptación:**
    *   Existe un modelo de base de datos para `PuntuacionJugador` que incluye `id_jugador`, `puntuacion_total`.
    *   Después de cada cálculo de puntos (partido, bonos), la puntuación total del jugador se actualiza en la base de datos.
    *   Se puede recuperar la puntuación total de cualquier jugador.
*   **Puntos de Historia:** 2

#### Historia de Usuario 11: Procesamiento Asíncrono de Puntuación con Redis
*   **Título:** Implementar procesamiento asíncrono de cálculo de puntos con Redis
*   **Descripción:** Como sistema, quiero que el cálculo de puntos se realice de forma asíncrona utilizando colas de mensajes (Redis), para evitar cuellos de botella al procesar múltiples resultados de partidos simultáneamente y garantizar la escalabilidad.
*   **Criterios de Aceptación:**
    *   Cuando un resultado oficial de un partido es recibido, se publica un evento a una cola de Redis (ej. una lista).
    *   Existe un Worker (microservicio) que consume eventos de esta cola de Redis.
    *   El Worker es responsable de invocar la lógica de cálculo de puntos para todos los pronósticos de ese partido.
    *   El Worker actualiza las puntuaciones de los jugadores y la puntuación total.
    *   Se puede simular el envío de varios resultados de partidos y verificar que los Workers los procesan de forma asíncrona.
*   **Puntos de Historia:** 8

#### Historia de Usuario 12: Manejo de Partidos Suspendidos y Reanudados
*   **Título:** Implementar lógica para manejar partidos suspendidos y reanudados/postergados
*   **Descripción:** Como sistema, quiero que los pronósticos de los partidos suspendidos y luego reanudados o postergados se mantengan válidos y se puntúen normalmente una vez que se tenga un resultado oficial, para garantizar la equidad de los participantes.
*   **Criterios de Aceptación:**
    *   El sistema es capaz de actualizar la fecha y hora de inicio de un partido.
    *   Los pronósticos para el partido se mantienen en estado "pendiente" hasta que se registre un resultado oficial.
    *   Una vez registrado el resultado, el cálculo de puntos se realiza como un partido normal.
*   **Puntos de Historia:** 2

#### Historia de Usuario 13: Manejo de Partidos Cancelados o Suspendidos Indefinidamente
*   **Título:** Implementar lógica para anular pronósticos de partidos cancelados o suspendidos indefinidamente
*   **Descripción:** Como sistema, quiero que los pronósticos para partidos cancelados o suspendidos indefinidamente sean anulados (0 puntos), para reflejar que el evento no ocurrió a efectos de la quiniela.
*   **Criterios de Aceptación:**
    *   El sistema puede marcar un partido como "cancelado" o "anulado".
    *   Cuando un partido es marcado como "cancelado", los pronósticos asociados a ese partido no otorgan puntos a los jugadores.
    *   Se verifica que los jugadores no reciban puntos por pronósticos de partidos cancelados.
*   **Puntos de Historia:** 2

#### Historia de Usuario 14: Manejo de Resultados por Decisión Administrativa
*   **Título:** Implementar lógica para puntuar partidos con resultado por decisión administrativa
*   **Descripción:** Como sistema, quiero que los partidos con resultados por decisión administrativa (Walkover/Forfeit) se puntúen utilizando el resultado oficial declarado, para asegurar la consistencia con las reglas del torneo.
*   **Criterios de Aceptación:**
    *   El sistema permite registrar un resultado oficial para un partido, incluso si este es por decisión administrativa (ej. 3-0).
    *   El cálculo de puntos (acierto exacto, ganador/empate) se realiza normalmente con este resultado oficial.
    *   Se verifica que los jugadores obtengan puntos según el resultado administrativo declarado.
*   **Puntos de Historia:** 1

#### Historia de Usuario 15: Manejo de Cambios en Resultados Post-Partido
*   **Título:** Implementar lógica para considerar el resultado inicial oficial post-partido
*   **Descripción:** Como sistema, quiero que el resultado oficial de un partido inmediatamente después de su finalización sea el definitivo para el cálculo de puntos, ignorando cambios posteriores por apelaciones o sanciones, para simplificar el proceso y evitar reajustes constantes en la clasificación.
*   **Criterios de Aceptación:**
    *   El sistema registra el primer resultado oficial comunicado para un partido.
    *   Una vez calculados los puntos con ese resultado, cualquier modificación posterior del resultado oficial no afecta la puntuación ya asignada en la quiniela.
    *   Se verifica que la puntuación de los jugadores no cambia si el resultado oficial se modifica días después del partido.
*   **Puntos de Historia:** 1