from django.db import models
from django.contrib.auth.models import User
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

    education = models.JSONField(default=list, null=True, blank=True)
    employment = models.JSONField(default=list, null=True, blank=True)

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
        name = self.employment_file.name.split("/")[3]
        return name

    @property
    def candidate_fullname(self):
        name = self.candidate.first_name + " " + self.candidate.last_name
        return name

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(self).save(*args, **kwargs)


class verification_store(models.Model):
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
        super(self).save(*args, **kwargs)

class employee_files_locker(models.Model):
    def user_directory_path(instance, filename):
        if instance.created_date:
            x = instance.created_date.strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)
        else:
            x = datetime.now().strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)

    form16_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    aadhar_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    education_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    employment_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    passport_file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])

    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(self).save(*args, **kwargs)

    # form16_file_updated_date = models.DateTimeField(auto_now=True)
    # aadhar_file_updated_date = models.DateTimeField(auto_now=True)
    # education_file_updated_date = models.DateTimeField(auto_now=True)
    # employment_file_updated_date = models.DateTimeField(auto_now=True)
    # passport_file_updated_date = models.DateTimeField(auto_now=True)


class verified_files_locker(models.Model):
    def user_directory_path(instance, filename):
        if instance.created_date:
            x = instance.created_date.strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)
        else:
            x = datetime.now().strftime("%b%d%Y")
            return 'uploads/{0}/{1}/{2}'.format(x, instance.candidate.username, filename)

    education_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    employment_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    ecourt_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    address_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    passport_verified = models.FileField(upload_to=user_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    updated_date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.updated_date = datetime.now()
        super(self).save(*args, **kwargs)

    # education_verified_updated_date = models.DateTimeField(auto_now=True)
    # employment_verified_updated_date = models.DateTimeField(auto_now=True)
    # ecourt_verified_updated_date = models.DateTimeField(auto_now=True)
    # address_verified_updated_date = models.DateTimeField(auto_now=True)
    # passport_verified_updated_date = models.DateTimeField(auto_now=True)