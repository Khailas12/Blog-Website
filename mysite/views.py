from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from .models import TheBlog
from .forms import BlogForms
from django.http import Http404
from django.core import serializers



@csrf_protect
def create_blog(request, *args, **kwargs):
    form = BlogForms(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.cleaned_data
            instance.save()
            form = BlogForms()

        else:
            Http404
            
        
    context = {'form': form}        
    return render(request, 'forms.html', context)


def blog_view(request, pk, *args, **kwargs):
    try:
        # blog = TheBlog.objects.get(pk=pk)
        blog = TheBlog.objects.get(id=pk)
    except TheBlog.DoesNotExist:
        raise Http404('Blog not found')
    
    context = {'blog': blog}
    return render(request, 'blog/blog_view.html', context)