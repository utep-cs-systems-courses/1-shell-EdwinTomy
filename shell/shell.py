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
        print("Program terminated without exit code")
        sys.exit(1)

    # Change Directory
    if args[0] == "cd":
        try:
            if len(args) < 2:
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(args[1])
        except FileNotFoundError:
            print("File not found!")
            pass
        continue

    # Forking
    rc = os.fork()
    if rc < 0:
        os.write(1, "Fork failure :( !")
        sys.exit(1)

    # Child process for redirect & piping
    elif rc == 0:

        # Redirect output
        if '>' in args:
            i = args.index('>')
            os.close(1)
            os.open(args[i+1], os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
            child_command = args[:i]

        # Redirect output
        elif '<' in args:
            i = args.index('<')
            os.close(1)
            os.open(args[i + 1], os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
            child_command = args[:i]

        # Piping
        elif '|' in args:
            i = args.index('|')
            pipe1 = args[:i]
            pipe2 = args[(i + 1):]

            pr, pw = os.pipe()
            os.set_inheritable(pr, True)
            os.set_inheritable(pw, True)
            pipe_child = os.fork()

            if pipe_child < 0:
                sys.exit(1)

            if pipe_child == 0:
                os.close(1)
                os.dup(pw)
                os.set_inheritable(1, True)

                os.close(pr)
                os.close(pw)

                child_command = pipe1

            else:
                os.close(0)
                os.dup(pr)
                os.set_inheritable(0, True)

                os.close(pr)
                os.close(pw)

                child_command = pipe2

        # Command not found
        else:
            print("Command not found")
            sys.exit(1)

        # Try each directory in path
        for directory in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (directory, args[0])
            try:
                os.execve(program, child_command, os.environ)
            except FileNotFoundError:
                pass
        sys.exit(1)

    # Check for background processes
    else:
        childPidCode = os.wait()
