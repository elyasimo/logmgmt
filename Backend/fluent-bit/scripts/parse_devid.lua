function parse_devid(tag, timestamp, record)
    local hostname = record["host"]
    if hostname then
        local cnnid, country, city, product, device_number = hostname:match("sc%-([^-]+)%-([^-]+)%-([^-]+)%-([^-]+)%-(%d+)")
        if cnnid then
            record["cnnid"] = cnnid
            record["country"] = country
            record["city"] = city
            record["product"] = product
            record["device_number"] = device_number
            record["devname"] = hostname
        end
    end

    local devid = record["devid"]
    if devid then
        if devid:match("^FGT") then
            record["vendor"] = "Fortinet"
            record["device_type"] = "Firewall"
        elseif devid:match("^FPX") then
            record["vendor"] = "Fortinet"
            record["device_type"] = "Proxy"
        -- Add more vendor-specific parsing here as needed
        end
    end

    return 2, timestamp, record
end

