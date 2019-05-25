from django.db import models
import django.utils.timezone as timezone

from conf.mongo import mongoc
from bson.objectid import ObjectId

# Create your models here.
class Content(models.Model):
    code = models.CharField(verbose_name="股票代码", max_length=10)
    title = models.CharField(verbose_name="标题", max_length=100)
    _info = models.CharField(verbose_name="内容对应的mongoid", blank=True, null=True, max_length=50)  # to mongodb
    url = models.CharField(verbose_name="url", max_length=100)
    time = models.DateTimeField(default=timezone.now)

    def get_info(self):
        infos = mongoc.wechat_msg
        return infos.find_one({"_id": ObjectId(self._info)}).get("body")

    def set_info(self, body):
        infos = mongoc.wechat_msg
        info_id = infos.insert_one({"body":body}).inserted_id
        self._info = str(info_id)

    info = property(get_info, set_info)

    def __str__(self):
        return self.title