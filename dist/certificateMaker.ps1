$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=MyCodeSigner" -KeyExportPolicy Exportable -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddYears(5)
# MyCodeSigner is the name

$pwd = ConvertTo-SecureString -String "YourPasswordHere" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "C:\Users\YourUser\Desktop\MyCodeSigner.pfx" -Password $pwd


signtool sign /fd SHA256 /a /f "C:\Users\YourUser\Desktop\MyCodeSigner.pfx" /p YourPassword "C:\Path\To\YourFile.exe"


signtool verify /pa /v "C:\Path\To\YourFile.exe"
