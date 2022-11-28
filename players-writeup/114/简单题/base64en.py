import base64
with open("a.bin", "rb") as f:
    code=f.read()
b64code = base64.b64encode(code)
print(b64code)