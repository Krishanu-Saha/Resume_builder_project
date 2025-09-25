from rest_framework.permissions import BasePermission

# ✅ Admins only
class IsAdmin(BasePermission):
    """
    Permission that allows access only to admins.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'admin'
        )


# ✅ Resume users can only access their own resumes
class IsResumeOwner(BasePermission):
    """
    Permission that allows resume_users to access only their own resumes.
    Admins are NOT included here.
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'resume_user'
        )

    def has_object_permission(self, request, view, obj):
        # Only allow if the object belongs to the requesting user
        return hasattr(obj, "user") and obj.user == request.user


# ✅ Admins can access everything, Resume users can access only their own
class IsResumeOwnerOrAdmin(BasePermission):
    """
    - Admins have full access to all resumes
    - Resume users can only access their own resumes
    """
    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and request.user.role in ['admin', 'resume_user']
        )

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return hasattr(obj, "user") and obj.user == request.user
