from django.core.mail import send_mail

## Email template for user request new password
def order_confirmation_email(message_dict):
   contents = f"""
   Thank you for shopping at Django Web Shop!
   Order #{message_dict['order_id']}
   Order Total: {message_dict['order_total']}
   """
   send_mail(
      'Django Web Shop - Order confirmation',
      contents,
      'markushylleberg@gmail.com',
      [message_dict['email']],
      fail_silently=False
   )