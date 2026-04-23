#!/bin/sh
# Write the runtime config before nginx starts.
printf 'window.__MQTT_URL__ = "%s";\n'    "${MQTT_URL:-ws://localhost:9001}" \
  > /usr/share/nginx/html/config.js
printf 'window.__REAL_GUNS__ = "%s";\n'    "${REAL_GUNS:-}"    >> /usr/share/nginx/html/config.js
printf 'window.__REAL_MODULES__ = "%s";\n' "${REAL_MODULES:-}" >> /usr/share/nginx/html/config.js
exec nginx -g 'daemon off;'
