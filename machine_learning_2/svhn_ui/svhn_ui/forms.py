from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(required=True)
    use_autocrop = forms.BooleanField(initial=True, required=False)
