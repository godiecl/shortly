import logging

from base_model import BaseModel
from benchmark import benchmark
from logger import configure_logging
from peewee import IntegerField, TextField
from typeguard import typechecked


@typechecked
class Link(BaseModel):
    url = TextField(null=False, unique=True)
    short_url: TextField(null=False, unique=True, index=True)
    clicks: int = IntegerField(default=0, null=False)

    class Meta:
        table_name = "links"


@typechecked
def main():
    log.info("Starting main()")

    log.debug("Creating the database...")
    BaseModel.create_database()

    links = Link.find_all()
    for link in links:
        log.debug(
            f"Link: {link.url}, Short URL: {link.short_url}, Clicks: {link.clicks}"
        )

    log.info("Done.")


if __name__ == "__main__":
    # the logger
    configure_logging(log_level="DEBUG")
    log = logging.getLogger(__name__)

    with benchmark("main()", log):
        main()
