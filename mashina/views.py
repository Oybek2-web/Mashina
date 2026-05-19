from django.shortcuts import render, redirect, get_object_or_404
from .models import Mashina
from .forms import MashinaForms

def mashina_list(request):
    mashina = Mashina.objects.all()
    return render(request, 'mashina/mashina_list.html', {'mashina':mashina})

def mashina_create(request):
    if request.method == 'POST':
        form = MashinaForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mashina_list')
    form = MashinaForms()
    return render(request, 'mashina/mashina_create.html', {'form': form})

def mashina_update(request, id):
    mashina = get_object_or_404(Mashina, id=id)
    if request.method == 'POST':
        form = MashinaForms(request.POST, instance=mashina)
        if form.is_valid():
            form.save()
            return redirect('mashina_list')
    else:
        form = MashinaForms(instance=mashina)
    return render(request,'mashina/mashina_update.html',{'form': form})

def mashina_delete(request, id):
    mashina = get_object_or_404(Mashina, id=id)
    mashina.delete()
    return redirect('mashina_list')


