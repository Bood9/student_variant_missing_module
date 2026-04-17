from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm, ManagerOrderForm

def get_user_role(user):
    if user.is_superuser:
        return 'admin'
    if user.groups.filter(name='manager').exists():
        return 'manager'
    if user.groups.filter(name='client').exists():
        return 'client'
    return 'guest'

@login_required
def order_list(request):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'У вас нет доступа к заказам.')
        return redirect('products:product_list')
        
    if role in ['admin', 'manager']:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
        
    return render(request, 'orders/order_list.html', {'orders': orders, 'user_role': role})

@login_required
def order_create(request):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'Создавать заказы могут только клиенты.')
        return redirect('products:product_list')
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_list')
    else:
        initial = {}
        if 'product_id' in request.GET:
            initial['product'] = request.GET['product_id']
        form = OrderForm(initial=initial)
        
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Создать заказ', 'user_role': role})

@login_required
def order_update(request, pk):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'У вас нет доступа к заказам.')
        return redirect('products:product_list')
        
    if role in ['admin', 'manager']:
        order = get_object_or_404(Order, pk=pk)
        FormClass = ManagerOrderForm
    else:
        order = get_object_or_404(Order, pk=pk, user=request.user)
        FormClass = OrderForm
        
    if request.method == 'POST':
        form = FormClass(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно обновлен.')
            return redirect('orders:order_list')
    else:
        form = FormClass(instance=order)
        
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Редактировать заказ', 'user_role': role, 'order': order})

@login_required
def order_delete(request, pk):
    role = get_user_role(request.user)
    if role == 'guest':
        messages.error(request, 'У вас нет доступа к заказам.')
        return redirect('products:product_list')

    if role in ['admin', 'manager']:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ успешно удален.')
        return redirect('orders:order_list')
        
    return render(request, 'orders/order_confirm_delete.html', {'order': order, 'user_role': role})
