import importlib.util
import git
import os
import matplotlib.image as mpimg
import time

def get_git_root(path):
        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return git_root

root_folder=get_git_root(os.path.realpath(__file__))

spec_producer = importlib.util.spec_from_file_location(
    "producer",
    root_folder + "/src/common/rabbitmq_producer/producer.py"
)
producer = importlib.util.module_from_spec(spec_producer)
spec_producer.loader.exec_module(producer)

# Load sample image to send
img=mpimg.imread(root_folder+'/test/imgs/Lenna_(test_image).png')


p = producer.RabbitMQProducer()
for _ in range(1):
    # Create producer and send image
    time.sleep(2)
    p.send_img(img)