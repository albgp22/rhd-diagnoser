import importlib.util
import git
import os
import matplotlib.image as mpimg
import time
import sys
import numpy as np
from io import BytesIO

def get_git_root(path):
        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return git_root

root_folder=get_git_root(os.path.realpath(__file__))

spec_consumer = importlib.util.spec_from_file_location(
    "consumer",
    root_folder + "/src/common/rabbitmq_consumer/consumer.py"
)
consumer = importlib.util.module_from_spec(spec_consumer)
spec_consumer.loader.exec_module(consumer)

def custom_callback(ch, method, properties, body):
    load_bytes = BytesIO(body)
    loaded_np = np.load(load_bytes, allow_pickle=True)
    print("Image recieving worked! Exiting...")
    sys.exit(0)

# Create consumer
c = consumer.RabbitMQConsumer()
c.consume_img(custom_callback)