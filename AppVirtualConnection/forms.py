from django import forms

class GraficaForm(forms.Form):
    dato_x = forms.CharField(label="Dato X")
    dato_y = forms.CharField(label="Dato Y")