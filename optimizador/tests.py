from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from io import StringIO
import pandas as pd

from optimizador.data_loader import DataLoader, InvalidCSVError
from optimizador.optimization_model import OptimizationModel
from optimizador.output_presenter import ResultsHandler

class DataLoaderTestCase(TestCase):
    def setUp(self):
        # CSV válido con dos productos A y B
        self.valid_csv = (
            "Product_A_Production_Time_Machine_1,Product_A_Production_Time_Machine_2,"
            "Product_B_Production_Time_Machine_1,Product_B_Production_Time_Machine_2,"
            "Machine_1_Available_Hours,Machine_2_Available_Hours,"
            "Price_Product_A,Price_Product_B\n"
            "1.5,2.0,1.0,1.5,8,10,100,80\n"
        )

    def test_load_and_transform_valid(self):
        loader = DataLoader(StringIO(self.valid_csv))
        df = loader.load_and_transform()
        # Columnas esperadas
        self.assertListEqual(list(df.columns), ['product', 'revenue', 'time_machine1', 'time_machine2'])
        # Dos filas
        self.assertEqual(len(df), 2)
        # Capacidades
        self.assertAlmostEqual(loader.cap_machine1, 8.0)
        self.assertAlmostEqual(loader.cap_machine2, 10.0)

    def test_missing_column_raises(self):
        invalid_csv = (
            "Product_A_Production_Time_Machine_1,Machine_1_Available_Hours,"
            "Machine_2_Available_Hours,Price_Product_A\n"
            "1.5,8,10,100\n"
        )
        loader = DataLoader(StringIO(invalid_csv))
        with self.assertRaises(InvalidCSVError):
            loader.load_and_transform()

class OptimizationModelTestCase(TestCase):
    def test_solve_simple_max_revenue(self):
        # Datos con igual uso pero distinto revenue
        data = {
            'product': ['A', 'B'],
            'revenue': [100, 80],
            'time_machine1': [1, 1],
            'time_machine2': [1, 1],
        }
        df = pd.DataFrame(data)
        model = OptimizationModel(df, cap_machine1=10, cap_machine2=10)
        sol = model.solve()
        # Debe asignar todo a A (mayor revenue)
        self.assertAlmostEqual(sol['A'], 10)
        self.assertAlmostEqual(sol['B'], 0)
        self.assertAlmostEqual(sol['TotalRevenue'], 1000)

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('optimizador_process')
        # Definir un CSV válido similar al TestCase de DataLoader
        self.valid_csv = (
            "Product_A_Production_Time_Machine_1,Product_A_Production_Time_Machine_2,"
            "Product_B_Production_Time_Machine_1,Product_B_Production_Time_Machine_2,"
            "Machine_1_Available_Hours,Machine_2_Available_Hours,"
            "Price_Product_A,Price_Product_B\n"
            "1.5,2.0,1.0,1.5,8,10,100,80\n"
        )
        self.valid_file = SimpleUploadedFile(
            'test.csv', self.valid_csv.encode('utf-8'), content_type='text/csv'
        )

    def test_get_upload_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subir archivo CSV')

    def test_post_valid_file(self):
        response = self.client.post(self.url, {'csv_file': self.valid_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ingreso Total Óptimo')

    def test_post_invalid_file(self):
        invalid_file = SimpleUploadedFile('bad.csv', b'invalid', content_type='text/csv')
        response = self.client.post(self.url, {'csv_file': invalid_file})
        # La vista debería devolver el formulario con errores en csv_file
        self.assertEqual(response.status_code, 200)
        # Verificamos que el contexto incluya la clave 'form'
        self.assertIn('form', response.context)
        form = response.context['form']
        # El formulario debe estar vinculado y con error en csv_file
        self.assertTrue(form.is_bound)
        self.assertTrue(form.has_error('csv_file'))
        # Y el mensaje debe empezar con nuestro prefijo
        error_msg = form.errors['csv_file'][0]
        self.assertTrue(error_msg.startswith('Error leyendo CSV'))
