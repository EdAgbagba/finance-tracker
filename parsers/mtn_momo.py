import re

# find the txn type
def detect_type(text: str) -> str:
    if "Payment received for" in text:
        return "received"
    elif "Payment made for" in text:
        return "made"
    elif "Cash Out made for" in text:
        return "cash_out"
    elif "has been credited to your mobile money account" in text:
        return "credited"
    elif re.search(r"^Payment for GHS", text):
        return "bundle_payment"
    elif "Your payment of" in text and "has been completed" in text:
        return "payment_completed"
    else:
        return "unknown"


def extract_shared_fields(text: str) -> dict:
    balance = re.search(
        r"(?:Current Balance|new balance):?\s*GHS\s?([\d,]+\.\d{2})",
        text,
        re.IGNORECASE,
    )
    txn_id = re.search(r"(?:Financial )?Transaction I[dD]:?\s*(\d+)", text)
    fee = re.search(
        r"Fee (?:charged|was):?\s*GHS\s?([\d,]+\.\d{2})", text, re.IGNORECASE
    )

    return {
        "balance_after": balance.group(1) if balance else None,
        "transaction_id": txn_id.group(1) if txn_id else None,
        "fee": fee.group(1) if fee else None,
    }


def parse(text: str) -> dict:
    txn_type = detect_type(text)
    fields = extract_shared_fields(text)

    if txn_type == "received":
        m = re.search(
            r"Payment received for GHS\s?([\d,]+\.\d{2}) from ([A-Z\s\-]+?)\s+Current Balance",
            text,
        )
        fields.update(
            {
                "direction": "in",
                "amount": m.group(1) if m else None,
                "counterparty": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "made":
        m = re.search(
            r"Payment made for GHS\s?([\d,]+\.\d{2}) to ([A-Z\s\-]+?)\s+Current Balance",
            text,
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1) if m else None,
                "counterparty": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "cash_out":
        m = re.search(
            r"Cash Out made for GHS\s?([\d,]+\.\d{2}) to ([A-Z\s]+?)\.\s*Current Balance",
            text,
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1) if m else None,
                "counterparty": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "credited":
        m = re.search(r"An amount of GHS\s?([\d,]+\.\d{2}) has been credited", text)
        fields.update(
            {
                "direction": "in",
                "amount": m.group(1) if m else None,
                "counterparty": None,
            }
        )

    elif txn_type == "bundle_payment":
        m = re.search(
            r"^Payment for GHS\s?([\d,]+\.\d{2}) to ([A-Z\s]+?)\s*\.?Current Balance",
            text,
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1) if m else None,
                "counterparty": m.group(2).strip() if m else None,
            }
        )

    elif txn_type == "payment_completed":
        m = re.search(
            r"Your payment of GHS\s?([\d,]+\.\d{2}) to ([A-Z\s]+?) has been completed",
            text,
        )
        fields.update(
            {
                "direction": "out",
                "amount": m.group(1) if m else None,
                "counterparty": m.group(2).strip() if m else None,
            }
        )

    else:
        fields.update({"direction": None, "amount": None, "counterparty": None})

    fields["provider"] = "mtn_momo"
    fields["type"] = txn_type
    fields["raw_text"] = text
    return fields