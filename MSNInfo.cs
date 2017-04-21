using System.Collections.Generic;
using System.Linq;

namespace msn_patcher {
	class MSNInfo {
		public static MSNInfo Get(string v) {
			MSNInfo mi;
			if (BY_VERSION.TryGetValue(v, out mi)) return mi;
			return null;
		}

		private static MSNInfo[] ALL = new MSNInfo[] {
			new MSNInfo("1.0.0863",  0x263ce),
			new MSNInfo("2.0.0083",  0x2acef),
			new MSNInfo("2.0.0085",  0x2ad07),
			new MSNInfo("2.2.1053",  0x17160),
			new MSNInfo("3.0.0286",  0x1f234),
			new MSNInfo("3.5.0077",  0x30389),
			new MSNInfo("3.6.0025",  0x2f82d),
			new MSNInfo("4.5.0121",  0x4e692),
			new MSNInfo("4.6.0073",  0x1e794),
			new MSNInfo("4.6.0083",  0x2b9c4),
			new MSNInfo("5.0.0544",  0x46739, 0x655a0,  0xf048),
			new MSNInfo("6.0.0602",  0xccbf2, 0x1f164, 0x1f238),
			new MSNInfo("6.2.0137",  0xdffe1, 0x22ce0, 0x22d68),
			new MSNInfo("7.0.0777", 0x1406b1, 0x2cd80, 0x2ce18),
			new MSNInfo("7.0.0813", 0x147079, 0x2d098, 0x2d140),
			new MSNInfo("7.0.0820", 0x147112, 0x2cfb8, 0x2d060),
			new MSNInfo("7.5.0311", 0x157607, 0x2e8f8, 0x2e9b8),
		};
		private static IDictionary<string, MSNInfo> BY_VERSION;

		static MSNInfo() {
			BY_VERSION = ALL.ToDictionary(x => x.Version, x => x);
		}

		public readonly string Version;
		public readonly int OffsetNexus;
		public readonly int OffsetMSNP;
		public readonly int OffsetMulti;
		public readonly bool UsesRegistry;
		public readonly bool HasNexus;
		public readonly bool HasMSNP;
		public readonly bool HasMulti;

		private MSNInfo(string v, int multi, int nx = -1, int msn = -1) {
			this.Version = v;
			this.OffsetNexus = nx;
			this.OffsetMSNP = msn;
			this.OffsetMulti = multi;
			this.UsesRegistry = (v[1] == '.') && (v[0] < '5');
			this.HasNexus = (nx >= 0);
			this.HasMSNP = (msn >= 0 || this.UsesRegistry);
			this.HasMulti = (multi >= 0);
		}
	}
}
