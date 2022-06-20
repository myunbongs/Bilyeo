from pyexpat.errors import messages

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from bilyeo.models import Stuff, Rental, Category
from bilyeo.forms import AvailabilityForm, AcceptForm, StuffForm
from bilyeo.rental_functions.cal_rental_fee import find_total_rental_fee
from bilyeo.rental_functions.availability import check_availability
from django.contrib.auth.models import User

def index(request):
    stuff_list = Stuff.objects.all()
    category_list = Category.objects.all()

    context = {
        'stuff_list': stuff_list,
        'category_list': category_list,
    }
    return render(request, 'bilyeo/index.html', context)

@method_decorator(login_required, name="dispatch")
class StuffCreateView(View):
    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all()
        form = StuffForm()
        context = {
            'form': form,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/stuff_create.html', context)

    def post(self, request, *args, **kwargs):
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            stuff = Stuff.objects.create(
                author=self.request.user,
                name=data['name'],
                image=data['image'],
                desc=data['desc'],
                status=data['status'],
                category=data['category'],
                fee = data['fee'],
            )
            stuff.save()
            return redirect('bilyeo:stuff_detail', pk=stuff.pk)
        else:
            return HttpResponse(
                "<script>alert('해당 물품을 등록할 수 없습니다. 유효한 입력으로 시도해주세요. :)');location.href='/stuff_list/';</script>")
        return HttpResponse(
            "<script>alert('유효하지 않은 전송입니다. :(');location.href='/stuff_list/';</script>")

class StuffList(ListView):
    model = Stuff

    def get_context_data(self, **kwargs):
        context = super(StuffList, self).get_context_data()
        context['category_list'] = Category.objects.all()
        return context

@method_decorator(login_required, name="dispatch")
class StuffDetailView(View):
    def get(self, request, *args, **kwargs):
        stuff = get_object_or_404(Stuff, pk=self.kwargs['pk'])
        form = AvailabilityForm()
        category_list = Category.objects.all()

        if stuff.author == self.request.user:
            context = {
                'stuff': stuff,
                'form': form,
                'category_list': category_list,
            }

        else:
            context = {
                'stuff': stuff,
                'form': form,
                'category_list': category_list,
            }
        return render(request, 'bilyeo/stuff_detail.html', context)

    def post(self, request, *args, **kwargs):
        stuff = get_object_or_404(Stuff, pk=self.kwargs['pk'])
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if check_availability(stuff, data['rental_date'], data['return_date']):
                total_fee = find_total_rental_fee(data['rental_date'], data['return_date'], kwargs.get("pk"))
                rental = Rental.objects.create(
                    user=self.request.user,
                    stuff=stuff,
                    status='r',
                    rental_date=data['rental_date'],
                    return_date=data['return_date'],
                    total_fee = total_fee,
                )
                rental.save()
                return redirect('bilyeo:rental_detail', pk=rental.pk)
            else:
                return HttpResponse(
                    "<script>alert('해당 물품은 이미 예약되었습니다! 다른 물품으로 시도해주세요. :)');location.href='/stuff_list/';</script>")

        return HttpResponse(
            "<script>alert('유효하지 않은 전송입니다. :(');location.href='/stuff_list/';</script>")


@method_decorator(login_required, name="dispatch")
class StuffUpdateView(View):
    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all()
        form = StuffForm()
        context = {
            'form': form,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/stuff_update.html', context)

    def post(self, request, *args, **kwargs):
        stuff = get_object_or_404(Stuff, pk=self.kwargs['pk'])
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid() and stuff.author == self.request.user:
            data = form.cleaned_data

            category = data['category']
            if category == None:
                stuff.category = None
            else:
                stuff.category = Category.objects.get(name=category)

            stuff.name = data['name']
            stuff.image = data['image']
            stuff.desc = data['desc']
            stuff.status = data['status']
            stuff.fee = data['fee']

            stuff.save()
            return redirect('bilyeo:stuff_detail', pk=stuff.pk)
        else:
            return HttpResponse(
                "<script>alert('해당 물품을 변경할 수 없습니다. 유효한 입력으로 시도해주세요. :)');location.href='/stuff_list/';</script>")
        return HttpResponse(
            "<script>alert('유효하지 않은 전송입니다. :(');location.href='/stuff_list/';</script>")

@login_required
def StuffDeleteView(request, pk):
    stuff = get_object_or_404(Stuff, pk=pk)

    if stuff.author != request.user:
        return HttpResponse(
                "<script>alert('작성자만 삭제 가능합니다. :(');location.href='/stuff_list/';</script>")
    else:
        stuff.delete()
        return redirect('bilyeo:stuff_list')

    return HttpResponse(
            "<script>alert('해당 물품을 삭제할 수 없습니다. 유효한 입력으로 시도해주세요. :(');location.href='/stuff_list/';</script>")

@method_decorator(login_required, name="dispatch")
class RentalDetailView(View):
    def get(self, request, *args, **kwargs):
        rental = get_object_or_404(Rental, pk=self.kwargs['pk'])
        form = AcceptForm()
        category_list = Category.objects.all()

        context = {
            'rental': rental,
            'form': form,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/rental_detail.html', context)

    def post(self, request, *args, **kwargs):
        rental = get_object_or_404(Rental, pk=self.kwargs['pk'])
        form = AcceptForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rental.user = rental.user
            rental.stuff = rental.stuff
            rental.status = data['status']
            rental.rental_date = rental.rental_date
            rental.return_date = rental.return_date
            rental.save()
            return redirect('bilyeo:rental_detail', pk=rental.pk)
        else:
            return HttpResponse(
                "<script>alert('상태 변경에 실패했습니다! 유효한 입력으로 시도해주세요. :)');location.href='/rental/'" + rental.pk + ";</script>")
        return HttpResponse(
            "<script>alert('상태 변경에 실패했습니다! 유효한 입력으로 시도해주세요. :)');location.href='/rental/'" + rental.pk + ";</script>")

@method_decorator(login_required, name="dispatch")
class RentalUpdateView(View):
    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all()
        form = AvailabilityForm()
        context = {
            'form': form,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/stuff_update.html', context)

    def post(self, request, *args, **kwargs):
        rental = get_object_or_404(Rental, pk=self.kwargs['pk'])
        form = AvailabilityForm(request.POST, request.FILES)
        if form.is_valid() and rental.stuff.author == self.request.user:
            data = form.cleaned_data

            if check_availability(rental.stuff, data['rental_date'], data['return_date']):
                total_fee = find_total_rental_fee(data['rental_date'], data['return_date'], rental.stuff.pk)

                rental.rental_date = data['rental_date']
                rental.return_date = data['return_date']
                rental.total_fee = total_fee

                rental.save()
                return redirect('bilyeo:rental_detail', pk=rental.pk)
        else:
            return HttpResponse(
                "<script>alert('해당 대여를 변경할 수 없습니다! 유효한 입력으로 시도해주세요. :)');location.href='/rental/'" + rental.pk + ";</script>")
        return HttpResponse(
            "<script>alert('유효하지 않은 전송입니다. :(');location.href='/stuff_list/';</script>")


@login_required
def RentalDeleteView(request, pk):
    rental = get_object_or_404(Rental, pk=pk)

    if rental.user != request.user:
        return HttpResponse(
                "<script>alert('작성자만 삭제 가능합니다. :(');location.href='/stuff_list/';</script>")
    else:
        rental.delete()
        return redirect('bilyeo:my_rental_list')

    return HttpResponse(
            "<script>alert('해당 대여를 삭제할 수 없습니다. 유효한 입력으로 시도해주세요. :(');location.href='/stuff_list/';</script>")

@method_decorator(login_required, name="dispatch")
class MyRentalListView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        my_rental_list = Rental.objects.filter(user=user)
        category_list = Category.objects.all()

        context = {
            'my_rental_list': my_rental_list,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/my_rental_list.html', context)

@method_decorator(login_required, name="dispatch")
class MyStuffListView(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        my_stuff_list = Stuff.objects.filter(author__username=user.username)
        category_list = Category.objects.all()
        context = {
            'my_stuff_list': my_stuff_list,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/my_stuff_list.html', context)

class RequestRentalList(View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        request_list = Rental.objects.filter(stuff__author=user)
        category_list = Category.objects.all()
        context = {
            'request_list': request_list,
            'category_list': category_list,
        }
        return render(request, 'bilyeo/request_rental_list.html', context)


class RentalList(ListView):
    model = Rental

    def get_context_data(self, **kwargs):
        context = super(RentalList, self).get_context_data()
        context['category_list'] = Category.objects.all()
        context['no_category_post_count'] = Category.objects.filter(category=None).count()
        return context

# class RentalView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'bilyeo/rental.html'
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         if check_availability(data['stuff'], data['rental_date'], data['return_date']):
#             rental = Rental.objects.create(
#                 user=self.request.user,
#                 stuff=data['stuff'],
#                 rental_date=data['rental_date'],
#                 return_date=data['return_date'],
#             )
#             rental.save()
#             return HttpResponse(rental)
#         else:
#             return HttpResponse('해당 물품은 이미 예약되었습니다! 다른 물품으로 시도해주세요. :)')

def categories_posts(request, slug):
    if slug == 'no-category':
        category = '미분류'
        stuff_list = Stuff.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        stuff_list = Stuff.objects.filter(category=category)

    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': Stuff.objects.filter(category=None).count(),
        'category': category,
        'stuff_list': stuff_list
    }

    return render(request, 'bilyeo/rental_filter_list.html', context)
