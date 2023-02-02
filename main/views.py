from django.views.generic import TemplateView
from .form import EmployeeForm, VerificationForm
from .models import employee_store, verification_store
from django.db.models import Q
import json

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
import datetime


class IndexPageView(TemplateView):
    model = verification_store
    template_name = 'main/employee_form.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                submittedEmployees = verification_store.objects.filter(~Q(overAll_status='success'))
                paginator = Paginator(submittedEmployees, 3)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'main/admin/dashboard.html', {'submittedEmployees': page_obj})
            else:
                verification_record = verification_store.objects.filter(candidate=request.user.pk)
                if verification_record:
                    return render(request, 'main/employee_statusCheck.html', {"verification_record": verification_record.first()})
                else:
                    form = EmployeeForm()
                    return render(request, 'main/employee_form.html', {'form': form})
        else:
            return render(request, 'main/index.html')
        
    def post(self, request):
        if request.user.is_superuser:
            form = EmployeeForm(request.POST, request.FILES)
            if form.is_valid():
                return HttpResponseRedirect(reverse('index'))
            else:
                print("Not valid")
                return HttpResponseRedirect(reverse('index'))
        else:
            request.POST._mutable = True
            request.POST['candidate'] = request.user.pk
            form = EmployeeForm(request.POST, request.FILES)
            if form.is_valid():
                employee_store_form = form.save()
                verification_store.objects.create(candidate=request.user, employee_store= employee_store_form)
                return HttpResponseRedirect(reverse('index'))
            else:
                print("Not valid")
                print(form.errors)
                return HttpResponseRedirect(reverse('index'))


class AdminCandidatePageView(TemplateView):
    model = verification_store
    template_name = 'main/each_candidate.html'
    
    def get(self, request, pk):
        verification_record = verification_store.objects.filter(candidate=pk)
        VerificationFormWithInitial = VerificationForm(initial={
            'education_verified': verification_record.first().education_verified,
            'employment_verified': verification_record.first().employment_verified,
            'ecourt_verified': verification_record.first().ecourt_verified,
            'address_verified': verification_record.first().address_verified,
            'passport_verified': verification_record.first().passport_verified
        } )
        if verification_record:
            return render(request, 'main/admin/each_candidate.html', {"employee_record": verification_record.first(), "pk": pk, "form": VerificationFormWithInitial})
        else:
            return HttpResponseRedirect(reverse('index'))
        
    def post(self, request, pk):
        if request.user.is_superuser:
            verification_record = verification_store.objects.filter(candidate=pk)
            if request.FILES:
                verification_record_obj = verification_record.first()
                if request.FILES.get('education_verified'):
                    verification_record_obj.education_verified = request.FILES.get('education_verified')
                if request.FILES.get('employment_verified'):
                    verification_record_obj.employment_verified = request.FILES.get('employment_verified')
                if request.FILES.get('ecourt_verified'):
                    verification_record_obj.ecourt_verified = request.FILES.get('ecourt_verified')
                if request.FILES.get('address_verified'):
                    verification_record_obj.address_verified = request.FILES.get('address_verified')
                if request.FILES.get('passport_verified'):
                    verification_record_obj.passport_verified = request.FILES.get('passport_verified')
                verification_record_obj.save()

            dict_request = request.POST.dict()

            dict_request['csrfmiddlewaretoken'] = ''
            dict_request['employment_verified'] = ''
            dict_request['ecourt_verified'] = ''
            dict_request['address_verified'] = ''
            dict_request['passport_verified'] = ''
            dict_request['education_verified'] = ''
            
            dict_request.pop('csrfmiddlewaretoken')
            dict_request.pop('employment_verified')
            dict_request.pop('ecourt_verified')
            dict_request.pop('address_verified')
            dict_request.pop('passport_verified')
            dict_request.pop('education_verified')
            
            verification_record.update(**dict_request)
            return HttpResponseRedirect(reverse('AdminCandidatePageView', args=[pk]))


class CandidateReportPageView(TemplateView):
    model = verification_store
    template_name = 'main/reports.html'
    
    def get(self, request, pk):
        verification_record = verification_store.objects.filter(candidate=pk)
        if verification_record:
            collegeName = verification_record.first().employee_store.education[0]
            return render(request, 'main/admin/reports.html', {"verification_record": verification_record.first(), 'dateTime': datetime.datetime.now(), 'collegeName': collegeName })
        else:
            return HttpResponseRedirect(reverse('index'))

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'