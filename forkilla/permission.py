from rest_framework import permissions

class IsCommercialOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		print('calling is commercial')
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.groups.filter(name="commercial").exists()

	def has_object_permission(self, request, view, obj):
		print('calling is commercial')
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.groups.filter(name="commercial").exists()
