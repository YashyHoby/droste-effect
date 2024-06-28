
def handle_error_and_exit(text, flag=False):
    import sys
    if not flag:
        print(str(text))
        sys.exit(1)
    else:
        return True