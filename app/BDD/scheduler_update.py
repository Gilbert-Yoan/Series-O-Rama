from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import os

scheduler = BlockingScheduler()

def refresh_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    python_target = os.path.join(curr_dir,"..","preprocessing", "preprocessing_chargementBDD.py")
    source_path = os.path.join(curr_dir,"..","delta")
    #print("python ",python_target, source_path)
    subprocess.run(["python",python_target,source_path],shell=True)

scheduler.add_job(refresh_data, 'interval', seconds=5)
scheduler.start()