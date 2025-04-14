import os
from django.conf import settings
from mailersend import emails


template_content = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Your Password</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
<table width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f4f4; padding: 20px;">
    <tr>
        <td align="center">
            <table width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td align="center">
                        <h1 style="color: #333333;">Reset Your Password</h1>
                        <p style="color: #666666; font-size: 16px;">You requested to reset your password. Click the button below to set a new one:</p>
                        <a href="{{resetLink}}"
                           style="display: inline-block; background-color: #007BFF; color: #ffffff; text-decoration: none; padding: 12px 20px; border-radius: 5px; font-size: 16px; margin: 20px 0;">
                            Reset Password
                        </a>
                        <p style="color: #999999; font-size: 14px;">If you didn’t request this, you can safely ignore this email.</p>
                        <p style="color: #999999; font-size: 14px;">For further assistance, please contact us at <a href="mailto:support@example.com" style="color: #007BFF;">support@example.com</a>.</p>
                    </td>
                </tr>
                <tr>
                    <td align="center" style="padding-top: 20px; border-top: 1px solid #dddddd;">
                        <p style="color: #999999; font-size: 12px;">© 2024 Company Name. All rights reserved.</p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
</html>
'''


class EmailService:
    @staticmethod
    def send_email(reset_link, recipient_email, recipient_name):
        mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)

        # Define an empty dict to populate with mail values
        mail_body = {}

        # Sender information
        mail_from = {
            "name": "Your Name",
            "email": "no-reply@trial-69oxl5e2zedl785k.mlsender.net",
        }

        # Recipient information
        recipients = [
            {
                "name": recipient_name,
                "email": recipient_email,
            }
        ]

        reply_to = {
            "name": "Support Team",
            "email": "support@example.com",
        }


        # Interpolate the reset link
        html_content = template_content.replace("{{resetLink}}", reset_link)

        # Plaintext fallback content
        plaintext_content = f"Hi {recipient_name},\n\nYou requested to reset your password. Please click the link below:\n{reset_link}\n\nIf you didn’t request this, you can safely ignore this email.\n\nBest regards,\nYour Company"

        # Populate mail body
        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Reset Your Password", mail_body)
        mailer.set_html_content(html_content, mail_body)
        mailer.set_plaintext_content(plaintext_content, mail_body)
        mailer.set_reply_to(reply_to, mail_body)

        # Send the email
        mailer.send(mail_body)