
import os
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
)
import requests
import json
from dotenv import load_dotenv
load_dotenv()

from .models import Plan

VSEGPT_KEY= os.getenv('VSEGPT_KEY')
def gptiha(text):
    vopros=f'''
    Составь план по этому описанию: {text}. ТОЛЬКО ПЛАН В ВИДЕ НУМЕРОВАННОГО СПИСКА, БЕЗ ПРИВЕТ ПОКА И Т.П ТОЛЬКО ПЛАН.
    '''
    
    

    # Выполнение POST запроса
    response = requests.post(
        "https://api.vsegpt.ru/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {VSEGPT_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-5-nano",
            "messages": [{"role": "user", "content": vopros}]
        }
    )

    # Обработка ответа
    try:
        response_data = response.json()
        msg = response_data["choices"][0]["message"]["content"]
        print(msg.strip())
        return msg.strip()
    except KeyError:
        print("Ошибка api")
        return "Нейросети не удалось обработать ваш запрос из-за недействительного api ключа"
    

User = get_user_model()


class IndexPage(TemplateView):
    template_name = 'FiveMinutesTasks/index.html'



class PlanListView(ListView):
    model = Plan
    template_name = 'FiveMinutesTasks/allplans.html'
    context_object_name = 'plans'
    paginate_by = 3


class PlanDetailView(DetailView):
    model = Plan
    template_name = 'FiveMinutesTasks/plan_detail.html'
    context_object_name = 'plan'
    

class PlanCreateView(LoginRequiredMixin, CreateView):
    model = Plan
    fields = ['title', 'content']
    template_name = 'FiveMinutesTasks/ask.html'
    success_url = reverse_lazy('allplans')

    def form_valid(self, form):
        form.instance.owner = self.request.user

        # Взяли текст из textarea
        content_text = form.cleaned_data['content']

        # Передали в gptiha
        result = gptiha(content_text)

        # Если хочешь — записываем ответ ИИ в модель
        form.instance.content = result  # если есть поле
        
        # Сохраняем экземпляр, чтобы слаг был сгенерирован в save() методе
        self.object = form.save(commit=False)
        self.object.save()
        
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'FiveMinutesTasks/profile.html'

    def get_context_data(self, **kwargs):
        username = kwargs.get('username')
        profile_user = get_object_or_404(User, username=username)
        ctx = super().get_context_data(**kwargs)
        # put the viewed user under a different name so we don't overwrite
        # the request user available in the template context as `user`.
        ctx['profile_user'] = profile_user
        ctx['plans'] = Plan.objects.filter(owner=profile_user)
        return ctx
    
    

class UserPlansView(ListView):
    model = Plan
    template_name = 'FiveMinutesTasks/allplans.html'
    context_object_name = 'plans'
    paginate_by = 12

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Plan.objects.filter(owner=user).order_by('-created_at')
    

class About(TemplateView):
    template_name = "FiveMinutesTasks/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "О нас"
        return context