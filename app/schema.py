

ZONE = [
    {
        "name": "id",
        "type": "STRING",
        "description": "Primary Key",
    },
    {
        "name": "calories_out",
        "type": "FLOAT",
        "description": "Number of calories burned while in zone"
    },
    {
        "name": "max",
        "type": "INTEGER",
        "description": "Maximum heart rate while in zone"
    },
    {
        "name": "min",
        "type": "INTEGER",
        "description": "Minimum heart rate while in zone"
    },
    {
        "name": "minutes",
        "type": "INTEGER",
        "description": "Minutes in zone"
    },
    {
        "name": "name",
        "type": "STRING",
        "time": "Timestamp for day recorded"
    }
]

HEART_RATE = [
    {
        "name": "id",
        "type": "STRING",
        "description": "User id, Primary Key",
    },
    {
        "name": "time",
        "type": "TIMESTAMP",
        "description": "Timestamp of the data"
    },
    {
        "name": "heart_rate",
        "type": "INTEGER",
        "description": "Recorded heart rate"
    },
]
