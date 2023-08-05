from subprocess import Popen, PIPE, STDOUT
import os

class pySh(str):
    """
    Please see the distribution README for how to use pySh()
    """
    stdout = None
    stderr = None
    returncode = None
    merge_output = False

    def __getattr__(self, item):
        if self.is_executable(item):
            return lambda *a: self.run(item, *a)
        else:
            self.raise_not_found(item)


    @staticmethod
    def raise_not_found(item):


            # The executable requested doesn't exist in PATH
            raise AttributeError("'{}' could not be located in the system. "
                                 "Please try entering the full path and verify it is executable.".format(item))


    def is_executable(self, cmd):
        """
        Look for a command and verify it is executable by the current user
        Returns the full path if found, None if not
        """
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        if is_exe(cmd):
            return cmd

        cwdpath = os.path.join(os.getcwd(), cmd)
        if is_exe(cwdpath):
            return cwdpath

        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, cmd)
            if is_exe(exe_file):
                return exe_file
        return None

    @staticmethod
    def cast(instance):
        if type(instance) is list:
            return list([pySh(i) for i in instance])
        elif type(instance) is set:
            return set([pySh(i) for i in instance])
        else:
            return pySh(instance)


    def run(self, command, *args):
        """
        pySh main run function
        The first argument is the command name, evaluated by pySh.is_executable()
        Any additional arguments are passed to the command

        The string representation of pySh is used as the stdin for the command

        Returns a pySh instance of the command output
        """

        # Verify the command is executable
        exe = self.is_executable(command)
        if exe is None:
            self.raise_not_found(command)




        # Construct the command arguments
        cmd = [exe]
        cmd.extend([str(a) for a in args])

        # Run the command, with KeyboardInterrupt trap
        # If merge_output is true set stderr to the stdout PIPE
        if self.merge_output:
            stderr_out = STDOUT
        else:
            stderr_out = PIPE

        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=stderr_out, close_fds=True)
        try:
            stdout, stderr = p.communicate(input=str(self).encode())
        except KeyboardInterrupt:
            p.terminate()
            stdout, stderr = '', ''

        if stderr is not None:
            stderr = stderr.decode().strip()
        if stdout is not None:
            stdout = stdout.decode().strip()

        # Create the output instance and set its variables
        pipe_out = pySh(stdout)
        pipe_out.stdout = pySh(stdout)
        if stderr is not None:
            pipe_out.stderr = pySh(stderr)
        pipe_out.returncode = p.returncode
        pipe_out.merge_output = self.merge_output

        # Return the new pySh instance
        return pipe_out


