from decouple import config
from datetime import datetime


def base_template(subject, headline, message: list[str], button_text=None, button_link=None):
    """ Base template for email

    Args:
        `subject` (str): Subject of the email. Used in <title> tag.
        `headline` (str): Headline that is displayed in <h1> tag.
        `message` (list[str]): An array of messages that are displayed in <p> tags. The order is important.
        `button_text` (str): Optional. Text for the button
        `button_link` (str): Optional. Link for the button
    """
    company_name = "Pluto Health"
    footer_text = "We may send emails in future if they be beneficial for you or to convey any policy changes. We will never send marketing emails."
    footer_links = [
        {
            "text": "Contact Us",
            "link": "mailto:contact@company.com"
        },
        {
            "text": "Privacy Policy",
            "link": "https://company.com/privacy"
        }
    ]
    year = datetime.now().year
    if button_text and button_link:
        btn = f"""
        <br/>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
                <tbody>
                    <tr>
                        <td align="left">
                            <a href="{button_link}" target="_blank">
                                {button_text}
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>"""
    # Template
    styles = "body,table td{font-size:14px}.body,body{background-color:#f6f6f6}.container,.content{display:block;max-width:580px;padding:10px}.btn a,.btn table td{background-color:#fff}.btn,.btn a,.content,.wrapper{box-sizing:border-box}.align-center,.btn table td,.footer{text-align:center}.clear,.footer{clear:both}img{border:none;-ms-interpolation-mode:bicubic;max-width:100%}body{font-family:Helvetica,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.4;margin:0;padding:0;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}table{border-collapse:separate;mso-table-lspace:0pt;mso-table-rspace:0pt;width:100%}table td{font-family:sans-serif;vertical-align:top}.body{width:100%}.container{margin:0 auto!important;width:580px}.btn,.footer,.main{width:100%}.content{margin:0 auto}.main{background:#fff;border-radius:3px}.wrapper{padding:32px}.content-block{padding-bottom:10px;padding-top:10px}.footer{margin-top:10px}.footer a,.footer p,.footer span,.footer td{color:#999;font-size:12px;text-align:center}h1,h2,h3,h4{color:#000;font-weight:400;line-height:1.4;margin:0 0 30px}h1{font-size:35px;font-weight:300;line-height:1.15}ol,p,ul{color:#444;font-size:16px;font-weight:400;margin:0 0 15px}.btn a,a{color:#2372f5;text-decoration:none}ol li,p li,ul li{list-style-position:inside;margin-left:5px}a{font-weight:500}.btn>tbody>tr>td{padding-bottom:15px}.btn table{width:auto}.btn table td{border-radius:5px}.btn a{border:1px solid #2372f5;border-radius:2px;cursor:pointer;display:inline-block;font-size:14px;font-weight:500;margin:0;padding:12px 25px;text-transform:capitalize;letter-spacing:.5px}.btn-primary a{background-color:#2372f5;border-radius:4px;color:#fff;border:none}.last,.mb0{margin-bottom:0}.first,.mt0{margin-top:0}.align-right{text-align:right}.align-left{text-align:left}.text-sm{font-size:13px}.preheader{color:transparent;display:none;height:0;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;visibility:hidden;width:0}.powered-by a{text-decoration:none}hr{border:0;border-bottom:1px solid #f6f6f6;margin:20px 0}.logo{font-size:36px;color:#000;letter-spacing:-.75px;font-weight:700;}@media only screen and (max-width:620px){table.body h1{font-size:28px!important;margin-bottom:10px!important}table.body a,table.body ol,table.body p,table.body span,table.body td,table.body ul{font-size:16px!important}table.body .article,table.body .wrapper{padding:10px!important}table.body .content{padding:0!important}table.body .container{padding:0!important;width:100%!important}table.body .main{border-left-width:0!important;border-radius:0!important;border-right-width:0!important}table.body .btn a,table.body .btn table{width:100%!important}table.body .img-responsive{height:auto!important;max-width:100%!important;width:auto!important}}@media all{.ExternalClass{width:100%}.ExternalClass,.ExternalClass div,.ExternalClass font,.ExternalClass p,.ExternalClass span,.ExternalClass td{line-height:100%}.apple-link a{color:inherit!important;font-family:inherit!important;font-size:inherit!important;font-weight:inherit!important;line-height:inherit!important;text-decoration:none!important}#MessageViewBody a{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}.btn-primary a:hover,.btn-primary table td:hover{background-color:#2378fa!important}}"
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>{subject}</title>
        <style>{styles}</style>
    </head>
    <body>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
            <tr>
                <td>&nbsp;</td>
                <td class="container">
                    <div class="content">
                        <table role="presentation" class="main">
                            <tr>
                                <td class="wrapper">
                                    <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                        <tr>
                                        <td>
                                            <p class="company-name">
                                                <a href="{config("FRONTEND_URL")}" target="_blank" class="logo">{company_name}</a>
                                            </p>
                                            <br/>
                                            <h1>{headline}</h1>
                                            <br/>
                                            {''.join([f'<p>{msg}</p>' for msg in message])}
                                            {btn if button_text and button_link else ''}
                                            <hr/>
                                            <p class="text-sm">{footer_text}</p>
                                            <br/>
                                            <div class="align-center">{company_name} {year}.</div>
                                            <div class="align-center">
                                            {" • ".join([f'<a href="{link["link"]}" target="_blank">{link["text"]}</a>' for link in footer_links])}
                                            </div>
                                        </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div>
                </td>
                <td>&nbsp;</td>
            </tr>
        </table>
    </body>
    </html>
    """
    return template
