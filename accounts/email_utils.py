"""
accounts/email_utils.py
-----------------------
Centralised helper for sending OTP emails.
Sends a nicely formatted HTML email with a plain-text fallback.
"""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# ── HTML email template ────────────────────────────────────────────────────────
OTP_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Your Kaamgar OTP</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #333; }}
    .wrapper {{ max-width: 520px; margin: 40px auto; background: #ffffff;
                border-radius: 12px; overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,.08); }}
    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
               padding: 36px 32px; text-align: center; }}
    .header .brand {{ display: inline-flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
    .header .brand-icon {{ width: 42px; height: 42px; background: rgba(255,255,255,.2);
                           border-radius: 10px; display: flex; align-items: center;
                           justify-content: center; font-size: 1.3rem; font-weight: 800;
                           color: #fff; }}
    .header .brand-name {{ font-size: 1.3rem; font-weight: 700; color: #fff; }}
    .header h1 {{ font-size: 1rem; color: rgba(255,255,255,.85); font-weight: 400; margin-top: 4px; }}
    .body {{ padding: 40px 36px; }}
    .greeting {{ font-size: 1.05rem; margin-bottom: 16px; }}
    .desc {{ color: #555; font-size: .95rem; line-height: 1.6; margin-bottom: 28px; }}
    .otp-box {{ background: #f0f4ff; border: 2px dashed #667eea; border-radius: 12px;
                padding: 24px; text-align: center; margin-bottom: 28px; }}
    .otp-label {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .1em;
                  color: #667eea; font-weight: 600; margin-bottom: 8px; }}
    .otp-code {{ font-size: 2.8rem; font-weight: 800; letter-spacing: .25em;
                 color: #333; font-family: 'Courier New', monospace; }}
    .otp-timer {{ font-size: .82rem; color: #888; margin-top: 10px; }}
    .warning {{ background: #fff8e1; border-left: 4px solid #ffc107;
                border-radius: 6px; padding: 12px 16px; font-size: .85rem;
                color: #7a6020; margin-bottom: 24px; }}
    .footer {{ background: #f9fafb; border-top: 1px solid #eee;
               padding: 20px 36px; text-align: center; font-size: .78rem; color: #aaa; }}
    .footer a {{ color: #667eea; text-decoration: none; }}
  </style>
</head>
<body>
  <div class="wrapper">

    <!-- Header -->
    <div class="header">
      <div class="brand">
        <div class="brand-icon">K</div>
        <span class="brand-name">Kaamgar Connect</span>
      </div>
      <h1>Email Verification</h1>
    </div>

    <!-- Body -->
    <div class="body">
      <p class="greeting">Hi <strong>{username}</strong>,</p>
      <p class="desc">
        {purpose_text}
        Use the one-time passcode below to complete your verification.
      </p>

      <div class="otp-box">
        <div class="otp-label">Your OTP Code</div>
        <div class="otp-code">{otp}</div>
        <div class="otp-timer">⏱ This code expires in <strong>5 minutes</strong></div>
      </div>

      <div class="warning">
        🔒 <strong>Never share this code</strong> with anyone.
        Kaamgar Connect will never ask for your OTP over phone or chat.
      </div>

      <p style="font-size:.9rem;color:#777;">
        If you did not request this code, you can safely ignore this email.
        Your account will not be affected.
      </p>
    </div>

    <!-- Footer -->
    <div class="footer">
      &copy; 2025 Kaamgar Connect &nbsp;|&nbsp;
      <a href="#">Privacy Policy</a> &nbsp;|&nbsp;
      <a href="#">Help Center</a>
    </div>

  </div>
</body>
</html>
"""

# ── Plain-text fallback ────────────────────────────────────────────────────────
OTP_TEXT_TEMPLATE = (
    "Hi {username},\n\n"
    "{purpose_text}\n\n"
    "Your OTP code: {otp}\n\n"
    "This code expires in 5 minutes.\n"
    "Never share this code with anyone.\n\n"
    "— Kaamgar Connect"
)


# ── Public helper ──────────────────────────────────────────────────────────────
def send_otp_email(user, otp: str, purpose: str = "register") -> bool:
    """
    Send an OTP email to *user*.

    purpose: 'register' | 'login' | 'resend'
    Returns True on success, False on any error.
    """
    PURPOSE_TEXTS = {
        "register": (
            "Welcome to Kaamgar Connect! "
            "Please verify your email address to activate your account."
        ),
        "login": (
            "You're logging in to Kaamgar Connect. "
            "Please verify your identity."
        ),
        "resend": (
            "Here is your new verification code for Kaamgar Connect."
        ),
    }

    SUBJECTS = {
        "register": "Verify your Kaamgar Connect account",
        "login":    "Your Kaamgar Connect login OTP",
        "resend":   "Your new Kaamgar Connect OTP",
    }

    purpose_text = PURPOSE_TEXTS.get(purpose, PURPOSE_TEXTS["register"])
    subject      = SUBJECTS.get(purpose, SUBJECTS["register"])
    from_email   = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@kaamgar.com")

    ctx = {
        "username":     user.username,
        "otp":          otp,
        "purpose_text": purpose_text,
    }

    text_body = OTP_TEXT_TEMPLATE.format(**ctx)
    html_body = OTP_HTML_TEMPLATE.format(**ctx)

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as exc:
        # Log the error but don't crash the request
        import logging
        logging.getLogger(__name__).error(
            "OTP email failed for user=%s: %s", user.username, exc
        )
        return False