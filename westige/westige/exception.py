from rest_framework import status
from rest_framework.response import Response


def Custom_exception_handler(exc,context):
    
    print("exception ======================>",exc)
    if isinstance(exc,KeyError):
        return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(exc),"data":{}})
    if isinstance(exc,TypeError):
        return Response({"status":status.HTTP_400_BAD_REQUEST,"message":str(exc),"data":{}})
    
    detail= exc.detail
    print(detail)
    if isinstance(detail,list):
        return Response({"status":status.HTTP_400_BAD_REQUEST,"message":detail[0],"data":{}})
    if isinstance(detail,str):
        return Response({"status":status.HTTP_400_BAD_REQUEST,"message":detail,"data":{}})
    
    for key,value in detail.items():
        error=value[0]
    error_message=error
    return Response({"status":status.HTTP_400_BAD_REQUEST,"message":error_message,"data":{}})