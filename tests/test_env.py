from src.env import main_load_env
import pytest

def test_env_default(capsys):
  main_load_env('test.env')
  out = capsys.readouterr()
  assert out == 'test.env not found, using ops_env.env default file\n'