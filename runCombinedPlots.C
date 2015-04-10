void runCombinedPlots(){

  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  gROOT->LoadMacro("postFitPlotsCOMBINEINSERT.C");

  gStyle->SetOptStat(0);


postFitPlotsCOMBINEINSERT("htaumu_AllChannels_WeightedGlobal","LFV_gg0_pfMetFixOldjesNewFakeShape.root","LFV_gg1_pfMetFixOldjesNewFakeShape.root","LFV_vbf_pfMetFixOldjesNewFakeShape.root","GGF_rootfile.root","Boost_rootfile.root","VBF_rootfile.root","mlfit20.root","shapes_fit_s",
                 "M(#mu#tau)_{col} [GeV]", "S/(S+B) Weighted Events / 20 GeV",
                  50,299, -0.15,0.15,false,
                  .55, 0.92, 0.9, 0.5,
                  -1,-1,
                   true, true,true,
                   true, true,true,
                        true,
                        true,
                        "#mu#tau_{e}+#mu#tau_{h}, weighted", -1, 10);

postFitPlotsCOMBINEINSERT("htaumu_AllChannels_UnWeighted","LFV_gg0_pfMetFixOldjesNewFakeShape.root","LFV_gg1_pfMetFixOldjesNewFakeShape.root","LFV_vbf_pfMetFixOldjesNewFakeShape.root","GGF_rootfile.root","Boost_rootfile.root","VBF_rootfile.root","mlfit20.root","shapes_fit_s",
                 "M(#mu#tau)_{col} [GeV]", "Events / 20 GeV",
                  50,299, -0.95,0.95,false,
                  0.55, 0.92, 0.9, 0.5,
                  -1,-1,
                   true, true,true,
                   true, true,true,
                        true,
                        false,
			"#mu#tau_{e}+#mu#tau_{h}");
}

/*
postFitPlotsCOMBINEINSERT("htaumu_AllChannels_WeightedGlobal","LFV_gg0_jesshape_tesshape_uesshape_fakesshape_binshape.root","LFV_gg1_jesshape_tesshape_uesshape_fakesshape_binshape.root","LFV_vbf_20PAS.root","GGF_rootfile.root","Boost_rootfile.root","VBF_rootfile.root","mlfit20.root","shapes_fit_s",
                 "M(#mu#tau)_{col} [GeV]", "S/(S+B) Weighted Events / 20 GeV",
                  50,299, -0.15,0.15,false,
                  .55, 0.92, 0.9, 0.5,
                  -1,-1,
                   true, true,true,
                   true, true,true,
                        true,
                        true,
                        "#mu#tau_{e}+#mu#tau_{h}, weighted");

postFitPlotsCOMBINEINSERT("htaumu_AllChannels_UnWeighted","LFV_gg0_jesshape_tesshape_uesshape_fakesshape_binshape.root","LFV_gg1_jesshape_tesshape_uesshape_fakesshape_binshape.root","LFV_vbf_PAS20.root","GGF_rootfile.root","Boost_rootfile.root","VBF_rootfile.root","mlfit20.root","shapes_fit_s",
                 "M(#mu#tau)_{col} [GeV]", "Events / 20 GeV",
                  50,299, -0.95,0.95,false,
                  0.55, 0.92, 0.9, 0.5,
                  -1,-1,
                   true, true,true,
                   true, true,true,
                        true,
                        false,
                        "#mu#tau_{e}+#mu#tau_{h}");
}
*/
