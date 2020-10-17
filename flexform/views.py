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
from django.db.models import Case, When
from .serializer import FormSerializer, ObjectSerializer, FormMemberSerializer, ResultSerializer, FlexFormGetSerializer, FlexFormSetSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from basicauth import decode

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
    OpenModelForm,
    FormMemberModelForm,
    UpdateFormMemberModelForm
)
from .models import Book, Form, Object, Result, IdResult, FormMember

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ObjectViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class FormMemberViewSet(viewsets.ModelViewSet):
    queryset = FormMember.objects.all()
    serializer_class = FormMemberSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def perform_create(self, serializer):
        IdResult.objects.create(form=Form.objects.filter(id=serializer.validated_data['form'].id).first())
        id_result = IdResult.objects.filter().last()
        serializer.save(id_result=id_result)

class FlexFormGetViewGet(viewsets.ModelViewSet):
    queryset = Form.objects.none()
    model = Form
    serializer_class = FlexFormGetSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Form.objects.all()
        elif self.request.user.is_authenticated:
            form_members = FormMember.objects.filter(user=self.request.user).values_list('form')
            return Form.objects.filter(created_by=self.request.user) | \
                   Form.objects.filter(private=False) | \
                   Form.objects.filter(id__in=form_members)
        else:
            return Form.objects.filter(private=False)

class FlexFormSetViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all()
    model = Object
    serializer_class = FlexFormSetSerializer


@csrf_exempt
def send_object(request):
    encoded_str = request.headers['Authorization']
    username, password = decode(encoded_str)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse(" Unauthorized")
    if request.method == 'POST':
        form_id = request.GET.get("form_id", '') or ''
        if form_id == '':
            return HttpResponse("Missing form_id parameter")
        else:

            if user.is_superuser:
                form_selected = Form.objects.filter(id__in=form_id)
            elif user.is_authenticated:
                form_members = FormMember.objects.filter(user=user).values_list('form')
                form_selected = Form.objects.filter(id__in=form_id, created_by=user) | \
                       Form.objects.filter(id__in=form_id, private=False) | \
                       Form.objects.filter(id__in=form_id).filter(id__in=form_members)
            else:
                form_selected = Form.objects.filter(private=False)

            #form_selected = Form.objects.filter(id__in=form_id) # without auth filter

            if form_selected:
                objects = Object.objects.filter(form__in=form_selected)
                parameters=[]
                values=[]
                if objects:
                    count=0
                    for object in objects:
                        parameters.insert(count, object.label.lower())
                        if request.GET.get(parameters[count]) == '':
                            return HttpResponse('Parameter ' + parameters[count] + ' is empty')
                        elif request.GET.get(parameters[count]) == None:
                            return HttpResponse("Missing " + parameters[count] + ' as parameter')
                        else:
                            if object.type == 2:
                                string_int = request.GET.get(parameters[count])
                                try:
                                    string_int = float(request.GET.get(parameters[count]))
                                except ValueError:
                                    print('Please enter an integer')
                                if is_integer_num(string_int):
                                    values.insert(count, request.GET.get(parameters[count]))
                                    count += 1
                                else:
                                    return HttpResponse('Parameter ' + parameters[count] + ' is not a number')
                            else:
                                values.insert(count, request.GET.get(parameters[count]))
                                count += 1
                    countparam = 0
                    IdResult.objects.create(form=form_selected.last()).form
                    id_result = IdResult.objects.filter().last()

                    for object in objects:
                        Result.objects.create(form=form_selected.last(), object=object, id_result=id_result, value=values[countparam],created_by=request.user)
                        countparam += 1
                    return HttpResponse("Objects was sent")

                else:
                    return HttpResponse("No objects in this instance")
            else:
                return HttpResponse("Parameter form_id not found or you don't have permission to access this instance.\nPlease access ../api/flexform to check the instance information")

@csrf_exempt
def update_object(request):
    encoded_str = request.headers['Authorization']
    username, password = decode(encoded_str)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse(" Unauthorized")
    if request.method == 'POST':
        form_id = request.GET.get("form_id", '') or ''
        id_result = request.GET.get('id_response', '') or ''
        if form_id == '':
            return HttpResponse("Missing form_id parameter")
        elif id_result == '':
            return HttpResponse("Missing id_response parameter")
        else:
            if user.is_superuser:
                form_selected = Form.objects.filter(id__in=form_id)
            elif user.is_authenticated:
                form_members = FormMember.objects.filter(user=user).values_list('form')
                form_selected = Form.objects.filter(id__in=form_id, created_by=user) | \
                       Form.objects.filter(id__in=form_id, private=False) | \
                       Form.objects.filter(id__in=form_id).filter(id__in=form_members)
            else:
                form_selected = Form.objects.filter(private=False)

            if form_selected:
                print(form_selected)
                objects = Object.objects.filter(form__in=form_selected)
                parameters=[]
                values=[]
                form_filled = Result.objects.filter(form=form_selected.first(), id_result=IdResult.objects.filter(id=id_result).last())
                if form_filled.count() == 0:
                    return HttpResponse("id_response does not exist")
                if objects:
                    count=0
                    for object in objects:
                        parameters.insert(count, object.label.lower())
                        if request.GET.get(parameters[count]) == '':
                            return HttpResponse('Parameter ' + parameters[count] + ' is empty')
                        elif request.GET.get(parameters[count]) == None:
                            print("Nothing to do with "+parameters[count]+" parameter")
                        else:
                            if object.type == 2:
                                string_int = request.GET.get(parameters[count])
                                try:
                                    string_int = float(request.GET.get(parameters[count]))
                                except ValueError:
                                    print('Please enter an integer')

                                if is_integer_num(string_int):
                                    Result.objects.filter(form=form_selected.first(), object=object,
                                                          id_result=IdResult.objects.filter(
                                                              id=id_result).last()).update(value=request.GET.get(parameters[count]))
                                    count += 1
                                else:
                                    return HttpResponse('Parameter ' + parameters[count] + ' is not a number')
                            else:
                                Result.objects.filter(form=form_selected.first(), object=object,
                                                      id_result=IdResult.objects.filter(id=id_result).last()).update(
                                    value=request.GET.get(parameters[count]))
                                count += 1
                    if count > 0:
                        return HttpResponse("Objects was updated")
                    else:
                        return HttpResponse("Nothing to update")
                else:
                    return HttpResponse("No objects in this instance")
            else:
                return HttpResponse("Parameter form_id not found or you don't have permission to access this instance.\nPlease access ../api/flexform to check the instance information")

@csrf_exempt
def delete_object(request):
    encoded_str = request.headers['Authorization']
    username, password = decode(encoded_str)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return HttpResponse(" Unauthorized")
    if request.method == 'POST':
        form_id = request.GET.get("form_id", '') or ''
        id_result = request.GET.get('id_response', '') or ''
        if form_id == '':
            return HttpResponse("Missing form_id parameter")
        elif id_result == '':
            return HttpResponse("Missing id_response parameter")
        else:
            if user.is_superuser:
                form_selected = Form.objects.filter(id__in=form_id)
            elif user.is_authenticated:
                form_members = FormMember.objects.filter(user=user).values_list('form')
                form_selected = Form.objects.filter(id__in=form_id, created_by=user) | \
                       Form.objects.filter(id__in=form_id, private=False) | \
                       Form.objects.filter(id__in=form_id).filter(id__in=form_members)
            else:
                form_selected = Form.objects.filter(private=False)

            if form_selected:
                print(form_selected)
                form_filled = Result.objects.filter(form=form_selected.first(), id_result=IdResult.objects.filter(id=id_result).last())
                if form_filled.count() == 0:
                    return HttpResponse("id_response does not exist")
                else:
                    Result.objects.filter(form=form_selected.first(), id_result=IdResult.objects.filter(id=id_result).last()).delete()
                    IdResult.objects.filter(id=id_result).delete()
                    return HttpResponse(id_result + " from form_id "+ form_id + " was deleted")
            else:
                return HttpResponse("Parameter form_id not found or you don't have permission to access this instance.\nPlease access ../api/flexform to check the instance information")

def is_integer_num(n):
    if isinstance(n, int) or isinstance(n, float):
        return True
    else:
        return False

class Index(generic.ListView):
    template_name = 'index.html'
    model = Form
    context_object_name = 'forms'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Form.objects.all()
        elif self.request.user.is_authenticated:
            form_members = FormMember.objects.filter(user=self.request.user).values_list('form')
            return Form.objects.filter(created_by=self.request.user) | \
                   Form.objects.filter(private=False) | \
                   Form.objects.filter(id__in=form_members)
        else:
            return Form.objects.filter(private=False)
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if FormMember.objects.filter(user=self.request.user):
                context['objects'] = FormMember.objects.filter(user=self.request.user)
        context['objects'] = Object.objects.all()
        return context


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
    #queryset = Form.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Form.objects.all()
        elif self.request.user.is_authenticated:
            form_members = FormMember.objects.filter(user=self.request.user).values_list('form')

            return Form.objects.filter(created_by=self.request.user) \
                   | Form.objects.filter(private=False) \
                   | Form.objects.filter(id__in=form_members)

        else:
            return Form.objects.filter(private=False)


    def get_context_data(self, **kwargs):
        context = super(Forms, self).get_context_data(**kwargs)
        context['objects'] = Object.objects.all()
        context['members'] = FormMember.objects.all()
        return context

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
    id_result = request.GET.get('id_result', '') or ''
    form = Form.objects.filter(id=pk)
    objects = Object.objects.filter(form__in=form)
    #print(serializers.serialize("json", form))
    #print(serializers.serialize("json", objects))
    if id_result != '':
        form_filled = Result.objects.filter(form=form.first(), id_result=IdResult.objects.filter(id=id_result).last())
    else:
        form_filled = Result.objects.filter(form=form.first(), id_result=0)
    if request.method == "POST":
        if id_result != '':
            print(id_result)
            for object in objects:
                value = request.POST[pk + '_' + str(object.id)]
                Result.objects.filter(form=form.first(),object=object, id_result=IdResult.objects.filter(id=id_result).last()).update(value=value)
            return HttpResponseRedirect('../')
        else:
            IdResult.objects.create(form=form.first())
            for object in objects:
                value = request.POST[pk + '_' + str(object.id)]
                id_result = IdResult.objects.filter().last()

                Result.objects.create(form=form.first(), object=object, id_result=id_result ,value=value, created_by=request.user)
            return HttpResponseRedirect('../')

    return render(request, 'instance.html',
                  {'form_title': form.get().title,
                   'form_id': form.get().id,
                   'form_filled': form_filled,
                   'objects': objects}
                  )

def open_list(request):
    pk = request.GET.get('pk', '') or ''
    id_result = request.GET.get('id_result', '') or ''
    print(id_result)
    if id_result != '':
        Result.objects.filter(id_result__in=IdResult.objects.filter(id=id_result)).delete()
        IdResult.objects.filter(id=id_result).delete()
    form = Form.objects.filter(id=pk)
    results = Result.objects.filter(form__in=form)
    objects = Object.objects.filter(form__in=form)
    id_results = IdResult.objects.filter(form__in=form)

    print(serializers.serialize("json", results))
    #print(serializers.serialize("json", objects))


    return render(request, 'instance_list.html',
                  {'form_title':form.get().title,
                   'form_user': form.get().created_by,
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

###############################################

class MemberCreateView(BSModalCreateView):
    template_name = 'flexform/create_member.html'
    form_class = FormMemberModelForm
    success_message = 'Success: Member was created.'
    success_url = reverse_lazy('forms_page')

    def form_valid(self, form, *args,**kwargs):
        print(str(self.kwargs['pk']))
        if not self.request.is_ajax():
            form = form.save(commit=False)
            form.form = Form.objects.get(pk=self.kwargs['pk'])
            #form.created_by = self.request.user  # use your own profile here
            form.save()
        return HttpResponseRedirect(self.success_url)

class MemberReadView(BSModalReadView):
    model = FormMember
    template_name = 'flexform/read_member.html'

class MemberUpdateView(BSModalUpdateView):
    model = FormMember
    template_name = 'flexform/update_member.html'
    form_class = UpdateFormMemberModelForm
    success_message = 'Success: Member was updated.'
    success_url = reverse_lazy('forms_page')

class MemberDeleteView(BSModalDeleteView):
    model = FormMember
    template_name = 'flexform/delete_member.html'
    success_message = 'Success: Member was deleted.'
    success_url = reverse_lazy('forms_page')

class Developer(generic.ListView):
    template_name = 'developer.html'
    model = Form
    context_object_name = 'forms'