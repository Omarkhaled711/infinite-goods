"""
This view Handles forms for placing order
"""


from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    """
    Class for handling order form
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address_1',
                  'address_2', 'country', 'state', 'city', 'order_note']
