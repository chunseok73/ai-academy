"""화면 입력 검증. 일반 회원의 분류와 강좌 선택 범위를 제한합니다."""
from pathlib import Path
from django import forms
from academy.models import Offering, Enrollment
from .models import Post, Answer

class PostForm(forms.ModelForm):
    attachment = forms.FileField(label='첨부파일 (선택, 최대 10MB)', required=False)
    class Meta:
        model = Post
        fields = ['category', 'offering', 'title', 'content']
        widgets = {'content': forms.Textarea(attrs={'rows': 9})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['category'].choices = [('question', '질문')]
            ids = Enrollment.objects.filter(user=user, status='enrolled').values('offering_id')
            self.fields['offering'].queryset = Offering.objects.filter(pk__in=ids)
        self.fields['offering'].empty_label = '공통 게시판'

    def clean_attachment(self):
        file = self.cleaned_data.get('attachment')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('파일은 10MB 이하로 첨부하세요.')
            if Path(file.name).suffix.lower() not in {'.pdf','.txt','.png','.jpg','.jpeg','.zip','.pptx','.docx','.xlsx','.csv'}:
                raise forms.ValidationError('PDF, 문서, 이미지, ZIP 파일을 첨부하세요.')
        return file

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 4})}
