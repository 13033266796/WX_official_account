LOGGING_CONFIG = {
            "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "console_format": {
                                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(thread)d"
                                            
                        }
                        
                    },
                "handlers": {
                    "console": {
                                    "class": "logging.StreamHandler",
                                                "level": "DEBUG",
                                                            "formatter": "console_format",
                                                                        "stream": "ext://sys.stdout",
                                                                                
                        }
                        
                    },
                "loggers": {
                            "console": {"level": "DEBUG", "handlers": ["console"], "propagate": False}
                                
                    },
                    "root": {"level": "INFO", "handlers": ["console"]},
                    
        }

try:
        from local_settings import *  # noqa
except Exception as err:  # noqa
        pass


