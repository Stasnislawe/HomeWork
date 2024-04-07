from allauth.account import app_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView, FormView
from django.template.loader import render_to_string

from .models import Advert, Comment, User
from .forms import CommentForm, AdvertForm, RegistrationForm
from django.conf import settings


class HomeListView(ListView):
    model = Advert
    template_name = 'index.html'
    context_object_name = 'advert'
    ordering = '-time_create'


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Advert
    template_name = 'detail.html'
    context_object_name = 'advert'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'

    def get_success_url(self):
        return reverse_lazy('detail_page', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.advert_comment = self.get_object()
        self.object.author_comment = self.request.user
        self.object.save()
        html_content = render_to_string(
            'comment_created.html',
            {
                'comment': self.object,
                'link': f'{settings.SITE_URL}detail/{self.object.advert_comment.pk}' #//{{comment.advert_comment.pk
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{self.object.comm_text} {self.object.author_comment}',
            body=self.object.comm_text,  # это то же, что и message
            from_email='uvedomleniynewsportal@ya.ru',
            to=[self.object.advert_comment.author.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем
        return super().form_valid(form)


class AdvertCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = Advert
    template_name = 'edit_page.html'
    form_class = AdvertForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана'

    def get_context_data(self, **kwargs):
        kwargs['list_adverts'] = Advert.objects.filter(author=self.request.user).order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        html_content = render_to_string(
            'comment_added.html',
            {
                'ad': self.object,
                'link': f'{settings.SITE_URL}detail/{self.object.pk}'
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{self.object.heading} ',
            body=self.object.text,
            from_email='uvedomleniynewsportal@ya.ru',
            to=[],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super().form_valid(form)

class AdvertUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin,UpdateView):
    model = Advert
    template_name = 'edit_page.html'
    form_class = AdvertForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно обновлена'

    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class AdvertDeleteView(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись удалена'

    def post(self,request,*args,**kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

# class RegisterView(FormView):
#      form_class = SignupRegForm
#      template_name = 'registration/signup.html'
#      success_url = reverse_lazy("profile")


def update_comment_status(request, pk, type):
    item = Comment.objects.get(pk=pk)
    if request.user != item.advert_comment.author:
        return HttpResponse('deny')

    if type == 'public':
        import operator
        item.status = operator.not_(item.status)
        item.save()
        template = 'comment.html'
        context = {'item': item, 'status_comment': 'Комментарий опубликован'}
        html_content = render_to_string(
            'comment_accepted.html',
            {
                'comment': item,
                'link': f'{settings.SITE_URL}detail/{item.advert_comment.pk}'
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{item.comm_text} {item.author_comment}',
            body=item.comm_text,
            from_email='uvedomleniynewsportal@ya.ru',
            to=[item.author_comment.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return render(request, template, context)

    elif type == 'delete':
        item.delete()
        return HttpResponse('''
        <div class="alert alert-success">
        Комментарий удален
        </div>
        ''')

    return HttpResponse('1')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'registration/invalid_code.html')
        return redirect('login')

class AccountInactiveView(TemplateView):
    template_name = "account/snippets/account_inactive." + app_settings.TEMPLATE_EXTENSION


account_inactive = AccountInactiveView.as_view()
