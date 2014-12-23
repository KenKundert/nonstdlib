
class Execute():
    def __init__(
        self, cmd, accept=(0,), stdin=None, stdout=True, stderr=True, wait=True, 
        shell=False, showCmd=False
    ):
        """
        Execute a command and capture its output.

        cmd may be a list of strings (preferred) or a string. Ex: ['rm' '-f' 
        'core'] or 'rm -f core'.

        Raise an ExecuteError if return status is not in accept unless accept
        is set to True. By default, only a status of 0 is accepted.

        If stdin is None, no connection is made to the standard input, otherwise 
        stdin is expected to be a string and that string is sent to stdin.

        If stdout / stderr is true, stdout / stderr is captured and made 
        available from self.stdout / self.stderr.

        If wait is true, the run method does not return until the process ends.  
        In this case run() returns the status. Otherwise it return None and 
        instead calling wait() waits for the process to end and returns the 
        status.  Once wait() returns, either by calling constructor with 
        wait=True, or by calling wait(), the status is also available from 
        self.status,

        The default is to not use a shell to execute a command (safer).
        """
        self.cmd = cmd
        self.accept = accept
        self.save_stdout = stdout
        self.save_stderr = stderr
        self.wait_for_termination = wait
        self.showCmd = showCmd
        self._run(stdin, shell)

    def _run(self, stdin, shell):
        import subprocess
        streams = {}
        if stdin is not None:
            streams['stdin'] = subprocess.PIPE
        if self.save_stdout:
            streams['stdout'] = subprocess.PIPE
        if self.save_stderr:
            streams['stderr'] = subprocess.PIPE
        try:
            process = subprocess.Popen(
                self.cmd, shell=shell, **streams
            )
        except (IOError, OSError) as err:
            raise ExecuteError(self.cmd, err.filename, err.strerror)
        if stdin is not None:
            process.stdin.write(stdin.encode('utf-8'))
            process.stdin.close()
        self.pid = process.pid
        self.process = process
        if self.wait_for_termination:
            return self.wait()

    def wait(self):
        if self.save_stdout:
            self.stdout = self.process.stdout.read().decode('utf-8')
        else:
             self.stderr = None
        if self.save_stderr:
            self.stderr = self.process.stderr.read().decode('utf-8')
        else:
             self.stderr = None
        self.status = self.process.wait()
        self.process.stdout.close()
        self.process.stderr.close()
        if self.accept is not True and self.status not in self.accept:
            if self.stderr:
                raise ExecuteError(self.cmd, self.stderr, showCmd=self.showCmd)
            else:
                raise ExecuteError(
                    self.cmd,
                    "unexpected exit status (%d)." % self.status,
                    showCmd=self.showCmd)
        return self.status


class ShellExecute(Execute):
    def __init__(
        self, cmd, accept=(0,), stdin=None, stdout=True, stderr=True, wait=True, 
        shell=True, showCmd=False
    ):
        """
        Execute a command in a shell and capture its output

        This class is the same as Execute, except that by default it runs the 
        given command in a shell, which is less safe but often more convenient.
        """
        self.cmd = cmd
        self.accept = accept
        self.save_stdout = stdout
        self.save_stderr = stderr
        self.wait_for_termination = wait
        self.showCmd = showCmd
        self._run(stdin, True)


def execute(cmd, accept=(0,), stdin=None, shell=False):
    """
    Execute a command without capturing its output

    Raise an ExecuteError if return status is not in accept unless accept
    is set to True. By default, only a status of 0 is accepted. The default is 
    to not use a shell to execute a command (safer).
    If stdin is None, no connection is made to the standard input, otherwise 
    stdin is expected to be a string.
    """
    import subprocess
    streams = {'stdin': subprocess.PIPE} if stdin is not None else {}
    try:
        process = subprocess.Popen(cmd, shell=shell, **streams)
    except (IOError, OSError) as err:
        raise ExecuteError(cmd, err.filename, err.strerror)
    if stdin is not None:
        process.stdin.write(stdin.encode('utf-8'))
        process.stdin.close()
    status = process.wait()
    if accept is not True and status not in accept:
        raise ExecuteError(
            cmd,
            "unexpected exit status (%d)." % status,
            showCmd='brief'
        )
    return status

def shell_execute(cmd, accept=(0,), stdin=None, shell=True):
    """
    Execute a command without capturing its output

    Raise an ExecuteError if return status is not in accept unless accept
    is set to True. By default, only a status of 0 is accepted. The default is 
    to use a shell to execute a command (more convenient).
    """
    return execute(cmd, accept, stdin, shell=True)


def execute_bkgnd(cmd, stdin=None, shell=False):
    """
    Execute a command in the background without capturing its output.

    If stdin is None, no connection is made to the standard input, otherwise 
    stdin is expected to be a string.
    """
    import subprocess
    streams = {'stdin': subprocess.PIPE} if stdin is not None else {}
    try:
        process = subprocess.Popen(cmd, shell=shell, **streams)
    except (IOError, OSError) as err:
        raise ExecuteError(cmd, err.filename, err.strerror)
    if stdin is not None:
        process.stdin.write(stdin.encode('utf-8'))
        process.stdin.close()
    return process.pid


def shell_execute_bkgnd(cmd, stdin=None, shell=True):
    """
    Execute a command in the background without capturing its output.

    If stdin is None, no connection is made to the standard input, otherwise 
    stdin is expected to be a string.

    The default is to use a shell to execute a command (more convenient).
    """
    return execute_bkgnd(cmd, stdin, shell)

