from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from datetime import datetime
from django.core.validators import FileExtensionValidator


class employee_store(models.Model):

    def user_directory_path(instance, filename):
        if instance.created_date:
            x = instance.created_date.strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)
        else:
            x = datetime.now().strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)

    candidate = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True, null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)
    pan = models.CharField(max_length=10, null=True, blank=True)
    passport = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    
    address_period = models.CharField(max_length=50, null=True, blank=True)
    country_location = models.CharField(max_length=100, null=True, blank=True)

    education = models.JSONField(default=list, null=True, blank=True)
    employment = models.JSONField(default=list, null=True, blank=True)

    form16_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    aadhar_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    education_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    employment_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    passport_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def form16_filename(self):
        name = self.form16_file.name.split("/")[3]
        return name

    @property
    def aadhar_filename(self):
        name = self.aadhar_file.name.split("/")[3]
        return name

    @property
    def education_filename(self):
        name = self.education_file.name.split("/")[3]
        return name

    @property
    def employment_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'candidate_employment', uploader_type = 'candidate')
        print(filesObject)
        filesList = []
        for each in filesObject:
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file
                }
            )
        return filesList

    @property
    def candidate_fullname(self):
        name = self.candidate.first_name + " " + self.candidate.last_name
        return name

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(employee_store, self).save(*args, **kwargs)


class admin_store(models.Model):
    def user_directory_path(instance, filename):
        x = instance.created_date.strftime("%b%d%Y")
        return 'verified/{0}/{1}/{2}'.format(instance.candidate.username, x, filename)

    document_status_choice = (
        ('submitted', 'Submitted'),
        ('rejected', 'Rejected'),
        ('inprogress', 'In Progress'),
        ('success', 'Success'),
    )

    overall_status_choice = (
        ('majorDis', 'Red'),
        ('minorDis', 'Yellow'),
        ('inprogress', 'Gray'),
        ('inaccessible', 'Orange'),
        ('clear', 'Green'),
    )

    candidate = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True, null=True, blank=True)
    employee_store = models.OneToOneField(employee_store, on_delete=models.DO_NOTHING, unique=True, null=True, blank=True)

    education_status = models.CharField(choices=document_status_choice, default='submitted', max_length=10)
    employment_status = models.CharField(choices=document_status_choice, default='submitted', max_length=10)
    passport_status = models.CharField(choices=document_status_choice, default='submitted', max_length=10)
    address_status = models.CharField(choices=document_status_choice, default='submitted', max_length=10)
    court_status = models.CharField(choices=document_status_choice, default='submitted', max_length=10)

    education_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    employment_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    ecourt_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    address_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    passport_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    education_remark = models.CharField(max_length=1000, null=True, blank=True, default='')
    employment_remark = models.CharField(max_length=1000, null=True, blank=True, default='')
    passport_remark = models.CharField(max_length=1000, null=True, blank=True, default='')
    address_remark = models.CharField(max_length=1000, null=True, blank=True, default='')
    court_remark = models.CharField(max_length=1000, null=True, blank=True, default='')
    
    overAll_status = models.CharField(choices=overall_status_choice, default='inprogress', max_length=50, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(admin_store, self).save(*args, **kwargs)

    @property
    def education_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'education', uploader_type = 'admin')
        filesList = []
        for index, each in enumerate(filesObject):
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file,
                    'idx': index
                }
            )
        return filesList

    @property
    def employment_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'employment', uploader_type = 'admin')
        filesList = []
        for index, each in enumerate(filesObject):
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file,
                    'idx': index
                }
            )
        return filesList

    @property
    def ecourt_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'ecourt', uploader_type = 'admin')
        filesList = []
        for index, each in enumerate(filesObject):
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file,
                    'idx': index
                }
            )
        return filesList

    @property
    def address_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'address', uploader_type = 'admin')
        filesList = []
        for index, each in enumerate(filesObject):
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file,
                    'idx': index
                }
            )
        return filesList

    @property
    def passport_filename(self):
        filesObject = documents_store.objects.filter(candidate_obj = self.candidate, document_type = 'passport', uploader_type = 'admin')
        filesList = []
        for index, each in enumerate(filesObject):
            filesList.append(
                {
                    'filename': each.file.name.split("/")[3],
                    'filelink': each.file,
                    'idx': index
                }
            )
        return filesList

class documents_store(models.Model):

    document_type_choice = (
        ('candidate_employment', 'candidate_employment'),
        ('education', 'education'),
        ('employment', 'employment'),
        ('ecourt', 'ecourt'),
        ('address', 'address'),
        ('passport', 'passport'),
    )

    uploader_type_choice = (
        ('candidate', 'candidate'),
        ('admin', 'admin'),
    )

    def user_directory_path(instance, filename):
        if instance.created_date:
            x = instance.created_date.strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.admin_store.candidate.username, filename)
        else:
            x = datetime.now().strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.admin_store.candidate.username, filename)
    

    candidate_obj = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    admin_store = models.ForeignKey(admin_store, on_delete=models.DO_NOTHING, null=True, blank=True)

    file = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'])])

    document_type = models.CharField(choices=document_type_choice, default='candidate_employment', max_length=50, null=True, blank=True)
    uploader_type = models.CharField(choices=uploader_type_choice, default='candidate', max_length=50, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(documents_store, self).save(*args, **kwargs)