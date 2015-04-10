void runControlPlots(){

  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  gROOT->LoadMacro("plotsNoFitEle.C");

  gStyle->SetOptStat(0);


  gROOT->LoadMacro("plotsNoFit.C");
  gROOT->LoadMacro("plotsNoFitETau.C");
  gROOT->LoadMacro("plotsNoFitNoDataETau.C");
  gROOT->LoadMacro("postFitPlotsETauHad.C");
  gROOT->LoadMacro("postFitPlotsEMu.C");

/*
plotsNoFitNoDataETau(true,"ehad_GG_m_colinear_NODATA_SIGNAL_BR100","mlfit_preselection.root","ETauMlfitsMarch6","shapes_fit_s/datacard_et_0/",
                 400, 500, true,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitNoDataETau(true,"ehad_Boost_m_colinear_NODATA_SIGNAL_BR100","mlfit_preselection.root","ETauMlfitsMarch6","shapes_fit_s/datacard_et_1/",
                 400, 500, true,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitNoDataETau(true,"ehad_VBF_m_colinear_NODATA_SIGNAL_BR100","mlfit_preselection.root","ETauMlfitsMarch6","shapes_fit_s/datacard_et_2/",
                 400, 500, true, 
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
*/
postFitPlotsETauHad("ehad_GG_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","shapesETau0Jet.root","mlfit.root","ETauMarch12PreselMlfit","gg0etau","shapes_fit_s/datacard_et_0","shapes_prefit/datacard_et_0", true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  3700,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_Boost_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","shapesETau1Jet.root","mlfit.root","ETauMarch12PreselMlfit","boostetau","shapes_fit_s/datacard_et_1","shapes_prefit/datacard_et_1", true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1500,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_VBF_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","shapesETau2Jet.root","mlfit.root","ETauMarch12PreselMlfit","vbfetau","shapes_fit_s/datacard_et_2","shapes_prefit/datacard_et_2", true,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  750,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,true);

postFitPlotsETauHad("ehad_GG_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","shapesETau0Jet.root","mlfit.root","ETauMarch12PreselMlfit","gg0etau","shapes_prefit/datacard_et_0","shapes_prefit/datacard_et_0", false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  3700,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_Boost_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","shapesETau1Jet.root","mlfit.root","ETauMarch12PreselMlfit","boostetau","shapes_prefit/datacard_et_1","shapes_prefit/datacard_et_1", false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1500,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,false);
postFitPlotsETauHad("ehad_VBF_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","shapesETau2Jet.root","mlfit.root","ETauMarch12PreselMlfit","vbfetau","shapes_prefit/datacard_et_2","shapes_prefit/datacard_et_2", false,
                 500, 500, false,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  750,-1,-1,
                  false, "ONLYHIGGS_2Jets.root",false,false,true);


postFitPlotsEMu("emu_GG_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","gg0etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg0etau_mu","shapes_fit_s/gg0etau_mu_datacard","shapes_prefit/gg0etau_mu_datacard", true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1000);

postFitPlotsEMu("emu_Boost_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","gg1etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg1etau_mu","shapes_fit_s/gg1etau_mu_datacard","shapes_prefit/gg1etau_mu_datacard", true,
                 500, 500, false,
                 "M(e#tau){#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  700);
postFitPlotsEMu("emu_VBF_m_colinear_Preselection_PostFit","ETauMarch12PreselMlfit","gg2etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg2etau_mu","shapes_fit_s/gg2etau_mu_datacard","shapes_prefit/gg2etau_mu_datacard", true,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  400,-1,-1,
                  -1);
postFitPlotsEMu("emu_GG_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","gg0etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg0etau_mu","shapes_prefit/gg0etau_mu_datacard","shapes_prefit/gg0etau_mu_datacard", false,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 0-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  1000);

postFitPlotsEMu("emu_Boost_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","gg1etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg1etau_mu","shapes_prefit/gg1etau_mu_datacard","shapes_prefit/gg1etau_mu_datacard", false,
                 500, 500, false,
                 "M(e#tau){#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 1-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  700);
postFitPlotsEMu("emu_VBF_m_colinear_Preselection_PreFit","ETauMarch12PreselMlfit","gg2etau_mu_rootfile.root","mlfit.root","ETauMarch12PreselMlfit","gg2etau_mu","shapes_prefit/gg2etau_mu_datacard","shapes_prefit/gg2etau_mu_datacard", false,
                 500, 500, false,
                 "M(e#tau_{#mu})_{col} [GeV]", "Events / 10 GeV", "e#tau_{#mu} 2-Jet",
                  0, 300, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  400,-1,-1,
                  -1);

/*
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_m_colinear_BLINDED_PRESEL_BR100","collmassetau_noData_0j.root","etauFilesFeb6","",
                 100, 160, true,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 0-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_m_colinear_BLINDED_PRESEL_BR100","collmassetau_noData_1j.root","etauFilesFeb6","",
                 100, 160, true,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 10 GeV", "e#tau_{h} 1-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_m_colinear_BLINDED_PRESEL_BR100","collmassetau_noData_2j.root","etauFilesFeb6","",
                 100, 160, true,
                 "M(e#tau_{h})_{col} [GeV]", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_e_Eta_UNBLIND_PRESEL_BR100","eEta_0.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{e}", "Events / 0.5", "e#tau_{h} 0-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  6500,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_e_Eta_UNBLIND_PRESEL_BR100","eEta_1.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{e}", "Events / 0.5", "e#tau_{h} 1-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  2000,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_e_Eta_UNBLIND_PRESEL_BR100","eEta_2.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{e}", "Events / 0.5", "e#tau_{h} 2-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  600,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_e_t_DR_UNBLIND_PRESEL_BR100","e_t_DR_0.root","etauFilesFeb6","",
                 100, 200, true,
                 "#DeltaR_{e#tau}", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 3.2, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_e_t_DR_UNBLIND_PRESEL_BR100","e_t_DR_1.root","etauFilesFeb6","",
                 100, 200, true,
                 "#DeltaR_{e#tau}", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 3.2, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  1200,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_e_t_DR_UNBLIND_PRESEL_BR100","e_t_DR_2.root","etauFilesFeb6","",
                 100, 200, true,
                 "#DeltaR_{e#tau}", "Events / 50 GeV", "e#tau_{h} 2-Jet",
                  0, 3.2, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  500,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_eMtToPfMet_UNBLIND_PRESEL_BR100","eMtToPfMet_0.root","etauFilesFeb6","",
                 300, 400, true,
                 "e M_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_eMtToPfMet_UNBLIND_PRESEL_BR100","eMtToPfMet_1.root","etauFilesFeb6","",
                 300, 400, true,
                 "e M_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_eMtToPfMet_UNBLIND_PRESEL_BR100","eMtToPfMet_2.root","etauFilesFeb6","",
                 300, 400, true,
                 "e M_{T} [GeV]", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_ePt_UNBLIND_PRESEL_BR100","ePt_0.root","etauFilesFeb6","",
                 300, 400, true,
                 "e P_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_ePt_UNBLIND_PRESEL_BR100","ePt_1.root","etauFilesFeb6","",
                 300, 400, true,
                 "e P_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_ePt_UNBLIND_PRESEL_BR100","ePt_2.root","etauFilesFeb6","",
                 300, 400, true,
                 "e P_{T} [GeV]", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_pfMet_Et_UNBLIND_PRESEL_BR100","pfMet_Et_0.root","etauFilesFeb6","",
                 300, 400, true,
                 "MET [GeV]", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_pfMet_Et_UNBLIND_PRESEL_BR100","pfMet_Et_1.root","etauFilesFeb6","",
                 300, 400, true,
                 "MET [GeV]", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_pfMet_Et_UNBLIND_PRESEL_BR100","pfMet_Et_2.root","etauFilesFeb6","",
                 300, 400, true,
                 "MET [GeV]", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_t_Eta_UNBLIND_PRESEL_BR100","tEta_0.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{#tau}", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  6500,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_t_Eta_UNBLIND_PRESEL_BR100","tEta_1.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{#tau}", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  2000,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_t_Eta_UNBLIND_PRESEL_BR100","tEta_2.root","etauFilesFeb6","",
                 100, 200, true,
                 "#eta_{#tau}", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  -2.5, 2.5, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  600,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_tMtToPfMet_UNBLIND_PRESEL_BR100","tMtToPfMet_0.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau M_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_tMtToPfMet_UNBLIND_PRESEL_BR100","tMtToPfMet_1.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau M_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_tMtToPfMet_UNBLIND_PRESEL_BR100","tMtToPfMet_2.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau M_{T} [GeV]", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_GG_tPt_UNBLIND_PRESEL_BR100","tPt_0.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau P_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 0-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_Boost_tPt_UNBLIND_PRESEL_BR100","tPt_1.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau P_{T} [GeV]", "Events / 5 GeV", "e#tau_{h} 1-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);
plotsNoFitETau(true,"etauFilesFeb6/ehad_VBF_tPt_UNBLIND_PRESEL_BR100","tPt_2.root","etauFilesFeb6","",
                 300, 400, true,
                 "#tau P_{T} [GeV]", "Events / 10 GeV", "e#tau_{h} 2-Jet",
                  0, 200, 1, false,
                  0.55, 0.93, 0.9, 0.53,
                  -1,-1);


plotsNoFit(false,"muhad_VBF_m_colinear_UNBLIND_PRESEL_BR100","LFV_vbf_collMass_fakeRate_zjetsEmbed_newSignal.root","preselectionMetFix_Nov2","vbfmutau",
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 20 GeV", "#mu#tau_{h} 2-Jet",
                  0, 300, 1, false,
                  0.55, 0.93, 0.9, 0.53,
		  3000,-1);

plotsNoFit(false,"muhad_GG_m_colinear_UNBLIND_PRESEL_BR100","LFV_gg0_collMass_fakeRate_zjetsEmbed_newSignal.root","preselectionMetFix_Nov2","vbfmutau",
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{h} 0-Jet",
                  0, 300, 1, false,
                  0.55, 0.9, 0.9, 0.5,
                  -1,-1);

plotsNoFit(false,"muhad_Boost_m_colinear_UNBLIND_PRESEL_BR100","LFV_gg1_collMass_fakeRate_zjetsEmbed_newSignal.root","preselectionMetFix_Nov2","vbfmutau",
                 100, 160, false,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{h} 1-Jet",
                  0, 300, 1, false,
                  0.55, 0.9, 0.9, 0.5,
                  -1,-1);

plotsNoFitEle("muele_GG_m_colinear_UNBLIND_PRESEL_BR100","GGF_rootfile.root","GGF_rootfile.root","MuEleControl","GGF","GGF",false,
                 100, 160, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{e} 0-Jet",
                  0, 300, 1, false,
                  0.55, 0.9, 0.9, 0.5,
                  -1,-1,7500);

plotsNoFitEle("muele_Boost_m_colinear_UNBLIND_PRESEL_BR100","Boost_rootfile.root","Boost_rootfile.root","MuEleControl","Boost","Boost",false,
                 100, 160, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 10 GeV", "#mu#tau_{e} 1-Jet",
                  0, 300, 1, false,
                  0.55, 0.9, 0.9, 0.5,
                  -1,-1,2100);

plotsNoFitEle("muele_VBF_m_colinear_UNBLIND_PRESEL_BR100","VBF_rootfile.root","VBF_rootfile.root","MuEleControl","VBF","VBF",false,
                 100, 160, false,
                 "M(#mu#tau_{e})_{col} [GeV]", "Events / 20 GeV", "#mu#tau_{e} 2-Jet",
                  0, 300, 1, false,
                  0.55, 0.9, 0.9, 0.5,
                  -1,-1,800);
*/

}
