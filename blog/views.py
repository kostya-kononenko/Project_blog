from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from blog import forms
from blog.forms import RegisterUserForm, PostForm
from blog.models import Post, Author, Category
from django.http import HttpResponseRedirect


class LoginPageView(View):
    template_name = "registration/login.html"
    form_class = forms.LoginForm

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


class RegisterUserView(CreateView):
    model = Author
    template_name = "registration/registration.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("login")


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    ordering = ["-id"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

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
