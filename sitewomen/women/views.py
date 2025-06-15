from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView,FormView, CreateView, UpdateView, DeleteView

from .utils import DataMixin
from .forms import AddPostForm, UploadFileForm
from datetime import datetime
from django.core.paginator import Paginator

from .models import Category, TagPost, UploadFiles, Women
# Create your views here.


menu = [
    {'title': 'Об этом сайте', 'url_name': 'about', },
    {'title': 'Добавить статью', 'url_name': 'add_page', },
    {'title': 'Обратная связь', 'url_name': 'contact', },
]





# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)

#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }

#     return render(request, 'women/post.html', context=data)



class ShowPost(DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg= 'post_slug'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu  
        context['cat_selected'] = context['post'].cat_id
        return context

    def get_object(self, queryset = None):
        return get_object_or_404(Women.objects.all(), slug=self.kwargs[self.slug_url_kwarg])

def index(request):
    return HttpResponse('Страница приложения women.')


# def home(request):
#     posts = Women.published.all().select_related('cat')

#     data = {
#         'title': "Главная самая страница",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,

#     }
#     return render(request, 'women/index.html', context=data)

# def handle_uploaded_file(f):
    
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     unique_name = f"{timestamp}_{f.name}"
    

#     with open(f"G:/Games/python/Django/sitewomen/uploads/{unique_name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

class WomenHome(DataMixin,ListView):
    # model = Women
    template_name= 'women/index.html'
    context_object_name = 'posts'
    extra_context =  {
        'title': "Главная самая страница",
        'menu': menu,
        'cat_selected': 0,

    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context= super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))

    #     return context

@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'women/about.html', {'title': "О сайте", 'menu': menu, 'page_obj':page_obj})




# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#         #     try:
#         #         Women.objects.create(**form.cleaned_data)
#         #         return redirect('home')
#         #     except:
#         #         form.add_error(None,"Ошибка заполнения")
#         # else:
#         #     print(form.errors)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()

#     data = {
#           'menu': menu,
#           'title':"Добавление статьи",
#           'form': form
#     }
#     return render(request, 'women/addpage.html',data )  

# class AddPage(View):
#     def get(self,request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title':"Добавление статьи",
#             'form': form
#         }
#         return render(request, 'women/addpage.html',data )

#     def post(self,request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
        
#         data = {
#             'menu': menu,
#             'title':"Добавление статьи",
#             'form': form
#         }
#         return render(request, 'women/addpage.html',data ) 

class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    # model= Women
    # fields = ['title', 'slug', 'content', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    extra_context =  {
        'title': "Добавление статьи",
        'menu': menu,        
    }
    

class UpdatePage(UpdateView):
    model= Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    extra_context =  {
        'title': "Редактирование статьи",
        'menu': menu,        
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class WomenDeleteView(DeleteView):
    model = Women
    template_name = 'women/women_confirm_delete.html'
    success_url = reverse_lazy('home')  

extra_context =  {
        'title': "Удаление статьи",
        'menu': menu,        
    }


def contact(request):
    return HttpResponse('Страница контакта')


def login(request):
    return HttpResponse('Логин вход')


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts= Women.published.filter(cat_id=category.pk).select_related('cat')
#     data = {
#         'title': f"Рубрика:{category.name}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,

#     }
#     return render(request, 'women/index.html', context=data)

class WomenCategory(DataMixin,ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk

        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug= tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

    data ={
        'title':f"Тег: {tag.tag}",
        'menu':menu,
        'posts':posts,
        "cat_selected":None,

    }

    return render(request,'women/index.html',context=data)

class TagCategory(DataMixin,ListView):
    
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Тег: {self.tag.tag}"
        context['menu'] = menu
        context['cat_selected'] = None
        return context
        

    