from django import forms
from .models import CustomUser,UserProfile
from orders.models import  Address



class PhoneForm(forms.ModelForm):

    class Meta:
        
        fields = ['phone']
        labels = {
            'phone': 'phone',
                     
        }



class OTPForm(forms.ModelForm):

    class Meta:
      
        fields = ['otp']
        labels = {
            'otp': 'otp',
                     
        }  


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','phone','email')

    def __init__(self,*args,**kwargs):
        super(CustomUserForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','state','country','city')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)   

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'  




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','state','country','city',]
    
    def __init__(self, *args, **kwargs):
      super(AddressForm,self).__init__(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
