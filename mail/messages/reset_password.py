from mail.message import Message

_subject = 'Reset your password'
_html = '''
<html>
<body>
    <h1>Reset password</h1>
    <h4>temporary password: $password</a></h4>
</body>
</html>
'''

reset_password = Message(_subject, _html)