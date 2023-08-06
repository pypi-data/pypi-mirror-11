import sys
import subprocess


def execute_command(cmd, work_dir, stdin, stdout, stderr):
    """
    Execute external command

    :param cmd: command line string
    :param work_dir: working directory
    :param stdin: standard input
    :param stdout: standard output
    :param stderr: standard error
    :return: return code
    """
    try:
        ret_code = subprocess.call(
            cmd,
            shell=True,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            cwd=work_dir,
        )
    except KeyboardInterrupt:
        ret_code = 130

    return ret_code


def capture_command(cmd, work_dir, stdin=sys.stdin):
    """
    Execute external command and capture output

    :param cmd: command line string
    :param work_dir: working directory
    :param stdin: standard input
    :return: tuple of return code, stdout data and stderr data
    """
    stdout_data, stderr_data = None, None

    try:
        p = subprocess.Popen(
            cmd,
            shell=True,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=work_dir
        )
        stdout_data, stderr_data = p.communicate()
        ret_code = p.returncode
    except KeyboardInterrupt:
        ret_code = 130

    return ret_code, stdout_data, stderr_data
