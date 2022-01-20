from os import path

from dotenv import load_dotenv

current_dir = path.abspath(path.curdir)
env_file = path.join(current_dir, '.env')
load_dotenv(env_file)
