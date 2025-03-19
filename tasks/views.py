from rest_framework import status, views, permissions
from django.core.cache import cache
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Task, CustomUser
from .serializers import TaskSerializer, UserRegistrationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

def simulate_lambda_notification(task):
    print(f"AWS Lambda: Task '{task.title}' completed by {task.assigned_to.username}. Notify {task.assigned_by.username}.")

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        assigned_to = request.data.get('assigned_to')
        if not assigned_to:
            return Response({"message": "Assigned user is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            assigned_to = int(assigned_to)  
        except ValueError:
            return Response({"message": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)

        if not CustomUser.objects.filter(id=assigned_to).exists():
            return Response({"message": "Assigned user does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if assigned_to == request.user.id:
            return Response({"message": "You cannot assign tasks to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.data['assigned_by'] = request.user.id

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('assigned_by') == 'me':
            queryset = queryset.filter(assigned_by=self.request.user)

        return queryset

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        task = self.get_object()
        if self.request.user != task.assigned_to:
            raise PermissionDenied("Only the assigned user can update the task status.")
        task = serializer.save()
        if task.status == 'completed':
            simulate_lambda_notification(task)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()

class RateLimitedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    RATE_LIMIT = 5  
    TIME_WINDOW = 60  

    def get_client_identifier(self, request):
        """Identify the client (user or IP)."""
        if request.user.is_authenticated:
            return f"user:{request.user.username}"
        return f"ip:{request.META.get('REMOTE_ADDR')}"

    def get(self, request):
        client_id = self.get_client_identifier(request)
        cache_key = f"rate_limit:{client_id}"
        request_count = cache.get(cache_key, 0)

        if request_count >= self.RATE_LIMIT:
            return Response(
                {"message": "Rate limit exceeded. Try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        cache.set(cache_key, request_count + 1, timeout=self.TIME_WINDOW)

        return Response({"message": "Request successful!"})