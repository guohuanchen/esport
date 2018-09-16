from django import forms
from .models import *
from datetime import date, datetime
from calendar import monthrange

class AuthenticateForm(forms.Form):
    userid = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_userid', 'name':'input_userid', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'id':'input_password', 'name':'input_password','class': "form-control"}))


class RegistrationForm(forms.Form):
    userid = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_userid', 'name':'input_userid', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'id':'input_email', 'name':'input_email', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'id':'input_password1', 'name':'input_password1','class': "form-control"}))
    pname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_pname', 'name':'input_pname', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    #password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'id':'input_password2', 'name':'input_password2','class': "form-control"}))
    rank = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_rank', 'name':'input_rank', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    skypeid = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_skypeid', 'name':'input_skypeid', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))
    twitchid = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'input_twitchid', 'name':'input_twitchid', 'class': "form-control", 'style':'border:1px solid #D3D3D3'}))

    # def clean(self):
    #     if self.clean_data.has_key('password1') and self.clean_data.has_key('password2'):
    #         if self.clean_data['password1'] != self.clean_data['password2']:
    #             raise ValidationError("The passwords you have entered do not match.")
    #     return self.clean_data


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['server', 'champion', 'rating', 'pricerate', 'role', 'avatar', 'overview']


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()


class errorForm(forms.Form):
    email = forms.EmailField()


class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value and (len(value) < 13 or len(value) > 16):
            raise forms.ValidationError("Please enter in a valid "+\
                "credit card number.")
        return super(CreditCardField, self).clean(value)


class expDate(forms.MultiWidget):
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap;">%s</span>' % html


"""code snippet from STRIPE documentation """
"""user can select the months and years from the given selection in the selection boxes"""
class expDateInput(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in xrange(1, 13)]
    EXP_YEAR = [(x, x) for x in xrange(date.today().year,
                                       date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}),
            forms.ChoiceField(choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}),
        )
        super(expDateInput, self).__init__(fields, *args, **kwargs)
        self.widget = expDate(widgets =
            [fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(expDateInput, self).clean(value)
        if date.today() > exp:
            raise forms.ValidationError(
            "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            # find last day of the month
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None


class SalePaymentForm(forms.Form):
    CCnumber = CreditCardField(required=True, label="Card Number")
    expiration = expDateInput(required=True, label="Expiration")
    cvc = forms.IntegerField(required=True, label="CCV Number",
        max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))

    def clean(self):
        """
        The clean method will effectively charge the card and create a new
        Sale instance. If it fails, it simply raises the error given from
        Stripe's library as a standard ValidationError for proper feedback.
        """
        cleaned = super(SalePaymentForm, self).clean()

        if not self.errors:
            number = self.cleaned_data["number"]
            exp_month = self.cleaned_data["expiration"].month
            exp_year = self.cleaned_data["expiration"].year
            cvc = self.cleaned_data["cvc"]
            sale = Sale()

            # charge 10 bucks for testing, change the value
            success, instance = sale.charge(1000, CCnumber, exp_month, exp_year, cvc)

            if not success:
                raise forms.ValidationError("Error: %s" % instance.message)
            else:
                instance.save()
                """Payment succesful"""
                pass
        return cleaned
