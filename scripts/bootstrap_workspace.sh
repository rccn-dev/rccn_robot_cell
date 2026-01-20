#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

REPOS_FILE_DEFAULT="${WORKSPACE_DIR}/rccn_robot_cell.repos"

SKIP_VCS=0
SKIP_ROSDEP=0
SKIP_BUILD=0

usage() {
  cat <<'EOF'
Usage: scripts/bootstrap_workspace.sh [options]

Bootstraps this workspace for development:
  - imports source-only deps via vcstool (.repos)
  - installs system deps via rosdep
  - builds via colcon

Options:
  --skip-vcs        Do not run vcs import
  --skip-rosdep     Do not run rosdep install
  --skip-build      Do not run colcon build
  --repos <path>    Path to a .repos file (default: rccn_robot_cell.repos)
EOF
}

REPOS_FILE="${REPOS_FILE_DEFAULT}"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-vcs) SKIP_VCS=1; shift ;;
    --skip-rosdep) SKIP_ROSDEP=1; shift ;;
    --skip-build) SKIP_BUILD=1; shift ;;
    --repos)
      REPOS_FILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

cd "${WORKSPACE_DIR}"

if [[ ! -f "cyclonedds.xml" && -f "cyclonedds.xml.template" ]]; then
  echo "Creating cyclonedds.xml from template..."
  cp cyclonedds.xml.template cyclonedds.xml
fi

# Ensure ROS environment is sourced (helps rosdep pick ROS_DISTRO + colcon find packages)
if [[ -z "${ROS_DISTRO:-}" ]]; then
  if [[ -d /opt/ros/humble ]]; then
    # Prefer humble if present
    set +u
    source /opt/ros/humble/setup.bash
    set -u
  elif [[ -d /opt/ros/jazzy ]]; then
    set +u
    source /opt/ros/jazzy/setup.bash
    set -u
  else
    echo "ROS_DISTRO not set and /opt/ros/<distro> not found." >&2
    echo "Source your ROS 2 setup.bash first." >&2
    exit 1
  fi
else
  if [[ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]]; then
    # shellcheck disable=SC1090
    set +u
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
    set -u
  fi
fi

if [[ ${SKIP_VCS} -eq 0 ]]; then
  if ! command -v vcs >/dev/null 2>&1; then
    echo "vcstool is not installed (missing 'vcs')." >&2
    echo "Install it (Ubuntu/Debian): sudo apt-get install -y python3-vcstool" >&2
    exit 1
  fi

  mkdir -p src

  if [[ -f "${REPOS_FILE}" ]]; then
    # Only import if repo isn't already present, to keep re-runs fast and non-destructive.
    if [[ ! -d "src/kuka_kr300_support" ]]; then
      echo "Importing source dependencies from ${REPOS_FILE} ..."
      vcs import src < "${REPOS_FILE}"
    else
      echo "src/kuka_kr300_support already exists; skipping vcs import."
    fi
  else
    echo "No .repos file found at ${REPOS_FILE}; skipping vcs import."
    echo "(If you need source-only deps, add a .repos file and rerun.)"
  fi
fi

if [[ ${SKIP_ROSDEP} -eq 0 ]]; then
  if ! command -v rosdep >/dev/null 2>&1; then
    echo "rosdep is not installed (missing 'rosdep')." >&2
    echo "Install it (Ubuntu/Debian): sudo apt-get install -y python3-rosdep" >&2
    exit 1
  fi

  # rosdep init requires root and is safe to re-run.
  if command -v sudo >/dev/null 2>&1; then
    sudo rosdep init >/dev/null 2>&1 || true
    rosdep update
  else
    rosdep init >/dev/null 2>&1 || true
    rosdep update
  fi

  echo "Installing system dependencies via rosdep ..."
  # Default to ROS 2 packages only (robot_description + src overlay).
  # moveit_config/ currently contains ROS 1 catkin packages, which will not resolve cleanly in ROS 2.
  ROSDEP_PATHS=()
  for candidate in robot_description src; do
    if [[ -d "${candidate}" ]]; then
      ROSDEP_PATHS+=("${candidate}")
    fi
  done

  if [[ ${#ROSDEP_PATHS[@]} -eq 0 ]]; then
    echo "No package paths found to pass to rosdep (expected robot_description/, moveit_config/, and/or src/)." >&2
    exit 1
  fi

  rosdep install --from-paths "${ROSDEP_PATHS[@]}" -y --ignore-src
fi

if [[ ${SKIP_BUILD} -eq 0 ]]; then
  if ! command -v colcon >/dev/null 2>&1; then
    echo "colcon is not installed (missing 'colcon')." >&2
    echo "Install it (Ubuntu/Debian): sudo apt-get install -y python3-colcon-common-extensions" >&2
    exit 1
  fi

  echo "Building workspace (colcon) ..."
  # Limit to ROS 2 packages; see note above about moveit_config/ being catkin.
  colcon build --symlink-install --base-paths robot_description src

  echo
  echo "Done. In your current shell, run:"
  echo "  source install/setup.bash"
fi
