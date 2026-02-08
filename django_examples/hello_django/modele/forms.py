from django import forms

from modele.models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ["name", "description"]

    def clean_name(self):
        self.cleaned_data["name"] = self.cleaned_data["name"].title()
        return self.cleaned_data["name"]


class DepartmentForm2(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()