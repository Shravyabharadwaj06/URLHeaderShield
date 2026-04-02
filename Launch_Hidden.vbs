Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

' Open the web app
WshShell.Run "Page1.html", 1, False

' Navigate to the backend folder and start Django silently using pythonw
WshShell.CurrentDirectory = strPath & "\headerback"
WshShell.Run "pythonw manage.py runserver", 0, False

MsgBox "Header Shield is now running in the background." & vbCrLf & "Use 'STOP_Hidden_Server.vbs' to shut it down.", 64, "Header Shield Server"
