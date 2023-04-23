from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Advocate, Company
from .serializer import AdvocateSerializer, CompanySerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET', 'POST'])
def endpoints(request):
    data = ['/advocates', 'advocates/:username']
    return Response(data)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def advocates(request):
    if request.method == "GET":

        query = request.GET.get('query')
        if query is None:
            query = ''
        advocates = Advocate.objects.filter(Q(username__icontains= query))
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        advo = Advocate.objects.create(
            username = request.data['username'],
            bio = request.data['bio']
        )
        serializer = AdvocateSerializer(advo, many=False)
        return Response(serializer.data)
#class based view
class AdvocateDetail(APIView):
    def get(self, request, username):
        try:
            advocate = Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            return Response({'error': 'Advocate not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AdvocateSerializer(advocate)
        return Response(serializer.data)
        
    def put(self, request, username):
        advocate = Advocate.objects.get(username = username)
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def delete(self, request, username):
        advocate = Advocate.objects.get(username = username)
        advocate.delete()
        return Response('User deleted sucessfully')
        

'''Function based views'''
# @api_view(['GET', 'PUT', 'DELETE'])
# def advocates_details(request, username):
#     advocate = Advocate.objects.get(username=username)
#     if request.method == "GET":
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method =="PUT":
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']
#         advocate.save()
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
    
#     if request.method =="DELETE":
#         advocate.delete()
#         return Response('User deleted sucessfully')

@api_view(['GET'])
def companysinfo(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)