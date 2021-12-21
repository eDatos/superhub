import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from logzero import logger

import settings


def notify():
    logger.debug('Initializing notification handler')
    smtp = smtplib.SMTP(settings.SMTP_SERVER, port=settings.SMTP_PORT)
    smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

    send_from = settings.NOTIFICATION_FROM_ADDR
    send_to = settings.NOTIFICATION_TO_ADDRS

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    msg['Subject'] = 'Supermercados Canarias: Recopilación de establecimientos'

    logger.debug('Building content')
    buf = []
    buf.append(
        'Se adjunta fichero comprimido compuesto por '
        'ficheros csv para cada cadena de supermercados.'
    )
    content = '<br>'.join(buf)
    msg.attach(MIMEText(content, 'html'))

    logger.debug('Adding attachment')
    part = MIMEBase('application', 'octet-stream')
    attachment = settings.ZIPDATA_FILEPATH
    part.set_payload(attachment.read_bytes())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment.name}')
    msg.attach(part)

    logger.info('Sending message with attached files')
    smtp.sendmail(send_from, send_to, msg.as_string())

    smtp.quit()
