from usuarios.models import UserProfile

def menu(request):	
	"""
	if request.user.is_authenticated():
		profile = UserProfile.objects.get(usuario=request.user)
		ctx = {'usuario':profile}
		return ctx
	else:"""
	return {'usuario': 'none'}