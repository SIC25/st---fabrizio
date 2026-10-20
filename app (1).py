import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time

# Configuración de la página
st.set_page_config(
    page_title="Guía de Componentes Streamlit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🚀 Guía Completa de Componentes Streamlit")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("📋 Navegación")
sections = [
    "🎯 Elementos de Texto",
    "📊 Visualización de Datos",
    "🎮 Widgets Interactivos",
    "📝 Entrada de Datos",
    "📁 Carga de Archivos",
    "🎨 Layout y Contenedores",
    "📈 Gráficos y Charts",
    "💾 Estado de Sesión",
    "⚡ Funciones de Control"
]

selected_section = st.sidebar.selectbox("Selecciona una sección:", sections)

# Función para mostrar código
def show_code(code):
    st.code(code, language='python')

# SECCIÓN: Elementos de Texto
if selected_section == "🎯 Elementos de Texto":
    st.header("🎯 Elementos de Texto Más Utilizados")

    # st.title, st.header, st.subheader
    st.subheader("1. Títulos y Encabezados")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplo:**")
        st.title("Título Principal")
        st.header("Encabezado")
        st.subheader("Sub-encabezado")

    with col2:
        show_code("""
st.title("Título Principal")
st.header("Encabezado")
st.subheader("Sub-encabezado")
        """)

    # st.markdown
    st.subheader("2. Markdown y Texto Formateado")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplo:**")
        st.markdown("""
        **Texto en negrita**
        *Texto en cursiva*
        `Código inline`

        - Lista item 1
        - Lista item 2
        """)

    with col2:
        show_code("""
st.markdown('''
**Texto en negrita**
*Texto en cursiva*
`Código inline`

- Lista item 1
- Lista item 2
''')
        """)

    # st.write
    st.subheader("3. st.write() - El más versátil")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplo:**")
        st.write("Texto simple")
        st.write({"nombre": "Juan", "edad": 30})
        df_example = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        st.write(df_example)

    with col2:
        show_code("""
st.write("Texto simple")
st.write({"nombre": "Juan", "edad": 30})
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
st.write(df)
        """)

# SECCIÓN: Visualización de Datos
elif selected_section == "📊 Visualización de Datos":
    st.header("📊 Visualización de Datos")

    # DataFrame y métricas
    st.subheader("1. Mostrar DataFrames")

    # Crear datos de ejemplo
    df_sample = pd.DataFrame({
        'Producto': ['A', 'B', 'C', 'D', 'E'],
        'Ventas': [100, 200, 150, 300, 250],
        'Región': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    })

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**st.dataframe() - Interactivo:**")
        st.dataframe(df_sample, use_container_width=True)

        st.markdown("**st.table() - Estático:**")
        st.table(df_sample.head(3))

    with col2:
        show_code("""
df = pd.DataFrame({
    'Producto': ['A', 'B', 'C', 'D', 'E'],
    'Ventas': [100, 200, 150, 300, 250],
    'Región': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
})

st.dataframe(df, use_container_width=True)
st.table(df.head(3))
        """)

    # Métricas
    st.subheader("2. Métricas y KPIs")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Ventas Totales", "1,000", "10%")
    with col2:
        st.metric("Usuarios", "500", "-5%")
    with col3:
        st.metric("Ingresos", "$50K", "15%")
    with col4:
        st.metric("Conversión", "2.5%", "0.5%")

    show_code("""
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Ventas Totales", "1,000", "10%")
with col2:
    st.metric("Usuarios", "500", "-5%")
    """)

# SECCIÓN: Widgets Interactivos
elif selected_section == "🎮 Widgets Interactivos":
    st.header("🎮 Widgets Interactivos Más Populares")

    # Botones
    st.subheader("1. Botones")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")
        if st.button("Botón Simple"):
            st.success("¡Botón presionado!")

        if st.button("Procesar Datos", type="primary"):
            st.info("Procesando...")

    with col2:
        show_code("""
if st.button("Botón Simple"):
    st.success("¡Botón presionado!")

if st.button("Procesar", type="primary"):
    st.info("Procesando...")
        """)

    # Selectores
    st.subheader("2. Selectores")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")
        opcion = st.selectbox("Elige una opción:", ["Opción 1", "Opción 2", "Opción 3"])
        st.write(f"Seleccionaste: {opcion}")

        multiples = st.multiselect("Múltiples opciones:", ["A", "B", "C", "D"])
        st.write(f"Seleccionaste: {multiples}")

    with col2:
        show_code("""
opcion = st.selectbox(
    "Elige una opción:",
    ["Opción 1", "Opción 2", "Opción 3"]
)

multiples = st.multiselect(
    "Múltiples opciones:",
    ["A", "B", "C", "D"]
)
        """)

    # Sliders y inputs
    st.subheader("3. Sliders e Inputs")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")
        valor = st.slider("Selecciona valor:", 0, 100, 50)
        st.write(f"Valor: {valor}")

        numero = st.number_input("Ingresa número:", value=10)
        st.write(f"Número: {numero}")

        texto = st.text_input("Tu nombre:")
        if texto:
            st.write(f"Hola, {texto}!")

    with col2:
        show_code("""
valor = st.slider("Selecciona valor:", 0, 100, 50)
numero = st.number_input("Ingresa número:", value=10)
texto = st.text_input("Tu nombre:")

if texto:
    st.write(f"Hola, {texto}!")
        """)

# SECCIÓN: Entrada de Datos
elif selected_section == "📝 Entrada de Datos":
    st.header("📝 Entrada de Datos - Inputs y Formularios")

    # Inputs de texto
    st.subheader("1. Inputs de Texto")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")

        # Text input básico
        nombre = st.text_input("Nombre completo:", placeholder="Ingresa tu nombre")
        if nombre:
            st.write(f"Hola, **{nombre}**!")

        # Text input con password
        password = st.text_input("Contraseña:", type="password")
        if password:
            st.write("✅ Contraseña ingresada")

        # Text area para textos largos
        comentario = st.text_area(
            "Comentarios:",
            placeholder="Escribe tu comentario aquí...",
            height=100
        )
        if comentario:
            st.write(f"Comentario ({len(comentario)} caracteres): {comentario[:50]}...")

    with col2:
        show_code("""
# Input básico
nombre = st.text_input(
    "Nombre completo:",
    placeholder="Ingresa tu nombre"
)

# Input con contraseña
password = st.text_input(
    "Contraseña:",
    type="password"
)

# Área de texto
comentario = st.text_area(
    "Comentarios:",
    placeholder="Escribe aquí...",
    height=100
)
        """)

    # Inputs numéricos
    st.subheader("2. Inputs Numéricos")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")

        # Number input
        edad = st.number_input(
            "Edad:",
            min_value=0,
            max_value=120,
            value=25,
            step=1
        )
        st.write(f"Edad: {edad} años")

        # Number input con decimales
        precio = st.number_input(
            "Precio ($):",
            min_value=0.0,
            value=100.0,
            step=0.01,
            format="%.2f"
        )
        st.write(f"Precio: ${precio:.2f}")

        # Slider
        descuento = st.slider(
            "Descuento (%):",
            min_value=0,
            max_value=100,
            value=10,
            step=5
        )
        precio_final = precio * (1 - descuento/100)
        st.write(f"Precio con descuento: ${precio_final:.2f}")

        # Range slider
        rango_edad = st.select_slider(
            "Rango de edad:",
            options=["18-25", "26-35", "36-45", "46-55", "56+"],
            value="26-35"
        )
        st.write(f"Rango seleccionado: {rango_edad}")

    with col2:
        show_code("""
# Input numérico entero
edad = st.number_input(
    "Edad:",
    min_value=0,
    max_value=120,
    value=25,
    step=1
)

# Input numérico decimal
precio = st.number_input(
    "Precio ($):",
    min_value=0.0,
    value=100.0,
    step=0.01,
    format="%.2f"
)

# Slider
descuento = st.slider(
    "Descuento (%):",
    min_value=0,
    max_value=100,
    value=10
)

# Select slider
rango = st.select_slider(
    "Rango de edad:",
    options=["18-25", "26-35", "36-45"]
)
        """)

    # Selecciones
    st.subheader("3. Selectores y Opciones")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")

        # Selectbox
        pais = st.selectbox(
            "País:",
            ["México", "España", "Argentina", "Colombia", "Chile"]
        )
        st.write(f"País seleccionado: {pais}")

        # Multiselect
        hobbies = st.multiselect(
            "Hobbies:",
            ["Leer", "Deportes", "Música", "Viajar", "Cocinar", "Tecnología"],
            default=["Leer", "Tecnología"]
        )
        st.write(f"Hobbies: {', '.join(hobbies)}")

        # Radio buttons
        genero = st.radio(
            "Género:",
            ["Masculino", "Femenino", "Otro", "Prefiero no decir"],
            horizontal=True
        )
        st.write(f"Género: {genero}")

        # Checkbox
        acepta_terminos = st.checkbox("Acepto los términos y condiciones")
        newsletter = st.checkbox("Suscribirse al newsletter", value=True)

        if acepta_terminos:
            st.success("✅ Términos aceptados")

    with col2:
        show_code("""
# Selectbox
pais = st.selectbox(
    "País:",
    ["México", "España", "Argentina"]
)

# Multiselect
hobbies = st.multiselect(
    "Hobbies:",
    ["Leer", "Deportes", "Música"],
    default=["Leer"]
)

# Radio buttons
genero = st.radio(
    "Género:",
    ["Masculino", "Femenino", "Otro"],
    horizontal=True
)

# Checkbox
acepta = st.checkbox("Acepto términos")
newsletter = st.checkbox("Newsletter", value=True)
        """)

    # Fechas y tiempo
    st.subheader("4. Fechas y Tiempo")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")

        # Date input
        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento:",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        # Calcular edad
        if fecha_nacimiento:
            edad_calculada = (date.today() - fecha_nacimiento).days // 365
            st.write(f"Edad calculada: {edad_calculada} años")

        # Time input
        hora_reunion = st.time_input("Hora de reunión:")
        st.write(f"Reunión programada: {hora_reunion}")

        # Datetime input (combinando ambos)
        st.write("**Evento completo:**")
        col_fecha, col_hora = st.columns(2)
        with col_fecha:
            fecha_evento = st.date_input("Fecha del evento:")
        with col_hora:
            hora_evento = st.time_input("Hora del evento:")

        if fecha_evento and hora_evento:
            evento_completo = datetime.combine(fecha_evento, hora_evento)
            st.info(f"📅 Evento: {evento_completo.strftime('%d/%m/%Y a las %H:%M')}")

    with col2:
        show_code("""
from datetime import datetime, date

# Date input
fecha_nacimiento = st.date_input(
    "Fecha de nacimiento:",
    value=date(1990, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

# Time input
hora = st.time_input("Hora de reunión:")

# Combinando fecha y hora
fecha_evento = st.date_input("Fecha:")
hora_evento = st.time_input("Hora:")

evento = datetime.combine(fecha_evento, hora_evento)
        """)

    # Formulario completo
    st.subheader("5. Formulario Completo")

    st.markdown("**Ejemplo de formulario con st.form:**")

    with st.form("formulario_registro"):
        st.write("### 📋 Formulario de Registro")

        col1, col2 = st.columns(2)

        with col1:
            form_nombre = st.text_input("Nombre completo: *")
            form_email = st.text_input("Email: *", placeholder="usuario@email.com")
            form_telefono = st.text_input("Teléfono:")
            form_edad = st.number_input("Edad:", min_value=18, max_value=100, value=25)

        with col2:
            form_pais = st.selectbox("País:", ["México", "España", "Argentina", "Colombia"])
            form_profesion = st.selectbox("Profesión:", ["Estudiante", "Empleado", "Independiente", "Jubilado"])
            form_experiencia = st.slider("Años de experiencia:", 0, 30, 5)
            form_disponibilidad = st.radio("Disponibilidad:", ["Tiempo completo", "Medio tiempo", "Por proyectos"])

        form_comentarios = st.text_area("Comentarios adicionales:")
        form_acepta = st.checkbox("Acepto los términos y condiciones *")

        # Botón de submit
        submitted = st.form_submit_button("🚀 Registrarse", type="primary")

        if submitted:
            if form_nombre and form_email and form_acepta:
                st.success("✅ ¡Registro exitoso!")
                st.json({
                    "nombre": form_nombre,
                    "email": form_email,
                    "telefono": form_telefono,
                    "edad": form_edad,
                    "pais": form_pais,
                    "profesion": form_profesion,
                    "experiencia": form_experiencia,
                    "disponibilidad": form_disponibilidad,
                    "comentarios": form_comentarios
                })
            else:
                st.error("❌ Por favor completa todos los campos obligatorios (*)")

    # Código del formulario
    with st.expander("Ver código del formulario"):
        show_code("""
with st.form("formulario_registro"):
    st.write("### Formulario de Registro")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre: *")
        email = st.text_input("Email: *")
        telefono = st.text_input("Teléfono:")

    with col2:
        pais = st.selectbox("País:", ["México", "España"])
        profesion = st.selectbox("Profesión:", ["Estudiante", "Empleado"])

    acepta = st.checkbox("Acepto términos *")

    submitted = st.form_submit_button("Registrarse")

    if submitted:
        if nombre and email and acepta:
            st.success("¡Registro exitoso!")
        else:
            st.error("Completa campos obligatorios")
        """)

    # Tips y mejores prácticas
    st.subheader("💡 Tips y Mejores Prácticas")
    st.info("""
    **Para Entrada de Datos:**
    - Usa `placeholder` para dar ejemplos de formato
    - Establece `min_value` y `max_value` para validar rangos
    - Agrupa inputs relacionados en formularios con `st.form()`
    - Usa `st.columns()` para organizar inputs en diseño horizontal
    - Valida datos antes de procesarlos
    - Proporciona feedback inmediato al usuario
    """)

# SECCIÓN: Carga de Archivos
elif selected_section == "📁 Carga de Archivos":
    st.header("📁 Carga y Manejo de Archivos")

    st.subheader("1. st.file_uploader()")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplo:**")
        uploaded_file = st.file_uploader(
            "Sube un archivo CSV",
            type=['csv'],
            help="Solo archivos CSV permitidos"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head())
                st.success(f"Archivo cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
            except Exception as e:
                st.error(f"Error al leer archivo: {e}")

    with col2:
        show_code("""
uploaded_file = st.file_uploader(
    "Sube un archivo CSV",
    type=['csv'],
    help="Solo archivos CSV permitidos"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
        """)

    # Ejemplo con múltiples tipos
    st.subheader("2. Múltiples tipos de archivo")

    multi_files = st.file_uploader(
        "Sube múltiples archivos",
        type=['csv', 'xlsx', 'txt', 'json'],
        accept_multiple_files=True
    )

    if multi_files:
        st.write(f"Archivos subidos: {len(multi_files)}")
        for file in multi_files:
            st.write(f"- {file.name} ({file.type})")

# SECCIÓN: Layout y Contenedores
elif selected_section == "🎨 Layout y Contenedores":
    st.header("🎨 Layout y Contenedores")

    # Columnas
    st.subheader("1. Columnas (st.columns)")

    st.markdown("**Ejemplo de 3 columnas:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Columna 1")
        st.write("Contenido de la primera columna")

    with col2:
        st.success("Columna 2")
        st.write("Contenido de la segunda columna")

    with col3:
        st.warning("Columna 3")
        st.write("Contenido de la tercera columna")

    show_code("""
col1, col2, col3 = st.columns(3)

with col1:
    st.info("Columna 1")
    st.write("Contenido...")

with col2:
    st.success("Columna 2")

with col3:
    st.warning("Columna 3")
    """)

    # Tabs
    st.subheader("2. Pestañas (st.tabs)")

    tab1, tab2, tab3 = st.tabs(["📊 Datos", "📈 Gráficos", "⚙️ Configuración"])

    with tab1:
        st.write("Contenido de la pestaña de datos")
        st.dataframe(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}))

    with tab2:
        st.write("Contenido de gráficos")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
        st.line_chart(chart_data)

    with tab3:
        st.write("Configuraciones")
        st.slider("Parámetro 1", 0, 100, 50)

    # Expandir
    st.subheader("3. Secciones Expandibles")

    with st.expander("Ver más detalles"):
        st.write("Este contenido está oculto por defecto")
        st.json({"ejemplo": "datos", "valor": 123})

    # Contenedores
    st.subheader("4. Contenedores")

    container = st.container()
    container.write("Este es un contenedor")
    container.success("Mensaje en el contenedor")

# SECCIÓN: Gráficos y Charts
elif selected_section == "📈 Gráficos y Charts":
    st.header("📈 Gráficos y Visualizaciones")

    # Crear datos de ejemplo
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )

    # Gráficos básicos de Streamlit
    st.subheader("1. Gráficos Básicos de Streamlit")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Line Chart:**")
        st.line_chart(chart_data)

        st.markdown("**Bar Chart:**")
        st.bar_chart(chart_data['A'])

    with col2:
        show_code("""
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

st.line_chart(chart_data)
st.bar_chart(chart_data['A'])
        """)

    # Plotly
    st.subheader("2. Gráficos con Plotly")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Gráfico Interactivo:**")
        fig = px.scatter(
            x=chart_data.index,
            y=chart_data['A'],
            title="Gráfico de Dispersión"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        show_code("""
import plotly.express as px

fig = px.scatter(
    x=chart_data.index,
    y=chart_data['A'],
    title="Gráfico de Dispersión"
)
st.plotly_chart(fig, use_container_width=True)
        """)

    # Mapa
    st.subheader("3. Mapas")

    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [19.43, -99.13],  # Ciudad de México
        columns=['lat', 'lon']
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Mapa de puntos:**")
        st.map(map_data)

    with col2:
        show_code("""
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [19.43, -99.13],
    columns=['lat', 'lon']
)

st.map(map_data)
        """)

# SECCIÓN: Estado de Sesión
elif selected_section == "💾 Estado de Sesión":
    st.header("💾 Estado de Sesión (st.session_state)")

    st.subheader("¿Qué es el Session State?")
    st.write("Permite mantener variables entre ejecuciones de la app")

    # Contador ejemplo
    st.subheader("Ejemplo: Contador")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Funcionamiento:**")

        # Inicializar contador
        if 'contador' not in st.session_state:
            st.session_state.contador = 0

        # Botones para incrementar/decrementar
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("➕ Incrementar"):
                st.session_state.contador += 1
        with col_b:
            if st.button("➖ Decrementar"):
                st.session_state.contador -= 1
        with col_c:
            if st.button("🔄 Reset"):
                st.session_state.contador = 0

        st.metric("Contador", st.session_state.contador)

    with col2:
        show_code("""
# Inicializar
if 'contador' not in st.session_state:
    st.session_state.contador = 0

# Usar
if st.button("➕ Incrementar"):
    st.session_state.contador += 1

if st.button("➖ Decrementar"):
    st.session_state.contador -= 1

st.metric("Contador", st.session_state.contador)
        """)

    # Lista de tareas ejemplo
    st.subheader("Ejemplo: Lista de Tareas")

    # Inicializar lista
    if 'tareas' not in st.session_state:
        st.session_state.tareas = []

    col1, col2 = st.columns([2, 1])

    with col1:
        nueva_tarea = st.text_input("Nueva tarea:", key="input_tarea")

    with col2:
        if st.button("Agregar Tarea") and nueva_tarea:
            st.session_state.tareas.append(nueva_tarea)
            st.rerun()

    # Mostrar tareas
    if st.session_state.tareas:
        st.write("**Tareas:**")
        for i, tarea in enumerate(st.session_state.tareas):
            col_tarea, col_eliminar = st.columns([4, 1])
            with col_tarea:
                st.write(f"{i+1}. {tarea}")
            with col_eliminar:
                if st.button("🗑️", key=f"eliminar_{i}"):
                    st.session_state.tareas.pop(i)
                    st.rerun()

# SECCIÓN: Funciones de Control
elif selected_section == "⚡ Funciones de Control":
    st.header("⚡ Funciones de Control y Utilidades")

    # Progress bar
    st.subheader("1. Barras de Progreso")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplo:**")
        if st.button("Simular Proceso"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(101):
                progress_bar.progress(i)
                status_text.text(f'Progreso: {i}%')
                time.sleep(0.01)

            status_text.text('¡Completado!')
            st.success("Proceso terminado")

    with col2:
        show_code("""
if st.button("Simular Proceso"):
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(101):
        progress_bar.progress(i)
        status_text.text(f'Progreso: {i}%')
        time.sleep(0.01)

    st.success("Proceso terminado")
        """)

    # Alertas y mensajes
    st.subheader("2. Alertas y Mensajes")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Ejemplos:**")
        st.success("✅ Mensaje de éxito")
        st.info("ℹ️ Mensaje informativo")
        st.warning("⚠️ Mensaje de advertencia")
        st.error("❌ Mensaje de error")

    with col2:
        show_code("""
st.success("✅ Mensaje de éxito")
st.info("ℹ️ Mensaje informativo")
st.warning("⚠️ Mensaje de advertencia")
st.error("❌ Mensaje de error")
        """)

    # Spinner
    st.subheader("3. Spinner de Carga")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cargar con Spinner"):
            with st.spinner('Cargando...'):
                time.sleep(2)
            st.success('¡Listo!')

    with col2:
        show_code("""
if st.button("Cargar"):
    with st.spinner('Cargando...'):
        time.sleep(2)
    st.success('¡Listo!')
        """)

    # Balloons y snow
    st.subheader("4. Efectos Especiales")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎈 Globos"):
            st.balloons()

    with col2:
        if st.button("❄️ Nieve"):
            st.snow()

    with col3:
        st.write("Efectos de celebración")

# Footer
st.markdown("---")
st.markdown("""
### 📚 Recursos Adicionales

- [Documentación Oficial de Streamlit](https://docs.streamlit.io/)
- [Galería de Apps](https://streamlit.io/gallery)
- [Comunidad](https://discuss.streamlit.io/)

**💡 Tip:** Combina estos componentes para crear aplicaciones potentes e interactivas.
""")

# Información de la sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**💡 Tips:**
- Usa `st.write()` para mostrar cualquier cosa
- `st.session_state` para mantener datos
- Combina columnas y contenedores para layouts complejos
- Siempre prueba la responsividad
""")

st.sidebar.success("¡Explora cada sección para aprender más!")
