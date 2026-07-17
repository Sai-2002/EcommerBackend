from fastapi import APIRouter

from ..controllers.payment_controller import PaymentController

router = APIRouter()
controller = PaymentController()

router.post("/")(controller.create_payment)
router.get("/order/{order_id}")(controller.get_payment_by_order)
router.get("/{payment_id}")(controller.get_payment)
