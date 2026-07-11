from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import redirect
from django.http import JsonResponse
from .google_calendar import get_flow, get_service, get_busy_slots


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
    auth_url, state = flow.authorization_url(
        prompt='consent',
        access_type='offline',
    )
    code_verifier = flow.code_verifier
    # code_verifierをstateと一緒にキャッシュファイルに保存
    import json, os
    cache = {}
    cache_file = 'oauth_cache.json'
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            cache = json.load(f)
    cache[state] = code_verifier
    with open(cache_file, 'w') as f:
        json.dump(cache, f)
    return redirect(auth_url)

def oauth_callback(request):
    state = request.GET.get('state')
    import json, os
    cache_file = 'oauth_cache.json'
    code_verifier = None
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            cache = json.load(f)
        code_verifier = cache.get(state)
    print('callback code_verifier:', code_verifier)
    flow = get_flow()
    flow.fetch_token(
        authorization_response=request.build_absolute_uri(),
        state=state,
        code_verifier=code_verifier
    )
    creds = flow.credentials
    request.session['token'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
    }
    return JsonResponse({'message': 'ログイン成功'})

def index_view(request):
   return render(request, 'index.html')

class FreeSlotsView(APIView):
    def get(self, request):
        token = request.session.get('token')
        if not token:
            return Response({'error': 'ログインしてください'}, status=401)
        service = get_service(token)
        free_time = get_busy_slots(service)
        return Response({'busy_slots':free_time})
