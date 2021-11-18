import json
from datetime import datetime
from typing import Any


class Serialize(json.JSONEncoder):
    def default(self, field: Any) -> Any:
        if isinstance(field, datetime):
            return field.isoformat()
