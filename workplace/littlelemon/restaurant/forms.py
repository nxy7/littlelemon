from django.forms import ModelForm, DateInput, DateField, Select, ChoiceField, SelectMultiple, MultipleChoiceField, TypedMultipleChoiceField
from .models import Booking
import datetime


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    reservation_date = DateField(
        input_formats=['%d/%m/%Y'],
        initial=datetime.date.today(),
        widget=DateInput(attrs={
            'type': 'date'
            # 'class': 'form-control datetimepicker-input',
            # 'data-target': '#datetimepicker1'
        })
    )
    reservation_slot = TypedMultipleChoiceField(
        widget=Select,
        # choices=['10 AM', '11 AM', '12 AM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM'],
        choices=[
        (10, '10 AM'),
         (11, '11 AM'),
         (12, '12 AM'),
         (13, '1 PM'),
         (14,'2 PM'),
         (15,'3 PM'),
         (16,'4 PM'),
         (17,'5 PM'),
         (18,'6 PM'),
         (19,'7 PM'),
         (20,'8 PM'),
         (21,'9 PM'),
         (22,'10 PM')
         ],
    )
    class Meta:
        model = Booking
        fields = "__all__"
        # widgets = {
        #     'reservation_date': DateInput
        # }
