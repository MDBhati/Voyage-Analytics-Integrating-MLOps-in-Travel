FLIGHTS_SCHEMA = {
    "travelCode": "int64",
    "userCode": "int64",
    "from": "object",
    "to": "object",
    "flightType": "object",
    "price": "float64",
    "time": "float64",
    "distance": "float64",
    "agency": "object",
    "date": "object"
}


HOTELS_SCHEMA = {
    "travelCode": "int64",
    "userCode": "int64",
    "name": "object",
    "place": "object",
    "days": "int64",
    "price": "float64",
    "total": "float64",
    "date": "object"
}


USERS_SCHEMA = {
    "code": "int64",
    "company": "object",
    "name": "object",
    "gender": "object",
    "age": "int64"
}