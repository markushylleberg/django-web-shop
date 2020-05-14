from django.core.mail import send_mail

## Email template for user request new password
def new_password_req_email(message_dict):
   contents = f"""
   Hi, you've forgot your password?
   No worries! Below is the token you'll need to reset your password.
   Token: {message_dict['token']}
   """
   send_mail(
      'Django Web Shop - New Password Request',
      contents,
      'markushylleberg@gmail.com',
      [message_dict['email']],
      fail_silently=False
   )