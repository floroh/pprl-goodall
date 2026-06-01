#!/bin/sh
# run-goodall.sh
# Usage: ./run-goodall.sh [-d <target_dir>] <command> [args...]

# Default target directory
TARGET_DIR="/opt/pprl-goodall"

# Parse optional -d flag
while getopts "d:" opt; do
  case $opt in
    d)
      TARGET_DIR="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Shift parsed options so $@ contains the command
shift $((OPTIND - 1))

# Check that a command is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 [-d <target_dir>] <command> [args...]"
  exit 1
fi

# Change to target directory
cd "$TARGET_DIR" || {
  echo "Error: Cannot change directory to $TARGET_DIR" >&2
  exit 1
}

# Run the command
exec "$@"
