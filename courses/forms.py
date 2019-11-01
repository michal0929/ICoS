from django import forms
from .models import *
from quiz.models import Test
import re


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'for_everybody']

    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')

        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(course_name):
            raise forms.ValidationError("Please make sure course name contains (a-z, A-Z, 0-9, space) characters")

        return course_name

class AddQuizForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['quiz_title']

    def clean_quiz_name(self):
        quiz_title = self.cleaned_data.get('quiz_title')

        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(quiz_title):
            raise forms.ValidationError("Please make sure course name contains (a-z, A-Z, 0-9, space) characters")

        return quiz_title

class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_name']

    def clean_chapter_name(self):
        chapter_name = self.cleaned_data.get('chapter_name')
        regexp = re.compile(r'[0-9a-zA-Z ]')

        if not regexp.match(chapter_name):
            raise forms.ValidationError("Please make sure chapter name contains (a-z, A-Z, 0-9, space) characters")

        return chapter_name


class AddLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']


class AddTxtForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ["lesson"]


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'for_everybody']

class EditQuizForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['quiz_title']

class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_name']


class EditYTLinkForm(forms.ModelForm):
    class Meta:
        model = YTLink
        fields = ['link']


class EditTxtForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ["lesson"]


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
