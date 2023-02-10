from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views import generic

from .forms import NewOrUpdateBlogPostForm
from .models import Blog


def home_view(request):
    return render(request, '_base.html')


def list_view(request):
    return render(
        request=request,
        template_name='pages/list_view.html',
        context={
            'blogs_list': Blog.objects.filter(is_active=True).all()
        }
    )


@login_required
def detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.is_active:
        return render(
            request=request,
            template_name='pages/detail_view.html',
            context={
                'blog': blog
            }
        )
    else:
        return redirect(reverse('home_url'))


class AddBlogView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = NewOrUpdateBlogPostForm
    template_name = 'pages/add_blog.html'

    def test_func(self):
        return self.request.user.is_staff