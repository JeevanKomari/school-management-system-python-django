from rest_framework import viewsets
from .models import*
from .serializers import*
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class ClsViewSet(viewsets.ModelViewSet):
    queryset = Cls.objects.all()
    serializer_class = ClsSerializer
    permission_classes = [IsAuthenticated]



class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception = True)
        if valid:
            serializer.save()
            status_code= status.HTTP_201_CREATED
            response={
                'success': True,
                'status': status_code,
                'message' : 'user successfully created',
                'user': serializer.data
           }
            return Response( response, status=status_code)
    


TIME_ZONE ='Asia/Kolkata'
class UserLoginViewSet(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        user = User.objects.all()
        

        if valid:
            email= serializer.validated_data['email']
            password= serializer.validated_data['password']
        
            user = authenticate(email=email, password=password)
            if user is not None:
               
                login(request, user)
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                update_last_login(None, user)
                status_code = status.HTTP_200_OK
                response = {
                            'success': True,
                            'statusCode': status_code,
                            'message': 'User logged in successfully',
                            'access': access_token,
                            'refresh': refresh_token,
                            'last_login': user.last_login,
                            'user': serializer.data
                        }

                return Response(response, status=status_code)
                
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
