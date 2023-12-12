from src.env import main_load_env
from pytest import capsys

def test_env_default():
  main_load_env('test.env')
  out, err = capsys.readouterr()
  assert out == 'test.env not found, using ops_env.env default file\n'