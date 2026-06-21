from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):
    

    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")

        if not pushover_user or not pushover_token:
            return '{"notification": "error", "reason": "PUSHOVER_USER or PUSHOVER_TOKEN not set"}'

        print(f"Push: {message}")
        try:
            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data={"user": pushover_user, "token": pushover_token, "message": message},
                timeout=10,
            )
            response.raise_for_status()
            return '{"notification": "ok"}'
        except requests.RequestException as e:
            return f'{{"notification": "error", "reason": "{e}}}"'