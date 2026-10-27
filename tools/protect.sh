#!/usr/bin/env bash
# Password-protects every built page in docs/ with StatiCrypt (AES-256, client-side).
# Usage:  STATICRYPT_PASSWORD='...' tools/protect.sh      (run after: python3 build.py)
# The password is never stored in the repo. The salt in tools/.staticrypt.json is not secret;
# keeping it fixed lets "Remember me" work across all pages and survive rebuilds.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${STATICRYPT_PASSWORD:?Set STATICRYPT_PASSWORD first}"
npx --yes staticrypt@3.5.4 docs/*.html -d docs \
  --config tools/.staticrypt.json \
  --template tools/password_template.html \
  --remember 30 \
  --template-color-primary "#0E3727" --template-color-secondary "#8FDB6A" \
  --template-title "Staging preview" \
  --template-instructions "This is the private staging site for Procure &amp; Supply by Nomni. Enter the password you were given." \
  --template-placeholder "Password" \
  --template-button "Open the site" \
  --template-remember "Remember me on this device for 30 days" \
  --template-error "That password didn't work. Try again." \
  --template-toggle-show "Show password" --template-toggle-hide "Hide password" \
  --short
printf "User-agent: *\nDisallow: /\n" > docs/robots.txt
echo "Protected: $(ls docs/*.html | wc -l) pages"
