from user_agents import parse

def get_device_info(request):
    ua = parse(request.headers.get("user-agent"))
    
    return {
        "device": ua.device.family or "Desktop",
        "browser": ua.browser.family,
        "os": ua.os.family
    }
