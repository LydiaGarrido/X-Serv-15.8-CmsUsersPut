from django.shortcuts import render

# Create your views here.

from cms_users_put.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


FORMULARIO = """
    <form method = 'POST'>
    <b>Nombre: </b><br>
    <input type='text' name='nombre'><br>
    <b>Pagina: </b><br>
    <input type='text' name='page'><br>
    <input type='submit' value='Enviar'></form>
"""

def barra(request):
    content = Pages.objects.all()
    if request.user.is_authenticated():
        respuesta = "Logged in as " + request.user.username
        respuesta += ". <b><a href='logout'>Logout</a></b><br>"
    else:
        respuesta = "Not logged in. <b><a href='login'>Login</a></b><br>"
    respuesta += "<br>Páginas almacenadas:<br>"
    for pagina in content:
        respuesta += "<ul><li>" + pagina.name + " / " + pagina.page + "</ul></li>"
    return HttpResponse(respuesta)


@csrf_exempt
def pag(request, resource):
    if request.method == "GET":
        try:
            pagina = Pages.objects.get(name=resource)
            respuesta = pagina.page + "<br>"
        except Pages.DoesNotExist:
            if request.user.is_authenticated():
                respuesta = "La página no existe<br>"
                respuesta += FORMULARIO
                return HttpResponse(respuesta)
            else:
               volver = '<a href="http://localhost:8000/">Inicio</a>'
               respuesta = "La página no existe. Es necesario iniciar sesión para crear una nueva página. "
               return HttpResponse(respuesta + volver)

    elif request.method == "POST":
        name = request.POST['nombre']
        page = request.POST['page']
        nueva_pag = Pages(name=name, page=page)
        nueva_pag.save()
        respuesta = "Pagina guardada"

    elif request.method == "PUT":
        if request.user.is_authenticated():
            pag = Pages(name=resource, page=request.body)
            pag.save()
            volver = '<a href="http://localhost:8000/">Inicio</a>'
            respuesta = "Se ha guardado la pagina " + pag.name + ". " + volver
        else:
            volver = '<a href="http://localhost:8000/">Inicio</a>'
            respuesta = "Para crear una pagina se necesita hacer login " + volver
    else:
        return HttpResponse("Metodo no permitido")

    return HttpResponse(respuesta)

def error(request):
    volver = '<a href="http://localhost:8000/">Inicio</a>'
    respuesta = "Ha ocurrido un error: la pagina no esta disponible. " 
    HttpResponse(respuesta + volver)

