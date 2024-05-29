from subprocess import PIPE, Popen

def execute_open_reac():
    p = Popen(["ampl", "reactiveopf.run"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    p.wait()
    return p