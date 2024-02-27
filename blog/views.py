from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from .models import BlogPost
from django.shortcuts import redirect


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'post_content', 'preview',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        form.instance.view_count = 0  # Устанавливаем начальное количество просмотров

        # Получаем изображение из формы и сохраняем его в поле модели
        if 'preview' in self.request.FILES:
            form.instance.preview = self.request.FILES['preview']

        return super().form_valid(form)
    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'post_content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'slug': self.object.slug})


class BlogListView(ListView):
    model = BlogPost
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # Увеличиваем счетчик просмотров
        self.object = self.get_object()
        self.object.view_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:list')
