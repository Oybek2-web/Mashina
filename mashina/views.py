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


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def chat_interface(request):
    return render(request, 'chat_interface.html')


@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Sayt mavzusi bo'yicha kontekst
        system_prompt = """Siz Mashina (avtomobillar) sayti uchun yordamchi assistantsiz. 
        Foydalanuvchilarga avtomobillar, ularning xususiyatlari, narxlari va boshqa 
        savollariga javob berasiz. O'zbek tilida javob bering."""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # yoki "gpt-4"
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content

            return JsonResponse({
                'success': True,
                'response': ai_response
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Invalid request'})