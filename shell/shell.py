import os, sys, re

while True:
    path = os.getcwd() + "$"

    # User input
    os.write(1, path.encode())
    inp = os.read(0, 1000).decode().split()

    # Exit
    if inp[0] == "exit":
        sys.exit(1)

    # Change Directory
    if inp[0] == "cd":
        try:
            os.chdir(inp[1])
        except FileNotFoundError:
            os.write(1, f'{inp[0]}: No such file or directory:{inp[1]}')
        continue

    rc = os.fork()
    # fork failure
    if rc < 0:
        sys.exit(1)
    # child process

    elif rc == 0:
        args = inp
        if len(args) == 3 and args[1] == ">":
            os.close(1)
            os.open(args[2], os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:
                pass
        sys.exit(1)

    # parent
    else:
        childPidCode = os.wait()