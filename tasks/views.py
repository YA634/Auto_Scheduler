from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import redirect
from django.http import JsonResponse
from .google_calendar import get_flow

class TaskView(viewsets.ModelViewSet):
  model = Task
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

#GET    /api/tasks/      → 一覧取得
#POST   /api/tasks/      → 新規作成
#GET    /api/tasks/1/    → 詳細取得
#PUT    /api/tasks/1/    → 更新
#DELETE /api/tasks/1/    → 削除

#Googleログイン画面へリダイレクト
def oauth_login(request):
    flow = get_flow()
    auth_url, state = flow.authorization_url(prompt='consent')
    request.session['state'] = state
    return redirect(auth_url)

#Googleログイン後に戻ってくるURL
def oauth_callback(request):
    flow = get_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials
    request.session['token'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
    }
    return JsonResponse({'message': 'ログイン成功'})