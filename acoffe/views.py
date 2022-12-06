from django.shortcuts import render, redirect

from acoffe.models import coffe, ingridient

from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from django.core.paginator import Paginator

from django.urls import reverse, reverse_lazy

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout

from acoffe.forms import RegistrationForm, LoginForm, ContactForm, CoffeForm, CoffeAddForm

from django.core.mail import send_mail
from django.conf import settings

from django.contrib import messages

from rest_framework import viewsets

from acoffe.serializers import CoffeSerializer, IngridientSerializer

from django.contrib.auth.decorators import login_required, permission_required

from django.utils.decorators import method_decorator

# BASKET
from basket.forms import BasketAddProductForm

def home_page(request):
    return render(request, 'index.html')

# def list_coffe(request):
#     list_coffe = coffe.objects.all()
#     paginator = Paginator(list_coffe, 2)
#     page_num = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_num)

#     context = {
#         'list_coffe': list_coffe,
#         'page_obj': page_obj,
#         'title': 'Выбор кофе',
#     }
#     return render(request, 'acoffe/list_coffe.html', context)

def detail_coffe(reqest, coffe_id):
    detail_coffe = coffe.objects.get(pk=coffe_id)
    context = {
        'detail_coffe': detail_coffe,
# Добавляем корзину:
        'basket_form': BasketAddProductForm(),
    }
    return render(reqest, 'acoffe/detail_coffe.html', context)

def get_add_coffe(request):
    if request.method == 'POST':
        coffe_form = CoffeAddForm(request.POST)
        if coffe_form.is_valid():
            coffe_add = coffe.objects.create(
                name=coffe_form.cleaned_data['name'],
                description=coffe_form.cleaned_data['description'],
                price=coffe_form.cleaned_data['price'],
                )
            for ingridient in coffe_form.cleaned_data['ingridients']:
                coffe_add.ingridients.add(ingridient)
            return redirect('list_coffe')           
    else:
        coffe_form = CoffeAddForm()
    context = {
        'form': coffe_form,
    }
    return render(request, 'acoffe/create_coffe.html', context)

class CoffeList(ListView):
    model = coffe
    template_name = 'acoffe/list_coffe.html'
    context_object_name = 'list_coffe'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выбор кофе'
        return context

class CoffeDelete(DeleteView):
    model = coffe
    template_name = 'acoffe/delete_coffe.html'
    pk_url_kwarg = 'coffe_id'
    success_url = reverse_lazy('list_coffe')

    @method_decorator(permission_required('coffe.delete_coffe'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeUpdate(UpdateView):
    model = coffe
    form_class = CoffeForm
    template_name = 'acoffe/update_coffe.html'
    pk_url_kwarg = 'coffe_id'
    success_url = reverse_lazy('list_coffe')

    @method_decorator(permission_required('coffe.change_coffe'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class CoffeCreate(CreateView):
    model = coffe
    form_class = CoffeForm
    template_name = 'acoffe/create_coffe.html'
    success_url = reverse_lazy('list_coffe')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



def user_registration(request):
    if request.method == 'POST':
        # form = UserCreationForm(data=request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('log in')
    else:
        # form = UserCreationForm()
        form = RegistrationForm()        
    return render(request, 'acoffe/auth/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # form = AuthenticationForm(data=request.POST)
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = LoginForm()
    return render(request, 'acoffe/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home_page')

# EMAIL

def contact_email(request): 
    if request.method == 'POST': 
        form = ContactForm(request.POST) 
        if form.is_valid(): 
            print(form.cleaned_data)
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['kremnilandk@gmail.com'],
                fail_silently=False
                )
            if mail: 
                messages.success(request, 'Письмо успешно отправлено.') 
                return redirect('list_coffe') 
            else: 
                messages.error(request, 'Письмо не удалось отправить, попробуйте позже.') 
        else: 
            messages.warning(request, 'Письмо неверно заполнено, перепроверьте внесенные данные.') 
    else: 
        form = ContactForm() 
    return render(request, 'acoffe/email.html', {'form': form})

# API

class CoffeViewSet(viewsets.ModelViewSet):
    queryset = coffe.objects.all()
    # print(queryset)
    serializer_class = CoffeSerializer

class IngridientViewSet(viewsets.ModelViewSet):
    queryset = ingridient.objects.all()
    serializer_class = IngridientSerializer

# ERROR

def error_404(request, exception):
    response = render(request, 'acoffe/error/error.html', {'title': 'Страница не найдена', 'message': exception})
    # При переопределении вернет статусный код
    response.status_code = 404
    return response
