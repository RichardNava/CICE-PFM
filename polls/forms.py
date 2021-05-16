from .models import Sintoma, Patologia

CHOICES=[(0),(0)]

def lista():
    i=0
    for id1 in Sintoma.objects.all():
        if i == 0:
            CHOICES = [(id1.id,id1.nombre)]
        else:
            CHOICES = [(id1.id,id1.nombre)] + CHOICES
            print(CHOICES)
        i += 1
    return CHOICES

class UploadForm1(forms.Form):
    nombreSintoma = forms.CharField(max_length=800,required=True)
    # nombrePatologia = forms.CharField(max_length=800,required=True)
    
    class Meta:
        model = Sintoma
        fields = '__all__'

class UploadForm(forms.Form):
    nombrePatologia = forms.CharField(max_length=800,required=True)

    class Meta:
        model=Patologia
        fields = '__all__'