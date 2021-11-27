def read_mail(user, app_pwd, server, port, readonly = True):
    import imaplib
    import email
    
    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(user, app_pwd)
    mail.select('inbox', readonly = readonly)
    # ALL - all emails, UNSEEN - all new emails
    (check, message_ids) = mail.search(None, 'UNSEEN')
    
    final = []
    if check == 'OK':
        # Get list of message ids
        id_list = message_ids[0].split()
        if id_list != []:
            for i in id_list[::-1]:
                data = mail.fetch(str(int(i)), '(RFC822)')
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        # Get the message
                        message = email.message_from_bytes(arr[1])
                        # Get the plain text body
                        for part in message.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode = True).decode('utf-8')
                        # Format results       
                        final.append({'id': str(int(i)),
                                      'subject': message['subject'],
                                      'sender': message['from'],
                                      'date': message['Date'],
                                      'body': body,})
                        # Mark as read
                        mail.uid('STORE', str(int(i)), '+FLAGS', "\SEEN")
    mail.close()
    mail.logout()
    return final

emails = read_mail(user = 'test@gmail.com',
                  app_pwd = '',
                  server = 'imap.gmail.com',
                  port = 993,
                  readonly = True)
