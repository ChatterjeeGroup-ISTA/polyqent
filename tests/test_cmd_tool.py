import subprocess

def test_cmd_tool():
    cmd = "./PolyQEnt tests/res/test_instance.smt2 tests/res/test_config.json"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out, err = out.decode('utf-8'), err.decode('utf-8')

    assert 'The system is sat' in out
    
    model = ['Model:', 'c_1: 1.0', 'c_2: (/ 2051.0 2.0)', 'c_3: 0.0', 'c_4: (/ 1.0 2.0)']
    for line in model:
        assert line in out
    
    assert err == ''
    
    assert process.returncode == 0
    
    
    
test_cmd_tool()