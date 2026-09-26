# parsers/__init__.py
from . import telecel_cash, mtn_momo

MTN_MARKERS = ["currentbalance", "transactionid", "mtnmomo", "momoapp"]


# def route(text: str) -> dict:
#     lowercase_no_space_text = text.lower().replace(" ", "")
#     if "telecel" in lowercase_no_space_text:
#         return telecel_cash.parse(text)
#     elif any(marker in lowercase_no_space_text for marker in MTN_MARKERS):
#         return mtn_momo.parse(text)
#     else:
#         return {"provider": "unknown", "type": "unknown", "raw_text": text}


def route(text: str) -> dict:
    lowercase_no_space_text = text.lower().replace(" ", "")
    
    if any(marker in lowercase_no_space_text for marker in MTN_MARKERS):
        return mtn_momo.parse(text)
    elif "telecel" in lowercase_no_space_text:
        return telecel_cash.parse(text)
    else:
        return {"provider": "unknown", "type": "unknown", "raw_text": text}