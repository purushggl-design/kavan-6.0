import re
import sys

filepath = 'apps/authentication/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix StandardResponse.success("Message", data=data) -> StandardResponse.success(data=data, message="Message")
text = re.sub(r'StandardResponse\.success\((["\'][^"\']+["\']),\s*data=(.*?)\)', r'StandardResponse.success(data=\2, message=\1)', text)

# Fix StandardResponse.success("Message", ...) -> StandardResponse.success(message="Message", ...)
text = re.sub(r'StandardResponse\.success\((["\'][^"\']+["\'])(.*?)\)', r'StandardResponse.success(message=\1\2)', text)

# Fix status_code= -> status=
text = text.replace('status_code=', 'status=')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed views.py")
