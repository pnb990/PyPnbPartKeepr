#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

# This script fixes Git worktree configuration inside a devcontainer.
# It detects if the workspace is a worktree and sets GIT_COMMON_DIR, GIT_DIR, GIT_WORK_TREE accordingly.
# Requires the master repo to be mounted at /home/dev/master.

set -e

echo "[devcontainer] Vérification Git / worktree..."

WORKSPACE="/home/dev/project"
GIT_FILE="$WORKSPACE/.git"
MASTER_MOUNT="/home/dev/master"

# 1) Check .git existence
if [ ! -e "$GIT_FILE" ]; then
    echo "[devcontainer] Pas de .git -> pas un repo Git."
    exit 0
fi

# 2) If .git is a directory → not a worktree
if [ -d "$GIT_FILE" ]; then
    echo "[devcontainer] Repo principal détecté → aucune action."
    exit 0
fi

# 3) Extract gitdir (host path)
GITDIR_HOST=$(sed -n 's/gitdir: //p' "$GIT_FILE")
echo "[devcontainer] Worktree détecté."
echo "[devcontainer] gitdir host = $GITDIR_HOST"

# 4) Extract master repo path (host) and worktree name (git)
MASTER_HOST=$(printf "%s\n" "$GITDIR_HOST" | sed -E 's|(.*)/\.git/worktrees/[^/]+|\1|')
WORKTREE_NAME=$(printf "%s\n" "$GITDIR_HOST" | sed -E 's|.*/\.git/worktrees/([^/]+)|\1|')

echo "[devcontainer] master host path = $MASTER_HOST"
echo "[devcontainer] worktree name    = $WORKTREE_NAME"

# 5) Check if master is mounted
if [ ! -d "$MASTER_MOUNT/.git" ]; then
    echo "[devcontainer] ⚠️ Master seems not mounted in $MASTER_MOUNT"
    echo "[devcontainer] (normal if you work in the master or without worktrees)"
    echo "[devcontainer] May need to add this mount in your devcontainer.json \"mounts\" section:"
    echo "[devcontainer] \"source=\${localWorkspaceFolder}/../master,target=/home/dev/master,type=bind\""
    exit 0
fi

# 6) Set Git variables
export GIT_COMMON_DIR="$MASTER_MOUNT/.git"
export GIT_DIR="$MASTER_MOUNT/.git/worktrees/$WORKTREE_NAME"
export GIT_WORK_TREE="$WORKSPACE"

echo "[devcontainer] Git configured for worktree:"
echo "  GIT_COMMON_DIR=$GIT_COMMON_DIR"
echo "  GIT_DIR=$GIT_DIR"
echo "  GIT_WORK_TREE=$GIT_WORK_TREE"

# Inject into ~/.bashrc for new interactive shells
{
    echo "export GIT_COMMON_DIR=$GIT_COMMON_DIR"
    echo "export GIT_DIR=$GIT_DIR"
    echo "export GIT_WORK_TREE=$GIT_WORK_TREE"
} >> /home/dev/.bashrc

echo "[devcontainer] ✔️ Worktree configuration completed."
