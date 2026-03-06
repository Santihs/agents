import logging

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
from models import openrouter_model
from config import settings

logger = logging.getLogger(__name__)


@function_tool
def send_email(subject: str, html_body: str) -> str:
    """Send an email with the given subject and HTML body"""
    sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
    from_email = Email(settings.from_email)
    to_email = To(settings.to_email)
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    logger.info("Email sent, status_code=%d", response.status_code)
    return "success"


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=openrouter_model,
)
