import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool

# Configura aquí tu API KEY (puedes usar Gemini que es gratuita)
#os.environ["GEMINI_API_KEY"] = "AIzaSyApFM3sWqpCWX3ykjczb9mnZVOWPXYT-04"


gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key="AIzaSyApFM3sWqpCWX3ykjczb9mnZVOWPXYT-04"
)

file_tool = FileReadTool(file_path='especificaciones_quiniela.md')
# 1. Definimos los Agentes
arquitecto = Agent(
  role='Arquitecto de Soluciones Cloud',
  goal='Diseñar una infraestructura escalable para una quiniela en tiempo real.',
  backstory='Experto en arquitecturas distribuidas. Te enfocas en la consistencia de datos, '
        'sincronización de tiempos para apuestas y uso de colas de mensajes (Redis/RabbitMQ).'
        'Eres meticuloso. Tu prioridad es que el archivo de especificaciones refleje todos los acuerdos alcanzados.',
  llm=gemini_llm,
  tools=[file_tool],
  verbose=True, # Para que veas el "pensamiento" en la terminal
  allow_delegation=False
)

# 1. Definimos al Agente Product Owner
product_owner = Agent(
    role='Product Owner Senior',
    goal='Desglosar los requisitos técnicos en Historias de Usuario claras y estimadas.',
    backstory=(
        'Eres el puente entre la ingeniería y el producto. Sabes priorizar tareas '
        'técnicas para que el equipo de desarrollo pueda empezar a construir.'
        'Eres experto en metodologías Ágiles y Scrum. Tu habilidad consiste en '
        'tomar conceptos técnicos complejos y dividirlos en tareas pequeñas, '
        'asignándoles valor de negocio y puntos de historia (Fibonacci).'
    ),
    llm=gemini_llm,
    tools=[file_tool],
    verbose=True
)

# # 2. Definimos la Tarea

tarea_arquitectura = Task(
    description=(
        "1. Lee el archivo 'especificaciones_quiniela.md' para entender la lógica de puntos y reglas.\n"
        "2. Define el sistema de puntuación que se otorgara a los jugadores (acierta el resultado, acierta el ganador o empate) y aplicación de puntos por bono.\n"
        "Define las reglas que falten en 'especificaciones_quiniela.md' con respecto a logica de negocio (hasta cuando esta permitido enviar jugadas, cuando se hacen los calculos, como se otorgan los tickets, etc).\n"
        "3. Define el stack tecnológico (Sugerencia: NestJS, Angular, PostgreSQL).\n"
        "4. IMPORTANTE: Explica cómo manejaremos la sincronización de hora (NTP) para que nadie apueste "
        "después de iniciado un partido, y si necesitamos colas para procesar miles de resultados.\n"
        "5. Escribe estas decisiones en una nueva sección '## ARQUITECTURA TÉCNICA'.\ "
        "INTERACTÚA con el usuario para ajustar el diseño.\n"
        "NO TERMINES esta tarea hasta que el usuario diga explícitamente 'APROBADO'."
    ),
    expected_output="Propuesta técnica detallada sobre sistema de puntuacion, reglas de negocio, frameworks, infraestructura y sincronización validada por el usuario. El contenido completo del archivo .md actualizado con TODA la información del proyecto.",
    agent=arquitecto,
    human_input=True,
    output_file="especificaciones_quiniela.md",
    append=True,
    create_directory=True
)


# 2. Tarea de Refinamiento de Backlog
tarea_backlog = Task(
    description=(
        "Lee el archivo 'especificaciones_quiniela.md'.\n"
        "Basado en la 'ARQUITECTURA TÉCNICA' que acaba de definir el Arquitecto, "
        "crea el '## BACKLOG DE PRODUCTO' con historias de usuario para:\n"
        "- Configuración del entorno Docker y servicios.\n"
        "- Implementación del servicio de validación de tiempo.\n"
        "- Desarrollo de la lógica de puntos y persistencia.\n"
        "4. Cada Historia de Usuario debe tener: Título, Descripción (Como [rol] quiero [acción] para [beneficio]), "
        "Criterios de Aceptación y Puntos de Historia (1, 2, 3, 5, 8)."
    ),
    expected_output="Sección '## BACKLOG DE PRODUCTO' añadida con historias de usuario detalladas, valoradas.",
    agent=product_owner,
    output_file="especificaciones_quiniela.md",
    append=True, # Mantenemos la historia del archivo
    context=[tarea_arquitectura]
)

# 3. Formamos el equipo (de un solo integrante por ahora)
equipo = Crew(
  agents=[arquitecto, product_owner],
  tasks=[tarea_arquitectura, tarea_backlog],
  process="sequential",
  memory=True,
  memory_llm=gemini_llm, 
  verbose=True
)

# 4. ¡A trabajar!
resultado = equipo.kickoff()
print("\n\n########################")
print("## RESULTADO DEL AGENTE ##")
print("########################\n")
print(resultado)