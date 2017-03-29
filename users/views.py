
# Django
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout

# Local Django
from users.variables import USER_FORM_PREFIX, USER_LOGIN_PREFIX
from users.forms import UserRegisterForm, UserLoginForm, PostForm
from users.models import User
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

        return super(UserView, self).render_to_response(context)


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
            point.user = request.user
            point.save()

            return redirect('users:detail', pk=article.pk)
    else:
        edit_form = PostForm
    return render(request, 'users/post_edit.html', {'edit_form': edit_form})
