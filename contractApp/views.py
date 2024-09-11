
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

from contract.models import Contract


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_list_contract')
                else:
                    return redirect('index')  # Remplacez par le nom de la vue du dashboard revendeur
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def is_staff(user):
    return user.is_staff

@login_required
@login_required
@user_passes_test(is_staff)
def list_contract_admin(request):
    # Le code existant pour afficher les contrats
    contracts = Contract.objects.all()  # Exemple
    return render(request, 'valid_contract.html', {'contracts': contracts})



from django.contrib.auth.views import LoginView

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        # Vérifier si les champs sont vides
        if not request.POST.get('username') or not request.POST.get('password'):
            messages.error(request, "Les champs nom d'utilisateur et mot de passe sont obligatoires.")
        elif form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('admin_list_contract')
                else:
                    return redirect('index')
                  # Redirige vers la page d'index après connexion
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect.")
        return super().form_invalid(form)