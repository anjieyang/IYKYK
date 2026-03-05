#!/usr/bin/env bash
# UncommonRoute — One-line installer
#
# Usage:
#   curl -fsSL https://anjieyang.github.io/uncommon-route/install | bash
#   curl -fsSL https://anjieyang.github.io/uncommon-route/install | bash -s -- --openclaw
#
# Options:
#   --openclaw    Also register as an OpenClaw provider
#   --port N      Proxy port (default: 8403)
#   --no-serve    Install only, don't start the proxy
#
set -euo pipefail

VERSION="0.1.0"
PACKAGE="uncommon-route"
DEFAULT_PORT=8403
INSTALL_OPENCLAW=false
START_SERVE=true
PORT=$DEFAULT_PORT

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

log()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
err()   { echo -e "${RED}[✗]${NC} $1"; }
info()  { echo -e "${BLUE}[i]${NC} $1"; }
header(){ echo -e "\n${BOLD}$1${NC}"; }

# ── Parse args ────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --openclaw)   INSTALL_OPENCLAW=true; shift ;;
    --port)       PORT="$2"; shift 2 ;;
    --no-serve)   START_SERVE=false; shift ;;
    -h|--help)
      echo "Usage: curl -fsSL https://anjieyang.github.io/uncommon-route/install | bash"
      echo "  --openclaw    Register as OpenClaw provider"
      echo "  --port N      Proxy port (default: 8403)"
      echo "  --no-serve    Don't start proxy after install"
      exit 0 ;;
    *) shift ;;
  esac
done

# ── Banner ────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}  UncommonRoute v${VERSION}${NC}"
echo -e "  SOTA LLM Router — 98% accuracy, <1ms local routing"
echo ""

# ── Step 1: Check Python ─────────────────────────────────────────────

header "Checking Python..."

PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" &>/dev/null; then
    ver=$("$candidate" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    if [[ "$major" -ge 3 && "$minor" -ge 11 ]]; then
      PYTHON="$candidate"
      log "Found $candidate ($ver)"
      break
    else
      warn "$candidate is $ver (need 3.11+)"
    fi
  fi
done

if [[ -z "$PYTHON" ]]; then
  err "Python 3.11+ not found"
  info "Install Python first:"
  case "$(uname -s)" in
    Darwin)
      info "  brew install python@3.12"
      if command -v brew &>/dev/null; then
        read -p "  Install now with brew? [Y/n] " -r answer
        if [[ "${answer:-Y}" =~ ^[Yy]$ ]]; then
          brew install python@3.12
          PYTHON="python3"
        fi
      fi
      ;;
    Linux)
      info "  Ubuntu/Debian: sudo apt install python3.12 python3.12-venv"
      info "  Fedora:        sudo dnf install python3.12"
      ;;
  esac
  if [[ -z "$PYTHON" ]]; then
    err "Cannot proceed without Python 3.11+"
    exit 1
  fi
fi

# ── Step 2: Install package ──────────────────────────────────────────

header "Installing $PACKAGE..."

INSTALLED=false

# Try pipx first (cleanest)
if command -v pipx &>/dev/null; then
  if pipx install "$PACKAGE" 2>/dev/null; then
    log "Installed via pipx"
    INSTALLED=true
  fi
fi

# Try uv
if [[ "$INSTALLED" == false ]] && command -v uv &>/dev/null; then
  if uv pip install "$PACKAGE" 2>/dev/null; then
    log "Installed via uv"
    INSTALLED=true
  fi
fi

# Fall back to pip --user
if [[ "$INSTALLED" == false ]]; then
  if $PYTHON -m pip install "$PACKAGE" --user --quiet 2>/dev/null; then
    log "Installed via pip"
    INSTALLED=true
  elif $PYTHON -m pip install "$PACKAGE" --user --break-system-packages --quiet 2>/dev/null; then
    log "Installed via pip (system override)"
    INSTALLED=true
  fi
fi

if [[ "$INSTALLED" == false ]]; then
  err "Failed to install $PACKAGE"
  info "Try manually: pip install $PACKAGE"
  exit 1
fi

# Verify
if command -v uncommon-route &>/dev/null; then
  log "CLI available: $(uncommon-route --version)"
else
  warn "CLI not on PATH — you may need to add ~/.local/bin to PATH"
  info "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# ── Step 3: OpenClaw integration (optional) ──────────────────────────

if [[ "$INSTALL_OPENCLAW" == true ]]; then
  header "Registering with OpenClaw..."
  if command -v openclaw &>/dev/null; then
    info "OpenClaw found — installing JS bridge plugin..."
    if openclaw plugins install @anjieyang/uncommon-route 2>/dev/null; then
      log "JS bridge plugin installed (auto-manages proxy lifecycle)"
    else
      warn "Plugin install failed — falling back to config patch"
      uncommon-route openclaw install --port "$PORT" 2>/dev/null && log "Config patch applied" || warn "Config patch failed"
    fi
  else
    info "OpenClaw not found — applying config patch"
    uncommon-route openclaw install --port "$PORT" 2>/dev/null && log "Config patch applied" || warn "Skipped"
  fi
fi

# ── Step 4: Start proxy (optional) ──────────────────────────────────

if [[ "$START_SERVE" == true ]]; then
  header "Starting proxy..."
  info "Port: $PORT"
  echo ""
  uncommon-route serve --port "$PORT" &
  PROXY_PID=$!
  sleep 2

  if kill -0 $PROXY_PID 2>/dev/null; then
    log "Proxy running (PID $PROXY_PID)"
  else
    warn "Proxy may have failed to start"
  fi
fi

# ── Done ─────────────────────────────────────────────────────────────

header "Setup complete!"
echo ""
echo -e "  ${BOLD}Quick start:${NC}"
echo "    uncommon-route route \"what is 2+2\"          # Route a prompt"
echo "    uncommon-route serve --port $PORT             # Start proxy"
echo "    uncommon-route spend set hourly 5.00          # Set spend limit"
echo "    uncommon-route openclaw status                # Check OpenClaw"
echo ""
echo -e "  ${BOLD}Use with any OpenAI client:${NC}"
echo "    export OPENAI_BASE_URL=http://127.0.0.1:$PORT/v1"
echo "    export OPENAI_API_KEY=your-upstream-key"
echo ""
echo -e "  ${BOLD}Docs:${NC} https://github.com/anjieyang/UncommonRoute"
echo ""
