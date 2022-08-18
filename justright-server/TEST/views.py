from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.parsers import FileUploadParser 
class FileUploadView(APIView): 
    parser_classes = [FileUploadParser, ] 
    def put(self, request, filename, format=None): 
        file_obj = request.data['file'] 
        with open(filename, 'wb') as f: 
            for chunk in file_obj.chunks(): 
                f.write(chunk) 
        return Response(f'{filename} uploaded',status=204)