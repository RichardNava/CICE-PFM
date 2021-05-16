from django.urls import path
from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('create_paciente/<str:dni>/<int:edad>/<str:peso>/<int:altura>/', views.create_paciente, name='create_paciente'),
    path('create_sintoma/<str:nombre>/<int:grado>/<int:valor_adicional>', views.create_sintoma, name='create_sintoma'),
    path('create_patologia/<str:nombre>/<int:grado>/<int:valor_adicional>', views.create_patologia, name='create_patologia'),
    path('consulta_informe/<str:dni>', views.consulta_informe, name='consulta_informe'),
    path('load_sint_csv/', views.load_sint_csv, name='load_sint_csv'),
    path('load_pat_csv/', views.load_pat_csv, name='load_pat_csv'),
    path('prueba/<str:dni>', views.prueba, name='prueba'),
    #! LABELS
    path('ejemplo_label', views.ejemplo_label, name='ejemplo_label'),
    #! TITLES
    path('ejemplo_title', views.ejemplo_title, name='ejemplo_title'),
    #! TABLES
    path('ejemplo_tables', views.ejemplo_tables, name='ejemplo_tables'),
    #! IF
    path('ejemplo_tables_if', views.ejemplo_tables_if, name='ejemplo_tables_if'),
    #! HTML-VARIOS
    path('ejemplo_varios', views.ejemplo_varios, name='ejemplo_varios'),
    #! FORM
    path('ejemplo_form', views.ejemplo_form, name='ejemplo_form'),
    #! LOGIN
    path('login', views.login, name='login'),

    path('datos_paciente', views.datos_paciente, name='datos_paciente'),
    path('patologias', views.patologias_form, name='patologias'),
    path('sintomas', views.sintomas_form, name='sintomas'),
]