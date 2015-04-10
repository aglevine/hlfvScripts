void runFakes(){

  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  gROOT->LoadMacro("plotsNoFitEleBand.C");
  gROOT->LoadMacro("plotsNoFitBand.C");

  gStyle->SetOptStat(0);

plotsNoFitEleBand("fakesEle","GGF_fr_rootfile2.root","GGF_fr_rootfile2.root","MuEleControl","GGF","GGF",false,
			100,150,false,"M(#mu#tau_{e})_{col} [GeV]", "Events / 10 GeV",
			0,300,
			 -0.95,0.95,1, true,
                  	0.5, 0.93, 0.9, 0.53,300);

plotsNoFitBand(false,"fakes","LFV_ssgg0_collMass_fakeRate_zjetsEmbed_newSignal.root","preselection_Nov9_SSFakes","vbfmutau",
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV",
                  0, 300, 1, true,
                  0.5, 0.93, 0.9, 0.53,
		  -1,0.001, 1.,100.0  );


}
