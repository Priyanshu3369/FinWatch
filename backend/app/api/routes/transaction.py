from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status , Query
from ...core.deps import get_current_user
from ...db.mongo import db
import pandas as pd
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    contents = await file.read()
    try:
        df = pd.read_csv(pd.compat.StringIO(contents.decode()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")

    transactions = []
    for _, row in df.iterrows():
        tx = {
            "user_id": ObjectId(current_user["_id"]),
            "description": row.get("description") or "",
            "amount": float(row.get("amount") or 0),
            "date": pd.to_datetime(row.get("date")).to_pydatetime() if row.get("date") else datetime.utcnow(),
            "category": row.get("category") or None,
            "is_fraud": False,
            "created_at": datetime.utcnow(),
        }
        transactions.append(tx)

    if not transactions:
        raise HTTPException(status_code=400, detail="No transactions found")

    result = await db.transactions.insert_many(transactions)

    return {
        "message": f"Uploaded {len(result.inserted_ids)} transactions ✅"
    }

@router.get("/")
async def get_transactions(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, description="Max transactions to return")
):
    cursor = db.transactions.find({"user_id": ObjectId(current_user["_id"])}).sort("date", -1).limit(limit)
    transactions = []
    async for tx in cursor:
        tx["_id"] = str(tx["_id"])
        tx["user_id"] = str(tx["user_id"])
        tx["date"] = tx["date"].isoformat()
        tx["created_at"] = tx["created_at"].isoformat()
        transactions.append(tx)

    return {"transactions": transactions}


@router.get("/check-fraud")
async def check_fraud(
    current_user: dict = Depends(get_current_user)
):
    # Very simple rule: flag any single tx > $1000 as suspicious
    cursor = db.transactions.find({
        "user_id": ObjectId(current_user["_id"]),
        "amount": {"$gt": 1000},
        "is_fraud": False
    })

    flagged_ids = []
    async for tx in cursor:
        await db.transactions.update_one(
            {"_id": tx["_id"]},
            {"$set": {"is_fraud": True}}
        )
        flagged_ids.append(str(tx["_id"]))

    return {"flagged_transactions": flagged_ids}
