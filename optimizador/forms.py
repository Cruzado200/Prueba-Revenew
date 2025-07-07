from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Archivo CSV",
        help_text="Sube tu CSV con la estructura aplanada de productos y capacidades."
    )
    integer_solution = forms.BooleanField(
        required=False,
        label="Solución entera",
        help_text="Activa para que las cantidades sean enteras; desactiva para permitir decimales."
    )
