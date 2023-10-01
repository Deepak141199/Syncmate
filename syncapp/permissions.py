from rest_framework.permissions import BasePermission

class mypermission(BasePermission):
  def has_permission(self, request, view):
    if request.method in['GET','POST','PUT','PATCH','DELETE']:
      return True
    
    return False