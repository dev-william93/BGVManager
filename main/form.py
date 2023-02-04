from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = employee_store
        fields = ("candidate", "education", "employment", "aadhar", "pan", "passport", "address", "employment_file", "education_file", "passport_file", "aadhar_file", "form16_file")
        labels = {'passport': 'Passport Number', 'address': 'Present Address From To', 'form16_file': 'Form 16', 'aadhar_file': 'Aadhar File', 'employment_file': 'Employment', 'education_file': 'Education'}
        widgets = {
            "education" : forms.TextInput(attrs={'class': 'form-control'}),
            "employment" : forms.TextInput(attrs={'class': 'form-control'}),
            "aadhar" : forms.TextInput(attrs={'class': 'form-control'}),
            "pan" : forms.TextInput(attrs={'class': 'form-control'}),
            "passport" : forms.TextInput(attrs={'class': 'form-control'}),
            "address" : forms.Textarea(attrs={'class': 'form-control', 'spellcheck': 'true'}),
            "education" : forms.TextInput(attrs={'class': 'form-control'}),
            "employment" : forms.TextInput(attrs={'class': 'form-control'}),

            "candidate" : forms.Select(attrs={'class': 'form-control'}),
            "education_status" : forms.Select(attrs={'class': 'form-control'}),
            "employment_status" : forms.Select(attrs={'class': 'form-control'}),

            "form16_file" : forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': "application/pdf,application/msword,.doc,.docx"}),
            "aadhar_file" : forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': "application/pdf,application/msword,.doc,.docx"}),
            "employment_file" : forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': "application/pdf,application/msword,.doc,.docx"}),
            "education_file" : forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': "application/pdf,application/msword,.doc,.docx"}),
            "passport_file" : forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true', 'accept': "application/pdf,application/msword,.doc,.docx"}),
        }
        
    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                obj = self.model.objects.create(file=f)
        return super(EmployeeForm, self).form_valid(form)
    
    def clean_pan(self):
        pan = self.cleaned_data['pan']
        if len(pan)<9:
            raise forms.ValidationError("Pan Number must contain 10 digits.")
        return pan
    def clean_aadhar(self):
        aadhar = self.cleaned_data['aadhar']
        if len(aadhar)<11 or  not aadhar.isdigit():
            raise forms.ValidationError("Adhar Number must contain 12 digits and integer input")
        return aadhar
class VerificationForm(forms.ModelForm):
    class Meta:
        model = verification_store
        fields = ("overAll_status", "education_verified", "employment_verified", "ecourt_verified", "address_verified", "passport_verified", "education_remark", "employment_remark", "passport_remark", "address_remark", "court_remark")
        widgets = {
            "overAll_status": forms.Select(attrs={'class': 'form-control','label':"Color Code"}),
            "education_verified" : forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': "image/png, image/jpeg" }),
            "employment_verified" : forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': "image/png, image/jpeg"}),
            "ecourt_verified" : forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': "image/png, image/jpeg"}),
            "address_verified" : forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': "image/png, image/jpeg"}),
            "passport_verified" : forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': "image/png, image/jpeg"}),
            "education_remark" : forms.TextInput(attrs={'class': 'form-control'}),
            "employment_remark" : forms.TextInput(attrs={'class': 'form-control'}),
            "passport_remark" : forms.TextInput(attrs={'class': 'form-control'}),
            "address_remark" : forms.TextInput(attrs={'class': 'form-control'}),
            "court_remark" : forms.TextInput(attrs={'class': 'form-control'})
        }
        
    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.request.FILES:
            for f in self.request.FILES.getlist('file'):
                obj = self.model.objects.create(file=f)
        return super(EmployeeForm, self).form_valid(form)