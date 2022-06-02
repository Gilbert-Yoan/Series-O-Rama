from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import os
import shutil

scheduler = BlockingScheduler()

def refresh_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    python_target = os.path.join(curr_dir,"..","preprocessing", "preprocessing_chargementBDD.py")
    source_path = os.path.join(curr_dir,"..","..","DELTA")
    #print("python ",python_target, source_path)
    #Execution fouille
    subprocess.run(["python",python_target,source_path],shell=True)
    #Suppression delta après execution
    shutil.rmtree(source_path)

scheduler.add_job(refresh_data, 'cron', hour=0, minute=1)
scheduler.start()