void runPlotsPreFitFromFit(){

	  gROOT->LoadMacro("tdrstyle.C");
	  setTDRStyle();
	  gROOT->LoadMacro("postFitPlots.C");
	  gROOT->LoadMacro("postFitPlotsEle.C");

	  gStyle->SetOptStat(0);


postFitPlots("muhad_GG_m_colinear_UNBLIND_PreFitNew","LFV_gg0_jesshape_tesshape_uesshape_fakesshape_binshape.root","mlfit.root","UnblindNEW","gg0mutau","shapes_prefit/datacard_gg0_pfMetFixOldjesNewFakeShape", true,
                 100, 160, true,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV",
                  75, 350, -0.95,0.95,1, false,
                  0.60, 0.9, 0.9, 0.5);

postFitPlots("muhad_Boost_m_colinear_UNBLIND_PreFitNew","LFV_gg1_jesshape_tesshape_uesshape_fakesshape_binshape.root","mlfit.root","UnblindNEW","boostmutau","shapes_prefit/datacard_gg1_pfMetFixOldjesNewFakeShape", true,
                 100, 160, true,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 10 GeV",
                  0, 350, -0.95,0.95,1,false,
                  0.60, 0.9, 0.9, 0.5);

postFitPlots("muhad_VBF_m_colinear_UNBLIND_PreFitNew","LFV_vbf_jesshape_tesshape_uesshape_fakesshape_binshape.root","mlfit.root","UnblindNEW","vbfmutau","shapes_prefit/datacard_vbf_pfMetFixOldjesNewFakeShape",true,
                 100, 150, true,
                 "M(#mu#tau_{h})_{col} [GeV]", "Events / 50 GeV",
                  0, 349, -0.95,1.45,1, false,
                  0.60, 0.9, 0.9, 0.5,
                  20,-1,-1,
                   true,  "ONLYHIGGS_2Jets.root",true);
}
