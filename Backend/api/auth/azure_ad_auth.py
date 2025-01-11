from msal import ConfidentialClientApplication
from ..config import AZURE_AD_CLIENT_ID, AZURE_AD_CLIENT_SECRET, AZURE_AD_TENANT_ID

def authenticate_azure_ad(username: str, password: str) -> dict:
    authority = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}"
    scopes = ["https://graph.microsoft.com/.default"]

    app = ConfidentialClientApplication(
        AZURE_AD_CLIENT_ID,
        authority=authority,
        client_credential=AZURE_AD_CLIENT_SECRET
    )

    result = app.acquire_token_by_username_password(
        username,
        password,
        scopes
    )

    if "access_token" in result:
        return {"success": True, "token": result["access_token"]}
    else:
        return {"success": False, "error": result.get("error_description", "Authentication failed")}

