## Requirements
* First, install the required packages with `pip install -r requirements.txt`
* You will also need to install [NSIS](https://nsis.sourceforge.io) and the nsProcess [plug-in](https://nsis.sourceforge.io/NsProcess_plugin) to build installers for WLM 2009 and Yahoo! Messenger.

## Usage
### Placing installers
* Run `run_impl.py` in order to create `working-dir` and its subfolders
* Inside `working-dir`, navigate to `input` and place your unpatched MSN or Yahoo installers in their respective folders

### Patching
In this repository's root directory run `run_impl.py` again but as administrator.

#### Windows 11
If you're using Windows 11 that can be done with `sudo python run_impl.py`

#### Other versions
If not, using this Powershell command is recommended: `Start-Process python -ArgumentList ".\run_impl.py" -Verb RunAs`

### Finishing
Your patched installers will be in `working-dir` inside the `final` folder.

## External projects

`msi2xml` is from http://msi2xml.sourceforge.net.

`e_wise` is from https://kannegieser.net/veit/quelle/index_e.htm.

`escargot.dll` is built from https://gitlab.com/escargot-chat/msn-switcher.
