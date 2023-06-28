from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View

import blog
from blog.forms import RegisterUserForm, PostForm, RegisterEditUserForm, CommentForm, LoginForm
from blog.models import Post, Category, Author, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


class LoginPageView(View):
    template_name = "registration/login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={
            "form": form,
            "message": message
        }
                      )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("/")
        message = "Login failed!"
        return render(request, self.template_name, context={
            "form": form,
            "message": message}
                      )


class AuthorRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("login")


class AuthorEditView(UpdateView):
    form_class = RegisterEditUserForm
    template_name = "registration/author_edit_registration.html"
    success_url = reverse_lazy("blog:post-list")

    def get_object(self, queryset=None):
        return self.request.user


class AuthorEditPasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "registration/author_password_change.html"
    success_url = reverse_lazy("author-password-success")


def password_success(request):
    return render(request, "registration/author_password_success.html")


class AuthorListView(ListView):
    model = Author
    template_name = "registration/author_list.html"


class AuthorDetailView(DetailView):
    model = Author
    template_name = "registration/author_detail.html"
    queryset = Author.objects.all().prefetch_related("follows")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_post_list'] = Post.objects.all().select_related("authors").filter(authors=self.object)
        context['author'] = self.object
        return context


def follow_user(request, pk):
    author_obj = Author.objects.get(id=pk)
    current_user_obj = Author.objects.get(id=request.user.id)
    following = author_obj.follows.all().prefetch_related("follows")

    if pk != current_user_obj.id:
        if current_user_obj in following:
            author_obj.follows.remove(current_user_obj.id)
        else:
            author_obj.follows.add(current_user_obj.id)
    return HttpResponseRedirect(reverse("author-detail", args=[author_obj.id]))


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = ["-id"]
    queryset = Post.objects.all().prefetch_related("authors")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    queryset = Post.objects.all().prefetch_related("authors")

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = "blog/post_form.html"


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = "__all__"
    success_url = reverse_lazy("blog:post-list")


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_delete_confirm.html"
    success_url = reverse_lazy("blog:post-list")


class CategoryListView(ListView):
    model = Category
    template_name = "blog/category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "blog/category_detail.html"


class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"
    template_name = "blog/category_form.html"
    success_url = reverse_lazy("blog:category-list")


class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"
    template_name = "blog/category_form.html"
    success_url = reverse_lazy("blog:category-list")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "blog/category_delete_confirm.html"
    success_url = reverse_lazy("blog:category-list")


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("blog:post-detail", args=[str(pk)]))


class CommentCreateView(CreateView):
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        form.instance.post_id = self.kwargs["pk"]
        return super().form_valid(form)
