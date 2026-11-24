#!/bin/sh
# Chạy crawler trên HOST dưới dạng dịch vụ user tạm thời của systemd, có giới hạn RAM cứng (vượt thì chỉ crawler bị giết).
# Dùng: sh code/crawl/run.sh <unit> <sites.tsv> <out_dir> [tham số crawl.cjs...]   → log: <out_dir>.log ; trả về ngay
# Xem: flatpak-spawn --host systemctl --user status <unit> ; dừng: flatpak-spawn --host systemctl --user stop <unit>
# Ghim: Playwright 1.66.0-alpha-2026-11-09 (npx cache), Chrome for Testing 153.0.8010.12 (ms-playwright chromium-1243)
cd "$(dirname "$0")/../.." || exit 1
UNIT=$1; shift; SITES=$1; OUTD=$2
mkdir -p "$OUTD"
exec flatpak-spawn --host systemd-run --user --unit="$UNIT" --collect --quiet \
  -p MemoryMax="${MEM_MAX:-2200M}" -p MemorySwapMax=0 -p Restart=on-failure -p RestartSec=10 \
  -p StandardOutput=append:"$PWD/$OUTD.log" -p StandardError=append:"$PWD/$OUTD.log" \
  --setenv=PW_DIR="$HOME/.npm/_npx/9833c18b2d85bc59" --setenv=CHROME="$HOME/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome" \
  --setenv=HB_EVERY="${HB_EVERY:-60}" --setenv=MIN_FREE_MB="${MIN_FREE_MB:-700}" \
  /usr/bin/node "$PWD/code/crawl/crawl.cjs" "$PWD/$SITES" "$PWD/$OUTD" $(shift 2; echo "$@")
