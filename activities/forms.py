from django import forms
from .models import Project, Activity, ActivityLog

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','description','start_date','end_date']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['project','name','planned_start','planned_end','progress_percent','status']

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['activity','date','progress_percent','notes']
