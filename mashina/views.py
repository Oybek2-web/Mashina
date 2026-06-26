from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Mashina
from .forms import MashinaForms
from groq import Groq
import os
import json

groq_api_key = getattr(settings, 'GROQ_API_KEY', None) or os.getenv('GROQ_API_KEY')

if not groq_api_key:
    print("⚠️ WARNING: GROQ_API_KEY topilmadi!")
    client = None
else:
    print("✅ GROQ_API_KEY yuklandi")
    client = Groq(api_key=groq_api_key)


def mashina_list(request):
    mashina = Mashina.objects.all()
    return render(request, 'mashina/mashina_list.html', {'mashina': mashina})


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
    return render(request, 'mashina/mashina_update.html', {'form': form})


def mashina_delete(request, id):
    mashina = get_object_or_404(Mashina, id=id)
    mashina.delete()
    return redirect('mashina_list')


def chat_interface(request):
    return render(request, 'chat_interface.html')


@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            print(f"📩 Xabar: {user_message}")

            if not client:
                return JsonResponse({
                    'success': False,
                    'error': 'Groq API kaliti sozlanmagan'
                })

            system_prompt = """Siz Mashina (avtomobillar) sayti uchun yordamchi assistantsiz. 
            Foydalanuvchilarga avtomobillar, ularning xususiyatlari, narxlari va boshqa 
            savollariga javob berasiz. Doimo o'zbek tilida javob bering."""

            # ✅ YANGI MODEL
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            print(f"🤖 Javob: {ai_response}")

            return JsonResponse({
                'success': True,
                'response': ai_response
            })

        except Exception as e:
            print(f"❌ XATO: {str(e)}")
            import traceback
            traceback.print_exc()

            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Invalid request'})