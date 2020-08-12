from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
import json
from django.http import JsonResponse

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm,
    FormModelForm,
    ObjectModelForm,
    OpenModelForm
)
from .models import Book, Form, Object, Result

class Index(generic.ListView):
    template_name = 'index.html'
    model = Form
    context_object_name = 'forms'
    queryset = Form.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.all()
        return context
    '''model = Form
    context_object_name = 'forms'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(book_type=int(self.request.GET['type']))
        return qs'''



class BookFilterView(BSModalFormView):
    template_name = 'examples/filter_book.html'
    form_class = BookFilterForm

    def form_valid(self, form):
        if 'clear' in self.request.POST:
            self.filter = ''
        else:
            self.filter = '?type=' + form.cleaned_data['type']

        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('index') + self.filter


class BookCreateView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = Book
    template_name = 'examples/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


class BookReadView(BSModalReadView):
    model = Book
    template_name = 'examples/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = Book
    template_name = 'examples/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'examples/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('index')


def books(request):
    data = dict()
    if request.method == 'GET':
        books = Book.objects.all()
        data['table'] = render_to_string(
            '_books_table.html',
            {'books': books},
            request=request
        )
        return JsonResponse(data)

######## Forms ########

class Forms(generic.ListView):
    template_name = 'forms.html'
    model = Form
    context_object_name = 'forms'
    queryset = Form.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Forms, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.all()
        return context
    '''model = Form
    context_object_name = 'forms'
    template_name = 'forms.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if 'type' in self.request.GET:
            qs = qs.filter(form_type=int(self.request.GET['type']))
        return qs'''


class FormCreateView(BSModalCreateView):
    template_name = 'examples/create_form.html'
    form_class = FormModelForm
    success_message = 'Success: Instance was created.'
    success_url = reverse_lazy('forms_page')

    def form_valid(self, form):
        if not self.request.is_ajax():
            form = form.save(commit=False)
            form.created_by = self.request.user  # use your own profile here
            form.save()
        return HttpResponseRedirect(self.success_url)

class FormUpdateView(BSModalUpdateView):
    model = Form
    template_name = 'examples/update_form.html'
    form_class = FormModelForm
    success_message = 'Success: Instance was updated.'
    success_url = reverse_lazy('forms_page')


class FormReadView(BSModalReadView):
    model = Form
    template_name = 'examples/read_form.html'


class FormDeleteView(BSModalDeleteView):
    model = Form
    template_name = 'examples/delete_form.html'
    success_message = 'Success: Instance was deleted.'
    success_url = reverse_lazy('forms_page')

def forms(request):
    data = dict()
    if request.method == 'GET':
        forms = Form.objects.all()

        data['table'] = render_to_string(
            '_forms_table.html',
            {'forms': forms},
            request=request
        )
        objects(request)
        return JsonResponse(data)

class FormOpenView(BSModalReadView):
    model = Form
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['objects'] = Object.objects.all()
        return context
    template_name = 'examples/open_form.html'

def send_form(request):
    print("AA")
    if request.method == "POST":
        print("POST")
        return HttpResponseRedirect('../')
    elif request.method == "GET":
        print("GET")
        return HttpResponseRedirect('../')
    else:
        return HttpResponseRedirect('../')

######## Object ########

class ObjectCreateView(BSModalCreateView):
    template_name = 'examples/create_object.html'
    form_class = ObjectModelForm
    success_message = 'Success: Object was created.'
    success_url = reverse_lazy('forms_page')

    def form_valid(self, form, *args,**kwargs):
        print(str(self.kwargs['pk']))
        if not self.request.is_ajax():
            form = form.save(commit=False)
            form.form = Form.objects.get(pk=self.kwargs['pk'])
            form.created_by = self.request.user  # use your own profile here
            form.save()
        return HttpResponseRedirect(self.success_url)

class ObjectUpdateView(BSModalUpdateView):
    model = Object
    template_name = 'examples/update_object.html'
    form_class = ObjectModelForm
    success_message = 'Success: Object was updated.'
    success_url = reverse_lazy('forms_page')


class ObjectReadView(BSModalReadView):
    model = Object
    template_name = 'examples/read_object.html'


class ObjectDeleteView(BSModalDeleteView):
    model = Object
    template_name = 'examples/delete_object.html'
    success_message = 'Success: Object was deleted.'
    success_url = reverse_lazy('forms_page')


def objects(request):
    data = dict()
    if request.method == 'GET':
        objects = Object.objects.all()
        data['table'] = render_to_string(
            '_forms_table.html',
            {'objects': objects},
            request=request
        )
        print( JsonResponse(data))
        return JsonResponse(data)

