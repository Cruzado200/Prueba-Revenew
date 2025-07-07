import pandas as pd

class InvalidCSVError(Exception):
    pass

class DataLoader:
    """
    Lee un CSV con la estructura:
      - Product_<X>_Production_Time_Machine_1
      - Product_<X>_Production_Time_Machine_2
      - Price_Product_<X>
      - Machine_1_Available_Hours
      - Machine_2_Available_Hours

    Y devuelve:
      - df con columnas [product, revenue, time_machine1, time_machine2]
      - cap_machine1, cap_machine2
    """
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self._raw = None
        self.df = None
        self.cap_machine1 = None
        self.cap_machine2 = None

    def load(self):
        try:
            self._raw = pd.read_csv(self.csv_file)
        except Exception as e:
            raise InvalidCSVError(f"Error leyendo CSV: {e}")
        return self._raw

    def transform(self):
        raw = self._raw if self._raw is not None else self.load()

        # Extraer capacidades (primera fila)
        try:
            self.cap_machine1 = float(raw['Machine_1_Available_Hours'].iloc[0])
            self.cap_machine2 = float(raw['Machine_2_Available_Hours'].iloc[0])
        except KeyError as e:
            raise InvalidCSVError(f"Falta columna de capacidad: {e}")

        # Detectar nombres de productos a partir de precios
        products = []
        for col in raw.columns:
            if col.startswith('Price_Product_'):
                products.append(col.replace('Price_Product_', ''))

        if not products:
            raise InvalidCSVError("No se encontraron columnas de Price_Product_<X>")

        # Construir nuevo DataFrame
        data = {'product': [], 'revenue': [], 'time_machine1': [], 'time_machine2': []}
        for p in products:
            try:
                rev = float(raw[f'Price_Product_{p}'].iloc[0])
                t1  = float(raw[f'Product_{p}_Production_Time_Machine_1'].iloc[0])
                t2  = float(raw[f'Product_{p}_Production_Time_Machine_2'].iloc[0])
            except KeyError as e:
                raise InvalidCSVError(f"Falta columna esperada para producto {p}: {e}")
            data['product'].append(p)
            data['revenue'].append(rev)
            data['time_machine1'].append(t1)
            data['time_machine2'].append(t2)

        self.df = pd.DataFrame(data)
        return self.df

    def load_and_transform(self):
        self.load()
        return self.transform()
