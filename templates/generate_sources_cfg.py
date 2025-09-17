#!/usr/bin/python3
import os
import subprocess
from datetime import datetime
import argparse
import re


def is_git_repo(path):
    """Check if a directory is a Git repository."""
    return os.path.isdir(os.path.join(path, ".git"))


def convert_to_https_url(remote_url):
    """Convert Git SSH URL to HTTPS if necessary."""
    ssh_pattern = re.compile(r"git@([^:]+):(.+)\.git")
    match = ssh_pattern.match(remote_url)
    if match:
        host, repo_path = match.groups()
        return f"https://{host}/{repo_path}.git"
    return remote_url  # Return as-is if not an SSH URL


def get_git_info(path, mode):
    """Get the Git URL and branch name or commit hash."""
    try:
        # Get the remotes list
        remotes = (
            subprocess.check_output(["git", "remote"], cwd=path, stderr=subprocess.PIPE)
            .decode("utf-8")
            .splitlines()
        )

        if not remotes:
            print(f"{path} has no remotes")
            return None, None

        remote_name = remotes[0]
        remote_url = (
            subprocess.check_output(
                ["git", "config", f"remote.{remote_name}.url"],
                cwd=path,
                stderr=subprocess.PIPE,
            )
            .decode("utf-8")
            .strip()
        )

        if mode == "prod":
            remote_url = convert_to_https_url(remote_url)
            commit_hash = (
                subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=path, stderr=subprocess.PIPE
                )
                .decode("utf-8")
                .strip()
            )
            return remote_url, commit_hash
        elif mode == "dev":
            commit_hash = (
                subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=path, stderr=subprocess.PIPE
                )
                .decode("utf-8")
                .strip()
            )

            # Get all branches containing the commit
            branches = (
                subprocess.check_output(
                    ["git", "branch", "--contains", commit_hash],
                    cwd=path,
                    stderr=subprocess.PIPE,
                )
                .decode("utf-8")
                .splitlines()
            )

            # Extract branch names
            branch_names = [
                branch.strip("* ").strip()
                for branch in branches
                if "detached" not in branch
            ]

            if not branch_names:
                print(f"{path}: No branches contain commit {commit_hash}")
                return remote_url, "HEAD"

            # Try to find a branch with the correct commit
            for branch in branch_names:
                latest_commit = (
                    subprocess.check_output(
                        ["git", "rev-list", "--max-count=1", branch],
                        cwd=path,
                        stderr=subprocess.PIPE,
                    )
                    .decode("utf-8")
                    .strip()
                )

                if latest_commit == commit_hash:
                    return remote_url, branch

            # Fallback to the current branch
            current_branch = (
                subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=path,
                    stderr=subprocess.PIPE,
                )
                .decode("utf-8")
                .strip()
            )

            return remote_url, current_branch

    except subprocess.CalledProcessError as e:
        print(f"Error accessing git in {path}: {e}")
        return None, None


def generate_cfg_file(base_path, output_file, mode):
    """Generate a configuration file with Git repository info."""
    git_entries = []
    all_subdirs = []

    for subdir in os.listdir(base_path):
        subdir_path = os.path.join(base_path, subdir)
        if os.path.isdir(subdir_path):
            all_subdirs.append(subdir)
            if is_git_repo(subdir_path):
                remote_url, identifier = get_git_info(subdir_path, mode)
                if remote_url and identifier:
                    git_entries.append((subdir, remote_url, identifier))

    git_entries.sort(key=lambda entry: entry[0])

    with open(output_file, "w") as cfg_file:
        cfg_file.write("[sources]\n")
        for subdir, remote_url, identifier in git_entries:
            if mode == "prod":
                cfg_file.write(f"{subdir} = git {remote_url} rev={identifier}\n")
            elif mode == "dev":
                cfg_file.write(f"{subdir} = git {remote_url} branch={identifier}\n")

    print(f"Configuration file generated: {output_file}")
    print(f"Total subdirectories: {len(all_subdirs)}")
    print(f"Git repositories found: {len(git_entries)}")

    if len(all_subdirs) != len(git_entries):
        print("Some subdirectories are not valid Git repositories or skipped:")
        skipped = set(all_subdirs) - set([entry[0] for entry in git_entries])
        for subdir in skipped:
            print(f"  - {subdir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a configuration file with Git repo info."
    )
    parser.add_argument(
        "--mode",
        choices=["prod", "dev"],
        default="prod",
        help="Mode of operation: 'prod' (default) or 'dev'",
    )
    parser.add_argument(
        "--base-folder",
        default="src",
        help="Base folder containing the Git repositories (default: 'src')",
    )

    args = parser.parse_args()

    now = datetime.now().strftime("%Y%m%d.%H%M")
    output_suffix = "prod" if args.mode == "prod" else "dev"
    output_cfg = f"sources.{output_suffix}.{now}.cfg"

    if os.path.isdir(args.base_folder):
        generate_cfg_file(args.base_folder, output_cfg, args.mode)
    else:
        print(f"The specified path '{args.base_folder}' is not a valid directory.")
