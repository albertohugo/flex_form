from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
import json
from django.http import JsonResponse
from django.core import serializers

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
from .models import Book, Form, Object, Result, IdResult

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
    template_name = 'flexform/filter_book.html'
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
    template_name = 'flexform/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('index')


class BookUpdateView(BSModalUpdateView):
    model = Book
    template_name = 'flexform/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


class BookReadView(BSModalReadView):
    model = Book
    template_name = 'flexform/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = Book
    template_name = 'flexform/delete_book.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('index')


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'flexform/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('index')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'flexform/login.html'
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
    template_name = 'flexform/create_form.html'
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
    template_name = 'flexform/update_form.html'
    form_class = FormModelForm
    success_message = 'Success: Instance was updated.'
    success_url = reverse_lazy('forms_page')


class FormReadView(BSModalReadView):
    model = Form
    template_name = 'flexform/read_form.html'


class FormDeleteView(BSModalDeleteView):
    model = Form
    template_name = 'flexform/delete_form.html'
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


def open_form(request):
    pk = request.GET.get('pk', '') or ''
    form = Form.objects.filter(id=pk)
    objects = Object.objects.filter(form__in=form)
    #print(serializers.serialize("json", form))
    #print(serializers.serialize("json", objects))

    if request.method == "POST":
        IdResult.objects.create(form=form.first())
        for object in objects:
            value = request.POST[pk + '_' + str(object.id)]
            id_result = IdResult.objects.filter().last().id

            Result.objects.create(form=form.first(), object=object, id_result=id_result ,value=value, created_by=request.user)
        return HttpResponseRedirect('../')

    return render(request, 'instance.html',
                  {'form_title':form.get().title,
                   'form_id': form.get().id,
                   'objects':objects}
                  )

def open_list(request):
    pk = request.GET.get('pk', '') or ''
    id_result = request.GET.get('id_result', '') or ''
    print(id_result)
    if id_result != '':
        Result.objects.filter(id_result__in=id_result).delete()
        IdResult.objects.filter(id__in=id_result).delete()
    form = Form.objects.filter(id=pk)
    results = Result.objects.filter(form__in=form)
    objects = Object.objects.filter(form__in=form)
    id_results = IdResult.objects.filter(form__in=form)
    #print(serializers.serialize("json", results))
    #print(serializers.serialize("json", objects))


    return render(request, 'instance_list.html',
                  {'form_title':form.get().title,
                   'results': results,
                   'objects': objects,
                   'form_id': form.get().id,
                   'id_results': id_results
                   }
                  )

class FormOpenView(generic.ListView):
    template_name = 'instance.html'
    model = Form
    context_object_name = 'forms'
    queryset = Form.objects.all()

    def get_context_data(self, **kwargs):
        context = super(FormOpenView, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.all()
        return context

######## Object ########

class ObjectCreateView(BSModalCreateView):
    template_name = 'flexform/create_object.html'
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
    template_name = 'flexform/update_object.html'
    form_class = ObjectModelForm
    success_message = 'Success: Object was updated.'
    success_url = reverse_lazy('forms_page')


class ObjectReadView(BSModalReadView):
    model = Object
    template_name = 'flexform/read_object.html'


class ObjectDeleteView(BSModalDeleteView):
    model = Object
    template_name = 'flexform/delete_object.html'
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

