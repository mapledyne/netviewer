#!/usr/bin/env python3
"""
Simple script to run the NetViewer application directly
"""
import sys

# Force output to be unbuffered
sys.stdout = open(sys.stdout.fileno(), mode=sys.stdout.mode, buffering=1)

try:
    from netviewer import __version__
    print(
        f"Starting NetViewer application (version {__version__})...",
        flush=True
    )
except ImportError:
    print("Starting NetViewer application...", flush=True)

try:
    from netviewer.app import main
    main()
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1) 