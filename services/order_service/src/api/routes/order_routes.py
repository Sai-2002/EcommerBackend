from fastapi import APIRouter
from ..controllers.order_controller import OrderController

router = APIRouter()
controller = OrderController()

router.post("/")(controller.create_order)
router.get("/user/{user_id}")(controller.list_user_orders)
router.get("/{order_id}")(controller.get_order)
router.patch("/{order_id}/status")(controller.update_order_status)
