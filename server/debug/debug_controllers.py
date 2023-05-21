# fastapi
from fastapi import APIRouter

from server.task import triger_monthly_statement_generation

router = APIRouter(
    prefix="/debug",
    tags=["debug"],
    dependencies=[],
    responses={
        400: {"description": "Bad request"}
    },
)


@router.get("/generate-statements/")
def get_bank_accounts():
    task = triger_monthly_statement_generation.delay()
    return {"details": f"Task #{task} scheduled"}
