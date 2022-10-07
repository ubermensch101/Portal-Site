from logging import PlaceHolder
from django.db import models
from django.contrib.auth.models import User
from .storage import OverwriteStorage
from tinymce.models import HTMLField

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.Username, instance.ProblemID, filename)


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username




class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/', storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

class MainModel(models.Model):
    Languages = (
('','Choose...'),
('Py', 'Python'),
('C++', 'C++'),
('Java', 'JavaLang'),
('SQL', 'Standard Query Language'),
('PHP','PHP'),
('R', 'R'),
('Perl','Perl'),
('C#', 'C#'),
('js','JavaScript')
)
    Username = models.CharField(max_length= 255)
    ProblemID = models.IntegerField(max_length = 255, blank=False)
    Language = models.CharField(max_length = 255, choices=Languages)
    File = models.FileField(upload_to=user_directory_path, storage=OverwriteStorage())
  
