from django.db.models import query
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .models import TheBlog
from .forms import BlogForms
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q


class BlogHome(ListView):
    model = TheBlog
    template_name = 'index.html'
    
    def get_queryset(self):
        queryset = TheBlog.objects.all()

        return queryset            


@csrf_protect
@login_required
def create_blog(request, *args, **kwargs):
    form = BlogForms(request.POST or None)
    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.cleaned_data
            instance.save()
            form = BlogForms()
            
            # blog_id = request.GET.get('b_id')
            # print('first', blog_id)
            # b_id = {'blog_id.b_id': blog_id}

            # response = HttpResponse(status=302)
            # response = HttpResponseRedirect(f'/blog/{b_id}/')
            # return response
            return redirect('/')

        else:
            Http404
            
    context = {'form': form}        
    return render(request, 'forms.html', context)


@csrf_protect
@login_required
def blog_view(request, pk, *args, **kwargs):

    blog = get_object_or_404(TheBlog, pk=pk)
    
    context = {'blog': blog}
    return render(request, 'blog/blog_view.html', context)