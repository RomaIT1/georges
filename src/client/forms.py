from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
   class Meta:
      model = Order
      fields = ['name', 'phone', 'amount', 'invoice_id', 'districts', 'self_pickup', 'user_agent', 'address', 'details', 'comment_client']
      widgets = {
         'name': forms.TextInput(attrs={
            'placeholder': "Ім'я",
         }),
         'phone': forms.TextInput(attrs={
            'placeholder': "Телефон",
         }),
         'amount': forms.TextInput(attrs={
            'class': "form__field form__field--hidden",
            'id': 'cart-amount-field',
            'type': 'hidden',
         }),
         'user_agent': forms.TextInput(attrs={
            'class': "form__field form__field--hidden",
            'id': 'cart-user-agent-field',
            'type': 'hidden',
         }),
         'address': forms.TextInput(attrs={
            'placeholder': "Вулиця, будинок",
         }),
         'details': forms.Textarea(attrs={
            'class': "form__field form__field--hidden",
            'id': "cart-details-field",
         }),
         'comment_client': forms.Textarea(attrs={
            'placeholder': "Коментар",
         }),
      }