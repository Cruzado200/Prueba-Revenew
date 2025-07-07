from django.shortcuts import render
from .forms import CSVUploadForm
from .data_loader import DataLoader, InvalidCSVError
from .optimization_model import OptimizationModel
from .output_presenter import ResultsHandler

def upload_and_optimize(request):
    """
    Vista para subir el CSV, transformar datos, resolver el modelo y mostrar resultados.
    """
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            loader = DataLoader(request.FILES['csv_file'])
            try:
                df_ready = loader.load_and_transform()
            except InvalidCSVError as e:
                form.add_error('csv_file', f"Error leyendo CSV: {e}")
                return render(request, 'optimizador/upload.html', {'form': form})

            # Recogemos la preferencia del usuario:
            integer_only = form.cleaned_data['integer_solution']

            # Instanciamos el optimizador con el flag integer_only
            model = OptimizationModel(
                df_ready,
                loader.cap_machine1,
                loader.cap_machine2,
                integer=integer_only
            )
            solution = model.solve()

            context = ResultsHandler(
                solution,
                df_ready,
                loader.cap_machine1,
                loader.cap_machine2
            ).to_context()
            return render(request, 'optimizador/results.html', context)
    else:
        form = CSVUploadForm()

    return render(request, 'optimizador/upload.html', {'form': form})