from __future__ import annotations

import builtins
import getpass
from pathlib import Path
import sys

from main import main


def simulate_input_file(path: str):
    lines = [l.rstrip('\n') for l in Path(path).read_text(encoding='utf-8').splitlines()]
    it = iter(lines)

    def fake_input(prompt: str = '') -> str:
        try:
            val = next(it)
            print(f"{prompt}{val}")
            return val
        except StopIteration:
            raise EOFError("No more simulated input")

    def fake_getpass(prompt: str = '') -> str:
        try:
            val = next(it)
            print(f"{prompt}********")
            return val
        except StopIteration:
            raise EOFError("No more simulated input")

    return fake_input, fake_getpass


if __name__ == '__main__':
    # choose which sequence file to run; default runs admin then user
    seq_admin = 'cli_inputs_admin.txt'
    seq_user = 'cli_inputs_user.txt'

    # Run admin flow
    fi, fg = simulate_input_file(seq_admin)
    orig_input = builtins.input
    orig_getpass = getpass.getpass
    try:
        builtins.input = fi
        getpass.getpass = fg
        print('--- RUNNING ADMIN FLOW ---')
        main()
    except Exception as e:
        print('Error during admin flow:', e)
    finally:
        builtins.input = orig_input
        getpass.getpass = orig_getpass

    # Run user flow
    fi, fg = simulate_input_file(seq_user)
    try:
        builtins.input = fi
        getpass.getpass = fg
        print('\n--- RUNNING USER FLOW ---')
        main()
    except Exception as e:
        print('Error during user flow:', e)
    finally:
        builtins.input = orig_input
        getpass.getpass = orig_getpass

    print('\n--- SIMULATION COMPLETE ---')
