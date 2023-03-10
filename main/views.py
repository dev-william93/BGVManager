from django.views.generic import TemplateView
from .forms import EmployeeForm, VerificationForm
from .models import *
from django.db.models import Q
import json

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
import os, sys
from django.http import FileResponse
import datetime

@method_decorator(login_required, name='dispatch')
class IndexPageView(TemplateView):
    model = admin_store
    template_name = 'main/employee_form.html'
    
    def get(self, request):
        try:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    submittedEmployees = admin_store.objects.filter(~Q(overAll_status='success'))
                    paginator = Paginator(submittedEmployees, 15)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    return render(request, 'main/admin/dashboard.html', {'submittedEmployees': page_obj})
                else:
                    verification_record = admin_store.objects.filter(candidate=request.user.pk)
                    if verification_record:
                        return render(request, 'main/employee_statusCheck.html', {"verification_record": verification_record.first()})
                    else:
                        form = EmployeeForm()
                        return render(request, 'main/employee_form.html', {'form': form})
            else:
                return render(request, 'main/index.html')
        except:
            return HttpResponseRedirect(reverse('index'))
        
    def post(self, request):
        # try:
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
            employment_files = request.FILES.getlist('employment_file')
            if form.is_valid():
                employee_store_form = form.save()
                admin_store_object  = admin_store.objects.create(candidate=request.user, employee_store= employee_store_form)
                UploadMultipleFiles(employment_files, request.user, 'candidate', admin_store_object, 'candidate_employment', False)
                return HttpResponseRedirect(reverse('index'))
            else:
                print("Not valid")
                print(form.errors)
                return HttpResponseRedirect(reverse('index'))
        # except:
        #     return HttpResponseRedirect(reverse('index'))

@method_decorator(login_required, name='dispatch')
class AdminCandidatePageView(TemplateView):
    model = admin_store
    template_name = 'main/each_candidate.html'
    
    def get(self, request, pk):
        try:
            verification_record = admin_store.objects.filter(candidate=pk)
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
        except:
            return HttpResponseRedirect(reverse('index'))
        
    def post(self, request, pk):
        # try:
        if request.user.is_superuser:
            verification_record = admin_store.objects.filter(candidate=pk)
            if request.FILES:
                verification_record_obj = verification_record.first()
                if request.FILES.getlist('education_verified'):
                    UploadMultipleFiles(request.FILES.getlist('education_verified'), verification_record_obj.candidate, 'admin', verification_record_obj, 'education', True)
                    verification_record_obj.education_verified = request.FILES.get('education_verified')
                if request.FILES.getlist('employment_verified'):
                    UploadMultipleFiles(request.FILES.getlist('employment_verified'), verification_record_obj.candidate, 'admin', verification_record_obj, 'employment', True)
                    verification_record_obj.employment_verified = request.FILES.get('employment_verified')
                if request.FILES.getlist('ecourt_verified'):
                    UploadMultipleFiles(request.FILES.getlist('ecourt_verified'), verification_record_obj.candidate, 'admin', verification_record_obj, 'ecourt', True)
                    verification_record_obj.ecourt_verified = request.FILES.get('ecourt_verified')
                if request.FILES.getlist('address_verified'):
                    UploadMultipleFiles(request.FILES.getlist('address_verified'), verification_record_obj.candidate, 'admin', verification_record_obj, 'address', True)
                    verification_record_obj.address_verified = request.FILES.get('address_verified')
                if request.FILES.getlist('passport_verified'):
                    UploadMultipleFiles(request.FILES.getlist('passport_verified'), verification_record_obj.candidate, 'admin', verification_record_obj, 'passport', True)
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

            # YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]

            dict_request['updated_date']= datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")
            # print(dict_request)
            verification_record.update(**dict_request)
            return HttpResponseRedirect(reverse('AdminCandidatePageView', args=[pk]))
        # except:
        #     return HttpResponseRedirect(reverse('index'))

class CandidateReportPageView(TemplateView):
    model = admin_store
    template_name = 'main/reports.html'
    
    def get(self, request, pk, businessUser):
        try:
            if request.user.is_superuser:
                verification_record = admin_store.objects.filter(candidate=pk)
                if verification_record:
                    userextension_obj = UserExtension.objects.get(user=pk)
                    collegeName = verification_record.first().employee_store.education[0]
                    return render(request, 'main/admin/reports.html', {"verification_record": verification_record.first(), 'dateTime': datetime.datetime.now(), 'collegeName': collegeName, 'businessUser': businessUser, 'userextension_obj': userextension_obj })
            else:
                return HttpResponseRedirect(reverse('index'))
        except:
            return HttpResponseRedirect(reverse('index'))

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'


@login_required
def secureView(request, text, userid, file):
    if request.user.is_superuser:
        filepath = 'uploads/'+ text + '/' + userid + '/' + file
        document = documents_store.objects.filter(file=filepath)
        if document:
            response = FileResponse(document[0].file)
        else:
            document_file = open('content/media/'+filepath, 'rb')
            response = FileResponse(document_file)
        return response
    else:
        return HttpResponseRedirect(reverse('index'))

def UploadMultipleFiles(files, candidate_obj, uploader_type, admin_store_object, doc_type, clearable):
    if clearable:
        documents_store.objects.filter(admin_store = admin_store_object,candidate_obj = candidate_obj, uploader_type = uploader_type, document_type = doc_type).delete()
    filesList = []
    for file in files:
        documents_store_obj = documents_store.objects.create(
            admin_store = admin_store_object,
            file = file,
            document_type = doc_type,
            candidate_obj = candidate_obj,
            uploader_type = uploader_type
        )
        filesList.append(
                {
                    'filename': documents_store_obj.file.name.split("/")[3],
                    'filelink': documents_store_obj.file
                }
            )
    return filesList