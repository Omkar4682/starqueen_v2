import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import MenuItem, GalleryImage, DeliveryOrder, OrderItem, DeliveryArea
from .forms import ReservationForm, DeliveryOrderForm


CATEGORY_EMOJIS = {
    'ice_cream':   ('🍨', 'Ice Cream'),
    'milkshakes':  ('🥤', 'Milkshakes'),
    'cold_coffee': ('☕', 'Cold Coffee'),
    'pizza':       ('🍕', 'Pizza'),
    'burgers':     ('🍔', 'Burgers'),
    'momos':       ('🥟', 'Momos'),
    'french_fries':('🍟', 'French Fries'),
    'fresh_juices':('🍊', 'Fresh Juices'),
    'smoothies':   ('🫐', 'Smoothies'),
    'lassi':       ('🥛', 'Lassi'),
    'falooda':     ('🌹', 'Falooda'),
}


def home(request):
    bestsellers = MenuItem.objects.filter(is_bestseller=True, is_available=True)[:6]
    categories_preview = [(emoji, label, key) for key, (emoji, label) in CATEGORY_EMOJIS.items()]
    return render(request, 'cafe/home.html', {
        'bestsellers': bestsellers,
        'categories_preview': categories_preview,
        'menu_categories': MenuItem.CATEGORY_CHOICES,
    })


def menu(request):
    categories = MenuItem.CATEGORY_CHOICES
    selected_category = request.GET.get('category', '')
    category_data = {}
    for cat_key, cat_name in categories:
        if selected_category and selected_category != cat_key:
            continue
        cat_items = MenuItem.objects.filter(category=cat_key, is_available=True)
        if cat_items.exists():
            category_data[cat_name] = {'key': cat_key, 'items': cat_items}
    return render(request, 'cafe/menu.html', {
        'category_data': category_data,
        'categories': categories,
        'selected_category': selected_category,
    })


def gallery(request):
    return render(request, 'cafe/gallery.html', {
        'interior_images': GalleryImage.objects.filter(category='interior'),
        'food_images': GalleryImage.objects.filter(category='food'),
        'customer_images': GalleryImage.objects.filter(category='customers'),
        'food_placeholders': ['Cold Coffee', 'Pizza Slice', 'Mango Falooda', 'Veg Momos', 'Oreo Shake', 'French Fries'],
    })


def events(request):
    return render(request, 'cafe/events.html')


def visit(request):
    return render(request, 'cafe/visit.html')


def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Thank you, {obj.name}! Your table for {obj.guests} on {obj.date.strftime('%d %B %Y')} at {obj.time.strftime('%I:%M %p')} is confirmed.")
            return redirect('reservation')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm()
    return render(request, 'cafe/reservation.html', {'form': form})


# ═══════════════════════════════════════════
#  HOME DELIVERY VIEWS
# ═══════════════════════════════════════════

def delivery_home(request):
    """Main delivery ordering page — like Swiggy/Zomato"""
    categories = MenuItem.CATEGORY_CHOICES
    category_data = {}
    for cat_key, cat_name in categories:
        items = MenuItem.objects.filter(category=cat_key, is_available=True)
        if items.exists():
            emoji, label = CATEGORY_EMOJIS.get(cat_key, ('🍽️', cat_name))
            category_data[cat_name] = {'key': cat_key, 'items': items, 'emoji': emoji}

    delivery_areas = DeliveryArea.objects.filter(is_available=True)
    return render(request, 'cafe/delivery.html', {
        'category_data': category_data,
        'delivery_areas': delivery_areas,
        'form': DeliveryOrderForm(),
    })


def place_order(request):
    """Handle order placement with cart items from POST"""
    if request.method == 'POST':
        form = DeliveryOrderForm(request.POST)
        cart_json = request.POST.get('cart_data', '[]')

        try:
            cart_items = json.loads(cart_json)
        except (json.JSONDecodeError, ValueError):
            cart_items = []

        if not cart_items:
            messages.error(request, "Your cart is empty! Please add items before placing an order.")
            return redirect('delivery_home')

        if form.is_valid():
            order = form.save(commit=False)

            # Calculate totals
            subtotal = Decimal('0')
            for ci in cart_items:
                try:
                    item = MenuItem.objects.get(id=ci['id'], is_available=True)
                    qty = int(ci.get('qty', 1))
                    subtotal += item.price * qty
                except (MenuItem.DoesNotExist, KeyError, ValueError):
                    continue

            # Delivery charge based on area
            delivery_charge = Decimal('30')
            try:
                area = DeliveryArea.objects.get(pincode=order.pincode, is_available=True)
                delivery_charge = area.delivery_charge
                if subtotal < area.min_order:
                    messages.error(request, f"Minimum order for {area.area_name} is ₹{area.min_order}.")
                    return redirect('delivery_home')
            except DeliveryArea.DoesNotExist:
                pass  # Use default delivery charge

            order.subtotal = subtotal
            order.delivery_charge = delivery_charge
            order.total = subtotal + delivery_charge
            order.save()

            # Save order items
            for ci in cart_items:
                try:
                    item = MenuItem.objects.get(id=ci['id'], is_available=True)
                    qty = max(1, int(ci.get('qty', 1)))
                    OrderItem.objects.create(order=order, menu_item=item, quantity=qty, price=item.price)
                except (MenuItem.DoesNotExist, KeyError, ValueError):
                    continue

            # Store order number in session for tracking
            request.session['last_order'] = order.order_number
            messages.success(request, f"🎉 Order #{order.order_number} placed successfully!")
            return redirect('order_confirmation', order_number=order.order_number)

        else:
            # Form invalid — re-render delivery page with errors
            categories = MenuItem.CATEGORY_CHOICES
            category_data = {}
            for cat_key, cat_name in categories:
                items = MenuItem.objects.filter(category=cat_key, is_available=True)
                if items.exists():
                    emoji, label = CATEGORY_EMOJIS.get(cat_key, ('🍽️', cat_name))
                    category_data[cat_name] = {'key': cat_key, 'items': items, 'emoji': emoji}
            messages.error(request, "Please fill in all required delivery details.")
            return render(request, 'cafe/delivery.html', {
                'category_data': category_data,
                'form': form,
                'cart_json': cart_json,
            })

    return redirect('delivery_home')


def order_confirmation(request, order_number):
    """Order success + live tracking page"""
    order = get_object_or_404(DeliveryOrder, order_number=order_number)
    order_items = order.items.select_related('menu_item').all()
    return render(request, 'cafe/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
    })


def track_order(request):
    """Track order by order number"""
    order = None
    order_items = []
    order_number = request.GET.get('order_number', '').strip().upper()

    if order_number:
        try:
            order = DeliveryOrder.objects.get(order_number=order_number)
            order_items = order.items.select_related('menu_item').all()
        except DeliveryOrder.DoesNotExist:
            messages.error(request, f"No order found with number #{order_number}. Please check and try again.")

    return render(request, 'cafe/track_order.html', {
        'order': order,
        'order_items': order_items,
        'order_number': order_number,
    })


def check_delivery_area(request):
    """AJAX: check if pincode is serviceable"""
    pincode = request.GET.get('pincode', '').strip()
    try:
        area = DeliveryArea.objects.get(pincode=pincode, is_available=True)
        return JsonResponse({
            'available': True,
            'area': area.area_name,
            'charge': str(area.delivery_charge),
            'min_order': str(area.min_order),
        })
    except DeliveryArea.DoesNotExist:
        # Default — we deliver everywhere in Beed
        return JsonResponse({
            'available': True,
            'area': 'Beed',
            'charge': '30',
            'min_order': '100',
        })
