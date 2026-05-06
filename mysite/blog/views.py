from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from .forms import CommentForm, CustomUserCreationForm
from .models import Post, Comment, CustomUser
from django.db.models import Q

# Create your views here.
class PostListView(generic.ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 4


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'photo']
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content', 'photo']
    # success_url = reverse_lazy("posts")

    def get_success_url(self):
        return reverse('post', kwargs={"pk": self.object.pk})


    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    context_object_name = "post"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    template_name = "comment_form.html"
    fields = ['content']

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    context_object_name = "comment"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'photo']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset = ...):
        return self.request.user


def search(request):
    query = request.GET.get('query')
    context = {
        'query': query,
        'posts': Post.objects.filter(Q(title__icontains=query) |
                                     Q(content__icontains=query) |
                                     Q(author__username__icontains=query)),
    }
    return render(request, template_name="search.html", context=context)