from django import forms
from .models import Material, MaterialMovement, Tool, ToolAssignment

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name','description','unit','stock','min_stock']

class MaterialMovementForm(forms.ModelForm):
    class Meta:
        model = MaterialMovement
        fields = ['material','kind','quantity','notes']

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['code','name','status','notes']

class ToolAssignmentForm(forms.ModelForm):
    class Meta:
        model = ToolAssignment
        fields = ['tool','user','notes']
