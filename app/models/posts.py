from tortoise import fields, models


class Post(models.Model):
    id = fields.IntField(pk=True)
    caption = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

class Upload(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    caption = fields.TextField()
    url = fields.TextField(null=True)
    file_type = fields.CharField(max_length=255, null=True)
    file_name = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
