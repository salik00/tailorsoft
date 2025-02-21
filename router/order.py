# from fastapi import FastAPI, Form, HTTPException, APIRouter, Depends, UploadFile, File
# from sqlalchemy.orm import Session
# from typing import List
# import models,schemas
# from database import get_db
# from sqlalchemy.exc import SQLAlchemyError
# import traceback
# import shutil
# import json
# import os

# router = APIRouter(prefix ="/order", tags=["ORDERS"])

# UPLOAD_FOLDER = "uploads/images"
# os.makedirs(UPLOAD_FOLDER,exist_ok=True)

# @router.post("/createorder", response_model=schemas.OrderCreateResponse)
# async def create_order(
#     order: str= Form(...),  # Accept order as a JSON string
    
#     image: UploadFile = File(None),
#     db: Session = Depends(get_db)   
# ):
#     # print(order)
#     # return
#     try:
     
#         order_data = json.loads(order)
#         order_obj = schemas.OrderCreate(**order_data)

#         total_quantity = sum(item.quantity for item in order_obj.items)
#         total_price = sum(item.price * item.quantity for item in order_obj.items)
    
#         image_path = None
#         if image and image.filename:
#             print(f"received image : {image.filename}")
            
#             image_extension = os.path.splitext(image.filename)[1]
#             new_filename = f"order_{order_obj.customer_name}_{order_obj.contact_no}{image_extension}"
#             image_filename = os.path.join(UPLOAD_FOLDER, new_filename)
         
#             try:
#                 with open(image_filename, "wb") as buffer:
#                     shutil.copyfileobj(image.file, buffer)  # Save file
                
#                 print(f"Image saved successfully at: {image_filename}")
#                 image_path = image_filename  # Assign saved path

#             except Exception as e:
#                     print(f"Error saving image: {str(e)}")
#                     raise HTTPException(status_code=500, detail="Failed to save image")
        
#         db_order = models.Order(
#             customer_name=order_obj.customer_name,
#             contact_no=order_obj.contact_no,
#             created_at = order_obj.created_at,
#             delivery_date=order_obj.delivery_date,
#             total_price=total_price,
#             total_quantity=total_quantity,
#             image_path = image_path,
#             order_status=order_obj.order_status
#         )
#         db.add(db_order)
#         db.commit()
#         db.refresh(db_order)
        
#         for item_data in order_obj.items:
#             item = models.OrderItem(
#                 item_name= item_data.item_name,
#                 quantity= item_data.quantity,
#                 price= item_data.price,
#                 order = db_order
#             )
#             db.add(item)
    
#         # db.add(db_order)
#         db.commit()
#         db.refresh(db_order)
#         if image:
#             db_order.image_path = image_path
#             db.commit()
#             db.refresh(db_order)
#          # Debugging: Print final stored image path
#         print(f"Final Image Path in DB: {db_order.image_path}")
#         print(f"Stored Image Path: {db_order.image_path}")  # Debugging

#         return db_order
    
#     except json.JSONDecodeError:
#             raise HTTPException(status_code=400, detail="Invalid JSON format for 'order' field.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# @router.get("/getorder", response_model=List[schemas.GetOrderResponse])
# def get_order(db:Session= Depends(get_db),limit:int=3, offset:int=0):
#     result = db.query(
#         models.Order.id.label("order_id"),
#         models.Order.customer_name,
#         models.Order.delivery_date,
#         models.Order.created_at,
#         models.Order.total_quantity,
#         models.Order.total_price,   
#         models.Order.image_path,
#         models.Order.order_status
#     ).order_by(models.Order.created_at.desc()).limit(limit).offset(offset).all()
#     return result



from fastapi import FastAPI, Form, HTTPException, APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
import traceback
import shutil
import json
import os

router = APIRouter(prefix="/order", tags=["ORDERS"])

UPLOAD_FOLDER = "uploads/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/createorder", response_model=schemas.OrderCreateResponse)
async def create_order(
    order: str = Form(...),  # Accept order as a JSON string
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    print("\n === STARTING ORDER CREATION ===")

    try:
        # Step 1: JSON Parsing
        print("\nStep 1: Parsing JSON Order")
        print("Raw Order Data:", order)
        try:
            order_data = json.loads(order)
            print("Parsed Order Data:", order_data)
        except json.JSONDecodeError as e:
            print("\n JSON Parsing Error")
            traceback.print_exc()
            raise HTTPException(status_code=400, detail="Invalid JSON format for 'order' field.")

        # Step 2: Schema Validation
        print("\nStep 2: Validating Order Schema")
        try:
            order_obj = schemas.OrderCreate(**order_data)
            print("Validated Order Object:", order_obj)
        except Exception as e:
            print("\n Schema Validation Error")
            print(str(e))
            traceback.print_exc()
            raise HTTPException(status_code=422, detail="Order schema validation failed")

        # Step 3: Calculate totals
        print("\n Step 3: Calculating Total Quantity and Price")
        try:
            total_quantity = sum(item.quantity for item in order_obj.items)
            total_price = sum(item.price * item.quantity for item in order_obj.items)
            print("Total Quantity:", total_quantity, "| Total Price:", total_price)
        except Exception as e:
            print("\n Calculation Error")
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Error calculating total quantity or price")

        # Step 4: Image Upload (if provided)
        image_path = None
        if image and image.filename:
            print("\n Step 4: Uploading Image")
            print("Image received:", image.filename)

            try:
                image_extension = os.path.splitext(image.filename)[1]
                new_filename = f"order_{order_obj.customer_name}_{order_obj.contact_no}{image_extension}"
                image_filename = os.path.join(UPLOAD_FOLDER, new_filename)

                with open(image_filename, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                image_path = image_filename
                print("Image saved at:", image_filename)

            except Exception as e:
                print("\n Image Upload Error")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail="Failed to save image")

        # Step 5: Save Order to Database
        print("\n Step 5: Saving Order to Database")
        try:
            db_order = models.Order(
                customer_name=order_obj.customer_name,
                contact_no=order_obj.contact_no,
                created_at=order_obj.created_at,
                delivery_date=order_obj.delivery_date,
                total_price=total_price,
                total_quantity=total_quantity,
                bill_no=order_obj.bill_no,
                image_path=image_path,
                order_status=order_obj.order_status
            )
            print("Order Object Created:", db_order)

            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            print(" Order Saved Successfully with ID:", db_order.id)

        except SQLAlchemyError as e:
            print("\n Database Order Save Error")
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to save order to the database")

        # Step 6: Save Order Items to Database
        print("\n Step 6: Saving Order Items to Database")
        try:
            for item_data in order_obj.items:
                item = models.OrderItem(
                    item_name=item_data.item_name,
                    quantity=item_data.quantity,
                    price=item_data.price,
                    order=db_order
                )
                db.add(item)
                print("Order Item Added:", item.item_name)

            db.commit()
            print("Order Items Saved Successfully")

        except SQLAlchemyError as e:
            print("\n Database Order Items Save Error")
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to save order items to the database")

        # Step 7: Update Image Path (if image exists)
        if image:
            print("\n Step 7: Updating Image Path in Database")
            try:
                db_order.image_path = image_path
                db.commit()
                db.refresh(db_order)
                print(" Final Image Path Saved:", db_order.image_path)
            except SQLAlchemyError as e:
                print("\n Database Image Path Update Error")
                traceback.print_exc()
                db.rollback()
                raise HTTPException(status_code=500, detail="Failed to update image path in the database")

        print("\n ORDER CREATION SUCCESSFUL")
        return db_order

    except Exception as e:
        print("\n UNEXPECTED ERROR")
        print(str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# ==================================================================== #
# ✅ GET ORDER WITH DEBUGGING
# ==================================================================== #
@router.get("/getorder", response_model=List[schemas.GetOrderResponse])
def get_order(db: Session = Depends(get_db), limit: int = 3, offset: int = 0):
    print("\n === FETCHING ORDERS ===")
    try:
        result = db.query(
            models.Order.id.label("order_id"),
            models.Order.customer_name,
            models.Order.delivery_date,
            models.Order.created_at,
            models.Order.total_quantity,
            models.Order.total_price,
            models.Order.image_path,
            models.Order.order_status
        ).order_by(models.Order.created_at.desc()).limit(limit).offset(offset).all()

        print("Orders Retrieved:", len(result))
        for order in result:
            print(order)

        return result

    except SQLAlchemyError as e:
        print("\nDatabase Fetch Error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to fetch orders from the database")

    except Exception as e:
        print("\nUNEXPECTED ERROR")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
