namespace msn_patcher
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
			this.btnChoose = new System.Windows.Forms.Button();
			this.btnPatch = new System.Windows.Forms.Button();
			this.openFileDialog = new System.Windows.Forms.OpenFileDialog();
			this.grpSelect = new System.Windows.Forms.GroupBox();
			this.btnAuto = new System.Windows.Forms.Button();
			this.grpProps = new System.Windows.Forms.GroupBox();
			this.tblProps = new System.Windows.Forms.TableLayoutPanel();
			this.lblMsnp = new System.Windows.Forms.Label();
			this.lblNexus = new System.Windows.Forms.Label();
			this.txtMsnp = new System.Windows.Forms.TextBox();
			this.txtNexus = new System.Windows.Forms.TextBox();
			this.lblVersion = new System.Windows.Forms.Label();
			this.txtVersion = new System.Windows.Forms.Label();
			this.lblMulti = new System.Windows.Forms.Label();
			this.chkMulti = new System.Windows.Forms.CheckBox();
			this.grpServ = new System.Windows.Forms.GroupBox();
			this.tblServ = new System.Windows.Forms.TableLayoutPanel();
			this.btnServEscargot = new System.Windows.Forms.Button();
			this.btnServOrig = new System.Windows.Forms.Button();
			this.grpApply = new System.Windows.Forms.GroupBox();
			this.btnServDev = new System.Windows.Forms.Button();
			this.grpSelect.SuspendLayout();
			this.grpProps.SuspendLayout();
			this.tblProps.SuspendLayout();
			this.grpServ.SuspendLayout();
			this.tblServ.SuspendLayout();
			this.grpApply.SuspendLayout();
			this.SuspendLayout();
			// 
			// btnChoose
			// 
			this.btnChoose.Dock = System.Windows.Forms.DockStyle.Right;
			this.btnChoose.Location = new System.Drawing.Point(253, 16);
			this.btnChoose.Name = "btnChoose";
			this.btnChoose.Size = new System.Drawing.Size(122, 40);
			this.btnChoose.TabIndex = 0;
			this.btnChoose.Text = "Choose File...";
			this.btnChoose.UseVisualStyleBackColor = true;
			this.btnChoose.Click += new System.EventHandler(this.btnChoose_Click);
			// 
			// btnPatch
			// 
			this.btnPatch.Dock = System.Windows.Forms.DockStyle.Fill;
			this.btnPatch.Location = new System.Drawing.Point(3, 16);
			this.btnPatch.Name = "btnPatch";
			this.btnPatch.Size = new System.Drawing.Size(372, 55);
			this.btnPatch.TabIndex = 0;
			this.btnPatch.Text = "Patch";
			this.btnPatch.UseVisualStyleBackColor = true;
			this.btnPatch.Click += new System.EventHandler(this.btnPatch_Click);
			// 
			// openFileDialog
			// 
			this.openFileDialog.DefaultExt = "exe";
			this.openFileDialog.FileName = "openFileDialog1";
			this.openFileDialog.Filter = "Exe files|*.exe";
			this.openFileDialog.FileOk += new System.ComponentModel.CancelEventHandler(this.openFileDialog_FileOk);
			// 
			// grpSelect
			// 
			this.grpSelect.Controls.Add(this.btnAuto);
			this.grpSelect.Controls.Add(this.btnChoose);
			this.grpSelect.Dock = System.Windows.Forms.DockStyle.Top;
			this.grpSelect.Location = new System.Drawing.Point(3, 3);
			this.grpSelect.Name = "grpSelect";
			this.grpSelect.Size = new System.Drawing.Size(378, 59);
			this.grpSelect.TabIndex = 3;
			this.grpSelect.TabStop = false;
			this.grpSelect.Text = "MSN";
			// 
			// btnAuto
			// 
			this.btnAuto.Dock = System.Windows.Forms.DockStyle.Fill;
			this.btnAuto.Location = new System.Drawing.Point(3, 16);
			this.btnAuto.Name = "btnAuto";
			this.btnAuto.Size = new System.Drawing.Size(250, 40);
			this.btnAuto.TabIndex = 1;
			this.btnAuto.Text = "Auto-Find";
			this.btnAuto.UseVisualStyleBackColor = true;
			// 
			// grpProps
			// 
			this.grpProps.Controls.Add(this.tblProps);
			this.grpProps.Dock = System.Windows.Forms.DockStyle.Fill;
			this.grpProps.Location = new System.Drawing.Point(3, 62);
			this.grpProps.Name = "grpProps";
			this.grpProps.Size = new System.Drawing.Size(378, 148);
			this.grpProps.TabIndex = 2;
			this.grpProps.TabStop = false;
			this.grpProps.Text = "Current Properties";
			// 
			// tblProps
			// 
			this.tblProps.ColumnCount = 2;
			this.tblProps.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 20F));
			this.tblProps.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 80F));
			this.tblProps.Controls.Add(this.lblMsnp, 0, 2);
			this.tblProps.Controls.Add(this.lblNexus, 0, 1);
			this.tblProps.Controls.Add(this.txtMsnp, 1, 2);
			this.tblProps.Controls.Add(this.txtNexus, 1, 1);
			this.tblProps.Controls.Add(this.lblVersion, 0, 0);
			this.tblProps.Controls.Add(this.txtVersion, 1, 0);
			this.tblProps.Controls.Add(this.lblMulti, 0, 3);
			this.tblProps.Controls.Add(this.chkMulti, 1, 3);
			this.tblProps.Dock = System.Windows.Forms.DockStyle.Fill;
			this.tblProps.Location = new System.Drawing.Point(3, 16);
			this.tblProps.Name = "tblProps";
			this.tblProps.RowCount = 5;
			this.tblProps.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
			this.tblProps.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
			this.tblProps.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
			this.tblProps.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 25F));
			this.tblProps.RowStyles.Add(new System.Windows.Forms.RowStyle());
			this.tblProps.Size = new System.Drawing.Size(372, 129);
			this.tblProps.TabIndex = 0;
			// 
			// lblMsnp
			// 
			this.lblMsnp.AutoSize = true;
			this.lblMsnp.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lblMsnp.Location = new System.Drawing.Point(3, 50);
			this.lblMsnp.Name = "lblMsnp";
			this.lblMsnp.Size = new System.Drawing.Size(68, 25);
			this.lblMsnp.TabIndex = 4;
			this.lblMsnp.Text = "MSNP";
			this.lblMsnp.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// lblNexus
			// 
			this.lblNexus.AutoSize = true;
			this.lblNexus.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lblNexus.Location = new System.Drawing.Point(3, 25);
			this.lblNexus.Name = "lblNexus";
			this.lblNexus.Size = new System.Drawing.Size(68, 25);
			this.lblNexus.TabIndex = 0;
			this.lblNexus.Text = "Nexus";
			this.lblNexus.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// txtMsnp
			// 
			this.txtMsnp.Dock = System.Windows.Forms.DockStyle.Fill;
			this.txtMsnp.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.txtMsnp.Location = new System.Drawing.Point(77, 53);
			this.txtMsnp.Name = "txtMsnp";
			this.txtMsnp.Size = new System.Drawing.Size(292, 20);
			this.txtMsnp.TabIndex = 3;
			this.txtMsnp.TextChanged += new System.EventHandler(this.txtMsnp_TextChanged);
			// 
			// txtNexus
			// 
			this.txtNexus.Dock = System.Windows.Forms.DockStyle.Fill;
			this.txtNexus.Font = new System.Drawing.Font("Consolas", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
			this.txtNexus.Location = new System.Drawing.Point(77, 28);
			this.txtNexus.Name = "txtNexus";
			this.txtNexus.Size = new System.Drawing.Size(292, 20);
			this.txtNexus.TabIndex = 2;
			this.txtNexus.TextChanged += new System.EventHandler(this.txtNexus_TextChanged);
			// 
			// lblVersion
			// 
			this.lblVersion.AutoSize = true;
			this.lblVersion.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lblVersion.Location = new System.Drawing.Point(3, 0);
			this.lblVersion.Name = "lblVersion";
			this.lblVersion.Size = new System.Drawing.Size(68, 25);
			this.lblVersion.TabIndex = 5;
			this.lblVersion.Text = "Version";
			this.lblVersion.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// txtVersion
			// 
			this.txtVersion.AutoSize = true;
			this.txtVersion.Dock = System.Windows.Forms.DockStyle.Fill;
			this.txtVersion.Location = new System.Drawing.Point(77, 0);
			this.txtVersion.Name = "txtVersion";
			this.txtVersion.Size = new System.Drawing.Size(292, 25);
			this.txtVersion.TabIndex = 6;
			this.txtVersion.Text = "No file selected";
			this.txtVersion.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// lblMulti
			// 
			this.lblMulti.AutoSize = true;
			this.lblMulti.Dock = System.Windows.Forms.DockStyle.Fill;
			this.lblMulti.Location = new System.Drawing.Point(3, 75);
			this.lblMulti.Name = "lblMulti";
			this.lblMulti.Size = new System.Drawing.Size(68, 25);
			this.lblMulti.TabIndex = 7;
			this.lblMulti.Text = "Multi";
			this.lblMulti.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// chkMulti
			// 
			this.chkMulti.AutoSize = true;
			this.chkMulti.Dock = System.Windows.Forms.DockStyle.Fill;
			this.chkMulti.Location = new System.Drawing.Point(77, 78);
			this.chkMulti.Name = "chkMulti";
			this.chkMulti.Size = new System.Drawing.Size(292, 19);
			this.chkMulti.TabIndex = 8;
			this.chkMulti.Text = "Allow multiple instances of MSN?";
			this.chkMulti.UseVisualStyleBackColor = true;
			this.chkMulti.CheckedChanged += new System.EventHandler(this.chkMulti_CheckedChanged);
			// 
			// grpServ
			// 
			this.grpServ.Controls.Add(this.tblServ);
			this.grpServ.Dock = System.Windows.Forms.DockStyle.Bottom;
			this.grpServ.Location = new System.Drawing.Point(3, 210);
			this.grpServ.Name = "grpServ";
			this.grpServ.Size = new System.Drawing.Size(378, 74);
			this.grpServ.TabIndex = 4;
			this.grpServ.TabStop = false;
			this.grpServ.Text = "Server Presets";
			// 
			// tblServ
			// 
			this.tblServ.ColumnCount = 3;
			this.tblServ.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
			this.tblServ.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
			this.tblServ.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 25F));
			this.tblServ.Controls.Add(this.btnServEscargot, 0, 0);
			this.tblServ.Controls.Add(this.btnServOrig, 1, 0);
			this.tblServ.Controls.Add(this.btnServDev, 2, 0);
			this.tblServ.Dock = System.Windows.Forms.DockStyle.Fill;
			this.tblServ.Location = new System.Drawing.Point(3, 16);
			this.tblServ.Name = "tblServ";
			this.tblServ.RowCount = 1;
			this.tblServ.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 100F));
			this.tblServ.Size = new System.Drawing.Size(372, 55);
			this.tblServ.TabIndex = 0;
			// 
			// btnServEscargot
			// 
			this.btnServEscargot.Dock = System.Windows.Forms.DockStyle.Fill;
			this.btnServEscargot.Location = new System.Drawing.Point(3, 3);
			this.btnServEscargot.Name = "btnServEscargot";
			this.btnServEscargot.Size = new System.Drawing.Size(180, 49);
			this.btnServEscargot.TabIndex = 1;
			this.btnServEscargot.Text = "Escargot";
			this.btnServEscargot.UseVisualStyleBackColor = true;
			this.btnServEscargot.Click += new System.EventHandler(this.btnServEscargot_Click);
			// 
			// btnServOrig
			// 
			this.btnServOrig.Dock = System.Windows.Forms.DockStyle.Fill;
			this.btnServOrig.Location = new System.Drawing.Point(189, 3);
			this.btnServOrig.Name = "btnServOrig";
			this.btnServOrig.Size = new System.Drawing.Size(87, 49);
			this.btnServOrig.TabIndex = 0;
			this.btnServOrig.Text = "Original";
			this.btnServOrig.UseVisualStyleBackColor = true;
			this.btnServOrig.Click += new System.EventHandler(this.btnServOrig_Click);
			// 
			// grpApply
			// 
			this.grpApply.Controls.Add(this.btnPatch);
			this.grpApply.Dock = System.Windows.Forms.DockStyle.Bottom;
			this.grpApply.Location = new System.Drawing.Point(3, 284);
			this.grpApply.Name = "grpApply";
			this.grpApply.Size = new System.Drawing.Size(378, 74);
			this.grpApply.TabIndex = 5;
			this.grpApply.TabStop = false;
			this.grpApply.Text = "Apply Changes";
			// 
			// btnServDev
			// 
			this.btnServDev.Dock = System.Windows.Forms.DockStyle.Fill;
			this.btnServDev.Location = new System.Drawing.Point(282, 3);
			this.btnServDev.Name = "btnServDev";
			this.btnServDev.Size = new System.Drawing.Size(87, 49);
			this.btnServDev.TabIndex = 2;
			this.btnServDev.Text = "Dev";
			this.btnServDev.UseVisualStyleBackColor = true;
			this.btnServDev.Click += new System.EventHandler(this.btnServDev_Click);
			// 
			// MainForm
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(384, 361);
			this.Controls.Add(this.grpProps);
			this.Controls.Add(this.grpSelect);
			this.Controls.Add(this.grpServ);
			this.Controls.Add(this.grpApply);
			this.Name = "MainForm";
			this.Padding = new System.Windows.Forms.Padding(3);
			this.Text = "MSN Patcher";
			this.grpSelect.ResumeLayout(false);
			this.grpProps.ResumeLayout(false);
			this.tblProps.ResumeLayout(false);
			this.tblProps.PerformLayout();
			this.grpServ.ResumeLayout(false);
			this.tblServ.ResumeLayout(false);
			this.grpApply.ResumeLayout(false);
			this.ResumeLayout(false);

        }

        #endregion
        private System.Windows.Forms.Button btnChoose;
        private System.Windows.Forms.Button btnPatch;
        private System.Windows.Forms.OpenFileDialog openFileDialog;
		private System.Windows.Forms.GroupBox grpSelect;
		private System.Windows.Forms.Button btnAuto;
		private System.Windows.Forms.GroupBox grpProps;
		private System.Windows.Forms.GroupBox grpServ;
		private System.Windows.Forms.TableLayoutPanel tblServ;
		private System.Windows.Forms.Button btnServOrig;
		private System.Windows.Forms.Button btnServEscargot;
		private System.Windows.Forms.GroupBox grpApply;
		private System.Windows.Forms.TableLayoutPanel tblProps;
		private System.Windows.Forms.Label lblNexus;
		private System.Windows.Forms.TextBox txtMsnp;
		private System.Windows.Forms.TextBox txtNexus;
		private System.Windows.Forms.Label lblMsnp;
		private System.Windows.Forms.Label lblVersion;
		private System.Windows.Forms.Label txtVersion;
		private System.Windows.Forms.Label lblMulti;
		private System.Windows.Forms.CheckBox chkMulti;
		private System.Windows.Forms.Button btnServDev;
	}
}

