"""Conecta aquí tu modelo entrenado. No genera predicciones ficticias."""


def predict(image):
    """Recibe PIL.Image RGB y devuelve probabilidades (0–1) que suman 1.

    Debe devolver estas claves exactamente:
    Papel, Cartón, Plástico, Vidrio, Metal, Otro / no identificado.
    Implementa el preprocesamiento y el orden de clases de TU modelo.
    Si necesita TensorFlow, PyTorch u ONNX, agrégalo a requirements.txt.
    Carga el modelo una sola vez, por ejemplo usando st.cache_resource.
    """
    raise NotImplementedError("Falta conectar un modelo entrenado en predictor.py. Utiliza Demostración para probar la interfaz.")
