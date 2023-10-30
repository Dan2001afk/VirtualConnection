from django import forms

class GraficaForm(forms.Form):
    dato_x = forms.CharField(label="Dato X")
    dato_y = forms.CharField(label="Dato Y")


    
class RegistrationForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data