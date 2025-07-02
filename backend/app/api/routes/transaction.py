from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
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
