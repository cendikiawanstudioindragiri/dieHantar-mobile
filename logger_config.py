# logger_config.py

import logging
import sys

def get_logger(name):
    """Konfigurasi dan kembalikan logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Buat handler untuk output ke console
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        # Buat formatter dan tambahkan ke handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Tambahkan handler ke logger
        logger.addHandler(handler)
        
    return logger
