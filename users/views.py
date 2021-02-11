from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ContactForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"


def send_msg(email, name, subject, body):
    sub = f"Письмо от {name} ({email})"
    bod = f""" Тема письма: {subject}
    Содержание:{body}
    """
    send_mail(
        sub, bod, email, ["admin@mail.net", ],
    )


'''
Проверка авторизации,
в дальнейшем у каждого пользователя будет своя "визитная карточка".
'''


@login_required
def user_contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            send_msg(email, name, subject, body)
            form.save()
            return redirect('thank-you')
    return render(request, 'contact.html', {'form': form})


def thankyou(request):
    return render(request, 'thankyou.html')
