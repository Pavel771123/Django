menu = [
    {'title': 'Об этом сайте', 'url_name': 'about', },
    {'title': 'Добавить статью', 'url_name': 'add_page', },
    {'title': 'Обратная связь', 'url_name': 'contact', },
    ]

class DataMixin:
    title_page = None
    extra_context = {}
    cat_selected = None

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = menu

    def get_mixin_context(self,context,**kwargs):
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context


    paginate_by = 3
    