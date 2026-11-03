from fastapi import status, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..database import SessionDep
from ..schemas import Create_txn
from ..models import Transactions
from parsers import route
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
import logging
from psycopg2.errors import UniqueViolation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(new_txn: Create_txn, session: SessionDep):
    parsed_data = route(new_txn.message)

    if parsed_data.get("provider") in (None, "unknown"):
        return JSONResponse(
            {"status": "skipped", "reason": "unrecognized message"},
            status_code=status.HTTP_200_OK,
        )

    try:
        txn = Transactions.model_validate(parsed_data)
        session.add(txn)
        session.commit()
        session.refresh(txn)
        return txn
    except ValidationError as e:
        logger.warning("Parsed data invalid: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message could not be parsed",
        )
    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return JSONResponse({"status": "duplicate"}, status_code=status.HTTP_200_OK)
        logger.exception("Integrity error")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Transaction violates a database constraint",
        )
    except OperationalError:
        session.rollback()
        logger.exception("Database unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable",
        )