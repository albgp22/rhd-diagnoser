import git
import importlib
import os

def get_git_root(path):
        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")
        return git_root

root_folder=get_git_root(os.path.realpath(__file__))

spec_client = importlib.util.spec_from_file_location(
    "consumer",
    root_folder + "/src/common/minio_client/client.py"
)
client = importlib.util.module_from_spec(spec_client)
spec_client.loader.exec_module(client)

c = client.MinioClient()