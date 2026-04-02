import logging
import yaml

# 1️⃣ Simulate config
config = {"logging": {"level": "WARNING"}}  # 👈 Change this to DEBUG or WARNING

# 2️⃣ Our setup function
def setup_logging(cfg):
    level = getattr(logging, cfg["logging"]["level"].upper())
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(message)s",
        force=True  # ⚠️ Resets logger for testing
    )

# 3️⃣ Run it
setup_logging(config)
logger = logging.getLogger(__name__)

logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")