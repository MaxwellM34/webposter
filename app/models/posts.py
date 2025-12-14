from tortoise import fields, models


class Post(models.Model):
    id = fields.IntField(pk=True)
    caption = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
