; Installer script for pre-patched Windows Live Messenger 2009 installers
; This contains the main installer logic for installing WLM 2009 components. This will then be templated by the patcher script to include the components for specific builds
!include "WinVer.nsh"
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"
!include "x64.nsh"

!define WLM_VERSION_NAME "Windows Live Messenger 2009"

Name "${{WLM_VERSION_NAME}}"
InstallDir "$PROGRAMFILES\Windows Live\Messenger"
OutFile "{outfile}"

!define ESCARGOT_TMP_PATH_BASE "$TEMP\escargot-installer"
!define ESCARGOT_TMP_PATH_WLM "${{ESCARGOT_TMP_PATH_BASE}}\{base_name}"
!define ESCARGOT_UNINSTALL_ENTRY "Software\Microsoft\Windows\CurrentVersion\Uninstall\WLM2009_Escargot"
!define WLM_UNINSTALLER_NAME "$INSTDIR\Uninstall.exe"

; MSI constants
!define MSI_ERROR_SUCCESS 0
!define MSI_ERROR_INSTALL_FAILURE 1603
!define MSI_ERROR_UNKNOWN_PRODUCT 1605
!define MSI_ERROR_PRODUCT_VERSION 1638
!define MSI_ERROR_SUCCESS_REBOOT_REQUIRED 3010
!define MSI_PROPERTY_PACKAGECODE "PackageCode"

; Template these variables
!define WLM_PRODUCT_CODE "{msi_product_code}"
!define CONTACTS_PRODUCT_CODE "{wlcomm_product_code}"

; String constants
!define INSTALLING_STRING "Installing "
!define NEWER_VERSION_PRE "A newer version of "
!define NEWER_VERSION_REST " has been detected"
!define INSTALLING_PATCHED " has been successfully uninstalled. Installing patched version..."
!define ALREADY_INSTALLED " is already installed."
!define CHECK_IF_PRESENT_PRE "Checking if "
!define CHECK_IF_PRESENT_REST " is present..."
!define SETUP_ABORT "Setup will now abort."
!define SKIPPING_TEXT "Skipping..."
; Product names
!define WLM_PRODUCT_NAME "Windows Live Messenger"
!define WLCOMM_PRODUCT_NAME "Windows Live Communications Platform"
!define MAER_PRODUCT_NAME "Microsoft Application Error Reporting"
!define MSVC_PRODUCT_NAME "Microsoft Visual C++ Runtime"
!define SEGOE_UI_PRODUCT_NAME "Segoe UI"

; MUI macros/defines
!define MUI_WELCOMEFINISHPAGE_BITMAP "{welcomefinish_bitmap}"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\msnmsgr.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${{WLM_VERSION_NAME}}"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

!macro CHECK_MUTEX goto
	; Create mutex
	System::Call "kernel32::CreateMutex(i 0, i 0, t 'InstallerEscargot-MSN') ?e"
	Pop $R0
	; If mutex already exists, activate existing window and abort
	StrCmp $R0 183 0 ${{goto}}
	StrLen $R0 "$(^Name)"
	IntOp $R0 $R0 + 1
	loop:
		FindWindow $R1 "#32770" "" 0 $R1
		IntCmp $R1 0 +4
		System::Call "user32::GetWindowText(i R1, t .R2, i R0) i."
		StrCmp $R2 "$(^Name)" 0 loop
		System::Call "user32::ShowWindow(i R1, i 9) i."
		Abort
!macroend

!macro MARKREBOOT_MACRO un
	Function ${{un}}MarkReboot
		; If reboot flag is already set, exit out of function. Else, set reboot flag
		IfRebootFlag +2 0
		SetRebootFlag true
	FunctionEnd
!macroend

!insertmacro MARKREBOOT_MACRO ""
!insertmacro MARKREBOOT_MACRO "un."

Var InstallCRT
Var ContactsBuildAlreadyInstalled
Var MessengerBuildAlreadyInstalled
Var OnSupportedOS

Section "install"
	; Check if same build of WLM/Contacts this installer is installing is already installed. If return code == 0 and package code (revision) is the same, uninstall and install our own version
	System::Call "msi::MsiGetProductInfo(t '${{WLM_PRODUCT_CODE}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
	${{If}} $1 == ${{MSI_ERROR_SUCCESS}}
		Push 1
		Pop $MessengerBuildAlreadyInstalled
		MessageBox MB_YESNO|MB_ICONEXCLAMATION "The build of ${{WLM_PRODUCT_NAME}} you're attempting to install is already installed on your system. Do you wish to overwrite this installation?" /SD IDYES IDNO QuitInstall
	${{EndIf}}
	
	System::Call "msi::MsiGetProductInfo(t '${{CONTACTS_PRODUCT_CODE}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
	${{If}} $1 == ${{MSI_ERROR_SUCCESS}}
		Push 1
		Pop $ContactsBuildAlreadyInstalled
	${{EndIf}}
	
	SetOutPath ${{ESCARGOT_TMP_PATH_WLM}}
	
	; Extract core installers
	File Messenger.msi
	File Contacts.msi
	
	; Check if runtime is installed. If not, install.
	System::Call "msi::MsiGetProductInfo(t '{{22B775E7-6C42-4FC5-8E10-9A5E3257BD94}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
	${{Switch}} $1
		${{Case}} ${{MSI_ERROR_SUCCESS}}
			Push 1
			Pop $InstallCRT
			${{Break}}
		${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
			Push 1
			Pop $InstallCRT
			${{Break}}
		${{Default}}
			; Possibly a fatal error occurred - quit installation
			Call ErrorOut
			${{Break}}
	${{EndSwitch}}
	
	${{If}} $InstallCRT == 1
		DetailPrint "${{INSTALLING_STRING}}${{MSVC_PRODUCT_NAME}}..."
		File crt.msi
		ExecWait 'msiexec /quiet /i "$OUTDIR\crt.msi"' $1
		${{Switch}} $1
			${{Case}} ${{MSI_ERROR_SUCCESS}}
				${{Break}}
			${{Case}} ${{MSI_ERROR_PRODUCT_VERSION}}
				DetailPrint "${{NEWER_VERSION_PRE}}${{MSVC_PRODUCT_NAME}}${{NEWER_VERSION_REST}}. ${{SKIPPING_TEXT}}"
				${{Break}}
			${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
				Call MarkReboot
				${{Break}}
			${{Default}}
				Call ErrorOut
				${{Break}}
		${{EndSwitch}}
	${{EndIf}}
	
	System::Call "msi::MsiGetProductInfo(t '{{95120000-00B9-0409-0000-0000000FF1CE}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
	
	${{Switch}} $1
		${{Case}} ${{MSI_ERROR_SUCCESS}}
			${{Break}}
		${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
			; Install MAER
			${{If}} ${{RunningX64}}
				DetailPrint "${{INSTALLING_STRING}}${{MAER_PRODUCT_NAME}} (x64)..."
				File dw20sharedamd64.msi
				ExecWait 'msiexec /quiet /i "$OUTDIR\dw20sharedamd64.msi"' $1
			${{Else}}
				DetailPrint "${{INSTALLING_STRING}}${{MAER_PRODUCT_NAME}} (x86)..."
				File dw20shared.msi
				ExecWait 'msiexec /quiet /i "$OUTDIR\dw20shared.msi"' $1
			${{EndIf}}
			
			${{Switch}} $1
				${{Case}} ${{MSI_ERROR_SUCCESS}}
					${{Break}}
				${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
					Call MarkReboot
					${{Break}}
				${{Default}}
					DetailPrint "${{MAER_PRODUCT_NAME}} could not install or a newer version of the component is installed. Continuing installation..."
					${{Break}}
			${{EndSwitch}}
			${{Break}}
		${{Default}}
			Call ErrorOut
			${{Break}}
	${{EndSwitch}}
	
	${{If}} ${{IsWinXP}}
		DetailPrint "${{CHECK_IF_PRESENT_PRE}}${{SEGOE_UI_PRODUCT_NAME}}${{CHECK_IF_PRESENT_REST}}"
		System::Call "msi::MsiGetProductInfo(t '{{A1F66FC9-11EE-4F2F-98C9-16F8D1E69FB7}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
		${{Switch}} $1
			${{Case}} ${{MSI_ERROR_SUCCESS}}
				${{Break}}
			${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
				DetailPrint "${{INSTALLING_STRING}}${{SEGOE_UI_PRODUCT_NAME}}"
				File SegoeFont.msi
				ExecWait 'msiexec /quiet /i "$OUTDIR\SegoeFont.msi"' $1
				${{Switch}} $1
					; The Segoe MSI seems to return a success error code regardless of if it's already installed or not
					${{Case}} ${{MSI_ERROR_SUCCESS}}
					${{Case}} ${{MSI_ERROR_PRODUCT_VERSION}}
						${{Break}}
					${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
						Call MarkReboot
						${{Break}}
					${{Default}}
						DetailPrint "Segoe UI could not be installed. Windows Live Messenger may not render text as expected."
						Sleep 500
						${{Break}}
				${{EndSwitch}}
				${{Break}}
			${{Default}}
				Call ErrorOut
				${{Break}}
		${{EndSwitch}}
	${{EndIf}}
	
	; Install main components
	
	DetailPrint "${{INSTALLING_STRING}}${{WLCOMM_PRODUCT_NAME}}..."
	${{If}} $ContactsBuildAlreadyInstalled == 1
		ExecWait 'msiexec /quiet /x ${{CONTACTS_PRODUCT_CODE}}' $1
		${{Switch}} $1
			${{Case}} ${{MSI_ERROR_SUCCESS}}
				DetailPrint "${{WLCOMM_PRODUCT_NAME}}${{INSTALLING_PATCHED}}"
				${{Break}}
			${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
				; Ignore
				${{Break}}
			${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
				Call MarkReboot
				${{Break}}
			${{Default}}
				Call ErrorOut
				${{Break}}
		${{EndSwitch}}
	${{EndIf}}
	
	ExecWait 'msiexec /quiet /i "$OUTDIR\Contacts.msi"' $1
	${{Switch}} $1
		${{Case}} ${{MSI_ERROR_SUCCESS}}
			${{Break}}
		${{Case}} ${{MSI_ERROR_PRODUCT_VERSION}}
			DetailPrint "${{NEWER_VERSION_PRE}}${{WLCOMM_PRODUCT_NAME}}${{NEWER_VERSION_REST}}. ${{SKIPPING_TEXT}}"
			${{Break}}
		${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
			Call MarkReboot
			${{Break}}
		${{Default}}
			Call ErrorOut
			${{Break}}
	${{EndSwitch}}
	
	DetailPrint "${{INSTALLING_STRING}}${{WLM_PRODUCT_NAME}}..."
	${{If}} $MessengerBuildAlreadyInstalled == 1
		ExecWait 'msiexec /quiet /x ${{WLM_PRODUCT_CODE}}' $1
		${{Switch}} $1
			${{Case}} ${{MSI_ERROR_SUCCESS}}
				DetailPrint "${{WLM_PRODUCT_NAME}}${{INSTALLING_PATCHED}}"
				${{Break}}
			${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
				; Ignore
				${{Break}}
			${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
				Call MarkReboot
				${{Break}}
			${{Default}}
				Call ErrorOut
				${{Break}}
		${{EndSwitch}}
	${{EndIf}}
	
	ExecWait 'msiexec /quiet /i "$OUTDIR\Messenger.msi"' $1
	${{Switch}} $1
		${{Case}} ${{MSI_ERROR_SUCCESS}}
			${{Break}}
		${{Case}} ${{MSI_ERROR_INSTALL_FAILURE}}
		${{Case}} ${{MSI_ERROR_PRODUCT_VERSION}}
			; Show error stating a new version of Messenger was detected
			Call CleanUp
			MessageBox MB_OK|MB_ICONEXCLAMATION "${{WLM_PRODUCT_NAME}} failed to install or a newer version is already present on the system. ${{SETUP_ABORT}}"
			Abort
			${{Break}}
		${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
			Call MarkReboot
			${{Break}}
		${{Default}}
			Call ErrorOut
			${{Break}}
	${{EndSwitch}}
	
	Call CleanUp
	
	; If "wlarp.exe" is found to be on the system, assume that the Essentials installer is already present and don't add our own uninstaller
	IfFileExists "$PROGRAMFILES\Windows Live\Installer\wlarp.exe" ContinueInstallation 0
	WriteUninstaller "${{WLM_UNINSTALLER_NAME}}"
	
	; Now add the actual uninstall entry
	WriteRegStr HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} UninstallString "$\"${{WLM_UNINSTALLER_NAME}}$\""
	WriteRegStr HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} InstallLocation $INSTDIR
	WriteRegStr HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} DisplayIcon "${{WLM_UNINSTALLER_NAME}}"
	WriteRegStr HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} DisplayName "${{WLM_VERSION_NAME}}"
	WriteRegStr HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} DisplayVersion "{version_string}"
	WriteRegDWORD HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} NoModify 0x00000001
	WriteRegDWORD HKLM ${{ESCARGOT_UNINSTALL_ENTRY}} NoRepair 0x00000001
	Goto ContinueInstallation
	
	QuitInstall:
		Abort "The same build of Windows Live Messenger was detected. Installation aborted."
	
	ContinueInstallation:
SectionEnd

Section "Uninstall"
	; Remove uninstall stuff
	Delete "${{WLM_UNINSTALLER_NAME}}"
	DeleteRegKey HKLM ${{ESCARGOT_UNINSTALL_ENTRY}}
	
	ExecWait 'msiexec /quiet /x ${{WLM_PRODUCT_CODE}}' $1
	${{Switch}} $1
		${{Case}} ${{MSI_ERROR_SUCCESS}}
		${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
			${{Break}}
		${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
			Call un.MarkReboot
			${{Break}}
		${{Default}}
			MessageBox MB_OK|MB_ICONEXCLAMATION "An error occurred while attempting to uninstall ${{WLM_PRODUCT_NAME}}. ${{SETUP_ABORT}}"
			Abort
			${{Break}}
	${{EndSwitch}}
	
	; Ask user if the uninstaller should uninstall Communications Platform since right now there's no easy way to detect that
	
	System::Call "msi::MsiGetProductInfo(t '${{CONTACTS_PRODUCT_CODE}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t ., *i ${{NSIS_MAX_STRLEN}}) i.r1"
	${{If}} $1 == ${{MSI_ERROR_SUCCESS}}
		MessageBox MB_YESNO|MB_ICONINFORMATION "Setup detected the corresponding build of Windows Live Communications Platform installed alongside Windows Live Messenger. Are you sure you want to uninstall it? This component is shared by other Windows Live applications (Movie Maker, Photo Gallery, Mail, etc.) and is required for them to run.$\n$\nIf you do not have any other Windows Live applications installed aside from Messenger, you can safely choose $\"No$\"." IDNO SkipContacts
		ExecWait 'msiexec /quiet /x ${{CONTACTS_PRODUCT_CODE}}' $1
		${{Switch}} $1
			${{Case}} ${{MSI_ERROR_SUCCESS}}
				DetailPrint "${{WLCOMM_PRODUCT_NAME}} was successfully uninstalled from the system."
				${{Break}}
			${{Case}} ${{MSI_ERROR_UNKNOWN_PRODUCT}}
				; Ignore
				${{Break}}
			${{Case}} ${{MSI_ERROR_SUCCESS_REBOOT_REQUIRED}}
				Call un.MarkReboot
				${{Break}}
			${{Default}}
				MessageBox MB_OK|MB_ICONEXCLAMATION "An error occurred while attempting to uninstall Windows Live Communications Platform. This component might still be installed, so if you don't need this component, try to get it removed as to prevent future Windows Live installations from not working as intended."
				${{Break}}
		${{EndSwitch}}
	${{EndIf}}
	SkipContacts:
SectionEnd

Function CleanUp
	SetOutPath $TEMP
	IfFileExists ${{ESCARGOT_TMP_PATH_WLM}}\*.* 0 DoNothing
	RMDir /r /REBOOTOK ${{ESCARGOT_TMP_PATH_WLM}}
	RMDir /REBOOTOK ${{ESCARGOT_TMP_PATH_BASE}}
	DoNothing:
FunctionEnd

Function ErrorOut
	Call CleanUp
	MessageBox MB_OK|MB_ICONEXCLAMATION "An error occurred while attempting to install one or more critical components. Setup will now abort."
	Abort
FunctionEnd

Function DetermineIfOnSupportedOS
	${{If}} ${{AtLeastWinXP}}
		${{If}} ${{AtLeastWinVista}}
			Push 1
			Pop $OnSupportedOS
		${{EndIf}}
		
		${{If}} ${{IsWinXP}}
		${{AndIf}} ${{AtLeastServicePack}} 2
			Push 1
			Pop $OnSupportedOS
		${{EndIf}}
	${{EndIf}}
FunctionEnd

Function .onInit
	!insertmacro CHECK_MUTEX CheckOS
	
	; Do OS checks
	CheckOS:
		Call DetermineIfOnSupportedOS
		
		${{If}} $OnSupportedOS == 1
			${{If}} ${{IsWinXP}}
				MessageBox MB_YESNO|MB_ICONEXCLAMATION "This installer is only recommended for usage on Windows Vista and higher due to issues with reliably using ${{WLM_VERSION_NAME}} on Windows XP for the time being. Do you wish to continue installation regardless?" IDYES Continue
				Quit
			${{EndIf}}
		${{Else}}
			MessageBox MB_OK|MB_ICONSTOP "Setup requires Windows XP SP2 and above to install."
			Quit
		${{EndIf}}
	Continue:
FunctionEnd

Function un.onInit
	!insertmacro CHECK_MUTEX Uninstall_Main
	
	Uninstall_Main:
		; OS detection doesn't work with uninstallers since for some reason Windows 95 compatibility mode is set on them. Just wing it.
		System::Call "msi::MsiGetProductInfo(t '${{WLM_PRODUCT_CODE}}', t '${{MSI_PROPERTY_PACKAGECODE}}', t .r0, *i ${{NSIS_MAX_STRLEN}}) i.r1"
		${{If}} $0 == ""
			MessageBox MB_OK|MB_ICONSTOP "Setup could not detect the appropriate version of ${{WLM_PRODUCT_NAME}} to uninstall on your system. You may have already uninstalled ${{WLM_PRODUCT_NAME}} through Windows Live Essentials or it isn't installed on your machine."
			Quit
		${{EndIf}}
FunctionEnd
