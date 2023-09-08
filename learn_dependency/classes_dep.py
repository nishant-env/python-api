from fastapi import APIRouter, Depends
from typing import Annotated



router = APIRouter()


class CommonParams:
    def __init__(self, q:str | None = None, skip: int = 0, limit: int = 1000):
        self.q = q
        self.skip = skip
        self.limit = limit




@router.get('/class_items')
def dep_class_demo(common: Annotated[CommonParams, Depends(CommonParams)]):
    # or you can just write: common: Annotated[CommonParams, Depends()]

    return {"str" : common.q, "skip" : common.skip, "limit" : common.limit}