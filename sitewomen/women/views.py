from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView,FormView, CreateView, UpdateView, DeleteView

from .utils import DataMixin
from .forms import AddPostForm, ContactForm, UploadFileForm
from django.core.paginator import Paginator

from .models import Category, TagPost, UploadFiles, Women
# Create your views here.


menu = [
    {'title': 'Об этом сайте', 'url_name': 'about', },
    {'title': 'Добавить статью', 'url_name': 'add_page', },
    {'title': 'Обратная связь', 'url_name': 'contact', },
]





class ShowPost(DataMixin,DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg= 'post_slug'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        return self.get_mixin_context(context,title=context['post'].title, cat_selected=post.cat_id)
        

    def get_object(self, queryset=None):
        return get_object_or_404(Women.objects.all(), slug=self.kwargs[self.slug_url_kwarg])

def index(request):
    return HttpResponse('Страница приложения women.')



class WomenHome(DataMixin,ListView):
    # model = Women
    template_name= 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat', 'author')



@login_required
def about(request):
    contact_list = Women.published.all().select_related('cat', 'author')
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'women/about.html', {'title': "О сайте", 'menu': menu, 'page_obj':page_obj})





class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    extra_context =  {
        'title': "Добавление статьи",
        'menu': menu,        
    }
    

class UpdatePage(PermissionRequiredMixin, DataMixin,UpdateView):
    model= Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women'
    
    slug_field = 'slug'  # ← какое поле использовать как slug
    slug_url_kwarg = 'post_slug'  # ← как называется параметр в path()

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class WomenDeleteView(DataMixin,DeleteView):
    model = Women
    template_name = 'women/women_confirm_delete.html'
    success_url = reverse_lazy('home')  

extra_context =  {
        'title': "Удаление статьи",
        'menu': menu,        
    }


class ContactFormView(LoginRequiredMixin,DataMixin,FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page='Обратная связь'

    def form_valid(self,form):
        print(form.cleaned_data)
        return super().form_valid(form)

def login(request):
    return HttpResponse('Логин вход')


class WomenCategory(DataMixin,ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat','author')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,title = 'Категория - ' + cat.name, cat_selected = cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug= tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')

#     data ={
#         'title':f"Тег: {tag.tag}",
#         'menu':menu,
#         'posts':posts,
#         "cat_selected":None,

#     }

#     return render(request,'women/index.html',context=data)

class TagCategory(DataMixin,ListView):
    
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat', 'author')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        
        return self.get_mixin_context(context,title = 'Тег ' + tag.tag)
        

    