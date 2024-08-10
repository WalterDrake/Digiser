from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

STATUS_CHOICES = [
    ('completed', 'Hoàn thành'),
    ('not_entered', 'Chưa nhập'),
    ('error', 'Báo lỗi')
]

DOCUMENT_TYPE_CHOICES = [
    ('cmc', 'CMC'),
    ('hn', 'HN'),
    ('kt', 'KT'),
    ('ks', 'KS'),
    ('kh', 'KH')
]

REGION_CHOICES = [
    ('hcm', 'Tp Hồ Chí Minh'),
    ('tien_giang', 'Tiền Giang'),
    ('ben_tre', 'Bến Tre')
]

class FilterForm(forms.Form):
    status = forms.MultipleChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    document_type = forms.MultipleChoiceField(
        choices=DOCUMENT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    region = forms.MultipleChoiceField(
        choices=REGION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    received_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    deadline = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))