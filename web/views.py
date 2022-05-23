from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from web.models import User
from web.serializers import UserSerializer

# Create your views here.
class PingPongView(APIView):
    def get(self, request):
        return Response({"message": "pong"})


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
