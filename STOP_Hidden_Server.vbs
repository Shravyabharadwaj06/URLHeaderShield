Set WshShell = CreateObject("WScript.Shell")

' Kill all pythonw processes to stop the hidden server
' Note: This might close other running pythonw scripts!
WshShell.Run "taskkill /F /IM pythonw.exe", 0, True

MsgBox "Header Shield background server has been stopped.", 64, "Header Shield Server"
