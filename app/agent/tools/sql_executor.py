import asyncpg
from app.config import settings
from typing import Dict, Any, List


# Whitelist of allowed tables and operations
ALLOWED_TABLES = ["users", "products", "orders", "events", "logs"]
ALLOWED_KEYWORDS = ["SELECT", "WHERE", "FROM", "JOIN", "GROUP BY", "ORDER BY", "LIMIT"]


async def sql_query(query: str) -> Dict[str, Any]:
    """Execute a SELECT query against the database with safety checks."""
    try:
        # Safety check: only SELECT allowed
        q_upper = query.strip().upper()
        if not q_upper.startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed"}
        
        # Check for dangerous keywords
        dangerous = ["DELETE", "DROP", "INSERT", "UPDATE", "ALTER", "TRUNCATE"]
        for keyword in dangerous:
            if keyword in q_upper:
                return {"error": f"Query contains forbidden keyword: {keyword}"}
        
        # Connect to database
        db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        try:
            conn = await asyncpg.connect(db_url, timeout=10)
        except Exception as e:
            return {"error": f"Could not connect to database: {str(e)}"}
        
        try:
            rows = await conn.fetch(query, timeout=10)
            result = [dict(row) for row in rows]
            return {"rows": result, "count": len(result)}
        finally:
            await conn.close()
            
    except Exception as e:
        return {"error": f"Query execution failed: {str(e)}"}
