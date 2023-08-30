from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializers
from .models import User
import jwt,datetime



class RegisterView(APIView):
    def post(self,request):
        serializer= UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incoreect Password')

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token=jwt.encode(payload,'secret',algorithm='HS256')

        response= Response()
        response.set_cookie(key='jwt',value=token,httponly=True)

        response.data={
            'jwt':token
        }
        
        return  response


class UserView(APIView):
    def get(self,request):
        token =request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializers(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'success'
        }
        return response


# class UserView(APIView):
#     def get(self, request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('Unauthenticated')

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])

#             user = User.objects.filter(id=payload.get('id')).first()

#             if user is None:
#                 raise AuthenticationFailed('User not found')

#             serializer = UserSerializers(user)

#             # Include the token in the response
#             response_data = {
#                 'user': serializer.data,
#                 'token': token
#             }

#             return Response(response_data)

#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token has expired')
#         except jwt.DecodeError:
#             raise AuthenticationFailed('Token is invalid')