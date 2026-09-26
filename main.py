from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from parsers import route
from contextlib import asynccontextmanager
from database import create_database, insert_transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/transactions/ingest", status_code=status.HTTP_201_CREATED)
async def ingest(payload: dict):
    try:
        parsed_data = route(payload["message"])
        if parsed_data["provider"] == "unknown":
            return {"status": "skipped", "reason": "unrecognized message"}
        else:
            new_txn_data = insert_transaction(parsed_data)
            return {"data": new_txn_data}
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing required field: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )
