from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from configurations import collection  # Make sure the collection is defined in the config
from typing import Optional
from bson import ObjectId
from databse.models import Student,StudentCreateResponse,UpdateStudentRequest

app = FastAPI()
router = APIRouter()

@router.post("/students",
             summary="Create Students",
             description="API to create a student in the system. All fields are mandatory and required while creating the student in the system.",
            responses={
        201: {
            "description": "A JSON response sending back the ID of the newly created student record.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties":{
                            "id":{
                                "type":"str"
                            }
                        }
                    }
                }
            }
        }
    }
            )
def create_student(new_student: Student):
    try:

        student_data = new_student.model_dump()  
        resp = collection.insert_one(student_data)

        return JSONResponse(
            status_code=201,
            content={"id": str(resp.inserted_id)}  
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")



@router.get("/students", summary="List students", description=" An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.",responses={
        200: {
            "description": "An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.",  
        }
    })
async def get_students(country: Optional[str] = Query(None, description="To apply filter of country. If not given or empty, this filter should be applied."),
                       age: Optional[int] = Query(None, description=" Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied."),
                       ):
    try:
        query = {}
        if country:
            query["address.country"] = {"$regex": f"^{country}$", "$options": "i"}

        if age is not None:
            query["age"] = {"$gte": age}

        students = list(collection.find(query))
        student_list = [{"name": student["name"], "age": student["age"]} for student in students]
        
        return JSONResponse(status_code=200, content={"data": student_list})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    

@router.get("/students/{id}",summary="Fetch student",description="The ID of the student previously created.",
            responses={
                200: {
            "description": "sample response",  
        }
            })
def get_by_id(id:str):
    try:
        id=ObjectId(id)
        student=collection.find_one({"_id":id})
        if not student:
            return HTTPException(status_code=404,detail=f"Id does not exist")
        
        student.pop("_id")
        return JSONResponse(status_code=200,content=student)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")



@router.patch(
    "/students/{id}",
    summary="Update student",
    description="API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.",
    responses={
        204: {
            "description": "No content",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object"
                    }
                }
            }
        }
    }
)
def update_student(id: str, updates: UpdateStudentRequest):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        
        object_id = ObjectId(id)
        update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")
        
        update_result = collection.update_one({"_id": object_id}, {"$set": update_data})
        
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} does not exist")
        
        return JSONResponse(status_code=204, content={})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")



@router.delete("/students/{id}", summary="Delete student")
def delete_student(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid student ID format")
        
        object_id = ObjectId(id)
        delete_result = collection.delete_one({"_id": object_id})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Student with ID {id} does not exist")
        
        return JSONResponse(status_code=200, content={})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")    

app.include_router(router)