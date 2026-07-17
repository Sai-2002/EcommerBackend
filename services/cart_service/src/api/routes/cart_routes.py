from fastapi import APIRouter

from ..controllers.cart_controller import CartController

router = APIRouter()
controller = CartController()

router.post("/")(controller.add_to_cart)
router.get("/{user_id}")(controller.get_cart)
router.put("/items/{item_id}")(controller.update_cart_item)
router.delete("/items/{item_id}")(controller.remove_from_cart)
router.delete("/{user_id}/clear")(controller.clear_cart)
