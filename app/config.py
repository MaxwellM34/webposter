TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:password@localhost:5432/testing"
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
