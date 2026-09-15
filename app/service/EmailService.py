from flask import current_app
from flask_mail import Message
from extensions.mail import mail


class EmailService:

    @staticmethod
    def _send(subject, recipients, html_body, text_body=None):
        app = current_app
        if not app.config.get("MAIL_USERNAME") or app.config.get("MAIL_SUPPRESS_SEND"):
            # No SMTP configured (or explicitly suppressed) - log instead of sending,
            # so local dev doesn't need real credentials.
            app.logger.info(
                "[EmailService] Suppressed email -> to=%s subject=%s\n%s",
                recipients, subject, text_body or html_body,
            )
            return

        msg = Message(subject=subject, recipients=recipients, html=html_body, body=text_body)
        mail.send(msg)

    @staticmethod
    def send_invite_email(to_email, invite_link, role, inviter_name, team_name=None):
        role_label = role.capitalize()
        team_line = f" to join the <strong>{team_name}</strong> team" if team_name else ""
        subject = f"You've been invited to Task Manager as a {role_label}"

        html_body = f"""
            <p>Hi,</p>
            <p>{inviter_name} has invited you{team_line} on Task Manager as a <strong>{role_label}</strong>.</p>
            <p><a href="{invite_link}">Click here to create your account</a></p>
            <p>This link expires in 7 days. If you weren't expecting this invite, you can ignore this email.</p>
        """
        text_body = (
            f"{inviter_name} has invited you{('to join ' + team_name + ' ') if team_name else ''}"
            f"on Task Manager as a {role_label}.\n\n"
            f"Create your account: {invite_link}\n\n"
            f"This link expires in 7 days."
        )

        EmailService._send(subject, [to_email], html_body, text_body)
