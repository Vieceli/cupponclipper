from cuponclipper001.contas.models import MeuUser
from cuponclipper001.contas.forms import FormularioRegistro

def getPerfil(request):
    """ gets the UserProfile instance for a user, creates one if it does not exist """
    try:
        perfil = request.user.get_profile()
    except:
        perfil = MeuUser(user=request.user)
        perfil.save()
    return perfil

def setPerfil(request):
    """ updates the information stored in the user's profile """
    perfil = getPerfil(request)
    perfil_form = FormularioRegistro(request.POST, instance=perfil)
    perfil_form.save()
    
