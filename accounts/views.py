from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic



from . import models
from . import mixin
from . import forms

from . import forms

# class LoginView(generic.FormView):
#     form_class = AuthenticationForm
#     success_url = reverse_lazy("etrade:user_home")
#     template_name = "accounts/login.html"
#
#     def get_form(self, form_class=None):
#         if form_class is None:
#             form_class = self.get_form_class()
#         return form_class(self.request, **self.get_form_kwargs())
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return super().form_valid(form)


def suggestion_view(request):
    form = forms.SuggestionForm()
    if request.method == 'POST':
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            send_mail(
                'Suggestion from {}'.format(form.cleaned_data['name']),
                form.cleaned_data['suggestion'],
                '{name} <{email}>'.format(**form.cleaned_data),
                ['kenneth@teamtreehouse.com']
            )
            messages.add_message(request, messages.SUCCESS,
                                 'Thanks for your suggestion!')
            return HttpResponseRedirect(reverse('suggestion'))
    return render(request, 'suggestion_form.html', {'form': form})


class LogoutView(generic.RedirectView):
    url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"