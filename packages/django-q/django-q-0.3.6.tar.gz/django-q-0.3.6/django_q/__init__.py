import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)

from .tasks import async, schedule, result, fetch
from .models import Task, Schedule, Success, Failure
from .cluster import Cluster

VERSION = (0, 3, 6)

default_app_config = 'django_q.apps.DjangoQConfig'
