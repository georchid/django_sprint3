from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Post, Category
from django.utils import timezone
from django.views.generic import ListView, DetailView


class IndexListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return (
            Post.objects
            .select_related("category")
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )[:5]
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (
            obj.pub_date > timezone.now()
            or not obj.is_published
            or not obj.category.is_published
        ):
            raise Http404("Публикация не найдена или недоступна")
        return obj


class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "post_list"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs["category_slug"]
        )
        if not self.category.is_published:
            raise Http404("Категория не опубликована")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return (
            queryset
            .select_related("category")
            .filter(
                category=self.category,
                is_published=True,
                pub_date__lte=timezone.now()
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
