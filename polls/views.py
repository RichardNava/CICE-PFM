from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import (login as auth_login, authenticate)
from .models import Paciente, Sintoma, Patologia, DetalleInforme, Informe
import csv

hepatitis_list = ['HEPATITIS A, HEPATITIS B, HEPATITIS C, HEPATITIS D, HEPATITIS E']
lipo_list = ['HIPERCOLESTEROLEMIA','HIPERTRIGLICERIDEMIA']

def calcular_imc(peso,altura):
    altura_imc = altura/100
    imc = peso/(altura_imc**2)
    return imc

def resultado_imc(paciente):
    imc = calcular_imc(paciente.peso,paciente.altura)
    if (imc < 16):
        return "Delgadez severa"
    elif (imc < 16.99):
        return "Delgadez moderada"
    elif (imc < 18.49):
        return "Delgadez aceptable"
    elif (imc < 24.99):
        return "Peso normal"
    elif (imc < 29.99):
        return "Sobrepeso"
    elif (imc < 34.99):
        return "Obesidad"

def calcular_carga(dic_pat,dic_sint,paciente:Paciente):
    carga_total = 0

    for key_sint, obj_sint in dic_sint.items():
        carga_total += obj_sint.grado
        for key_pat in dic_pat.keys():
            if key_sint.upper() == 'DIFICULTAD RESPIRATORIA': 
                if key_pat.upper() == 'ASMA':
                    carga_total += 5
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 3
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 3
                elif  key_pat.upper() == 'ALERGIAS A POLENES':
                    carga_total += 4
                elif  key_pat.upper() == 'APNEA DEL SUEÑO':
                    carga_total += 2                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 10
            if key_sint.upper() == 'DISNEA' or key_sint.upper() == 'APNEA': 
                if key_pat.upper() == 'ASMA':
                    carga_total += 3
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 2
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 2
                elif  key_pat.upper() == 'ALERGIAS A POLENES':
                    carga_total += 2
                elif  key_pat.upper() == 'APNEA DEL SUEÑO':
                    carga_total += 3                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 3
            if key_sint.upper() == 'FIEBRE ALTA' or key_sint.upper() == 'FIEBRE MEDIA': 
                if key_pat.upper() in hepatitis_list:
                    carga_total += 10
                elif  key_pat.upper() == 'OTRAS ALERGIAS':
                    carga_total += 4
                elif  key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 5
                elif  key_pat.upper() == 'SIDA':
                    carga_total += 10
                elif  key_pat.upper() == 'TRANSPLANTE PREVIO RECIENTE':
                    carga_total += 10                    
                elif  key_pat.upper() == 'TUBERCULOSIS':
                    carga_total += 10
                elif  key_pat.upper() == 'CISTITIS RECURRENTE' or key_pat.upper() == 'CANDIDIASIS RECURRENTE':
                    carga_total += 3
            if key_sint.upper() == 'DOLOR ABDOMINAL': 
                if key_pat.upper() in hepatitis_list:
                    carga_total += 10
                elif key_pat.upper() == 'INSUFICIENCIA RENAL':
                    carga_total += 8
                elif key_pat.upper() == 'ALERGIAS ALIMENTARIAS':
                    carga_total += 6
                elif key_pat.upper() == 'INTOLERANCIAS':
                    carga_total += 6
                elif key_pat.upper() == 'ENFERMEDAD DE CROHN':
                    carga_total += 10                    
                elif key_pat.upper() in lipo_list:
                    carga_total += 2
            if key_sint.upper() == 'PALPITACIONES': 
                if key_pat.upper() == 'PROBLEMAS DE COAGULACION':
                    carga_total += 5
                elif key_pat.upper() == 'INSUFICIENCIA CARDIACA':
                    carga_total += 20
            if key_sint.upper() == 'VERTIGOS' and key_pat.upper() == 'VERTIGOS':
                carga_total += 20

    for key_pat, obj_pat in dic_pat.items():
        carga_total += obj_pat.grado

    res_imc = resultado_imc(paciente)
    if res_imc == "Delgadez severa":
        carga_total += 2
        if paciente.edad <= 12 or paciente.edad >= 80: 
            carga_total -= 1
    elif res_imc == "Delgadez moderada":
        carga_total += 1
    elif res_imc == "Sobrepeso":
        carga_total += 1
        if paciente.edad <= 16 or paciente.edad >= 50:
            carga_total += 1
    elif res_imc == "Obesidad":
        carga_total += 3
        if paciente.edad <= 16 or paciente.edad >= 50:
            carga_total += 1

    if paciente.edad >= 80:
        carga_total +=2
    elif paciente.edad >= 60:
        carga_total +=1 

    return carga_total

def create_sintoma(request,nombre,grado,valor_adicional):
    obj = Sintoma.create(nombre,grado,valor_adicional)
    return HttpResponse(obj)

def create_paciente(dni,edad,peso,altura):
    obj = Paciente.create(dni,edad,peso,altura)
    return HttpResponse(obj)

def create_patologia(request,nombre,grado,valor_adicional):
    obj = Patologia.create(nombre,grado,valor_adicional)
    return HttpResponse(obj)

def determinar_gravedad(carga_total):
    if carga_total <= 10:
        print('Resultado = Leve')
        return 'LEVE: Pida cita en su Centro de Salud.'
    elif carga_total <= 20:
        print('Resultado = Moderado')
        return 'MODERADO: Acuda de urgencia a su Centro de Salud.'
    else:
        print('Resultado = Grave')
        return 'GRAVE: Acuda de urgencia a un Hospital.'

def consulta_informe(dni):
    lista_patologia,lista_sintoma,paciente = informe(dni)
    carga = calcular_carga(lista_patologia,lista_sintoma,paciente)
    print(carga)
    resultado = determinar_gravedad(carga)
    return HttpResponse(str(resultado))

def informe(dni):
    paciente = Paciente.objects.get(dni=dni)
    informe = Informe.objects.filter(fk_paciente=paciente).last()
    lista_sintoma= DetalleInforme.objects.filter(fk_informe=informe, fk_patologia=None)
    lista_patologia = DetalleInforme.objects.filter(fk_informe=informe, fk_sintoma=None)

    dic_sin = {}
    for item in lista_sintoma:
        dic_sin[ item.fk_sintoma.nombre ] = item.fk_sintoma

    dic_pat = {}
    for item in lista_patologia:
        dic_pat [ item.fk_patologia.nombre ] = item.fk_patologia

    return dic_pat,dic_sin,paciente

#! PASO 1
def datos_paciente(request):
    msg = 'Introduzca sus datos'
    if request.method == 'POST':
        # if Paciente.objects.get(dni=request.POST['dni']) is not None:
        paciente = Paciente.create(request.POST['dni'],request.POST['edad'],request.POST['peso'],request.POST['altura'])
        informe = Informe.objects.create(fk_paciente=paciente)
        patologias = Patologia.objects.all()
        patologias1 = patologias[len(patologias)//2:]
        patologias2 = patologias[:len(patologias)//2]
        context = {'paciente': paciente, 'patologias': patologias, 'patologias1': patologias1, 'patologias2': patologias2}
        return render(request,'Mysite/patologias.html', context)
        # else:
        #     msg = 'El paciente ya existe'

    context = {'message': msg}
    return render(request,'Mysite/datosPaciente.html', context)

def patologias_form(request):
    msg = 'PRUEBA'
    if request.method == 'POST':
        patologias = Patologia.objects.all()
        sintomas = Sintoma.objects.all()      
        paciente = Paciente.objects.get(dni=request.POST['dni'])
        informe = Informe.objects.filter(fk_paciente=paciente).last()      
        for pat in patologias:
            if request.POST.get(pat.nombre):
                patologia = Patologia.objects.get(id=request.POST[pat.nombre])
                obj = DetalleInforme.objects.create(fk_informe=informe, fk_patologia = patologia, fk_sintoma=None)
        context = {'paciente': paciente, 'patologias': patologias, 'sintomas': sintomas}
        return render(request,'Mysite/sintomas.html', context)
    context = {'message': msg}
    return render(request,'Mysite/patologias.html', context)

def sintomas_form(request):
    msg = 'PRUEBA'
    if request.method == 'POST':
        sintomas = Sintoma.objects.all()
        paciente = Paciente.objects.get(dni=request.POST['dni'])
        informe = Informe.objects.filter(fk_paciente=paciente).last()      
        for sint in sintomas:
            if request.POST.get(sint.nombre):
                sintoma = Sintoma.objects.get(id=request.POST[sint.nombre])
                obj = DetalleInforme.objects.create(fk_informe=informe, fk_patologia = None, fk_sintoma=sintoma)
        # context = {'paciente': paciente, 'patologias': patologias}
        consulta_informe(request.POST['dni'])
        # return render(request,'Mysite/resultado.html', context)
    context = {'message': msg}
    return render(request,'Mysite/sintomas.html', context)

def load_sint_csv(request):
    file_csv = open('D:/Programación/Cice/Proyecto/mysite/sintomas.csv', 'r',encoding='utf8') #! Sustituir el path antes de realizar la carga de los sintomas a la BBDD
    read = csv.reader(file_csv)
    sint_resp = ''
    lista_sintoma = Sintoma.objects.all()
    dic_sin = {}
    for item in lista_sintoma:
        dic_sin[ item.nombre ] = item
    for row in read:
        if not row[0].upper() in dic_sin.keys():
            obj = Sintoma.create(row[0].upper(),row[1],row[2])
            sint_resp += obj.toStr() + '<br>'
        else:
            sint_resp += 'El sintoma '+row[0].upper()+' ya existe en la base de datos. <br>'
    file_csv.close()
    return HttpResponse(sint_resp)

def load_pat_csv(request):
    file_csv = open('D:/Programación/Cice/Proyecto/mysite/patologias.csv', 'r',encoding='utf8') #! Sustituir el path antes de realizar la carga de los sintomas a la BBDD
    read = csv.reader(file_csv)
    pat_resp = ''
    lista_patologia = Patologia.objects.all()
    dic_pat = {}
    for item in lista_patologia:
        dic_pat[ item.nombre ] = item
    for row in read:
        if not row[0].upper() in dic_pat.keys():
            obj = Patologia.create(row[0].upper(),row[1],row[2])
            pat_resp += obj.toStr() + '<br>'
        else:
            pat_resp += 'La Patologia '+row[0].upper()+' ya existe en la base de datos. <br>'
    file_csv.close()
    return HttpResponse(pat_resp)

#! HTML
def prueba(request,dni):
    patologias = Patologia.objects.all()
    sintomas = Sintoma.objects.all()
    pacientes = Paciente.objects.filter(dni=dni).first()
    datos = {'patologias': patologias,'sintomas': sintomas, 'pacientes': pacientes}
    return render(request, 'Mysite/prueba.html', datos)

#! LABELS
def ejemplo_label(request):
    obj_paciente = Paciente.objects.filter(dni='1').first()
    datos = {
        'paciente' : obj_paciente
    }
    return render(request,'Mysite/label.html',datos)

#! TITULOS
def ejemplo_title(request):
    obj_paciente = Paciente.objects.filter(dni='1').first()
    datos = {
        'paciente' : obj_paciente
    }
    return render(request,'Mysite/titulos.html',datos)

#! TABLES
def ejemplo_tables(request):
    patologias = Patologia.objects.all
    datos = {
        'patologias' : patologias
    }
    return render(request,'Mysite/table.html',datos)

#! IF
def ejemplo_tables_if(request):
    patologias = Patologia.objects.all
    variable = False
    datos = {
        'patologias' : patologias,
        'variable' : variable
    }
    return render(request,'Mysite/table_if.html',datos)

#! IF
def ejemplo_varios(request):
    datos = {}
    return render(request,'Mysite/atr.html',datos)

#! FORM
def ejemplo_form(request):
    return render(request,'Mysite/form.html',{})

#! LOGIN
def login(request):
    msg = 'Please sign in'
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(username = usuario, password = clave)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                msg = 'login succesfully'
            else:
                msg = 'Your account is not activated'
        else:
            msg = 'Invalid login, please try again.'
    context = {'message': msg}
    return render(request,'Mysite/login.html', context)


# <QuerySet [
#     <Paciente: Paciente object (1)>,
#     <Paciente: Paciente object (2)>,
#     <Paciente: Paciente object (3)>,
# ]>

# def add_datos(request):
#     paciente = Paciente.objects.last()
#     sintomas = Sintoma.objects.all()
#     patologias = Patologia.objects.all()
#     form = UploadForm(data=request.POST, files=request.FILES)

#     if request == 'POST':
#         if form.is_valid():
#             newdocS = Sintoma(nombre=request.POST['nombre_sintoma'],grado=request.POST['grado_sintoma'])
#             newdocS.save(form)
# #             newdocP = Patologia(nombre=request.POST['nombre_patologia'],grado=request.POST['grado_patologia']) 
# #             newdocP.save(form)
#             return HttResponseRedirect('/detalle')
#         else:
#             form = UploadForm()
#     args={}
#     args=['form'] = UploadForm()
#     return render(request,"ingreso.html",args,{'form':form,'con':con})