import os, sys, re

while True:
    path = os.getcwd() + " $"

    # User input
    os.write(1, path.encode())
    args = os.read(0, 1000).decode().split()

    # Exit
    if args[0] == "exit":
        if len(args) > 1:
            print("Program terminated with exit code", args[1])
            sys.exit(int(args[1]))
        print("Program terminated with exit code")
        sys.exit(1)

    # Change Directory
    if args[0] == "cd":
        try:
            os.chdir(args[1])
        except FileNotFoundError:
            os.write(1, f'{args[0]}: No such file or directory:{args[1]}')
        continue

    rc = os.fork()

    # fork failure
    if rc < 0:
        os.write(1, "Fork failure :( !")
        sys.exit(1)

    # child process
    elif rc == 0:

        # redirect
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

        else:
            os.write(1, 'Command not found')

    # parent
    else:
        childPidCode = os.wait()