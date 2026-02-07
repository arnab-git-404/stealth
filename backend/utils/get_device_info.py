from user_agents import parse

def get_device_info(request):
    ua = parse(request.headers.get("user-agent"))
    
    if ua.is_mobile:
        device = "Mobile"
    elif ua.is_tablet:
        device = "Tablet"
    elif ua.is_pc:
        device = "Desktop"
    else:
        device = "Other"

    return {
        "device": device,
        "browser": ua.browser.family,
        "os": ua.os.family,
        "ip": request.client.host,
    }
