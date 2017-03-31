
# Django
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, FormView, ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout

# Local Django
from users.variables import USER_FORM_PREFIX, USER_LOGIN_PREFIX
from users.forms import UserRegisterForm, UserLoginForm, PostForm
from users.models import User, Activation
from magazines.models import Magazine, Article

class UserView(TemplateView):
    template_name = 'users/userform.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context.update({
            'name': _('User Page'),
            'user_form': UserRegisterForm(prefix=USER_FORM_PREFIX),
            'user_login': UserLoginForm(prefix=USER_LOGIN_PREFIX)
        })

        return context

    def post(self, request):
        context = self.get_context_data()

        if USER_FORM_PREFIX in request.POST:
            user_form = UserRegisterForm(request.POST, prefix=USER_FORM_PREFIX)
            context.update({'user_form': user_form})

            if user_form.is_valid():
                register = user_form.save(commit=False)
                register.save()
                m = Activation(user=register, key=get_random_string(length=50))
                m.save()

                subject = 'Hello'
                message = settings.LOCAL_HOST_ADDRESS + reverse(
                                                        'activation',
                                                        args=[m.key]
                                                        )
                sender = settings.EMAIL_HOST_USER
                to_list = register.email
                msg = EmailMessage(subject, message, sender, [to_list])
                msg.content_subtype = "html"
                msg.send()

                if register:
                    messages.success(
                        request, _('Registration Successful. Thank you.')
                    )
                    context.update({
                        'user_form':UserRegisterForm(prefix=USER_FORM_PREFIX)
                        })

                    return super(UserView, self).render_to_response(context)

            messages.error(
                request, _('Registration failed. Try again.')
            )

        if USER_LOGIN_PREFIX in request.POST:
            print(request.user.is_authenticated())
            user_login = UserLoginForm(request.POST, prefix=USER_LOGIN_PREFIX)
            context.update({'user_login': user_login})
            if user_login.is_valid():
                email = user_login.cleaned_data.get("email")
                password = user_login.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                login(request, user)
                print(request.user.is_authenticated())
                return HttpResponseRedirect('/index/')

        return super(UserView, self).render_to_response(context)


def user_logout(request):
    read = request.user.id
    if(not read):
        return HttpResponseRedirect('/')
    logout(request)
    return HttpResponseRedirect('/')


class IndexView(ListView):
    template_name = 'users/index.html'
    context_object_name = 'all_magazines'

    def get_queryset(self):
        return Magazine.objects.all()


class DetailView(DetailView):
    model = Article
    template_name = 'users/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comments'] = Article.objects.all()
        return context


def post_new(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article and request.method == 'POST':
        edit_form = PostForm(request.POST)
        if edit_form.is_valid():
            point = edit_form.save(commit=False)
            point.article = article
            point.users = request.user
            point.save()

            return redirect('users:detail', pk=article.pk)
    else:
        edit_form = PostForm
    return render(request, 'users/post_edit.html', {'edit_form': edit_form})


def activation(request, key):

    activation = get_object_or_404(Activation, key=key)
    activation.user.is_active = True
    activation.user.save()
    activation.user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, activation.user)

    return HttpResponseRedirect('/index/')
