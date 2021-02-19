from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q

from user.forms import UserEditForm
# Create your views here.

User = get_user_model()

class ProfileView(View):
    template_name_auth = 'user/authenticated_profile.html'
    template_name_anon = 'user/anonymous_profile.html'
    
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse('<h1>Sorry, this page isn\'t available.</h1>')

        if username == request.user.username:
            context = {'user': user}
            return render(request, self.template_name_auth, context=context)
        else:
            follows_this_user = False
            for follow_user in request.user.follow_user.all():
                if follow_user.follows == user:
                    follows_this_user = True

            context = {'user': user, 'follows_this_user': follows_this_user}
            return render(request, self.template_name_anon, context=context)


class ProfileEditView(View):
    template_name = 'user/profile_edit.html'
    form_class = UserEditForm
    
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        if request.user.username != username:
            return HttpResponse('<h1>Sorry, this page isn\'t available.</h1>')
        
        context = { 'form': self.form_class(instance=request.user) }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile_edit_view', request.user.username)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

            context = { 'form': form }
            return render(request, self.template_name, context)


class AllProfilesView(View):
    template_name = 'user/all_profiles.html'
    
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('s')
        if not search_term:
            all_profiles = User.objects.filter(
                    is_active=True
                ).exclude(
                    username=request.user.username
                ).values(
                    'picture', 'full_name', 'bio', 'username'
                )
        else:
            all_profiles = User.objects.filter(
                    is_active=True
                ).filter(
                    Q(username__contains=search_term) | Q(full_name__contains=search_term)
                ).exclude(
                    username=request.user.username
                ).values(
                    'picture', 'full_name', 'bio', 'username'
                )

        context = {'all_profiles': all_profiles}
        return render(request, self.template_name, context=context)