from django import forms
from .models import Script


class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script

    class Media:
        css = {
            'all': (
                'css/codemirror.css',
                'css/highlight.min.css'
            )
        }
        js = (
            'js/codemirror.js',
            'js/python.js',
            'js/highlight.min.js',
        )