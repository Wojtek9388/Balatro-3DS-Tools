import subprocess

def RunBatch(Path=None, Input=None, **kwargs):
    if Path is None:
        print("Warning: Invalid use of RunBatch - Path is required.")
        return -1

    # Start with the batch file path
    Cmd = [Path]

    # Add input argument if provided
    if Input:
        Cmd += ["--file", Input]
    else:
        pass

    # Add other --key value arguments from kwargs
    for Key, Value in kwargs.items():
        Cmd.append(f"--{Key}")
        if Value is not None:
            Cmd.append(str(Value))

    Output = subprocess.run(
        Cmd,
        shell=True,
        capture_output=True,
        text=True
    )


    return 


def CompressAudio(File):
    RunBatch("BatchTools\\AudioCompresser.bat", File)
    
    return 0