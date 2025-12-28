"""
CLI entry point for the Core CLI Todo Application.

This module sets up argparse with subcommands and dispatches to command handlers.
"""

import argparse
import sys
from src.services.task_service import TaskService
from src.cli import commands


# Module-level TaskService instance (persists during Python process)
# Note: In Phase I, this is truly in-memory - data is lost when process exits
_task_service = TaskService()


def setup_parser() -> argparse.ArgumentParser:
    """
    Set up the argument parser with subcommands.

    Returns:
        Configured ArgumentParser instance with all subcommands
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Core CLI Todo Application - Manage your tasks from the command line"
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add subcommand
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title (required)')
    add_parser.add_argument('--description', help='Task description (optional)', default='')

    # List subcommand
    list_parser = subparsers.add_parser('list', help='List all tasks')

    # Complete subcommand
    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('id', type=int, help='Task ID to mark as completed')

    # Incomplete subcommand
    incomplete_parser = subparsers.add_parser('incomplete', help='Mark a task as incomplete')
    incomplete_parser.add_argument('id', type=int, help='Task ID to mark as incomplete')

    return parser


def main():
    """
    Main entry point for the CLI application.

    Parses arguments and dispatches to appropriate command handler.
    """
    parser = setup_parser()
    args = parser.parse_args()

    # Check if a command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Use module-level TaskService (persists across commands in same process)
    # Dispatch to command handler
    if args.command == 'add':
        exit_code = commands.handle_add(args, _task_service)
    elif args.command == 'list':
        exit_code = commands.handle_list(args, _task_service)
    elif args.command == 'complete':
        exit_code = commands.handle_complete(args, _task_service)
    elif args.command == 'incomplete':
        exit_code = commands.handle_incomplete(args, _task_service)
    else:
        parser.print_help()
        exit_code = 1

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
