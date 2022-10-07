from django.urls import path
from .views import home, RegisterView  # Import the view here
from .views import profile, project1, project2, project3, formupload, FormUpload

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),  # This is what we added
    path('profile/', profile, name='users-profile'),
    path('project1/', project1, name='project1'),
    path('project2/', project2, name='project2'),
    path('project3/', project3, name='project3'),
    path('formupload/', FormUpload.as_view(), name='formupload'),
]
