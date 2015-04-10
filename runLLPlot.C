void runLLPlot(){

  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  gROOT->LoadMacro("postFitPlotsLL.C");

  gStyle->SetOptStat(0);


postFitPlotsLL("htaumu_AllChannels_LogSOverSB","dataALLNOREBIN.root","mlfit.root","shapes_fit_s",
		 "Log(S/S+B)","Events",
                  50,299, -0.15,0.15,true,
                  0.65,0.93,0.93,0.62,
                  0.8,5e4,
                   true, true,true,
                   true, true,true,
                        false,
                        false,
                        "#mu#tau_{e}+#mu#tau_{h}");

}
