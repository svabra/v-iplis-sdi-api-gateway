from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(docs_url=None)

origins = [
    #Angular app
    "http://localhost:4200",  
    "http://127.0.0.1:4200",
    "http://localhost:4201",  
    "http://127.0.0.1:4201",
    "http://localhost:8000",  
    "http://127.0.0.1:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return FileResponse("static/ndp-layout.html")

class RecognizedGroundPicture(BaseModel):
    url_path: str = Field(..., title="URL Path", description="The URL path of the recognized ground picture. Tag: ImageURL")
    lastUpdated: datetime = Field(..., title="Last Updated", description="The date and time when the ground picture was last updated. Tag: Timestamp")
    dataOwner: str = Field(..., title="Data Owner", description="The owner of the data. Tag: Owner")
    contact: str = Field(..., title="Contact", description="Contact information for the data owner. Tag: Contact")
    frequencyOfUpdate: str = Field(..., title="Frequency of Update", description="How frequently the data is updated. Tag: Frequency")

@app.get("/RecognizedGroundPicture/", response_model=RecognizedGroundPicture, 
         tags=["Recognized Ground Picture"], 
         summary="Get Recognized Ground Picture", 
         description="This endpoint returns the recognized ground picture.")
async def get_recognized_ground_picture():
    # This is a sample URL path, replace it with the actual path you want to return
    url_path = "https://upload.wikimedia.org/wikipedia/commons/e/e0/DesertStormMap_v2.svg"
    
    lastUpdated = datetime.now().isoformat()

    dataOwner = "Philipo Meiero"
    contact = "rgp@operationX10.vtg.admin.com"
    
    content = {
        "url_path": url_path,
        "lastUpdated": lastUpdated,
        "dataOwner": dataOwner,
        "contact": contact,
        "frequencyOfUpdate": "1d"
    }
    
    response = JSONResponse(content=content)    
    response.headers["labels"] = "classified"    
    # response.headers["labels"] = "public"    
    return response

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="IPLIS API",
        version="1.0.0",
        openapi_version="3.0.0",
        description="IPLIS Data Products",
        routes=app.routes,
        contact={
            "name": "Data Producer",
            "email": "support@example.com",
            "url": "https://www.admin.com",
        },
        terms_of_service="https://www.admin.com",
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.admin.ch/gov/de/_jcr_content/logo/image.imagespooler.png/1443432164932/Logo%20Schweizerische%20Eidgenossenschaft.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
