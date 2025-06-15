[Setup]
AppName=MyApp
AppVersion=1.0
DefaultDirName={pf}\MyApp
DefaultGroupName=MyApp
OutputDir=.
OutputBaseFilename=MyAppInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Beso\Documents\LibreScoreApp\httpsmusescore_downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MyApp"; Filename: "{app}\httpsmusescore_downloader.exe"

[Run]
Filename: "{app}\httpsmusescore_downloader.exe"; Description: "Run MyApp"; Flags: nowait postinstall skipifsilent
