from fastapi import APIRouter
from ..controllers.auth_controller import AuthController

router = APIRouter()
controller = AuthController()

router.post("/register")(controller.register)
router.post("/login")(controller.login)