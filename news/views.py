from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import *
from .models import *


# логика с помощью классов (замена функции index и get_category)
# ListView - для возварщения какого-то списка. В данном случае - списка статей
# DetailView - для возвращения какого-то определенного элемента
# CreateView - для создания элемента
@login_required()
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    messages.error(request, 'Статья удалена')
    return redirect('user_profile')


@login_required()
def edit_news(request, pk):
    item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = AddNewsForm(request.POST, instance=item)
        if form.is_valid():
            new_item = form.save(**form.cleaned_data)
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Статья обновлена')
            return redirect('user_profile')
    else:
        form = AddNewsForm(instance=item)
    return render(request, 'news/edit_news.html', {'form': form, 'item': item})



def user_profile(request):
    news = News.objects.filter(user=request.user)
    return render(request, 'news/profile_user.html', {'news': news})


def other_user_profile(request):
    pass


def user_logout(request):
    logout(request)
    return redirect('home')


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'news/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации!')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'news/login.html', context)


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    # extra_context = {'title_news': 'Список статей'} # для статичных данных

    # Для динамичных данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title_news'] = 'Список статей'
        return context

    # Поправка запроса (выборка)
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category', 'user')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category',
                                                                                                             'user')


# class ShowNews(DetailView):
#     model = News
#     template_name = 'news/news_page.html'
#     context_object_name = 'item'


@login_required(login_url='/login/')
def show_news(request, pk):
    item = News.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddCommentForm(data=request.POST)
        if form.is_valid():
            obj_type = ContentType.objects.get_for_model(item)
            Comments.objects.create(content_type=obj_type, object_id=item.id, user_comm=request.user,
                                    content=request.POST.get('content'))
            form = AddCommentForm()
            return HttpResponseRedirect(request.path_info)
    else:
        form = AddCommentForm()
    comments = Comments.objects.filter(object_id=item.pk)
    context = {'form': form,
               'item': item,
               'comments': comments}
    return render(request, 'news/news_page.html', context)


@login_required(login_url='/login/')
def add_news(request):
    if request.method == "POST":
        form = AddNewsForm(request.POST)
        if form.is_valid():
            news = form.save(**form.cleaned_data)
            news.user = request.user
            news.save()
            return redirect(news)
    else:
        form = AddNewsForm()
    return render(request, 'news/add_news.html', {'form': form})
# class AddNews(LoginRequiredMixin, CreateView):
#     form_class = AddNewsForm
#     template_name = 'news/add_news.html'
#     login_url = '/login/'

# success_url = reverse_lazy('home') - редирект на главную страницу
