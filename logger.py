#!/usr/bin/env python3
import logging
from datetime import datetime
import os
import json
import curses

def setup_logger():
    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger()
    return logger

def load_logs():
    """Load logs from the JSON file."""
    if not os.path.exists("experiments.json"):
        return []
    with open("experiments.json", "r") as file:
        return json.load(file)

def save_logs(logs):
    """Save logs to the JSON file."""
    with open("experiments.json", "w") as file:
        json.dump(logs, file, indent=4)

def log_experiment(logs, title, description):
    """Log a daily experiment with a title and description."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "description": description
    }
    logs.append(entry)
    save_logs(logs)

def list_experiments(stdscr, logs):
    """List all logged experiments in the TUI."""
    stdscr.clear()
    stdscr.addstr("--- All Logged Experiments ---\n")
    if not logs:
        stdscr.addstr("No experiments logged yet.\n")
    else:
        for idx, log in enumerate(logs, start=1):
            stdscr.addstr(f"{idx}. [{log['timestamp']}] {log['title']}\n")
            stdscr.addstr(f"   {log['description']}\n\n")
    stdscr.addstr("Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()

def log_experiment_tui(stdscr, logs):
    """Log a new experiment using the TUI."""
    curses.echo()
    stdscr.clear()
    stdscr.addstr("Enter experiment title: ")
    title = stdscr.getstr().decode("utf-8")
    stdscr.addstr("Enter experiment description: ")
    description = stdscr.getstr().decode("utf-8")
    log_experiment(logs, title, description)
    stdscr.addstr("\nExperiment logged successfully! Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()

def main_tui(stdscr):
    logger = setup_logger()
    logs = load_logs()

    menu = ["Log a new experiment", "View all experiments", "Exit"]
    current_selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr("--- Experiment Logger ---\n")
        for idx, item in enumerate(menu):
            if idx == current_selection:
                stdscr.addstr(f"> {item}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {item}\n")
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(menu)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(menu)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_selection == 0:
                log_experiment_tui(stdscr, logs)
            elif current_selection == 1:
                list_experiments(stdscr, logs)
            elif current_selection == 2:
                break

if __name__ == "__main__":
    curses.wrapper(main_tui)
