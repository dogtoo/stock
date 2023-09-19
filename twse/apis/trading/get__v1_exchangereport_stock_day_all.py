from __future__ import annotations

import datetime
import pydantic
import typing

from pydantic import BaseModel

from swagger_codegen.api.base import BaseApi
from swagger_codegen.api.request import ApiRequest
from swagger_codegen.api import json
class Response200(BaseModel):
    Change: typing.Optional[str]  = None
    ClosingPrice: typing.Optional[str]  = None
    Code: typing.Optional[str]  = None
    HighestPrice: typing.Optional[str]  = None
    LowestPrice: typing.Optional[str]  = None
    Name: typing.Optional[str]  = None
    OpeningPrice: typing.Optional[str]  = None
    TradeValue: typing.Optional[str]  = None
    TradeVolume: typing.Optional[str]  = None
    Transaction: typing.Optional[str]  = None

def make_request(self: BaseApi,


) -> typing.List[Response200]:
    """Daily transaction information of listed stocks"""

    
    body = None
    

    m = ApiRequest(
        method="GET",
        path="/v1/exchangeReport/STOCK_DAY_ALL".format(
            
        ),
        content_type=None,
        body=body,
        headers=self._only_provided({
        }),
        query_params=self._only_provided({
        }),
        cookies=self._only_provided({
        }),
    )
    return self.make_request({
    
        "200": {
            
                "application/json": typing.List[Response200],
            
        },
    
    }, m)