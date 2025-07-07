# Prueba Revenew

Proyecto Django para procesamiento de un CSV aplanado de productos y capacidades, resolución de un modelo de optimización lineal (máximo ingreso) y visualización de resultados.

## Contexto de negocio

Este proyecto permite a los responsables de producción determinar la asignación óptima de horas de máquina entre diferentes productos, maximizando el ingreso total y garantizando que no se superen las capacidades disponibles. Al usar un modelo de programación lineal, se obtienen beneficios como:

* **Maximización de ingresos**: Identifica la combinación de productos que genera la mayor rentabilidad.
* **Uso eficiente de recursos**: Asegura que cada máquina opere dentro de sus límites y evita tiempos ociosos.
* **Toma de decisiones basada en datos**: Proporciona resultados cuantitativos que respaldan la planificación de la producción.
* **Reducción de costos operativos**: Minimiza desperdicios y sobrecargas al optimizar la carga de trabajo.
* **Escalabilidad**: El mismo método puede adaptarse a más productos o a restricciones adicionales.

## Características

* Carga y transformación de un CSV con columnas:

  * `Product_<X>_Production_Time_Machine_1`
  * `Product_<X>_Production_Time_Machine_2`
  * `Price_Product_<X>`
  * `Machine_1_Available_Hours`
  * `Machine_2_Available_Hours`
* Modelo de optimización formulado con PuLP para maximizar ingresos sujeto a restricciones de capacidad de dos máquinas.
* Exportación de resultados en:

  * Tabla de cantidades óptimas por producto.
  * Gráficos de barras:
    * Cantidad óptima por producto.
    * Uso de horas en cada máquina con línea de capacidad.
* Pruebas unitarias para `DataLoader`, `OptimizationModel` y vistas.
* Se agregó un Slicer para saber si las soluciones esperadas son enteras o son del tipo decimal.
* Se realizó un frontend más pulcro para poder tener una vista más sofisticada.
* Se entrega una vista ejecutiva para el resultado, fomentando la toma de decisiones estratégicas.
  
## Requisitos

* Python 3.10+
* Virtualenv
* Django 4.x
* Pandas
* PuLP
* Matplotlib

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/Cruzado200/Prueba_Revenew.git
cd "Prueba Revenew"

# Crear y activar entorno virtual
python3.10 -m venv venv
venv\Scripts\activate     

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

En `revenew_project/settings.py`, verifica:

```python
TIME_ZONE = 'America/Santiago'
LANGUAGE_CODE = 'es-cl'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Uso

1. Ejecutar migraciones :

   ```bash
   python manage.py migrate
   ```
2. Iniciar servidor:

   ```bash
   python manage.py runserver
   ```
3. Abrir navegador en `http://127.0.0.1:8000/`.
4. Subir el CSV aplanado y ver resultados y gráficos.

## Estructura del proyecto

```text
Prueba Revenew/
├── manage.py
├── requirements.txt
├── revenew_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── optimizador/
    ├── data_loader.py
    ├── optimization_model.py
    ├── output_presenter.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── templates/optimizador/
    │   ├── upload.html
    │   └── results.html
    └── tests.py
```

## Pruebas

Para ejecutar el suite de tests:

```bash
python manage.py test optimizador
```
El archivo `optimizador/tests.py` define seis pruebas unitarias organizadas en tres clases:

1. **DataLoaderTestCase**
   - `test_load_and_transform_valid`: Verifica la carga y transformación de un CSV válido, comprobando columnas, filas y extracción de capacidades.
   - `test_missing_column_raises`: Asegura que la ausencia de una columna esencial lance `InvalidCSVError`.

2. **OptimizationModelTestCase**
   - `test_solve_simple_max_revenue`: Prueba un caso sencillo donde el producto con mayor revenue ocupa toda la capacidad disponible.

3. **ViewsTestCase**
   - `test_get_upload_form`: Comprueba que el `GET` a la raíz muestra el formulario de carga.
   - `test_post_valid_file`: Verifica que un `POST` con un CSV válido renderice los resultados con "Ingreso Total Óptimo".
   - `test_post_invalid_file`: Valida que un CSV corrupto re-renderice el formulario con un error en `csv_file` que comienza con "Error leyendo CSV".
