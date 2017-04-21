using System;
using Microsoft.Win32;
using System.ComponentModel;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace msn_patcher {
	struct State {
		public string Nexus;
		public string MSNP;
		public bool IsMulti;
	}

	public partial class MainForm : Form {
		private const string MSN_SERVER_KEY = @"HKEY_CURRENT_USER\SOFTWARE\Microsoft\MessengerService";

		private bool dirty;
		private string exefile;
		private MSNInfo exeinfo;
		private State exestate;
		private State uistate;

		public MainForm() {
			InitializeComponent();
			this.clearState();
			this.syncToUI();
		}
    
		private void clearState() {
			this.dirty = false;
			this.exefile = "";
			this.exeinfo = null;
			this.uistate.Nexus = "";
			this.uistate.MSNP = "";
			this.uistate.IsMulti = false;
			this.exestate = this.uistate;
		}

		private void syncToUI() {
			var enabled = (this.exeinfo != null);
			if (enabled) {
				this.txtVersion.Text = this.exeinfo.Version;
			} else {
				this.txtVersion.Text = "No file selected";
			}

			this.txtNexus.Text = (this.exeinfo != null && this.exeinfo.HasNexus ? this.uistate.Nexus : "N/A");
			this.txtMsnp.Text = (this.exeinfo != null && this.exeinfo.HasMSNP ? this.uistate.MSNP : "N/A");
			this.chkMulti.Checked = this.uistate.IsMulti;

			this.txtNexus.Enabled = enabled && this.exeinfo.HasNexus;
			this.txtMsnp.Enabled = enabled && this.exeinfo.HasMSNP;
			this.chkMulti.Enabled = enabled && this.exeinfo.HasMulti;
			this.btnPatch.Enabled = enabled && this.dirty;
			this.btnServEscargot.Enabled = enabled;
			this.btnServOrig.Enabled = enabled;
			this.btnServDev.Enabled = enabled;

			if (enabled && !this.dirty) {
				this.btnPatch.Text = "No changes made.";
			} else {
				this.btnPatch.Text = "Patch";
			}
		}

		private void onModified() {
			this.dirty = this.calcIsDirty();
			this.syncToUI();
		}

		private bool calcIsDirty() {
			if (this.exeinfo == null) return false;
			if (this.uistate.Nexus != this.exestate.Nexus && this.exeinfo.HasNexus) return true;
			if (this.uistate.MSNP != this.exestate.MSNP && this.exeinfo.HasMSNP) return true;
			if (this.uistate.IsMulti != this.exestate.IsMulti && this.exeinfo.HasMulti) return true;
			return false;
		}

		private void btnChoose_Click(object sender, EventArgs e) {
			this.openFileDialog.ShowDialog();
		}

		private void openFileDialog_FileOk(object sender, CancelEventArgs e) {
			var fn = this.openFileDialog.FileName;
			var vi = FileVersionInfo.GetVersionInfo(fn);
			var v = vi.FileVersion;
			if (string.IsNullOrEmpty(v)) {
				this.err("Invalid choice", "Please select msnmsgr.exe or msmsgs.exe");
				return;
			}

			var mi = MSNInfo.Get(v);
			if (mi == null) {
				this.err("Unknown version", string.Format("Version \"{0}\" is not in the database. Cannot patch.", v));
				return;
			}

			this.exefile = fn;
			this.exeinfo = mi;
			var dst = new byte[100];
			using (var s = new FileStream(fn, FileMode.Open, FileAccess.Read, FileShare.ReadWrite)) {
				if (mi.OffsetNexus >= 0) {
					s.Seek(mi.OffsetNexus, SeekOrigin.Begin);
					int l = s.Read(dst, 0, 40);
					var s1 = Encoding.ASCII.GetString(dst, 0, l);
					this.exestate.Nexus = s1;
					this.txtNexus.MaxLength = 40;
				} else {
					this.txtNexus.Text = "N/A";
				}

				if (mi.OffsetMSNP >= 0) {
					s.Seek(mi.OffsetMSNP, SeekOrigin.Begin);
					int l = s.Read(dst, 0, 21);
					var s1 = Encoding.ASCII.GetString(dst, 0, l);
					this.exestate.MSNP = s1;
					this.txtMsnp.MaxLength = 21;
				} else if (mi.UsesRegistry) {
					var serv = Registry.GetValue(MSN_SERVER_KEY, "Server", null) as string;
					if (serv == null) serv = "";
					this.exestate.MSNP = serv;
					this.txtMsnp.MaxLength = 50;
				} else {
					this.txtMsnp.Text = "N/A";
				}

				if (mi.OffsetMulti >= 0) {
					s.Seek(mi.OffsetMulti, SeekOrigin.Begin);
					var b = s.ReadByte();
					if ((b | 1) != '\xb7') {
						this.err("Unexpected multi byte", "The patcher encountered something unexpected in this file.");
						return;
					}
					this.exestate.IsMulti = (b == '\xb6');
				}
			}

			this.uistate = this.exestate;
			this.syncToUI();
		}

		private void err(string title, string msg, bool clear = true) {
			MessageBox.Show(msg, title, MessageBoxButtons.OK, MessageBoxIcon.Warning);
			if (clear) {
				this.clearState();
				this.syncToUI();
			}
		}

		private void btnPatch_Click(object sender, EventArgs e) {
			var fn = this.exefile;
			var mi = this.exeinfo;
			if (mi == null || string.IsNullOrEmpty(fn)) return;

			try {
				using (var s = new FileStream(fn, FileMode.Open, FileAccess.Write, FileShare.None)) {
					if (mi.HasNexus) {
						// TODO: Actually patch
					}

					if (mi.HasMSNP && !mi.UsesRegistry) {
						// TODO: Actually patch
					}

					if (mi.HasMulti) {
						// TODO: Actually patch
					}
				}

				if (mi.HasMSNP && mi.UsesRegistry) {
					Registry.SetValue(MSN_SERVER_KEY, "Server", this.uistate.MSNP);
				}
			} catch (UnauthorizedAccessException) {
				this.err("Cannot patch", "Please re-run patcher as Administrator", clear: false);
				return;
			} catch (IOException) {
				this.err("File in use", "File is in use. Close MSN and try again.", clear: false);
				return;
			}

			this.exestate = this.uistate;
			this.onModified();
		}

		private void chkMulti_CheckedChanged(object sender, EventArgs e) {
			this.uistate.IsMulti = this.chkMulti.Checked;
			this.onModified();
		}

		private void txtNexus_TextChanged(object sender, EventArgs e) {
			this.uistate.Nexus = this.txtNexus.Text;
			this.onModified();
		}

		private void txtMsnp_TextChanged(object sender, EventArgs e) {
			this.uistate.MSNP = this.txtMsnp.Text;
			this.onModified();
		}

		private void btnServEscargot_Click(object sender, EventArgs e) {
			this.uistate.Nexus = "https://m1.escargot.log1p.xyz/nexus-mock";
			this.uistate.MSNP = "m1.escargot.log1p.xyz";
			this.onModified();
		}

		private void btnServOrig_Click(object sender, EventArgs e) {
			this.uistate.Nexus = "https://nexus.passport.com/rdr/pprdr.asp";
			this.uistate.MSNP = "messenger.hotmail.com";
			this.onModified();
		}

		private void btnServDev_Click(object sender, EventArgs e) {
			this.uistate.Nexus = "https://m1.escargot.log1p.xyz/nexusdevel";
			this.uistate.MSNP = "messengerx-localho.st";
			this.onModified();
		}
	}
}
