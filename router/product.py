from typing import List, Optional
from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse


router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['watch', 'camera', 'phone']


@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get('/all')
def get_all_products():
    # return products
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response



@router.get('/withheader')
def get_products(
    response: Response,
    custom_header: List[str] = Header(None),
    test_cookie: Optional[str] = Cookie(None)
    ):
    if custom_header:
       response.headers ['custom_response_header'] = " and ".join(custom_header) # type: ignore
    return {
        'data': products,
        'custom_header': custom_header,
        'my_cookie': test_cookie    
    }



@router.get('/{id}', responses= {
    200: {
        "content": {
            "text/html": {
                "example": "<div>product</div>"
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "example": "product not available"
            }
        },
        "description": "A cleartext error message"
    }    
})
def get_product(id: int):
    if id > len (products):
       out = "products not available"
       return PlainTextResponse(status_code=404, content=out, media_type="text/plain" )
    else:   
       product = products[id]
       out = f"""
       <heads>
            <styles>
            .products {{
                width: 500px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center:
            }}
            </style>
        </head>
        <div class="product">Random product"<{product}</div>    
        """

    return HTMLResponse(content=out, media_type="text/html")