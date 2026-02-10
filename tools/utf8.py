import sys

def enable_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except:
        pass
