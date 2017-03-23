# Django
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from django.utils.translation import ugettext_lazy as _

#Local Django
from .models import Magazine, Article, Subject


class  MagazineDetails(DetailView):
        model = Magazine
        slug_field = 'pk'
        template_name = "templates/magazine_details.html"
        def get_context_data(self, **kwargs):
               context = super(MagazineDetails, self).get_context_data(**kwargs)
               context['article_list'] = Article.objects.filter(
                                                magazine=self.get_object()
                                                )
               return context


class MagazinesList(ListView):
    model = Magazine
    template_name = "templates/magazines_list.html"
    paginate_by = 10
    def get_queryset(self):
          query_set = self.model.objects.filter(
                                    subjects=self.kwargs.get('subjects')
                                    )
          return query_set
