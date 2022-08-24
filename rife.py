#!/usr/bin/env python3

from __future__ import annotations

import errno
import os
import sys
from src.console.print import print_error
import src.error
from src.parse import __main__


def main():
    try:
        
        __main__()
    except KeyboardInterrupt :
        print_error("\nInterrupted by user")
    except BrokenPipeError:
        print_error("\nBroken pipe")
    except PermissionError:
        print_error("\nPermission denied")
    except src.error.CantidateNotFoundError as e:
        print_error(f'Installation cantidate Not Found : {e}')
    
    except OSError as e:
        if e.errno == errno.ENOSPC:
            print_error("Run Out of Space")
        else:
            print_error(e)
            sys.exit(1)
    finally:
        os.system("pyclean")

if __name__ == "__main__":
    main()
