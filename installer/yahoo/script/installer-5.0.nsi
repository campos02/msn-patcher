!include "WinVer.nsh"
!include "LogicLib.nsh"
!include "MUI2.nsh"
!include "nsProcess.nsh"

!define YMSGR_FOLDER "$PROGRAMFILES\Yahoo!\Messenger"

Name "Yahoo! Messenger 5.0"
InstallDir ${{YMSGR_FOLDER}}
OutFile "{outfile}"

!define ESCARGOT_UNINSTALL_ENTRY "Software\Microsoft\Windows\CurrentVersion\Uninstall\Yahoo! Messenger"
!define YPAGER_KEY "Software\Yahoo\Pager"
!define YMSGR_UNINSTALLER_NAME "$INSTDIR\Uninstall.exe"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\YPager.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Yahoo! Messenger 5.0"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "install"
	SetOutPath $INSTDIR
	SetOverwrite ifdiff
	SetShellVarContext all
	
	${{nsProcess::KillProcess}} "YPager.exe" $R0
	; Small timeout to avoid race conditions
	Sleep 1000
	
	; Copy all main files to installation directly
	File MAINDIR\yacscom.dll
	File MAINDIR\yacsui.dll
	File MAINDIR\asw.dll
	File MAINDIR\yauto.dll
	File MAINDIR\aswres.dll
	File MAINDIR\ymsgipdl.ini
	File MAINDIR\ygxa_2.dll
	File MAINDIR\ypagerps.dll
	File MAINDIR\ypager.tlb
	File MAINDIR\idle.dll
	File MAINDIR\MyYahoo.dll
	File MAINDIR\ycrwin32.dll
	File MAINDIR\blank.html
	File MAINDIR\proxy.dll
	File MAINDIR\YServer.exe
	File /r MAINDIR\IMVCache
	File /r MAINDIR\Media
	File MAINDIR\stock.dll
	File MAINDIR\ft.dll
	File MAINDIR\res_msgr.dll
	File MAINDIR\filter1.txt
	File MAINDIR\emote.dat
	SetOverwrite off
	File MAINDIR\emote_user.dat
	SetOverwrite ifdiff
	File MAINDIR\ymsgip.dll
	File MAINDIR\privacy.txt
	File MAINDIR\ymsgr.ini
	File /r MAINDIR\skins
	File MAINDIR\YPager.exe
	File MAINDIR\escargot.dll
	File MAINDIR\YPager.exe-escargot.ini
	File MAINDIR\Ymsgr_tray.exe
	File MAINDIR\ViewInfo.reg
	File MAINDIR\ywcupl.dll
	File MAINDIR\ywcvwr.dll
	File MAINDIR\yupdater.exe
	File MAINDIR\d32-fw.dll
	File /r MAINDIR\YView
	File /r MAINDIR\tour
	File /r MAINDIR\defaults
	
	; Add default registry stuff
	WriteRegStr HKCU ${{YPAGER_KEY}} "" ""
	WriteRegStr HKCU ${{YPAGER_KEY}} "PreLogin" "http://msg.edit.yahoo.com/config/"
	WriteRegStr HKCU ${{YPAGER_KEY}} "LatestSocketServerUrl" "http://update.pager.yahoo.com/servers.html"
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "Enable PTP" 0x00000001
	WriteRegStr HKCU ${{YPAGER_KEY}} "Http Server" "shttp.msg.yahoo.com/notify/"
	WriteRegStr HKCU ${{YPAGER_KEY}} "IPLookup" "204.71.200.33,204.71.200.34 "
	WriteRegStr HKCU ${{YPAGER_KEY}} "ClientUpdatePage" "http://update.messenger.yahoo.com/msgrcli.html"
	WriteRegStr HKCU ${{YPAGER_KEY}}\FileTransfer "Server Name" "m1.escargot.log1p.xyz"
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "Stand By" 0x00000001
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "OtherCommunity" 0x00000000
	WriteRegStr HKCU ${{YPAGER_KEY}}\YMSGIP "Show Directory" "0"
	WriteRegStr HKCU ${{YPAGER_KEY}}\Game "Server" "http://gameprowler.yahoo.com/"
	WriteRegStr HKCU ${{YPAGER_KEY}}\skins "Skin_Directory" "default"
	WriteRegDWORD HKCU "${{YPAGER_KEY}}\Color Effects\default" "0" 0x000000FF
	WriteRegDWORD HKCU "${{YPAGER_KEY}}\Color Effects\default" "1" 0x0000FF00
	WriteRegDWORD HKCU "${{YPAGER_KEY}}\Color Effects\default" "2" 0x00FF0000
	WriteRegDWORD HKCU "${{YPAGER_KEY}}\Color Effects\default" "Type" 0x00000000
	WriteRegStr HKCU ${{YPAGER_KEY}} "host name" "m1.escargot.log1p.xyz"
	WriteRegStr HKCU ${{YPAGER_KEY}} "socket server" "m1.escargot.log1p.xyz"
	WriteRegStr HKCU "Software\Netscape\Netscape Navigator\Automation Protocols" ymsgr "Yauto.NSAuto.1"
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "Tour" 0x00000001
	WriteRegDWORD HKCU ${{YPAGER_KEY}}\View "Restore_Default" 0x00000001
	WriteRegDWORD HKCU ${{YPAGER_KEY}}\IMUnified "disable imip" 0x00000001
	WriteRegDWORD HKCU ${{YPAGER_KEY}}\FileTransfer "AllowMe" 0x00000001
	WriteRegStr HKCU ${{YPAGER_KEY}}\yurl "Finance Disclaimer" "http://msg.edit.yahoo.com/config/jlb"
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "Migrate" 0x000003e2
	
	File MAINDIR\n2pclient.dll
	File MAINDIR\tsd2.dll
	
	WriteRegStr HKCU Software\Microsoft\Windows\CurrentVersion\Run "Yahoo! Pager" "$INSTDIR\ypager.exe -quiet"
	WriteRegDWORD HKCU ${{YPAGER_KEY}} "Launch on Startup" 0x00000001
	
	; Start menu entries
	CreateDirectory "$SMPROGRAMS\Yahoo! Messenger"
	CreateShortcut "$SMPROGRAMS\Yahoo! Messenger\Yahoo! Messenger.lnk" $INSTDIR\YPager.exe
	CreateShortcut "$SMPROGRAMS\Yahoo! Messenger\Uninstall Yahoo! Messenger.lnk" ${{YMSGR_UNINSTALLER_NAME}}
	CreateDirectory "$STARTMENU\Yahoo! Messenger"
	CreateShortcut "$STARTMENU\Yahoo! Messenger\Yahoo! Messenger.lnk" $INSTDIR\YPager.exe
	
	; Desktop shortcut
	CreateShortcut "$DESKTOP\Yahoo! Messenger.lnk" $INSTDIR\YPager.exe
	
	; Register DLLs
	RegDLL yacscom.dll
	RegDLL yacsui.dll
	RegDLL asw.dll
	RegDLL yauto.dll
	RegDLL ypagerps.dll
	RegDLL MyYahoo.dll
	RegDLL ycrwin32.dll
	RegDLL proxy.dll
	;RegDLL YServer.exe
	RegDLL stock.dll
	RegDLL ft.dll
	;RegDLL YPager.exe
	;RegDLL Ymsgr_tray.exe
	RegDLL ywcupl.dll
	RegDLL ywcvwr.dll
	
	; Add typelib and URI stuff
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}} "" ""
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}} "AppID" "{{E5D12C42-7B4F-11D3-B5C9-0050045C3C96}}"
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}}\LocalServer32 "" "$INSTDIR\YPAGER.EXE"
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}}\ProgID "" "Ypager.Messenger.1"
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}}\TypeLib "" "{{E5D12C41-7B4F-11D3-B5C9-0050045C3C96}}"
	WriteRegStr HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}}\VersionIndependentProgID "" "Ypager.Messenger"
	WriteRegStr HKCR ymsgr "" "URL: YMessenger Protocol"
	WriteRegStr HKCR ymsgr\shell\open\command "" "$INSTDIR\YPAGER.EXE %1"
	WriteRegStr HKCR ymsgr "URL Protocol" ""
	WriteRegStr HKCR "MIME\Database\Content Type\application/ymsgr" "" ""
	WriteRegStr HKCR "MIME\Database\Content Type\application/ymsgr" "Extension" ".ymg"
	WriteRegStr HKCR YPager.Messenger "" "YPager Messenger"
	WriteRegStr HKCR YPager.Messenger\shell\open\command "" "$INSTDIR\YPager.exe %1"
	WriteRegStr HKCR .ymg "" "YPager.Messenger"
	WriteRegStr HKCR .ymg "Content Type" "application/ymsgr"
	WriteRegStr HKCR YPager.Messenger.1\shell\open\command "" "$INSTDIR\YPager.exe %1"
	WriteRegStr HKCR .yps "" "YPager.Messenger"
	WriteRegStr HKCR .yps "Content Type" "application/ymsgr"
	WriteRegStr HKCU ${{YPAGER_KEY}}\defaults "" ""
	
	File MAINDIR\default.reg
	
	; Uninstaller setup
	IfFileExists $PROGRAMFILES\Yahoo!\Messenger\UNWISE.EXE 0 +2
	Delete $PROGRAMFILES\Yahoo!\Messenger\UNWISE.EXE
	IfFileExists $PROGRAMFILES\Yahoo!\Messenger\INSTALL.LOG 0 +2
	Delete $PROGRAMFILES\Yahoo!\Messenger\INSTALL.LOG
	
	WriteUninstaller ${{YMSGR_UNINSTALLER_NAME}}
	WriteRegStr HKLM "${{ESCARGOT_UNINSTALL_ENTRY}}" UninstallString "$\"${{YMSGR_UNINSTALLER_NAME}}$\""
	WriteRegStr HKLM "${{ESCARGOT_UNINSTALL_ENTRY}}" DisplayName "Yahoo! Messenger"
SectionEnd

Section "Uninstall"
	SetShellVarContext all
	
	Delete "${{YMSGR_UNINSTALLER_NAME}}"
	${{nsProcess::KillProcess}} "YPager.exe" $R0
	; Small timeout to avoid race conditions
	Sleep 1000
	
	; First, delete registry entries and unregister DLLs
	DeleteRegKey HKCR CLSID\{{E5D12C4E-7B4F-11D3-B5C9-0050045C3C96}}
	DeleteRegKey HKCR ymsgr
	DeleteRegKey HKCR "MIME\Database\Content Type\application/ymsgr"
	DeleteRegKey HKCR YPager.Messenger
	DeleteRegKey HKCR .ymg
	DeleteRegKey HKCR YPager.Messenger.1
	DeleteRegKey HKCR .yps
	
	UnRegDLL "${{YMSGR_FOLDER}}\yacscom.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\yacsui.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\asw.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\yauto.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\ypagerps.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\MyYahoo.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\ycrwin32.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\proxy.dll"
	;UnRegDLL "${{YMSGR_FOLDER}}\YServer.exe"
	UnRegDLL "${{YMSGR_FOLDER}}\stock.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\ft.dll"
	;UnRegDLL "${{YMSGR_FOLDER}}\YPager.exe"
	;UnRegDLL "${{YMSGR_FOLDER}}\Ymsgr_tray.exe"
	UnRegDLL "${{YMSGR_FOLDER}}\ywcupl.dll"
	UnRegDLL "${{YMSGR_FOLDER}}\ywcvwr.dll"
	
	DeleteRegKey HKCU ${{YPAGER_KEY}}
	
	; Now, remove shortcuts
	IfFileExists "$STARTMENU\Yahoo! Messenger\Yahoo! Messenger.lnk" 0 +3
	Delete /REBOOTOK "$STARTMENU\Yahoo! Messenger\Yahoo! Messenger.lnk"
	RMDir /REBOOTOK "$STARTMENU\Yahoo! Messenger"
	IfFileExists "$SMPROGRAMS\Yahoo! Messenger\Yahoo! Messenger.lnk" 0 +2
	Delete /REBOOTOK "$SMPROGRAMS\Yahoo! Messenger\Yahoo! Messenger.lnk"
	IfFileExists "$SMPROGRAMS\Yahoo! Messenger\Uninstall Yahoo! Messenger.lnk" 0 +3
	Delete /REBOOTOK "$SMPROGRAMS\Yahoo! Messenger\Uninstall Yahoo! Messenger.lnk"
	RMDir /REBOOTOK "$SMPROGRAMS\Yahoo! Messenger"
	IfFileExists "$DESKTOP\Yahoo! Messenger.lnk" 0 +2
	Delete /REBOOTOK "$DESKTOP\Yahoo! Messenger.lnk"
	
	Delete "${{YMSGR_FOLDER}}\yacscom.dll"
	Delete "${{YMSGR_FOLDER}}\yacsui.dll"
	Delete "${{YMSGR_FOLDER}}\asw.dll"
	Delete "${{YMSGR_FOLDER}}\yauto.dll"
	Delete "${{YMSGR_FOLDER}}\aswres.dll"
	Delete "${{YMSGR_FOLDER}}\ymsgipdl.ini"
	Delete "${{YMSGR_FOLDER}}\ygxa_2.dll"
	Delete "${{YMSGR_FOLDER}}\ypagerps.dll"
	Delete "${{YMSGR_FOLDER}}\ypager.tlb"
	Delete "${{YMSGR_FOLDER}}\idle.dll"
	Delete "${{YMSGR_FOLDER}}\MyYahoo.dll"
	Delete "${{YMSGR_FOLDER}}\ycrwin32.dll"
	Delete "${{YMSGR_FOLDER}}\blank.html"
	Delete "${{YMSGR_FOLDER}}\proxy.dll"
	Delete "${{YMSGR_FOLDER}}\YServer.exe"
	RMDir /r "${{YMSGR_FOLDER}}\IMVCache"
	RMDir /r "${{YMSGR_FOLDER}}\Media"
	Delete "${{YMSGR_FOLDER}}\stock.dll"
	Delete "${{YMSGR_FOLDER}}\ft.dll"
	Delete "${{YMSGR_FOLDER}}\res_msgr.dll"
	Delete "${{YMSGR_FOLDER}}\filter1.txt"
	Delete "${{YMSGR_FOLDER}}\emote.dat"
	Delete "${{YMSGR_FOLDER}}\emote_user.dat"
	Delete "${{YMSGR_FOLDER}}\ymsgip.dll"
	Delete "${{YMSGR_FOLDER}}\privacy.txt"
	Delete "${{YMSGR_FOLDER}}\ymsgr.ini"
	RMDir /r "${{YMSGR_FOLDER}}\skins\default"
	RMDir /r "${{YMSGR_FOLDER}}\skins\games"
	RMDir /r "${{YMSGR_FOLDER}}\skins\custom"
	RMDir "${{YMSGR_FOLDER}}\skins"
	Delete /REBOOTOK "${{YMSGR_FOLDER}}\YPager.exe"
	Delete /REBOOTOK "${{YMSGR_FOLDER}}\escargot.dll"
	Delete /REBOOTOK "${{YMSGR_FOLDER}}\YPager.exe-escargot.ini"
	Delete "${{YMSGR_FOLDER}}\Ymsgr_tray.exe"
	Delete "${{YMSGR_FOLDER}}\ViewInfo.reg"
	Delete "${{YMSGR_FOLDER}}\ywcupl.dll"
	Delete "${{YMSGR_FOLDER}}\ywcvwr.dll"
	Delete "${{YMSGR_FOLDER}}\yupdater.exe"
	Delete "${{YMSGR_FOLDER}}\d32-fw.dll"
	RMDir /r "${{YMSGR_FOLDER}}\YView"
	RMDir /r "${{YMSGR_FOLDER}}\tour"
	RMDir /r "${{YMSGR_FOLDER}}\defaults"
	Delete "${{YMSGR_FOLDER}}\n2pclient.dll"
	Delete "${{YMSGR_FOLDER}}\tsd2.dll"
	Delete "${{YMSGR_FOLDER}}\default.reg"
	
	RMDir "${{YMSGR_FOLDER}}"
	RMDir "$PROGRAMFILES\Yahoo!"
	
	DeleteRegKey HKLM "${{ESCARGOT_UNINSTALL_ENTRY}}"
SectionEnd

Function .onInit
	${{IfNot}} ${{AtLeastWinXP}}
		MessageBox MB_OK|MB_ICONSTOP "Setup requires Windows XP or later to install."
		Quit
	${{EndIf}}
FunctionEnd
