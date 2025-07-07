import os
import uuid
import matplotlib.pyplot as plt
from django.conf import settings

class ResultsHandler:
    """
    Formatea la solución y genera:
      - Tabla con la cantidad de cada uno de los productos junto con el ingreso por producto.
      - gráfico de uso de Máquina 1 
      - gráfico de uso de Máquina 2 
      - gráfico de cantidades óptimas por producto
    """
    def __init__(self, solution: dict, dataframe, cap_machine1, cap_machine2):
        self.solution = solution
        self.df = dataframe
        self.cap1 = cap_machine1
        self.cap2 = cap_machine2

    def to_context(self) -> dict:
        """
        Prepara URLs de los gráficos de uso por máquina y de cantidades.
        Prepara los datos para mostrar la información
        """
        total = round(self.solution.get('TotalRevenue', 0),2)
        table_data = []
        for prod, qty in self.solution.items():
            if prod == 'TotalRevenue':
                continue
            unit_rev = round(float(self.df.loc[self.df['product'] == prod, 'revenue'].iloc[0]),2)
            ingreso = qty * unit_rev
            table_data.append({
                'product': prod,
                'quantity': qty,
                'income': ingreso
            })
        chart_url_m1 = self._generate_stacked_usage_chart('time_machine1', 'Máquina 1', self.cap1)
        chart_url_m2 = self._generate_stacked_usage_chart('time_machine2', 'Máquina 2', self.cap2)
        chart_url_qty = self._generate_qty_chart()

        return {
            'table_data': table_data,
            'total_revenue': total,
            'chart_url_m1': chart_url_m1,
            'chart_url_m2': chart_url_m2,
            'chart_url_qty': chart_url_qty,
        }

    def _generate_stacked_usage_chart(self, time_col: str, machine_label: str, capacity: float) -> str:
        """
        Genera un gráfico de barras apiladas con una sola barra que muestra
        el uso de horas segmentado por producto para la máquina indicada.
        Incluye línea de capacidad.
        """
        products = []
        usages = []
        for prod, qty in self.solution.items():
            if prod == 'TotalRevenue':
                continue
            tiempo = float(self.df.loc[self.df['product'] == prod, time_col].iloc[0])
            products.append(prod)
            usages.append(qty * tiempo)

        fig, ax = plt.subplots()
        bottom = 0
        for prod, usage in zip(products, usages):
            ax.bar([0], [usage], bottom=bottom, label=prod)
            bottom += usage

        ax.axhline(capacity, linestyle='--', color='black', label=f'Capacidad ({capacity})')
        ax.set_xticks([0])
        ax.set_xticklabels([machine_label])
        ax.set_ylabel('Horas usadas')
        ax.set_title(f'Uso {machine_label}')
        ax.legend()

        filename = f"{time_col}_{uuid.uuid4().hex}.png"
        full_path = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        fig.savefig(full_path)
        plt.close(fig)

        return os.path.join(settings.MEDIA_URL, filename)

    def _generate_qty_chart(self) -> str:
        """
        Genera un gráfico de barras que muestra la cantidad óptima de cada producto.
        """
        products = []
        qtys = []
        for prod, qty in self.solution.items():
            if prod == 'TotalRevenue':
                continue
            products.append(prod)
            qtys.append(qty)

        fig, ax = plt.subplots()
        ax.bar(products, qtys)
        ax.set_xlabel('Producto')
        ax.set_ylabel('Cantidad óptima')
        ax.set_title('Cantidades Óptimas por Producto')

        filename = f"qty_{uuid.uuid4().hex}.png"
        full_path = os.path.join(settings.MEDIA_ROOT, filename)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        fig.savefig(full_path)
        plt.close(fig)

        return os.path.join(settings.MEDIA_URL, filename)
