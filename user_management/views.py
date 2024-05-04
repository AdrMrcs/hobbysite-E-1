from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm

from .models import Profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = '__all__'
    template_name = "user_update.html"

    def get_success_url(self):
        return reverse_lazy("login")

    def get_object(self, queryset=None):
        return self.request.user.Profile

def register(request):
    user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            p = Profile()
            p.user = user
            p.name = user.username
            p.email = user.email
            p.save()
            return redirect('login')
        
    
    ctx = {'user_form': user_form}
    return render(request, 'registration/register.html', ctx)
