import logging
from typing import List, Type, TypeVar

from peewee import AutoField, Model, SqliteDatabase
from typeguard import typechecked

# defines a generic type variable T that must be a subclass of BaseModel.
# This allows you to use type hints for methods that work with any subclass of BaseModel,
# improving type safety and code clarity.
T = TypeVar("T", bound="BaseModel")


@typechecked
class BaseModel(Model):
    """Base model for all database models."""

    id = AutoField(primary_key=True)
    log = logging.getLogger(__name__)

    class Meta:
        """Meta class for BaseModel."""

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
        """Create the database and tables for all subclasses of BaseModel."""
        models = cls.__subclasses__()
        cls.log.debug(f"Creating database with models: {[m.__name__ for m in models]}")
        db = cls._meta.database
        with db:
            db.create_tables(models, safe=True)

    @classmethod
    def find_all(cls: Type[T]) -> List[T]:
        """Find all instances of the model."""
        cls.log.debug(f"Finding all instances of {cls.__name__} ..")
        instances = list(cls.select())
        cls.log.debug(f".. found {len(instances)} instances of {cls.__name__}.")
        return instances

    @classmethod
    def save_all(cls: Type[T], instances: List[T]) -> None:
        """
        Save all instances of the model to the database.

        :param instances:
        :return:
        """
        cls.log.debug(f"Saving {len(instances)} instances of {cls.__name__} ..")
        db = cls._meta.database
        with db.atomic():
            to_insert = []
            to_update = []

            for instance in instances:
                if instance.id is None:
                    to_insert.append(instance)
                else:
                    to_update.append(instance)

            cls.log.debug(
                f"Prepared {len(to_insert)} instances for insertion and {len(to_update)} instances for update."
            )

            if to_insert:
                cls.bulk_create(instances)

            if to_update:
                cls.bulk_update(
                    to_update, fields=[f.name for f in cls._meta.sorted_fields]
                )
