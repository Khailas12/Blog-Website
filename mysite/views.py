from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from .models import TheBlog
from .forms import BlogForms
from django.http import Http404
from django.http import HttpResponseRedirect


@csrf_protect
def create_blog(request, *args, **kwargs):
    form = BlogForms(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form = BlogForms()
            
            context = {
                'form': form,
                'instance': instance,
                }
            return (redirect, 'blog_view.html', context)
    
        else:
            Http404
        
    context = {'form': form}        
    return render(request, 'forms.html', context)