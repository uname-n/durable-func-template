from azure.functions import AuthLevel
from azure.durable_functions import DFApp

app = DFApp(http_auth_level=AuthLevel.FUNCTION)
