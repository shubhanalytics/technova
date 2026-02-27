import subprocess
import sys

def test_security_checks():
    res = subprocess.run([sys.executable, 'scripts/security_checks.py'], capture_output=True, text=True)
    print(res.stdout)
    assert res.returncode == 0
