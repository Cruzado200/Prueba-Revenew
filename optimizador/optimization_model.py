import pulp

class OptimizationModel:
    """
    Encapsula y resuelve el modelo de optimización:
    maximizar sum(revenue_i * x_i)
    sujeto a:
      sum(time_machine1_i * x_i) ≤ cap_machine1
      sum(time_machine2_i * x_i) ≤ cap_machine2
      x_i ≥ 0
    :contentReference[oaicite:0]{index=0}
    """

    def __init__(self, dataframe, cap_machine1, cap_machine2, integer=False):
        """
        :param dataframe: pandas.DataFrame con columnas
                          ['product','revenue','time_machine1','time_machine2']
        :param cap_machine1: capacidad total de la máquina 1 (float o int)
        :param cap_machine2: capacidad total de la máquina 2 (float o int)
        """
        self.df = dataframe
        self.cap1 = cap_machine1
        self.cap2 = cap_machine2
        self.integer = integer
        self.model = None
        self.decision_vars = None
        self.solution = None

    def solve(self):
        self.model = pulp.LpProblem("RevenueMaximization", pulp.LpMaximize)
        var_cat = pulp.LpInteger if self.integer else pulp.LpContinuous
        # 2) Crear variable x_<product> ≥ 0 para cada producto
        self.decision_vars = {
            row['product']: pulp.LpVariable(
                f"x_{row['product']}", lowBound=0, cat=var_cat
            )
            for _, row in self.df.iterrows()
        }

        # 3) Añadir función objetivo: Σ revenue * x
        self.model += pulp.lpSum(
            self.decision_vars[p] * float(self.df.loc[self.df['product']==p, 'revenue'])
            for p in self.decision_vars
        ), "TotalRevenue"

        # 4) Restricción de capacidad máquina 1: Σ time_machine1 * x ≤ cap1
        self.model += pulp.lpSum(
            self.decision_vars[p] * float(self.df.loc[self.df['product']==p, 'time_machine1'])
            for p in self.decision_vars
        ) <= self.cap1, "Machine1Capacity"

        # 5) Restricción de capacidad máquina 2: Σ time_machine2 * x ≤ cap2
        self.model += pulp.lpSum(
            self.decision_vars[p] * float(self.df.loc[self.df['product']==p, 'time_machine2'])
            for p in self.decision_vars
        ) <= self.cap2, "Machine2Capacity"

        self.model.solve()

        result = {p: var.value() for p, var in self.decision_vars.items()}
        result['TotalRevenue'] = pulp.value(self.model.objective)
        self.solution = result
        return result