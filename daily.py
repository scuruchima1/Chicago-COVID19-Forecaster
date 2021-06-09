# import datagather
import makesets
import forecaster
import time
time.sleep(5)
# import graphic
import config
from git import Repo

path = config.repopath
commit_message = 'New forecast'

try: 
    repo = Repo(path)
    repo.git.add(update=True)
    repo.index.commit(commit_message)
    origin = repo.remote(name = 'origin')
    origin.push()
except Exception as E:
    print('-An error occured, no code was pushed')
    print(E)