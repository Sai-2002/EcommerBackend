from fastapi import APIRouter
from ..controllers.product_controller import ProductController

router = APIRouter()
controller = ProductController()

router.post("/categories")(controller.create_category)
router.get("/categories")(controller.list_categories)
router.post("/")(controller.create_product)
router.get("/")(controller.list_products)
router.get("/{product_id}")(controller.get_product)
router.put("/{product_id}")(controller.update_product)
router.delete("/{product_id}")(controller.delete_product)
