import logging
from pathlib import Path

def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "medicoast.log",
        filemode="a",  # append mode
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
