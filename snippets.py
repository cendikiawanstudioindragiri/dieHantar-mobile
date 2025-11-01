import datetime

data = {
    "stringExample": "Hello, World!",
    "booleanExample": True,
    "numberExample": 3.14159265,
    "dateExample": datetime.datetime.now(tz=datetime.timezone.utc),
    "arrayExample": [5, True, "hello"],
    "nullExample": None,
    "objectExample": {"a": 5, "b": True},
}

db.collection("data").document("one").set(data)
