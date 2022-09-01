from pyexpat import model
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from . import models , serializers
import json
# Create your views here.


'''
{
    name
    username
    phone
    email
    password
    
}

'''
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def registerUser(request):
    
    try:
        body = json.loads(request.body)
        assert 'name' in body
        assert 'username' in body
        assert 'phone' in body
        assert 'password' in body

    except Exception as e:
        return Response({'error' : e , "message" : 'provide valid params'} , status=status.HTTP_406_NOT_ACCEPTABLE)
    

    user = User.objects.create(username = body['username'], password = make_password(body['password']))
    
    body['user'] = user
    del body['password']
    profile = models.Profile.objects.create(**body)

    globalDB = models.globalDB.objects.create(profile = profile ,is_registered = True, parent = user)
    
    return Response({"message": "User Created", "success": "true"}, status=status.HTTP_200_OK)


'''
{   
    name
    phone
    email [optional]
    username [optional]
}

'''
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def addContacts(request):
    try: 
        body = json.loads(request.body)
        parent = body['parent']
        del body['parent']
        if 'username' not in body.keys():
            body['username'] = body['name'] + "_" + body['phone'][:5]
        profile = models.Profile.objects.create(**body)
        # body['parent'] = parent
        globalDB = models.globalDB.objects.create(profile = profile , is_registered = False )
        
        return Response({"message": "Contact Created", "success": "true"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_406_NOT_ACCEPTABLE)

'''
{'user_id'
    'name',
'phone'
    ''}

'''
@permission_classes([IsAuthenticated])
@api_view(['POST'])  
def searchUser(request):
    try: 
        body = json.loads(request.body)
        keys = list(body.keys())
       
        print(body , body.keys() , list(body.keys()))
        if 'name'== keys[0]:
                result = models.globalDB.objects.filter(profile__name__icontains = body['name'])
        elif 'phone' == keys[0]:
                result = models.globalDB.objects.filter(profile__phone__contains = body['phone'])
        else :
            result = models.globalDB.objects.filter(profile__name__icontains = body['name'] , profile__phone__contains = body['phone'])
        print(result.values_list())
        result_serial = serializers.globalDBSerializer(result , many = True).data
        
        print(result_serial)
        #show email if the user is registered and that contact is owned/added by the user
        return Response({"result": result_serial, "success": "true"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_406_NOT_ACCEPTABLE)

'''
{
    user_id

}

'''
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def markSpamByID(request):
    #update spam % and spam_count
    try:
        body = json.loads(request.body)

        profile = models.Profile.objects.get(uuid = body['user_id'])
        global_user = models.globalDB.objects.get(profile =  profile)
        n_global_user = len(models.globalDB.objects.all())
        global_user.n_spam +=1
        global_user.spam_likelyhood = calculateSpamPercent(global_user.n_spam , n_global_user)
        global_user.save()

        
        return Response({"message": "Contact marked as Spam", "success": "true"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_406_NOT_ACCEPTABLE)

def calculateSpamPercent(n_spam , total_records):
    
        
    spam_percent = (n_spam/total_records) * 100
    print('spam_percent : ',spam_percent ,round(spam_percent ,2))
    return round(spam_percent ,2)