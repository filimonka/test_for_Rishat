import os

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from dotenv import load_dotenv
import stripe

from items.models import Item, ItemInOrder, Order

load_dotenv()


API_KEY = os.getenv('STRIPE_SECRET_KEY')
PUB_KEY = os.getenv('STRIPE_PUBLIC_KEY')


class ItemView(TemplateView):
    template_name = 'session.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = get_object_or_404(Item, id=self.kwargs['id'])
        context['api_key'] = API_KEY
        context['public_key'] = PUB_KEY
        return context


class OrderView(TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=self.kwargs['id'])
        context['items'] = ItemInOrder.objects.filter(
            order_id=self.kwargs['id']
        )
        context['id'] = self.kwargs['id']
        context['api_key'] = API_KEY
        context['public_key'] = PUB_KEY
        return context


class BuyView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=self.kwargs['id'])
        checkout_session = stripe.checkout.Session.create(
            api_key=API_KEY,
            line_items=[
                {
                    'price_data': {
                        'unit_amount': item.price,
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name
                        }
                    },
                    'quantity': 1,
                }
            ],
            payment_method_types=['card'],
            mode='payment',
            success_url='http://localhost/success/',
            cancel_url='http://localhost/cancel/'
        )
        return Response(data={'sessionId': checkout_session['id'], })


class PayForOrderVew(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        items = ItemInOrder.objects.filter(order_id=self.kwargs['id'])
        discount = None
        if order.discount.count() > 0:
            discount = order.discount.all()[0]
            coupon = stripe.Coupon.create(
                api_key=API_KEY,
                percent_off=discount.percentage,
                name=discount.name,
                duration='once'
            )
            discount = [
                {
                    'coupon': coupon
                }
            ]        
        checkout_session = stripe.checkout.Session.create(
            api_key=API_KEY,
            line_items=[
                {
                    'price_data': {
                        'unit_amount': item.item.price,
                        'currency': item.item.currency,
                        'product_data': {
                            'name': item.item.name
                        }
                    },
                    'quantity': item.amount,
                }add
                for item in items
            ],
            discounts=discount,
            payment_method_types=['card'],
            mode='payment',
            success_url='http://localhost/success/',
            cancel_url='http://localhost/cancel/'
        )
        return Response(data={'sessionId': checkout_session['id'], })


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'
