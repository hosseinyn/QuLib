from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="نام شما " , widget=forms.TextInput(attrs={"placeholder" : "نام خود را وارد کنید..." , "class" : "mt-1 w-full rounded-lg border border-gray-200 focus:outline-none p-3"}) , min_length=2 , max_length=19 , required=True , error_messages={
            'required': 'لطفاً نام خود را وارد کنید.',
            'min_length': 'نام باید حداقل ۲ کاراکتر باشد.',
            'max_length': 'نام نمی‌تواند بیشتر از ۱۹ کاراکتر باشد.',
        },)

    subject = forms.CharField(label="موضوع پیام " , widget=forms.TextInput(attrs={"placeholder" : "موضوع پیام خود را وارد کنید..." , "class" : "mt-1 w-full rounded-lg border border-gray-200 focus:outline-none p-3"}) , min_length=2 , max_length=19 , required=True , error_messages={
            'required': 'موضوع پیام الزامی است.',
            'min_length': 'موضوع باید حداقل ۲ کاراکتر باشد.',
            'max_length': 'موضوع نمی‌تواند بیشتر از ۱۹ کاراکتر باشد.',
        },)

    email = forms.EmailField(label="ایمیل شما " , widget=forms.EmailInput(attrs={"placeholder" : "آدرس ایمیل خود را وارد کنید..." , "class" : "mt-1 w-full rounded-lg border border-gray-200 focus:outline-none p-3"}) , required=True , error_messages={
            'required': 'وارد کردن ایمیل الزامی است.',
            'invalid': 'فرمت ایمیل وارد شده صحیح نیست.',
        },)

    TYPE_OF_MESSAGE_CHOICES = [
        ('عمومی', 'عمومی'),
        ('امنیتی', 'امنیتی'),
        ('مشکل یا ایراد', 'مشکل یا ایراد'),
        ('همکاری' , 'همکاری')
    ]

    kind_of_message = forms.ChoiceField(choices=TYPE_OF_MESSAGE_CHOICES , label="نوع پیام را انتخاب کنید" , required=True , widget=forms.Select(attrs={"class" : "mt-1 w-full rounded-lg border border-gray-200 focus:outline-none p-3"}) , error_messages={
            'required': 'لطفاً نوع پیام را انتخاب کنید.'
        },)

    message = forms.CharField(label="پیام شما (حداقل 14 کاراکتر و حداکثر 1000 کاراکتر)" , widget=forms.Textarea(attrs={"placeholder" : "متن پیام خود را وارد کنید..." , "class" : "mt-1 w-full resize-none rounded-lg border border-gray-200 focus:outline-none p-3" , "rows" : "4"}) , required=True , min_length=14 , max_length=1000 , error_messages={
            'required': 'لطفاً پیام خود را وارد کنید.',
            'min_length': 'پیام باید حداقل 14 کاراکتر باشد.',
            'max_length': 'پیام نمیتواند بیشتر از 1000 کاراکتر باشد.',
        },)