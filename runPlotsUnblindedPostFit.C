void runPlotsUnblindedPostFit(){

  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  gROOT->LoadMacro("postFitPlots.C");
  gROOT->LoadMacro("postFitPlotsEle.C");
  gROOT->LoadMacro("postFitPlotsETauHad.C");
  gROOT->LoadMacro("postFitPlotsEMu.C");

  gStyle->SetOptStat(0);


postFitPlotsETauHad("ehad_GG_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","shapesETau0Jet.root","mlfit.root","ETauMarch12Mlfit","gg0etau","shapes_fit_s/datacard_et_0","shapes_fit_s/datacard_et_0",true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1200,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_Boost_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","shapesETau1Jet.root","mlfit.root","ETauMarch12Mlfit","boostetau","shapes_fit_s/datacard_et_1", "shapes_fit_s/datacard_et_1", true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  220,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_VBF_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","shapesETau2Jet.root","mlfit.root","ETauMarch12Mlfit","vbfetau","shapes_fit_s/datacard_et_2", "shapes_fit_s/datacard_et_2",true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  40,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,true);
postFitPlotsETauHad("ehad_GG_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","shapesETau0Jet.root","mlfit.root","ETauMarch12Mlfit","gg0etau","shapes_fit_s/datacard_et_0","shapes_prefit/datacard_et_0",true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1200,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_Boost_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","shapesETau1Jet.root","mlfit.root","ETauMarch12Mlfit","boostetau","shapes_fit_s/datacard_et_1", "shapes_prefit/datacard_et_1", true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  220,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_VBF_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","shapesETau2Jet.root","mlfit.root","ETauMarch12Mlfit","vbfetau","shapes_fit_s/datacard_et_2", "shapes_prefit/datacard_et_2",true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  40,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,true);
postFitPlotsETauHad("ehad_GG_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","shapesETau0Jet.root","mlfit.root","ETauMarch12Mlfit","gg0etau","shapes_prefit/datacard_et_0","shapes_prefit/datacard_et_0",false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1200,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_Boost_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","shapesETau1Jet.root","mlfit.root","ETauMarch12Mlfit","boostetau","shapes_prefit/datacard_et_1", "shapes_prefit/datacard_et_1", false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  220,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_VBF_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","shapesETau2Jet.root","mlfit.root","ETauMarch12Mlfit","vbfetau","shapes_prefit/datacard_et_2", "shapes_prefit/datacard_et_2",false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  40,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,true);


postFitPlotsEMu("emu_GG_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","gg0etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg0etau_mu","shapes_fit_s/gg0etau_mu_datacard", "shapes_fit_s/gg0etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  100);
postFitPlotsEMu("emu_Boost_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","gg1etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg1etau_mu","shapes_fit_s/gg1etau_mu_datacard", "shapes_fit_s/gg1etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau){#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  140);
postFitPlotsEMu("emu_VBF_m_colinear_UNBLIND_PostFit_PostfitSignal","ETauMarch12Mlfit","gg2etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg2etau_mu","shapes_fit_s/gg2etau_mu_datacard", "shapes_fit_s/gg2etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1
                  );
postFitPlotsEMu("emu_GG_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","gg0etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg0etau_mu","shapes_fit_s/gg0etau_mu_datacard", "shapes_fit_s/gg0etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  100);
postFitPlotsEMu("emu_Boost_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","gg1etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg1etau_mu","shapes_fit_s/gg1etau_mu_datacard", "shapes_prefit/gg1etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau){#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  140);
postFitPlotsEMu("emu_VBF_m_colinear_UNBLIND_PostFit_PrefitSignal","ETauMarch12Mlfit","gg2etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg2etau_mu","shapes_fit_s/gg2etau_mu_datacard", "shapes_prefit/gg2etau_mu_datacard",true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1
                  );
postFitPlotsEMu("emu_GG_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","gg0etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg0etau_mu","shapes_prefit/gg0etau_mu_datacard", "shapes_prefit/gg0etau_mu_datacard",false,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  100);

postFitPlotsEMu("emu_Boost_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","gg1etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg1etau_mu","shapes_prefit/gg1etau_mu_datacard", "shapes_prefit/gg1etau_mu_datacard",false,
                 500, 500, false,
                 "M(e#tau){#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  140);
postFitPlotsEMu("emu_VBF_m_colinear_UNBLIND_Selection_Prefit","ETauMarch12Mlfit","gg2etau_mu_rootfile.root","mlfit.root","ETauMarch12Mlfit","gg2etau_mu","shapes_prefit/gg2etau_mu_datacard", "shapes_prefit/gg2etau_mu_datacard",false,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1
                  );



/*
postFitPlots("muhad_GG_m_colinear_UNBLIND_PostFit","jespfMetOct7","LFV_gg0_collMass_fakeRate_zjetsEmbed_newSignal.root","mlfit.root","outCombinedFitsAll","vbfmutau","shapes_fit_s/datacard_gg0_pfMetFixOldjesNewFakeShape", true,
                 500, 500, false,
                 "M(#mu#atau_{h})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  -1,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",true,false);
*/
/*
postFitPlots("muhad_Boost_m_colinear_UNBLIND_PostFit","jespfMetOct7","LFV_gg1_collMass_fakeRate_zjetsEmbed_newSignal.root","mlfit.root","outCombinedFitsAll","vbfmutau","shapes_fit_s/datacard_gg1_pfMetFixOldjesNewFakeShape", true,
                 500, 500, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1,false,
                  0.60, 0.9, 0.9, 0.5);

postFitPlots("muhad_VBF_m_colinear_UNBLIND_PostFit","jespfMetOct7","LFV_vbf_collMass_fakeRate_zjetsEmbed_newSignal.root","mlfit.root","outCombinedFitsAll","vbfmutau","shapes_fit_s/datacard_vbf_pfMetFixOldjesNewFakeShape",true,
                 500, 500, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 50 GeV", "#mu#tau_{h} 2-Jet",
                  0, 300, -0.95,1.45,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1,
                   false,  "ONLYHIGGS_2Jets.root",true);


postFitPlotsEle("muele_GG_m_colinear_UNBLIND_PostFit","CombinedPlots20","GGF_rootfile.root","mlfit.root","outCombinedFitsAll","GGF","shapes_fit_s/datacard_MuEle_0Jet", true,
                 100, 150, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{e} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
		  60);

postFitPlotsEle("muele_Boost_m_colinear_UNBLIND_PostFit","CombinedPlots20","Boost_rootfile.root","mlfit.root","UnblindNEW","Boost","shapes_fit_s/datacard_MuEle_1Jet", true,
                 100, 150, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{e} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
		  70);

postFitPlotsEle("muele_VBF_m_colinear_UNBLIND_PostFit","CombinedPlots20","VBF_rootfile.root","mlfit.root","UnblindNEW","VBF","shapes_fit_s/datacard_MuEle_2Jet", true,
                 100, 150, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 20 GeV", "#mu#tau_{e} 2-Jet",
			  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
	          9);

postFitPlots("muhad_GG_m_colinear_UNBLIND_PostFitBadMET","jesnonesignalJune18_VHVV","LFV_gg0_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone_singletfix.root","mlfit.root","outPAS","vbfmutau","shapes_fit_s/datacard_MuTau_0Jet_new", true,
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV",
                  75, 350, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  -1,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",true,false);

postFitPlots("muhad_Boost_m_colinear_UNBLIND_PostFitBadMET","jesnonesignalJune18_VHVV","LFV_gg1_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone_singletfix.root","mlfit.root","outPAS","vbfmutau","shapes_fit_s/datacard_MuTau_1Jet_new", true,
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV",
                  0, 350, -0.95,0.95,1,false,
                  0.60, 0.9, 0.9, 0.5);

postFitPlots("muhad_VBF_m_colinear_UNBLIND_PostFitBadMET","jesnonesignalJune18_VHVV","LFV_vbf_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone_singletfix.root","mlfit.root","outPAS","vbfmutau","shapes_fit_s/datacard_MuTau_2Jet_new",true,
                 100, 150, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 50 GeV",
                  0, 349, -0.95,1.45,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1,
                   false,  "ONLYHIGGS_2Jets.root",true);
*/
}

