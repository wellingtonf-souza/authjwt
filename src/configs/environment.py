from dotenv import load_dotenv
import os
load_dotenv()

environment_config = {
    'key':  os.getenv('KEY'), 
    'exp_time': int(os.getenv('EXP_TIME'))
}