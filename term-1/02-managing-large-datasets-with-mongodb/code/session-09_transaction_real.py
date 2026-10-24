# Session 9 · The real thing: a multi-document transaction with PyMongo
# Needs a replica set or sharded cluster (a free Atlas M0 cluster works; a single
# standalone mongod does NOT support transactions).
from pymongo import MongoClient, ReadPreference
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

client = MongoClient("mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority")
db = client.kgs

def place_order(session):
    product = db.products.find_one({"_id": 106}, session=session)
    if product["stock"] < 2:
        raise ValueError("not enough stock")              # any exception aborts the transaction
    db.products.update_one({"_id": 106}, {"$inc": {"stock": -2}}, session=session)
    db.orders.insert_one({"_id": 6001, "customerId": 2, "status": "Pending",
                          "items": [{"productId": 106, "qty": 2, "price": product["price"]}]},
                         session=session)

with client.start_session() as session:
    # with_transaction starts, commits, and retries on TransientTransactionError /
    # UnknownTransactionCommitResult for up to 120 seconds
    session.with_transaction(
        place_order,
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority"),
        read_preference=ReadPreference.PRIMARY,
    )
print("order placed atomically")
