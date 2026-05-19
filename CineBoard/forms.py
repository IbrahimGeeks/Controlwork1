from django import forms
from .models import Comment, VipBooking 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Оставьте ваш отзыв о фильме', 'class': 'form-control'}),
        }

class VipBookingForm(forms.ModelForm):
    class Meta:
        model = VipBooking
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.NumberInput(attrs={'placeholder': 'Введите номер места (1-20)', 'class': 'form-control'}),
        }