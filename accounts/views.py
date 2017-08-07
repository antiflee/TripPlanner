from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.views .generic import DetailView
from django.views import View
from django.views.generic.edit import FormView

from .forms import UserRegisterForm
from .models import UserProfile


User = get_user_model()

class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, username__iexact=self.kwargs.get("username"))

    def get_context_data(self, *args, **kwargs):
        this_username = self.kwargs.get("username")
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context['following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
            if self.request.user.username != self.get_object().username:
                context['diff_user'] = True
            else:
                context['diff_user'] = False
        context['this_username'] = this_username
        return context

class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        print("1111",toggle_user,request.user)
        if request.user.is_authenticated():
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)

class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/trip/'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)
