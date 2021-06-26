from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import HiddenInput
from django.shortcuts import render
from .models import News, Comment, User, Profile
from django.views import generic, View
from .forms import AddCommentForm, AddNews, ExtendedRegisterForm
from django.http import HttpResponseRedirect


class AnotherLoginView(LoginView):
    template_name = 'app_news/login.html'


class AnotherLogoutView(LogoutView):
    template_name = 'app_news/logout.html'


class NewsView(generic.ListView):
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    queryset = News.objects.filter(activity=True).order_by('date_create').reverse()

    # первая реализация посредствам ввода необходимого тега
    def post(self, request):
        tag = request.POST.get('tag')
        date = request.POST.get('date')
        if tag and date:
            news_list = News.objects.filter(tag=tag, date_create__contains=date)
            return render(request, 'app_news/news_list.html', context={'news_list': news_list})
        elif date:
            news_list = News.objects.filter(date_create__contains=date)
            return render(request, 'app_news/news_list.html', context={'news_list': news_list})
        elif tag:
            news_list = News.objects.filter(tag=tag)
            return render(request, 'app_news/news_list.html', context={'news_list': news_list})
        else:
            news_list = News.objects.all().order_by('date_create').reverse()
            return render(request, 'app_news/news_list.html', context={'news_list': news_list})


class NewsDetailView(generic.DetailView):
    model = News
    queryset = News.objects.filter(activity=True).select_related()

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        initial = None

        if self.request.user.is_authenticated:
            initial = {'username': self.request.user.username}

        comment_form = AddCommentForm(initial=initial)
        if self.request.user.is_authenticated:
            comment_form.fields['username'].widget = HiddenInput()
            # второй вариант удаления поля из формы
            # comment_form.fields.pop('name_user')

        context['comment_form'] = comment_form

        return context

    def post(self, request, pk, *args, **kwargs):
        create_new_comment = AddCommentForm(request.POST)

        if create_new_comment.is_valid():
            comment_text = create_new_comment.cleaned_data['comment_text']
            username = request.user.username
            if not request.user.username:
                if not User.objects.filter(username='anon'):
                    User.objects.create(username='anon')
                username = 'anon'
            elif not User.objects.filter(username=username):
                User.objects.create(username=username)
            id_user = User.objects.get(username=username)
            # id_news = News.objects.get(id=pk)
            # Comment.objects.create(user=name_user, comment_text=comment_text, title_news=id_news)
            Comment.objects.create(username=id_user, comment_text=comment_text, title_news_id=pk)
            return HttpResponseRedirect(f'/news/{pk}')


class CreateNews(View):

    def get(self, request):
        create_news_form = AddNews()
        return render(request, 'app_news/create_new_news.html', context={'create_news_form': create_news_form})

    def post(self, request):
        create_news_form = AddNews(request.POST)

        if create_news_form.is_valid():
            number_published_news = Profile.objects.get(user=request.user).number_published_news
            Profile.objects.filter(user=request.user).update(number_published_news=number_published_news + 1)
            News.objects.create(**create_news_form.cleaned_data)
            return HttpResponseRedirect('/news_list/')

        return render(request, 'app_news/create_new_news.html', context={'create_news_form': create_news_form})


class NewsEdit(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        news_form = AddNews(instance=news)
        return render(request, 'app_news/news_edit.html', context={'news_form': news_form, 'news_id': news_id})

    def post(self, request, news_id):
        news = News.objects.get(id=news_id)
        news_form = AddNews(request.POST, instance=news)

        if news_form.is_valid():
            news.save()
        return HttpResponseRedirect(f'/news/{news_id}')


class UnpublishedNews(View):
    def get(self, request):
        news_list = News.objects.filter(activity=False)
        return render(request, 'app_news/unpublished_news.html', {'news_list': news_list})

    def post(self, request):
        if request.POST:
            print(request.POST)
            for news_id in request.POST:
                if news_id == 'csrfmiddlewaretoken':
                    continue
                News.objects.filter(id=news_id).update(activity=True)
        news_list = News.objects.filter(activity=False)
        return render(request, 'app_news/unpublished_news.html', {'news_list': news_list})


class UnverifiedUsers(View):
    def get(self, request):
        group = Group.objects.get(name='Верифицированные пользователи')
        moder = Group.objects.get(name='Модераторы')
        user_list = User.objects.exclude(groups=group).exclude(groups=moder).exclude(username='admin')
        return render(request, 'app_news/unverified_users.html', {'user_list': user_list})

    def post(self, request):
        group = Group.objects.get(name='Верифицированные пользователи')
        moder = Group.objects.get(name='Модераторы')
        if request.POST:
            for user_id in request.POST:
                if user_id == 'csrfmiddlewaretoken':
                    continue
                group.user_set.add(user_id)
        user_list = User.objects.exclude(groups=group).exclude(groups=moder).exclude(username='admin')
        return render(request, 'app_news/unverified_users.html', {'user_list': user_list})


def register_view(request):
    if request.method == 'POST':
        form = ExtendedRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                phone_number=phone_number,
                city=city,
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/news_list/')
    else:
        form = ExtendedRegisterForm()
    return render(request, 'app_news/register.html', {'form': form})


# вьюха для показания всей информации пользователя
def account_view(request):
    information_users = request.user
    return render(request, 'app_news/account.html', {'account': information_users})


# вторая реализация представление для новой страницы с тегами
def news_tag(request, tag):
    news_list = News.objects.filter(tag=tag)
    return render(request, 'app_news/news_list.html', {'news_list': news_list})
