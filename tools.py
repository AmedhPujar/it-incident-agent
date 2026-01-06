from langchain.tools import tool

@tool
def server_health_check(server_name: str):
    """Checks CPU and Status for a given server."""
    return {"server": server_name, "cpu_usage": "98%", "status": "CRITICAL"}

@tool
def restart_service(service_name: str):
    """Restarts a system service to fix errors."""
    return f"SUCCESS: Service {service_name} restarted successfully."
