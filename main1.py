from app.models.base import *
from app.db.database import db, engine
from app.db.base import Base
from app.enums.enums import PurchaseOrderStatus



# s1 = Supplier(
#     name= "Yash Solanki",
#     email ="ys6244864@gami.com",
#     mobile = 8734821090,
#     lead_time_days = 8

# )


# db.add(s1)
# db.commit()


# c1 =Category(
#     name="Electronics"
# )

# db.add(c1)
# db.commit()

# p1 = Product(
#     sku ="ABC",
#     qty= 5,
#     cost= 100,
#     description = "Hello",
#     category_id= "daf0bf42-435a-43d7-be35-451639cf6b63"

# )

# db.add(p1)
# db.commit()


# po1 = PurchaseOrder(
#     product_id = "4a787dda-9aa8-42e3-9828-9236474ba72e",
#     qty =10,
#     unit_cost = 1500,
#     total_cost = 15000,
#     lead_time_days = 8,
#     status = "draft",
#     supplier_id = "d9ef4a25-1c30-46a6-b7be-ec43ed7eecb4"
# )

# db.add(po1)
# db.commit()
from uuid import UUID


# p1 = Product(
#     sku="ELEC-IPH-001",
#     name="iPhone 15 Pro",
#     description="Apple iPhone 15 Pro 128GB",
#     qty=0, 
#     cost=120000, 
#     model="A2849",
#     brand="Apple",
#     category_id="f19960a9-cbcc-403d-b15a-a5066a812e7c"  # Example UUID of Category
# )

# db.add(p1)
# db.commit()
# Base.metadata.drop_all(engine)







