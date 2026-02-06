from django import forms
from .models import ContactInquiry, Feedback


class ContactInquiryForm(forms.ModelForm):
    """
    Contact inquiry form with basic spam protection.
    """
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }


class FeedbackForm(forms.ModelForm):
    """
    Feedback form with optional rating.
    """
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (Optional)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email (Optional)'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Feedback', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
