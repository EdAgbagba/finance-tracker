# Finance Tracker

A personal finance tracker that turns mobile money SMS alerts (MTN MoMo, Telecel Cash) into structured transaction records, via a FastAPI backend.

## How it works

1. An iOS Shortcuts automation triggers on incoming SMS and forwards the raw message text to this backend via a webhook POST request.
2. The backend detects which provider sent the message and routes it to that provider's parser.
3. Each parser extracts amount, direction, counterparty, balance, and fee using regex tailored to that provider's message format.
4. Parsed transactions are normalized into a shared format and (once storage is wired up) saved to a database for querying and summarizing.

## Project status

This is an early-stage, self-directed learning project — currently in active development.

- [x] MTN MoMo parser — handles payments received/made, cash out, bundle purchases, credits, and completed payments
- [x] Telecel Cash parser — handles sent/received transfers, withdrawals, bundle purchases, interest credit, and balance notifications
- [ ] Shared field normalization across both parsers
- [ ] `models.py` — SQLModel `Transaction` table
- [ ] `database.py` — engine/session setup
- [ ] `main.py` — `/transactions/ingest` endpoint wired to parsers + database
- [ ] `GET /transactions` and `GET /summary` endpoints
- [ ] Deployment (Railway/Render)
- [ ] AirtelTigo Money parser
- [ ] React Native frontend

## Project structure

```
finance-tracker/
├── main.py                  # FastAPI app entrypoint
├── parsers/
│   ├── mtn_momo.py          # MTN MoMo SMS parser
│   └── telecel_cash.py      # Telecel Cash SMS parser
├── requirements.txt
└── .gitignore
```

## Tech stack

- **Python** / **FastAPI** — backend API
- **SQLModel** — ORM (planned)
- **iOS Shortcuts** — SMS capture and forwarding, no native mobile app required for ingestion
- **Regex** — provider-specific message parsing

## Why mobile money SMS?

Mobile money (MTN MoMo, Telecel Cash, AirtelTigo Money) is the dominant way everyday transactions happen in Ghana. Each provider sends a confirmation SMS for every transaction, but the format differs between providers and even between transaction types from the same provider — so this project treats each message shape as its own case, then normalizes everything into one consistent transaction record.

## Getting SMS onto the backend without an Android app

iOS doesn't allow apps to read SMS directly. This project instead uses a Shortcuts automation (Message trigger → Get Contents of URL) to forward incoming texts straight to the ingest endpoint as they arrive, with no manual intervention needed after setup.

## Running locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Use [ngrok](https://ngrok.com) to expose your local server to your phone during development:

```bash
ngrok http 8000
```

## License

Personal project — not yet licensed for reuse.
