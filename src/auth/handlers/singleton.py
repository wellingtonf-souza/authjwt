from cmath import exp
from .creator import TokenCreator
from src.configs import environment_config
import os

token_creator = TokenCreator(
    key =  environment_config['key'], 
    exp_time = environment_config['exp_time']
)