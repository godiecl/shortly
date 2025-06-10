from typing import List, Type, TypeVar

from peewee import AutoField, Model, SqliteDatabase
from typeguard import typechecked

T = TypeVar("T", bound="BaseModel")


@typechecked
class BaseModel(Model):
    id = AutoField(primary_key=True)

    class Meta:
        database = SqliteDatabase(
            "..\\output\\database.sqlite",
            pragmas={
                # "journal_mode": "wal",
                "foreign_keys": 1
            },
        )
        strict_tables = True

    @classmethod
    def create_database(cls) -> None:
        models = cls.__subclasses__()
        db = cls._meta.database
        with db:
            db.create_tables(models, safe=True)

    @classmethod
    def find_all(cls: Type[T]) -> List[T]:
        return list(cls.select())

    @classmethod
    def save_all(cls: Type[T], instances: List[T]) -> None:
        db = cls._meta.database
        with db.atomic():
            to_insert = []
            to_update = []

            for instance in instances:
                if instance.id is None:
                    to_insert.append(instance)
                else:
                    to_update.append(instance)

            if to_insert:
                cls.bulk_create(instances)

            if to_update:
                cls.bulk_update(
                    to_update, fields=[f.name for f in cls._meta.sorted_fields]
                )
