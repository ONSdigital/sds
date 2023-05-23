import os

import firebase_admin
from config.config_factory import ConfigFactory
from firebase_admin import _apps, firestore
from google.cloud import firestore as gfs

config = ConfigFactory.get_config()


def __get_db():
    if config.CONF == "unit":
        if not _apps:
            firebase_admin.initialize_app()

        __db = firestore.client()
    else:
        __db = gfs.Client(project=config.PROJECT_ID)
    return __db


db = __get_db()
