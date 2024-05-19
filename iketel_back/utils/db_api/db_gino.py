# from gino import Gino
# import sqlalchemy as sa
# from sqlalchemy import Column, BigInteger, String
# from typing import List
# import datetime
# from data import config
# from loguru import logger
# from asgiref.sync import async_to_sync
# db = Gino()
#
# class BaseModel(db.Model):
#     __abstract__ = True
#
#     def __str__(self):
#         model = self.__class__.__name__
#         table: sa.Table = sa.inspect(self.__class__)
#         primary_key_columns: List[sa.Column] = table.primary_key.columns
#         values = {
#             column.name: getattr(self, self._column_name_map[column.name])
#             for column in primary_key_columns
#         }
#         values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
#         return f"<{model} {values_str}>"
#
#
# class TimedBaseModel(BaseModel):
#     __abstract__ = True
#
#     created_at = db.Column(db.DateTime(True), server_default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime(True),
#         default=datetime.datetime.now(),
#         onupdate=datetime.datetime.now(),
#         server_default=db.func.now(),
#     )
#
#
# async def on_startup():
#     logger.info("Setup PostgreSQL Connection")
#     await db.set_bind(config.POSTGRES_URI)
#
#
# async def on_shutdown():
#     bind = db.pop_bind()
#     if bind:
#         logger.info("Close PostgreSQL Connection")
#         await bind.close()
