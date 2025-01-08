FROM fluent/fluent-bit:1.9

# Copy configuration files
COPY config/fluent-bit.conf /fluent-bit/etc/fluent-bit.conf
COPY config/parsers.conf /fluent-bit/etc/parsers.conf
COPY config/input.conf /fluent-bit/etc/input.conf
COPY config/filter.conf /fluent-bit/etc/filter.conf
COPY config/output.conf /fluent-bit/etc/output.conf

# Copy Lua script
COPY scripts/parse_devid.lua /fluent-bit/scripts/parse_devid.lua

# Expose ports
EXPOSE 5170 5171 5172 5173 5174 5175

# Start Fluent Bit
CMD ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf"]

