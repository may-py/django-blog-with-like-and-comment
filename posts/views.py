from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = '-date_created'
    template_name = 'posts/home.html'

class UsersPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = '-date_created'
    template_name = 'posts/user_post.html'

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        context['total_likes'] = stuff.total_likes()
        return context

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/createupdate.html'
    fields = ['title','content','image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/createupdate.html'
    fields = ['title','content','image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
            
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
    

def PostLikeView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if not request.user in post.likes.all():
        post.likes.add(request.user)
        # return HttpResponseRedirect(reverse('posts:post-detail', args=[str(pk)]))
        return redirect(request.META['HTTP_REFERER'])
    else:
        post.likes.remove(request.user)
        # return HttpResponseRedirect(reverse('posts:post-detail', args=[str(pk)]))
        return redirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(reverse('posts:post-detail', args=[str(pk)]))



class CommentView(CreateView):
    model = Comment
    template_name = 'posts/comment.html'
    fields = ["body"]

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        # form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('posts:post-detail',kwargs={'pk':self.kwargs['pk']})


class CommentDeleteView(DeleteView):
    model= Comment
    template_name = 'posts/comment.html'

    def test_func(self):
        comment = get_objects()
        if comment.name == self.request.user:
            return True
        else:
            return False
    
    def get_success_url(self):
        post = get_object_or_404(Post,id=self.request.POST.get('post_id'))
        return reverse_lazy('posts:post-detail', kwargs={'pk':post.id})

