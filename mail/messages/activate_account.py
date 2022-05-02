from mail.message import Message

_subject = 'Activate your account'
_html = '''
<html>
<body>
    <h1>Welcome $username, activate your account</h1>
    <h4><a href="$link">Use this link</a></h4>
</body>
</html>
'''

activate_account = Message(_subject, _html)