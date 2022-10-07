from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import DocumentForm,MainForm, ProjectForm
from .forms import RegisterForm, LoginForm, ProjectForm
from django.http import HttpResponseRedirect
from .functions import check_code
from docroom.settings import MEDIA_URL


def home(request):
    return render(request, 'users/home.html')



class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')


class CustomLoginView(LoginView):
    form_class = LoginForm
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

def project1(request):
    if request.method == "Post" :
        return render(request, 'users/project1.html', {'form': form})
    else:
        form = ProjectForm()
        return render(request, 'users/project1.html', {'form': form})
def project2(request):
    return render(request, 'users/project2.html')

def project3(request):
    return render(request, 'users/project3.html')


class FormUpload(View):
    form_class=MainForm
    initial={'key': 'value'}
    template_name="users/formupload.html"


    def get(self, request, *args, **kwargs):
        form=MainForm()
        return render(request, 'users/formupload.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            filename=str(request.FILES["File"].name)
            username=str(form.cleaned_data.get("Username"))
            problem_id=str(form.cleaned_data.get("ProblemID"))

            file_url=MEDIA_URL + "user_"+username+"/"+problem_id+"/"+filename
            input_test_url=MEDIA_URL + "/tests/"+problem_id+".txt"
            ideal_output_url=MEDIA_URL + "ideal_output/"+problem_id+".txt"
            user_output_url=file_url=MEDIA_URL + "user_"+username+"/"+problem_id+"/"+"temp_output.txt"

            code_result=check_code(file_url, input_test_url, ideal_output_url, user_output_url)
            if code_result == 0:
                messages.success(request, f'Submission Accepted!')
            else:
                messages.error(request, f'Wrong Answer :(')
            return redirect("users-home")

        else:
            form=MainForm()
            return render(request, 'users/formupload.html', {'form': form})




def formupload(request):
    if request.method == 'POST':
        form = MainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            filename=request.FILES["File"].name
            username=request.POST["Username"]
            problem_id=request.POST["ProblemID"]

            file_url=MEDIA_URL + "user_"+username+"/"+problem_id+"/"+filename
            input_test_url=MEDIA_URL + "/tests/"+problem_id+".txt"
            ideal_output_url=MEDIA_URL + "ideal_output/"+problem_id+".txt"
            user_output_url=file_url=MEDIA_URL + "user_"+username+"/"+problem_id+"/"+"temp_output.txt"

            code_result=check_code(file_url, input_test_url, ideal_output_url, user_output_url)



            return redirect("users-home")
        else:
            form=MainForm()
        return render(request, 'users/formupload.html', {'form': form})
    else:
        form=MainForm()
        return render(request, 'users/formupload.html', {'form': form})