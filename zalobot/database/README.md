# Database Package

Database models và connection management.

## Files:

- **models.py**: SQLModel models (Order, User, etc.)
- **connection.py**: Database engine, session management, init_db()

## Usage:

```python
from zalobot.database import init_db, get_session, Order

# Initialize database
init_db()

# Use in FastAPI dependency
from zalobot.database import get_session

@app.get("/orders")
def get_orders(session: Session = Depends(get_session)):
    orders = session.query(Order).all()
    return orders
```

