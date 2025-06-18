from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserUpdateForm(ModelForm):
    class Meta:
        model=User
        fields=('last_name','first_name')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class']='form-control'

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields=('username','email')
