import re
from enum import Enum


def detect_type(text: str) -> str:
    lowered = text.lower()

    if "as interest earned" in lowered:
        return "interest"
    elif "bundle purchase request" in lowered:
        return "bundle_purchase"
    elif "you have withdrawn" in lowered:
        return "withdrawal"
    elif "sent to" in lowered and "confirmed" in lowered:
        return "sent"
    elif "you have received" in lowered:
        return "received"
    elif "wallet balance is" in lowered:
        return "balance_check"
    else:
        return "unknown"


def extract_shared_fields(text: str) -> dict:
    # Different messages phrase balance differently, so try several patterns
    balance = (
        re.search(r"Telecel Cash balance is\s*GHS([\d,]+\.\d{2})", text)
        or re.search(r"new Telecel Cash balance is\s*GHS([\d,]+\.\d{2})", text)
        or re.search(r"Telecel Cash wallet balance is\s*GHS([\d,]+\.\d{2})", text)
        or re.search(r"new balance is\s*GHS([\d,]+\.\d{2})", text)
    )
    ref = re.match(r"^(\d{16})", text)
    charged = re.search(r"You were charged GHS([\d,]+\.\d{2})", text)

    return {
        "balance_after": balance.group(1) if balance else None,
        "transaction_id": ref.group(1) if ref else None,
        "fee": charged.group(1) if charged else None,
    }


def parse(text: str) -> dict:
    txn_type = detect_type(text)
    fields = extract_shared_fields(text)

    if txn_type == "sent":
        m = re.search(
            r"GHS([\d,]+\.\d{2}) sent to\s+(\d+)\s*-?\s*([A-Za-z'\s]+?)\s+on", text
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1).replace(",", "") if m else None,
                "counterparty_number": m.group(2) if m else None,
                "counterparty_name": m.group(3).strip() if m else None,
            }
        )

    elif txn_type == "received":
        m = re.search(
            r"you have received GHS([\d,]+\.\d{2}) from (.+?) on \d{4}-\d{2}-\d{2}",
            text,
            re.IGNORECASE,
        )
        fields.update(
            {
                "direction": "in",
                "amount": m.group(1).replace(",", "") if m else None,
                "counterparty_name": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "withdrawal":
        m = re.search(
            r"you have withdrawn GHS([\d,]+\.\d{2}) from (.+?)\.? on \d{4}-\d{2}-\d{2}",
            text,
            re.IGNORECASE,
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1).replace(",", "") if m else None,
                "counterparty_name": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "bundle_purchase":
        m = re.search(
            r"bundle purchase request of GHS([\d,]+\.\d{2})", text, re.IGNORECASE
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1).replace(",", "") if m else None,
                "counterparty_name": "TELECEL BUNDLE",
            }
        )

    elif txn_type == "interest":
        m = re.search(
            r"received GHS([\d,]+\.\d{2}) from Telecel Cash as interest",
            text,
            re.IGNORECASE,
        )
        fields.update(
            {
                "direction": "in",
                "amount": m.group(1).replace(",", "") if m else None,
                "counterparty_name": "TELECEL INTEREST",
            }
        )

    elif txn_type == "balance_check":
        # No money movement — just a balance notification, no amount to extract
        fields.update(
            {
                "direction": None,
                "amount": None,
                "counterparty_name": None,
            }
        )

    else:
        fields.update({"direction": None, "amount": None, "counterparty_name": None})

    fields["provider"] = "telecel_cash"
    fields["type"] = txn_type
    fields["raw_text"] = text
    return fields