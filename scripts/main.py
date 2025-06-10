import logging

from dotenv import load_dotenv
from typeguard import typechecked

from benchmark import benchmark
from logger import configure_logging

@typechecked
def main():
    log.debug("Starting main()")

    log.debug("Done.")

if __name__ == "__main__":
    # the logger
    configure_logging(log_level="DEBUG")
    log = logging.getLogger(__name__)

    # environment variables
    if load_dotenv("..\\.env"):
        log.debug("Environment variables loaded successfully.")
    else:
        log.error("Failed to load environment variables.")

    with benchmark("main()", log):
        main()
