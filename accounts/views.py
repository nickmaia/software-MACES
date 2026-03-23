from django.contrib.auth import authenticate, login
from rest_framework import permissions, views
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms_config import UserProfileForm, CustomPasswordChangeForm
from django.contrib import messages

User = get_user_model()


class UserCreate(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, "accounts/register.html", {"form": UserSerializer()})

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("simulation_with_mass")  # Usando o nome da URL
        else:
            return render(
                request,
                "accounts/register.html",
                {"form": serializer, "error": serializer.errors},
            )


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        # Aqui, passe 'username' em vez de 'email' diretamente, já que 'authenticate' espera 'username'
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("simulation_with_mass")  # Usando o nome da URL
        else:
            # A mensagem de erro é mostrada se a autenticação falhar
            return render(
                request, "accounts/login.html", {"error": "Invalid email or password."}
            )

    def get(self, request):
        # Simplesmente retorna a página de login no GET
        return render(request, "accounts/login.html")


class LogoutView(views.APIView):
    def get(self, request):
        logout(request)
        return redirect("login")  # Usando o nome da URL


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('update_profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'accounts/update_profile.html', context)
