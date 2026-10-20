import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time

# Se conservan los imports originales. Estos permiten leer imágenes y ZIP.
from io import BytesIO
from zipfile import ZipFile, BadZipFile
from PIL import Image, ImageOps, UnidentifiedImageError

st.set_page_config(page_title="ReCircular | Análisis de residuos", page_icon="♻️", layout="wide")
CLASES = ["Papel", "Cartón", "Plástico", "Vidrio", "Metal", "Otro / no identificado"]
COLORES = dict(zip(CLASES, ["#38bdf8", "#c99c63", "#2dd4bf", "#a78bfa", "#94a3b8", "#fb7185"]))
MAX_ARCHIVOS, MAX_BYTES, MAX_TOTAL = 50, 10 * 1024**2, 100 * 1024**2
Image.MAX_IMAGE_PIXELS = 20_000_000
COLUMNAS = ["id", "fecha", "iteracion", "archivo", "origen", "modo", "modelo", "prediccion", "confianza", "tiempo_ms", "etiqueta_real"]
PROBS = [f"p_{i}" for i in range(len(CLASES))]
TODAS = COLUMNAS + PROBS

st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1400px}
h1,h2,h3{letter-spacing:-.025em}
[data-testid="stMetric"]{border:1px solid #26384b;border-radius:14px;padding:16px}
[data-testid="stSidebar"]{border-right:1px solid #26384b}
.stButton button{border-radius:10px}
</style>""", unsafe_allow_html=True)

for clave, valor in {"historial": pd.DataFrame(columns=TODAS), "resultados": [], "carga_id": 0, "lote": 0}.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


def demo_20():
    """20 lotes ficticios de 10 imágenes. No son entrenamiento ni validación real."""
    rng = np.random.default_rng(42)
    filas = []
    for it in range(1, 21):
        for j in range(10):
            real = CLASES[int(rng.integers(len(CLASES)))]
            pred = real if rng.random() < .78 else str(rng.choice([c for c in CLASES if c != real]))
            conf = float(rng.uniform(45, 97))
            probs = rng.dirichlet(np.ones(len(CLASES) - 1)) * (100 - conf)
            p = list(probs)
            p.insert(CLASES.index(pred), conf)
            # Garantiza que la categoría informada sea la de mayor puntuación.
            pred = CLASES[int(np.argmax(p))]
            filas.append(dict(id=f"demo-{it}-{j}", fecha=f"{date.today().isoformat()}T10:{it:02d}:{j:02d}",
                              iteracion=it, archivo=f"ejemplo_{it:02d}_{j:02d}.jpg", origen="Dataset de ejemplo",
                              modo="Demostración", modelo="Simulador v1", prediccion=pred,
                              confianza=max(p), tiempo_ms=float(rng.uniform(80, 450)), etiqueta_real=real,
                              **dict(zip(PROBS, p))))
    return pd.DataFrame(filas, columns=TODAS)


def validar_tabla(df):
    if set(TODAS) - set(df.columns):
        raise ValueError("Faltan columnas. Utiliza la plantilla CSV exportada por esta aplicación.")
    df = df[TODAS].copy()
    if len(df) > 20000 or df.empty:
        raise ValueError("El CSV debe contener entre 1 y 20 000 registros.")
    for c in ["id", "archivo", "origen", "modo", "modelo", "prediccion", "etiqueta_real"]:
        df[c] = df[c].fillna("").astype(str)
    if df.id.eq("").any() or df.id.duplicated().any():
        raise ValueError("Cada registro requiere un id único y no vacío.")
    if not df.prediccion.isin(CLASES).all() or not df.etiqueta_real.isin([""] + CLASES).all():
        raise ValueError("Hay categorías desconocidas.")
    if not df.modo.isin(["Real", "Demostración"]).all():
        raise ValueError("Modo debe ser Real o Demostración.")
    pd.to_datetime(df.fecha, errors="raise", utc=True)
    for c in ["iteracion", "confianza", "tiempo_ms"] + PROBS:
        df[c] = pd.to_numeric(df[c], errors="raise")
        if not np.isfinite(df[c].to_numpy(dtype=float)).all():
            raise ValueError("No se permiten valores NaN o infinitos.")
    if (df.iteracion < 1).any() or (df.iteracion % 1 != 0).any() or (df.tiempo_ms < 0).any():
        raise ValueError("Iteración debe ser un entero positivo y tiempo_ms no negativo.")
    if not df[PROBS].ge(0).all().all() or not df[PROBS].le(100).all().all():
        raise ValueError("Las puntuaciones deben estar entre 0 y 100.")
    if not np.allclose(df[PROBS].sum(axis=1), 100, atol=.02):
        raise ValueError("Las puntuaciones por fila deben sumar 100 %.")
    if not np.allclose(df.confianza, df[PROBS].max(axis=1), atol=.02):
        raise ValueError("Confianza debe coincidir con la puntuación máxima.")
    maxima = df[PROBS].to_numpy().max(axis=1)
    indices = df.prediccion.map({c: i for i, c in enumerate(CLASES)}).to_numpy()
    if not np.allclose(df[PROBS].to_numpy()[np.arange(len(df)), indices], maxima, atol=.02):
        raise ValueError("La predicción debe tener la puntuación máxima.")
    df.iteracion = df.iteracion.astype(int)
    return df


def normalizar_imagen(datos):
    if len(datos) > MAX_BYTES:
        raise ValueError("Supera 10 MB por imagen.")
    with Image.open(BytesIO(datos)) as im:
        if im.width * im.height > 20_000_000:
            raise ValueError("Supera 20 megapíxeles.")
        im.load()
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((1600, 1600))
        return im.copy()


def cargar_imagenes(archivos, foto):
    imagenes, errores = [], []
    total, intentos = 0, 0

    def agregar(nombre, datos, origen):
        nonlocal total, intentos
        intentos += 1
        total += len(datos)
        if intentos > MAX_ARCHIVOS or total > MAX_TOTAL:
            raise ValueError("Límite de lote: 50 imágenes o 100 MB descomprimidos.")
        try:
            imagenes.append((nombre, normalizar_imagen(datos), origen))
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as e:
            errores.append(f"{nombre}: {e}")

    for f in archivos:
        if f.size > MAX_TOTAL:
            errores.append(f"{f.name}: el archivo supera 100 MB.")
            continue
        if f.name.lower().endswith(".zip"):
            try:
                with ZipFile(f) as z:
                    entries = [x for x in z.infolist() if not x.is_dir() and x.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
                    if not entries:
                        errores.append(f"{f.name}: no contiene imágenes compatibles.")
                    if len(entries) + intentos > MAX_ARCHIVOS or sum(x.file_size for x in entries) + total > MAX_TOTAL:
                        raise ValueError("ZIP supera el límite de 50 imágenes o 100 MB descomprimidos.")
                    for x in entries:
                        if x.file_size > MAX_BYTES:
                            errores.append(f"{x.filename}: supera 10 MB.")
                            continue
                        if x.flag_bits & 1:
                            errores.append(f"{x.filename}: imagen cifrada no admitida.")
                            continue
                        # Lee en memoria: nunca extrae rutas del ZIP al disco.
                        with z.open(x) as fuente:
                            datos = fuente.read(MAX_BYTES + 1)
                        agregar(x.filename, datos, "ZIP")
            except (BadZipFile, ValueError, RuntimeError, OSError, NotImplementedError) as e:
                errores.append(f"{f.name}: {e}")
        else:
            agregar(f.name, f.getvalue(), "Archivo")
    if foto:
        agregar("captura_camara.jpg", foto.getvalue(), "Cámara")
    return imagenes, errores


def predecir(imagen, modo, indice):
    if modo == "Demostración":
        rng = np.random.default_rng(indice + 137)
        valores = rng.dirichlet(np.ones(len(CLASES))) * .3
        valores[int(rng.integers(len(CLASES)))] += .7
        return valores, "Simulador v1"
    # Contrato del modelo real: predictor.predict(PIL.Image) -> dict.
    from predictor import predict
    salida = predict(imagen)
    if set(salida) != set(CLASES):
        raise ValueError("El modelo debe devolver exactamente las seis categorías configuradas.")
    valores = np.array([salida[c] for c in CLASES], dtype=float)
    if not np.isfinite(valores).all() or (valores < 0).any() or (valores > 1).any() or not np.isclose(valores.sum(), 1, atol=.001):
        raise ValueError("El modelo debe devolver probabilidades entre 0 y 1 que sumen 1.")
    return valores / valores.sum(), "Modelo conectado"


def exportar(df, nombre, key):
    st.download_button("Descargar CSV", df.to_csv(index=False).encode("utf-8-sig"), nombre, "text/csv", key=key)


def grafico(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=20, r=20, t=55, b=20), legend_title_text="")
    st.plotly_chart(fig, width="stretch")


def matriz_y_metricas(df):
    etiquetados = df[df.etiqueta_real.isin(CLASES)]
    if etiquetados.empty:
        st.info("Asigna etiquetas de referencia en Validación para evaluar aciertos y errores.")
        return
    cm = pd.crosstab(etiquetados.etiqueta_real, etiquetados.prediccion).reindex(index=CLASES, columns=CLASES, fill_value=0)
    exactitud = (etiquetados.prediccion == etiquetados.etiqueta_real).mean() * 100
    st.metric("Exactitud sobre imágenes etiquetadas", f"{exactitud:.1f}%", help="Aciertos / registros etiquetados × 100")
    st.caption(f"Base de evaluación: {len(etiquetados)} imágenes. Los registros sin etiqueta quedan excluidos.")
    grafico(px.imshow(cm, text_auto=True, labels=dict(x="Predicción", y="Etiqueta de referencia", color="Imágenes"),
                      color_continuous_scale="Teal", title="Matriz de confusión"))
    filas = []
    for c in CLASES:
        tp = cm.loc[c, c]
        predichos, reales = cm[c].sum(), cm.loc[c].sum()
        precision = tp / predichos if predichos else None
        recall = tp / reales if reales else None
        f1 = 2 * tp / (predichos + reales) if predichos + reales else None
        filas.append({"Residuo": c, "Precisión (%)": None if precision is None else precision * 100,
                      "Recall (%)": None if recall is None else recall * 100,
                      "F1 (%)": None if f1 is None else f1 * 100, "Soporte": int(reales)})
    tabla = pd.DataFrame(filas)
    st.dataframe(tabla.round(2), hide_index=True, width="stretch")
    st.caption("Precisión = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2TP/(2TP+FP+FN). Sin denominador se muestra vacío.")


st.sidebar.title("♻️ ReCircular")
st.sidebar.caption("Clasificación y evaluación de residuos")
selected_section = st.sidebar.radio("Navegación", ["Analizar residuos", "Dashboard", "Validación y datos"])
umbral = st.sidebar.slider("Umbral de revisión (%)", 0, 100, 75)
st.sidebar.caption("Una puntuación inferior al umbral se marca para revisión; no demuestra por sí sola un error.")
st.sidebar.divider()
st.sidebar.caption("Historial de esta sesión. Exporta el CSV para conservarlo antes de cerrar o recargar la sesión.")

if selected_section == "Analizar residuos":
    st.title("Del residuo a una decisión")
    st.write("Captura una foto o carga un lote y revisa la puntuación de cada categoría.")
    modo = st.radio("Modo de análisis", ["Demostración", "Real"], horizontal=True)
    if modo == "Demostración":
        st.warning("DEMOSTRACIÓN: las categorías y porcentajes son simulados; no reconocen el contenido de la foto.")
    else:
        st.info("Este modo requiere conectar tu modelo en predictor.py. Sin él, no se generan predicciones.")
    izquierda, derecha = st.columns(2)
    with izquierda:
        with st.container(border=True):
            st.subheader("Cámara")
            if st.toggle("Prender cámara", key=f"cam_toggle_{st.session_state.carga_id}"):
                foto = st.camera_input("Tomar una foto", key=f"cam_{st.session_state.carga_id}")
            else:
                foto = None
            st.caption("Captura de fotografía; no es análisis de video en vivo. Permite el acceso a la cámara en el navegador.")
    with derecha:
        with st.container(border=True):
            st.subheader("Fotos o ZIP")
            archivos = st.file_uploader("Selecciona archivos", type=["jpg", "jpeg", "png", "webp", "zip"],
                                        accept_multiple_files=True, key=f"files_{st.session_state.carga_id}")
            st.caption("Hasta 50 imágenes por lote · 10 MB por imagen · 100 MB descomprimidos. Una categoría principal por foto.")
    iniciar, limpiar = st.columns([2, 1])
    analizar = iniciar.button("Iniciar análisis", type="primary", width="stretch", disabled=not (archivos or foto))
    if limpiar.button("Limpiar carga y resultados", width="stretch"):
        st.session_state.carga_id += 1
        st.session_state.resultados = []
        st.rerun()
    if analizar:
        st.session_state.resultados = []
        try:
            imagenes, errores = cargar_imagenes(archivos, foto)
            for error in errores:
                st.warning(error)
            filas, resultados = [], []
            lote = max(st.session_state.lote, int(st.session_state.historial.iteracion.max()) if not st.session_state.historial.empty else 0) + 1
            progreso = st.progress(0, text="Procesando lote")
            for i, (nombre, im, origen) in enumerate(imagenes):
                inicio = time.perf_counter()
                try:
                    p, modelo = predecir(im, modo, i + lote * 100)
                except Exception as e:
                    st.error(f"No se pudo analizar {nombre}: {e}")
                    if modo == "Real":
                        break
                    continue
                fila = dict(id=f"{time.time_ns()}-{i}", fecha=datetime.now().astimezone().isoformat(),
                            iteracion=lote, archivo=nombre, origen=origen, modo=modo, modelo=modelo,
                            prediccion=CLASES[int(np.argmax(p))], confianza=float(max(p) * 100),
                            tiempo_ms=(time.perf_counter() - inicio) * 1000, etiqueta_real="", **dict(zip(PROBS, p * 100)))
                filas.append(fila)
                resultados.append((im, fila))
                progreso.progress((i + 1) / len(imagenes), text=f"Imagen {i + 1} de {len(imagenes)}")
            progreso.empty()
            if filas:
                st.session_state.historial = pd.concat([st.session_state.historial, pd.DataFrame(filas)], ignore_index=True)
                st.session_state.resultados = resultados
                st.session_state.lote = lote
                st.success(f"Lote {lote} guardado en el historial: {len(filas)} imágenes.")
            elif not errores:
                st.info("No se generaron resultados.")
        except (ValueError, OSError) as e:
            st.error(str(e))
    st.subheader("Resultados del último análisis")
    if not st.session_state.resultados:
        st.info("Tus resultados aparecerán aquí después de iniciar el análisis.")
    for im, fila in st.session_state.resultados:
        with st.expander(f"{fila['archivo']} · {fila['prediccion']} · {fila['confianza']:.1f}%", expanded=len(st.session_state.resultados) == 1):
            a, b = st.columns([1, 2])
            a.image(im, width=260)
            b.write(f"**Modo:** {fila['modo']} · **Tiempo de inferencia:** {fila['tiempo_ms']:.1f} ms")
            if fila['confianza'] < umbral:
                b.warning("Requiere revisión por puntuación baja.")
            else:
                b.success("Supera el umbral configurado.")
            tabla = pd.DataFrame({"Residuo": CLASES, "Puntuación (%)": [fila[p] for p in PROBS]})
            with b:
                grafico(px.bar(tabla, x="Puntuación (%)", y="Residuo", orientation="h", color="Residuo",
                               color_discrete_map=COLORES, range_x=[0, 100]))
            st.caption("Puntuación del modelo o simulador; no equivale a exactitud medida ni a probabilidad calibrada. No se detectan objetos individuales.")
    st.subheader("Historial")
    h = st.session_state.historial
    if not h.empty:
        st.dataframe(h[COLUMNAS].iloc[::-1], hide_index=True, width="stretch")
        exportar(h, "historial_reciclaje.csv", "export_main")
    else:
        st.caption("Todavía no hay análisis en esta sesión.")

elif selected_section == "Dashboard":
    st.title("Resultados y desempeño")
    fuente = st.radio("Datos", ["Ejemplo · 20 iteraciones", "Historial de sesión"], horizontal=True)
    if fuente.startswith("Ejemplo"):
        df = demo_20()
        st.warning("DATOS SINTÉTICOS: 20 lotes de ejemplo, con 10 imágenes ficticias por lote. No son épocas de entrenamiento ni resultados reales.")
    else:
        df = st.session_state.historial.copy()
    if df.empty:
        st.info("Analiza imágenes o importa un historial en la tercera vista.")
    else:
        a, b, c, d = st.columns(4)
        modos = a.multiselect("Modo", sorted(df.modo.unique()), default=sorted(df.modo.unique()))
        categorias = b.multiselect("Residuo predicho", CLASES, default=CLASES)
        rango = c.slider("Puntuación (%)", 0, 100, (0, 100))
        estado = d.selectbox("Revisión", ["Todos", "Bajo umbral", "Sobre umbral"])
        ids = sorted(df.iteracion.unique().tolist())
        iteraciones = st.multiselect("Iteraciones / lotes", ids, default=ids[-20:])
        df = df[df.modo.isin(modos) & df.prediccion.isin(categorias) & df.confianza.between(*rango) & df.iteracion.isin(iteraciones)]
        if estado != "Todos":
            df = df[df.confianza < umbral] if estado == "Bajo umbral" else df[df.confianza >= umbral]
        if df.empty:
            st.info("No hay registros para estos filtros.")
        else:
            if df.modo.nunique() > 1:
                st.warning("La selección mezcla resultados reales y simulados. Filtra por modo para evaluar el sistema real.")
            a, b, c, d = st.columns(4)
            a.metric("Imágenes", len(df))
            b.metric("Puntuación media", f"{df.confianza.mean():.1f}%")
            c.metric("Inferencia media", f"{df.tiempo_ms.mean():.1f} ms")
            d.metric("Bajo umbral", f"{(df.confianza < umbral).mean() * 100:.1f}%")
            resumen = df.groupby("iteracion", as_index=False).agg(puntuacion=("confianza", "mean"), tiempo_ms=("tiempo_ms", "mean"), imagenes=("id", "count"))
            a, b = st.columns(2)
            with a:
                conteo = df.prediccion.value_counts().rename_axis("Residuo").reset_index(name="Imágenes")
                grafico(px.bar(conteo, x="Residuo", y="Imágenes", color="Residuo", color_discrete_map=COLORES, title="Distribución por residuo"))
                grafico(px.line(resumen, x="iteracion", y="puntuacion", markers=True, range_y=[0, 100], title="Puntuación media por iteración"))
                grafico(px.scatter(df, x="tiempo_ms", y="confianza", color="prediccion", color_discrete_map=COLORES, hover_data=["archivo", "iteracion", "modo"], title="Puntuación frente a latencia"))
            with b:
                grafico(px.histogram(df, x="confianza", nbins=15, color_discrete_sequence=["#2dd4bf"], range_x=[0, 100], title="Distribución de puntuaciones"))
                grafico(px.box(df, x="prediccion", y="tiempo_ms", color="prediccion", color_discrete_map=COLORES, title="Latencia por categoría"))
                fig = go.Figure(go.Bar(x=resumen.iteracion, y=resumen.imagenes, marker_color="#38bdf8"))
                fig.update_layout(title="Volumen por iteración", xaxis_title="Iteración", yaxis_title="Imágenes")
                grafico(fig)
            st.subheader("Eficacia con etiquetas de referencia")
            matriz_y_metricas(df)
            exportar(df, "dashboard_filtrado.csv", "export_dash")
            st.caption("Los filtros se aplican a todos los gráficos y métricas. Filtrar por predicción o puntuación cambia la muestra de evaluación.")

else:
    st.title("Validación y datos")
    st.write("Contrasta predicciones con etiquetas de referencia y conserva tus análisis.")
    h = st.session_state.historial.copy()
    with st.expander("Importar historial CSV", expanded=h.empty):
        st.caption("Importa el esquema completo de un CSV exportado por esta app. Se agrega por id, sin duplicar registros existentes.")
        exportar(pd.DataFrame(columns=TODAS), "plantilla_historial.csv", "plantilla")
        archivo_csv = st.file_uploader("Historial exportado", type=["csv"], key="import_csv")
        if st.button("Importar CSV", disabled=archivo_csv is None):
            try:
                if archivo_csv.size > 20 * 1024**2:
                    raise ValueError("El CSV supera 20 MB.")
                nuevo = validar_tabla(pd.read_csv(archivo_csv))
                nuevo = nuevo[~nuevo.id.isin(h.id)]
                st.session_state.historial = pd.concat([h, nuevo], ignore_index=True)
                st.success(f"Se agregaron {len(nuevo)} registros. Las etiquetas y el modo proceden del CSV; no se autentican externamente.")
                h = st.session_state.historial.copy()
            except Exception as e:
                st.error(f"No se pudo importar: {e}")
    if not h.empty:
        st.subheader("Etiquetas de referencia")
        st.caption("Consulta la imagen original antes de etiquetar. Las imágenes se muestran en la vista de análisis solo para el último lote; el CSV conserva datos, no fotografías.")
        vista = st.radio("Registros para validar", ["Real", "Demostración"], horizontal=True)
        seleccion = h[h.modo == vista]
        if not seleccion.empty:
            with st.form("etiquetas"):
                editor = st.data_editor(seleccion[["id", "archivo", "prediccion", "confianza", "etiqueta_real"]], hide_index=True,
                                        disabled=["id", "archivo", "prediccion", "confianza"],
                                        column_config={"etiqueta_real": st.column_config.SelectboxColumn("Etiqueta de referencia", options=[""] + CLASES)},
                                        width="stretch")
                guardar = st.form_submit_button("Guardar etiquetas", type="primary")
            if guardar:
                mapa = editor.set_index("id").etiqueta_real.fillna("")
                mask = h.id.isin(mapa.index)
                h.loc[mask, "etiqueta_real"] = h.loc[mask, "id"].map(mapa)
                st.session_state.historial = h
                seleccion = h[h.modo == vista]
                st.success("Etiquetas guardadas en esta sesión.")
            matriz_y_metricas(seleccion)
        else:
            st.info("No hay registros del modo seleccionado.")
        exportar(h, "historial_validado.csv", "export_valid")
        with st.expander("Borrar historial de esta sesión"):
            confirmar = st.checkbox("Quiero eliminar el historial de esta sesión")
            if st.button("Borrar historial", disabled=not confirmar):
                st.session_state.historial = pd.DataFrame(columns=TODAS)
                st.session_state.resultados = []
                st.session_state.lote = 0
                st.rerun()
    with st.expander("Cómo interpretar los resultados"):
        st.markdown("""- **Puntuación:** valor que asigna el modelo a una categoría; no es una medida de exactitud.
- **Exactitud:** proporción de predicciones que coinciden con etiquetas de referencia.
- **Latencia:** tiempo de llamada al predictor por imagen; excluye lectura, gráficos y carga de archivos. En demostración se mide el simulador; el dashboard de ejemplo usa tiempos ficticios.
- **Iteración:** un lote de análisis, no una época de entrenamiento. El dashboard selecciona los últimos 20 lotes por defecto.
- **Alcance:** clasificación de una categoría principal por fotografía, sin cajas de detección ni validación de reciclabilidad local.
- **Historial:** temporal por sesión; usa exportación/importación CSV para conservarlo. Para persistencia compartida se necesita una base de datos.
""")
