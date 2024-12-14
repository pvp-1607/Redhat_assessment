import subprocess
import os
import pytest
import re

SAMPLE_LOG = "tests/sample_logs/sample.log"

def strip_ansi(text):
    """Remove ANSI escape sequences from the given text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def test_help_option():
    result = subprocess.run(["python", "util.py", "--help"], capture_output=True, text=True)
    assert "usage" in result.stdout

def test_first_lines():
    result = subprocess.run(["python", "util.py", "-f", "2", SAMPLE_LOG], capture_output=True, text=True)
    assert len(result.stdout.splitlines()) == 2

def test_last_lines():
    result = subprocess.run(["python", "util.py", "-l", "2", SAMPLE_LOG], capture_output=True, text=True)
    assert len(result.stdout.splitlines()) == 2

def test_timestamps():
    result = subprocess.run(["python", "util.py", "--timestamps", SAMPLE_LOG], capture_output=True, text=True)
    assert "12:34:56" in result.stdout

def test_ipv4():
    result = subprocess.run(["python", "util.py", "--ipv4", SAMPLE_LOG], capture_output=True, text=True)
    assert "192.168.1.1" in result.stdout

def test_ipv6():
    result = subprocess.run(["python", "util.py", "--ipv6", SAMPLE_LOG], capture_output=True, text=True)
    clean_output = strip_ansi(result.stdout)  # Strip ANSI escape sequences
    assert "2001:0db8::1" in clean_output
