from turbo.components import BroadcastComponent, UserBroadcastComponent


class AlertBroadcastComponent(BroadcastComponent):
    template_name = "app/components/sample_broadcast_component.html"


class CartCountComponent(UserBroadcastComponent):
    template_name = "app/components/cart_count_component.html"

    def get_context(self):
        return {"count": 99}  # user.cart.items_in_cart
