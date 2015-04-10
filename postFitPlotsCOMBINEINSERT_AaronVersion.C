void postFitPlotsCOMBINEINSERT(TString name="collMass",TString fileDataMuHad0Jet="asdf", TString fileDataMuHad1Jet = "asdf", TString fileDataMuHad2Jet = "asdf", TString fileDataMuEle0Jet = "asdf", TString fileDataMuEle1Jet = "asdf", TString fileDataMuEle2Jet = "asdf", TString file="fit2_signalV5_collMass_type1.root", TString dirInternal="filesBoosted", TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", double xmin=200, double xmax=300, double ymin=-2, double ymax=2, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1, double MIN=-1, bool mutau0=true, bool mutau1=true, bool mutau2=true, bool muele0=true, bool muele1=true, bool muele2=true, bool REBIN=true, bool weightSOverSB=true,TString channelName="#mu#tau", double minsubs=-1, double maxsubs=-1){


	gROOT->LoadMacro("tdrstyle.C");
	setTDRStyle();
	double kForPlotting=1;
	double branchingratioTauTau=0.063;
	double branchingratioTauMu=0.1;
	double Lumi=19717;

	gROOT->LoadMacro("CMS_lumi.C");
	writeExtraText = false;
	int iPeriod = 2;
	// second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
	int iPos=11;// : top-left, left-aligned
	// iPos=33 : top-right, right-aligned
	// iPos=22 : center, centered
	// mode generally :
	//   iPos = 10*(alignement 1/2/3) + position (1/2/3 = left/center/right)
	//  example_plot( iPeriod, 11 );  // left-aligned
	//  example_plot( iPeriod, 33 );  // right-aligned
	//  example_plot( iPeriod, 0 );   // out of frame (in exceptional cases)
	//  example_plot( iPeriod, 11 );  // default: left-aligned
	//  example_plot( iPeriod, 22 );  // centered
	//  example_plot( iPeriod, 33 );  // right-aligned


	bool muonchannels[3]={mutau0,mutau1,mutau2};
	bool elechannels[3]={muele0,muele1,muele2};

	int NBins=30; 
	if(mutau2 || muele2 || REBIN) { REBIN=true; NBins=15;}

	TFile *_fileMC= new TFile("CombinedPlots20PAS/"+file);
	TFile *_fileDataMuHad0Jet= new TFile("CombinedPlots20PAS/"+fileDataMuHad0Jet);
        TFile *_fileDataMuHad1Jet= new TFile("CombinedPlots20PAS/"+fileDataMuHad1Jet);
        TFile *_fileDataMuHad2Jet= new TFile("CombinedPlots20PAS/"+fileDataMuHad2Jet);
        TFile *_fileDataMuEle0Jet= new TFile("CombinedPlots20PAS/"+fileDataMuEle0Jet);
        TFile *_fileDataMuEle1Jet= new TFile("CombinedPlots20PAS/"+fileDataMuEle1Jet);
        TFile *_fileDataMuEle2Jet= new TFile("CombinedPlots20PAS/"+fileDataMuEle2Jet);


	//TString dirInternalAllMU[3]={dirInternal+"/datacard_gg0_pfMetFixOldjesNewFakeShape",dirInternal+"/datacard_gg1_pfMetFixOldjesNewFakeShape", dirInternal+"/datacard_vbf20_pfMetFixOldjesNewFakeShape"};
        TString dirInternalAllMU[3]={dirInternal+"/datacard_MuTau_0Jet_new",dirInternal+"/datacard_MuTau_1Jet_new", dirInternal+"/datacard_vbf_PAS20"};
	TString dirInternalAllELE[3]={dirInternal+"/datacard_MuEle_0Jet",dirInternal+"/datacard_MuEle_1Jet", dirInternal+"/datacard_MuEle_2Jet"};

	TString dirInternalSignal="shapes_prefit";

	TH1F* hdata_obs = new TH1F("hdata_obs","",NBins,0,300);
	TH1F* hFAKES = new TH1F("hFAKES","",NBins,0,300);
	TH1F* hFAKESLEPTON = new TH1F("hFAKESLEPTON","",NBins,0,300);
	TH1F* hDY = new TH1F("hDY","",NBins,0,300);
	TH1F* hWW = new TH1F("hWW","",NBins,0,300);
	TH1F* hTOP = new TH1F("hTOP","",NBins,0,300);
	TH1F* hTT = new TH1F("hTT","",NBins,0,300);
	TH1F* hZTauTau = new TH1F("hZTauTau","",NBins,0,300);
	TH1F* hLFVVBF126 = new TH1F("hLFVVBF126","",NBins,0,300);
	TH1F* hSMVBF126 = new TH1F("hSMVBF126","",NBins,0,300);
	TH1F* hSMHWWVBF126 = new TH1F("hSMHWWVBF126","",NBins,0,300);
	TH1F* hLFVGG126 = new TH1F("hLFVGG126","",NBins,0,300);
	TH1F* hSMGG126 = new TH1F("hSMGG126","",NBins,0,300);
	TH1F* hSMHWWGG126 = new TH1F("hSMHWWGG126","",NBins,0,300);
	TH1F* hWGamma = new TH1F("hWGamma","",NBins,0,300);
	TH1F* hWGammaStar = new TH1F("hWGammaStar","",NBins,0,300);

	double weightMuTau[3]={1,1,1};
	double weightMuEle[3]={1,1,1};

	int binA=hdata_obs->FindBin(100);
	int binB=hdata_obs->FindBin(150);

	for (int i=0; i<3; i++){
		cout << "starting" << i <<endl;
		if(muonchannels[i]!=true) continue;
		TH1F *hFAKES_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/fakes");hFAKES_2->SetName("fakesHisto");
		TString Extra="/zjetsother";
		if(i==2) Extra="/fakes"; // in the postfit directory the DY for VBF is not saved, since it has 0 events
		TH1F *hDY_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+Extra); hDY_2->SetName("dyHisto");
		TH1F *hWW_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/ww");
		TH1F *hTOP_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/singlet");
		TH1F *hTT_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/ttbar");
		TH1F *hZTauTau_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/ztautau");
		TH1F *hLFVVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/LFVVBF");
		TH1F *hLFVGG126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/LFVGG");
		TH1F *hSMGG126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/SMGG126");
		TH1F *hSMVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/SMVBF126");
		Extra="/fakes";
		if(i!=0) Extra="/WWGG126";
		TH1F *hSMHWWGG126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+Extra); hSMHWWGG126_2->SetName("smwwgg");
		if(i==0) hSMHWWGG126_2->Scale(0);
		TH1F *hSMHWWVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/WWVBF126"); hSMHWWVBF126_2->SetName("wwsm");
		cout << "got histos" << endl;
		if(i!=2 && (REBIN)) {
			hFAKES_2->Rebin(2); hDY_2->Rebin(2); hWW_2->Rebin(2); hTOP_2->Rebin(2); hTT_2->Rebin(2); hZTauTau_2->Rebin(2);
			hLFVVBF126_2->Rebin(2); hLFVGG126_2->Rebin(2); hSMGG126_2->Rebin(2); hSMVBF126_2->Rebin(2);
			hSMHWWVBF126_2->Rebin(2);
			if(i!=0) hSMHWWGG126_2->Rebin(2);
		}

		// WEIGHT	
		double bckg=hWW_2->Integral(binA,binB)+hFAKES_2->Integral(binA,binB) + hTOP_2->Integral(binA,binB) + hTT_2->Integral(binA,binB) + hZTauTau_2->Integral(binA,binB);
		bckg+=hSMVBF126_2->Integral(binA,binB)+hSMGG126_2->Integral(binA,binB)+hSMHWWVBF126_2->Integral(binA,binB);
		if(i!=2) bckg+=hDY_2->Integral(binA,binB);
		else hDY_2->Scale(0);
		if(i!=0) bckg+=hSMHWWGG126_2->Integral(binA,binB);
		else hSMHWWGG126_2->Scale(0);

		double signal=hLFVGG126_2->Integral(binA,binB)+hLFVVBF126_2->Integral(binA,binB);

		weightMuTau[i]=signal/(signal+bckg);
		cout<<"Weighting MuTau Channel  "<<i<<" --> "<<weightMuTau[i]<<endl;

		if(weightSOverSB){
			hFAKES_2->Scale(weightMuTau[i]);
			hDY_2->Scale(weightMuTau[i]);
			hWW_2->Scale(weightMuTau[i]);
			hTOP_2->Scale(weightMuTau[i]);
			hTT_2->Scale(weightMuTau[i]);
			hZTauTau_2->Scale(weightMuTau[i]);
			hLFVVBF126_2->Scale(weightMuTau[i]);
			hLFVGG126_2->Scale(weightMuTau[i]);
			hSMVBF126_2->Scale(weightMuTau[i]);
			hSMGG126_2->Scale(weightMuTau[i]);
			hSMHWWVBF126_2->Scale(weightMuTau[i]);
			hSMHWWGG126_2->Scale(weightMuTau[i]);
		}

		// MERGE

		fillNewHisto(hFAKES,hFAKES_2);
		if(i!=2) fillNewHisto(hDY,hDY_2);
		fillNewHisto(hWW,hWW_2);
		fillNewHisto(hTOP,hTOP_2);
		fillNewHisto(hTT,hTT_2);
		fillNewHisto(hZTauTau,hZTauTau_2);
		fillNewHisto(hLFVVBF126,hLFVVBF126_2);
		fillNewHisto(hLFVGG126,hLFVGG126_2);
		fillNewHisto(hSMVBF126,hSMVBF126_2);
		fillNewHisto(hSMGG126,hSMGG126_2);
		fillNewHisto(hSMHWWVBF126,hSMHWWVBF126_2);
		if(i!=0) fillNewHisto(hSMHWWGG126,hSMHWWGG126_2);

	}

	for (int i=0; i<3; i++){
		if(elechannels[i]!=true) continue;

		TH1F *hFAKESLEPTON_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/Fakes"); hFAKESLEPTON_2->SetName("hFAKESLEPTON_2");
		TString Extra="/DYnoTauTau";
		if(i==2) Extra="/Fakes"; // in the postfit directory the DY for VBF is not saved, since it has 0 events
		TH1F *hDY_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra);
		TH1F *hWW_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/WW");
		Extra="/WG";
		if(i!=1) Extra="/Fakes";
		TH1F *hWGamma_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra); hWGamma_2->SetName("hWGamma_2");
		Extra="/WGStar";
		if(i==2) Extra="/Fakes";
		TH1F *hWGammaStar_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra); hWGammaStar_2->SetName("hWGammaStar_2");
		TH1F *hTOP_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/TOP");
		TH1F *hTT_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/TT");
		TH1F *hZTauTau_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ZTauTau");
		TH1F *hLFVVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/LFVVBF");
		TH1F *hLFVGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/LFVGG");
		TH1F *hSMGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ggHTauTau");
		TH1F *hSMVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/vbfHTauTau");
		TH1F *hSMHWWGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ggHWW");
		TH1F *hSMHWWVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/vbfHWW");

		if(i!=2 && (REBIN)) {
			hFAKESLEPTON_2->Rebin(2); hDY_2->Rebin(2); hWW_2->Rebin(2); hTOP_2->Rebin(2); hTT_2->Rebin(2); hZTauTau_2->Rebin(2);
			hLFVVBF126_2->Rebin(2); hLFVGG126_2->Rebin(2); hSMGG126_2->Rebin(2); hSMVBF126_2->Rebin(2);
			hSMHWWGG126_2->Rebin(2); hSMHWWVBF126_2->Rebin(2);
			hWGamma_2->Rebin(2); hWGammaStar_2->Rebin(2);
		}


		// WEIGHT       
		double bckg=hWW_2->Integral(binA,binB)+hFAKESLEPTON_2->Integral(binA,binB) + hTOP_2->Integral(binA,binB) + hTT_2->Integral(binA,binB) + hZTauTau_2->Integral(binA,binB);
		bckg+=hSMVBF126_2->Integral(binA,binB)+hSMGG126_2->Integral(binA,binB)+hSMHWWVBF126_2->Integral(binA,binB)+hSMHWWGG126_2->Integral(binA,binB);
		if(i!=2) {bckg+=hDY_2->Integral(binA,binB)+hWGammaStar_2->Integral(binA,binB);}
		else {hDY_2->Scale(0); hWGammaStar_2->Scale(0);}
		if (i==1) bckg+=hWGamma_2->Integral();
		else hWGamma_2->Scale(0);

		double signal=hLFVGG126_2->Integral()+hLFVVBF126_2->Integral();

		weightMuEle[i]=signal/(signal+bckg);
		cout<<"Weighting MuEle Channel  "<<i<<" --> "<<weightMuEle[i]<<endl;

		if(weightSOverSB){
			hFAKESLEPTON_2->Scale(weightMuEle[i]);
			hDY_2->Scale(weightMuEle[i]);
			hWW_2->Scale(weightMuEle[i]);
			hTOP_2->Scale(weightMuEle[i]);
			hTT_2->Scale(weightMuEle[i]);
			hZTauTau_2->Scale(weightMuEle[i]);
			hWGamma_2->Scale(weightMuEle[i]);
			hWGammaStar_2->Scale(weightMuEle[i]);
			hLFVVBF126_2->Scale(weightMuEle[i]);
			hLFVGG126_2->Scale(weightMuEle[i]);
			hSMVBF126_2->Scale(weightMuEle[i]);
			hSMGG126_2->Scale(weightMuEle[i]);
			hSMHWWVBF126_2->Scale(weightMuEle[i]);
			hSMHWWGG126_2->Scale(weightMuEle[i]);
		}

		fillNewHisto(hFAKESLEPTON,hFAKESLEPTON_2);
		if(i!=2) fillNewHisto(hDY,hDY_2);
		fillNewHisto(hWW,hWW_2);
		if(i!=2) fillNewHisto(hWGammaStar,hWGammaStar_2);
		if(i==1) fillNewHisto(hWGamma,hWGamma_2);
		fillNewHisto(hTOP,hTOP_2);
		fillNewHisto(hTT,hTT_2);
		fillNewHisto(hZTauTau,hZTauTau_2);
		fillNewHisto(hLFVVBF126,hLFVVBF126_2);
		fillNewHisto(hLFVGG126,hLFVGG126_2);
		fillNewHisto(hSMVBF126,hSMVBF126_2);
		fillNewHisto(hSMGG126,hSMGG126_2);
		fillNewHisto(hSMHWWVBF126,hSMHWWVBF126_2);
		fillNewHisto(hSMHWWGG126,hSMHWWGG126_2);



	}



	TString dirInternalDataAllMU[3]={"gg0mutau","boostmutau","vbfmutau"};

	for (int i=0; i<3; i++){
		cout << "starting data" <<endl;
		if(muonchannels[i]!=true) continue;
		if(i == 0){
                  TH1F *hdata_obs_2=(TH1F*)_fileDataMuHad0Jet->Get(dirInternalDataAllMU[i]+"/data_obs");
		}
		else if (i  == 1){
		  TH1F *hdata_obs_2=(TH1F*)_fileDataMuHad1Jet->Get(dirInternalDataAllMU[i]+"/data_obs");
		}
		else if (i == 2){
                  TH1F *hdata_obs_2=(TH1F*)_fileDataMuHad2Jet->Get(dirInternalDataAllMU[i]+"/data_obs");
                }
		cout << "declared histos" << endl;
		//TH1F *hdata_obs_2=(TH1F*)_fileData->Get(dirInternalDataAllMU[i]+"/data_obs");
		hdata_obs_2->SetName("hdata_obs_2");
		if(weightSOverSB) hdata_obs_2->Scale(weightMuTau[i]);
		if(i!=2 && (REBIN)) hdata_obs_2->Rebin(2);
		cout << "filling data histo" << endl;
		fillNewHisto(hdata_obs,hdata_obs_2);
	}

	TString dirInternalDataAllELE[3]={"GGF","Boost","VBF"};

	for (int i=0; i<3; i++){
		if(elechannels[i]!=true) continue;
                if(i == 0){
                  TH1F *hdata_obs_2=(TH1F*)_fileDataMuEle0Jet->Get(dirInternalDataAllELE[i]+"/data_obs");
                }
                else if (i  == 1){
                  TH1F *hdata_obs_2=(TH1F*)_fileDataMuEle1Jet->Get(dirInternalDataAllELE[i]+"/data_obs");
                }
                else if (i == 2){
                  TH1F *hdata_obs_2=(TH1F*)_fileDataMuEle2Jet->Get(dirInternalDataAllELE[i]+"/data_obs");
                }

		//TH1F *hdata_obs_2=(TH1F*)_fileData->Get(dirInternalDataAllELE[i]+"/data_obs");
		hdata_obs_2->SetName("hdata_obs_2");
		if(weightSOverSB) hdata_obs_2->Scale(weightMuEle[i]);
		if(i!=2 && (REBIN) ) hdata_obs_2->Rebin(2);
		fillNewHisto(hdata_obs,hdata_obs_2);
	}



	TH1F *hSMHIGGS=(TH1F*) hSMVBF126->Clone();hSMHIGGS->SetName("hSMHIGGS");
	hSMHIGGS->Add(hSMGG126);
	TH1F *hSMHWWHIGGS=(TH1F*) hSMHWWVBF126->Clone();hSMHWWHIGGS->SetName("hSMHWWHIGGS");
	hSMHWWHIGGS->Add(hSMHWWGG126);

	hWGamma->Add(hWGammaStar);

	hFAKES->Add(hFAKESLEPTON);
	hFAKES->SetFillColor(kMagenta-10); hFAKES->SetLineColor(kMagenta+3); hFAKES->SetLineWidth(1);
	hFAKESLEPTON->SetFillColor(kMagenta-9); hFAKESLEPTON->SetLineColor(kMagenta+4); hFAKESLEPTON->SetLineWidth(1);

	hZTauTau->SetFillColor(kOrange-4); hZTauTau->SetLineColor(kOrange+4); hZTauTau->SetLineWidth(1);

        hDY->SetFillColor(kAzure+3); hDY->SetLineColor(kAzure+4); hDY->SetLineWidth(1);
        hWW->SetFillColor(kAzure+3); hWW->SetLineColor(kAzure+3); hWW->SetLineWidth(1);
        hWGamma->SetFillColor(kAzure+3); hWGamma->SetLineColor(kAzure+3); hWGamma->SetLineWidth(1);

        hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hTT->SetFillColor(kGreen-2); hTT->SetLineColor(kGreen-2); hTT->SetLineWidth(1);



	hSMHIGGS->SetFillColor(kMagenta); hSMHIGGS->SetLineColor(kMagenta+1); hSMHIGGS->SetLineWidth(1);
	hSMHWWHIGGS->SetFillColor(kMagenta); hSMHWWHIGGS->SetLineColor(kMagenta+1); hSMHWWHIGGS->SetLineWidth(1);

	hLFVGG126->SetLineColor(kBlue);  hLFVGG126->SetLineWidth(3);
	hLFVVBF126->SetLineColor(kBlue); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);
	hSMHIGGS->SetLineColor(kMagenta); hSMHIGGS->SetLineWidth(3);
	hSMHWWHIGGS->SetLineColor(kMagenta); hSMHWWHIGGS->SetLineWidth(3);



	hdata_obs->SetMarkerSize(1); // Closer to Daniel's

	// PLOT

	TCanvas *c1 = new TCanvas("canvas_"+name);
	TPad *Pad1= new TPad("pad1","",0,0.2,1,1); Pad1->Draw(); Pad1->cd();;
	Pad1->SetLeftMargin(0.2147651);
	Pad1->SetRightMargin(0.06543624);
	Pad1->SetTopMargin(0.07);
	Pad1->SetBottomMargin(0.04);

	TH1F* fullMC2=hFAKES->Clone();  fullMC2->Add(hZTauTau); fullMC2->Add(hTT); fullMC2->Add(hWW); fullMC2->Add(hWGamma);
	fullMC2->Add(hDY); fullMC2->Add(hTOP); fullMC2->Add(hSMHIGGS);  fullMC2->Add(hSMHWWHIGGS);
	fullMC2->SetFillColor(kGray+2); fullMC2->SetFillStyle(3002); fullMC2->SetMarkerSize(0); fullMC2->SetLineWidth(2);
	fullMC2->Draw("hist");

	fullMC2->GetXaxis()->SetTitle("");
	fullMC2->GetYaxis()->SetTitle(Yaxis);
	fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
	fullMC2->GetYaxis()->SetTitleOffset(1.2);
	fullMC2->GetYaxis()->SetTitleSize(0.05);
	fullMC2->GetXaxis()->SetNdivisions(0);
	fullMC2->GetYaxis()->SetLabelSize(0.04);


	TH1F* hSignal=hLFVGG126->Clone(); hSignal->SetName("hSignal");
	hSignal->Add(hLFVVBF126);

        hSignal->SetLineColor(kBlue);  hSignal->SetLineWidth(3);
	hSignal->SetLineStyle(2);

	THStack* stack = new THStack("stack","");
	stack->Add(hFAKES);
	stack->Add(hWW);
	stack->Add(hWGamma);
        stack->Add(hDY);
	stack->Add(hTT);
	stack->Add(hTOP);
	stack->Add(hZTauTau);
	stack->Add(hSMHIGGS);;
	stack->Add(hSMHWWHIGGS);
	stack->Add(hSignal);

	int bins=hdata_obs->GetNbinsX()+1;

	/*
	   cout<<"Yields  "<<endl;
	   cout<<"DATA	    \t" <<hdata_obs->Integral()+hdata_obs->GetBinContent(bins)<<endl;
	   cout<<"VV           \t" <<hWW->Integral()+hWW->GetBinContent(bins)<<endl;
	   cout<<"TOP          \t" <<hTOP->Integral()+hTOP->GetBinContent(bins)<<endl;
	   cout<<"TT           \t" <<hTT->Integral()+hTT->GetBinContent(bins)<<endl;
	   cout<<"DY           \t" <<hDY->Integral()+hDY->GetBinContent(bins)<<endl;
	   cout<<"ZTauTau      \t" <<hZTauTau->Integral()+hZTauTau->GetBinContent(bins)<<endl;
	   cout<<"FAKES        \t" <<hFAKES->Integral()+hFAKES->GetBinContent(bins)<<endl;
	   cout<<"hFAKESLEPTON \t" <<hFAKESLEPTON->Integral()+hFAKESLEPTON->GetBinContent(bins)<<endl;
	   cout<<"hSMHIGGS     \t" <<hSMHIGGS->Integral()+hSMHWWHIGGS->Integral()+hSMHIGGS->GetBinContent(bins)+hSMHWWHIGGS->GetBinContent(bins)<<endl;
	   cout<<"LFVGG126     \t" <<hLFVGG126->Integral()+hLFVGG126->GetBinContent(bins)<<endl;
	   cout<<"LFVVBF126    \t" <<hLFVVBF126->Integral()+hLFVVBF126->GetBinContent(bins)<<endl;
	 */
	stack->Draw("samehist");
	fullMC2->Draw("sames,E2");

//	hSignal->Draw("sameshist");

	double maxData=hdata_obs->GetMaximum();
	double maxMC=stack->GetMaximum()*1.2;
	double maxLFV=hSignal->GetMaximum();
	double minMC=stack->GetMinimum();

	if(maxData>maxMC) {maxMC=1.2*maxData;}
	if(maxLFV>maxMC) {maxMC=1.2*maxLFV;}
	if(MAX!=-1) {maxMC=MAX;}
	if(minMC<1) minMC=0;

	stack->SetMaximum(maxMC);
	stack->GetYaxis()->SetRangeUser(minMC,maxMC);
	fullMC2->SetMaximum(maxMC);
	fullMC2->GetYaxis()->SetRangeUser(minMC,maxMC);

	hdata_obs->Draw("sames");


	TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
	leg->SetFillColor(0);
	leg->SetBorderSize(0);
	leg->SetFillStyle(0);
	TLegendEntry *entry;
	entry=leg->AddEntry(hdata_obs,"Data","p");
	entry=leg->AddEntry(fullMC2,"Bkgd. uncertainty","f");
	//entry=leg->AddEntry(hSMHWWHIGGS,"SM HWW","f");
	entry=leg->AddEntry(hSMHIGGS,"SM H","f");
	entry=leg->AddEntry(hZTauTau,"Z#rightarrow#tau#tau","f");
        entry=leg->AddEntry(hDY,"Other","f");
        entry=leg->AddEntry(hTOP,"t#bar{t}, t, #bar{t}","f");
	entry=leg->AddEntry(hFAKES,"MisID'd #tau, e, #mu","f");
	entry=leg->AddEntry(hSignal,"LFV Higgs, (B=0.9%)","l");
	//        entry=leg->AddEntry("NULL","Br(h#rightarrow#mu#tau)=1%","");
	//        entry=leg->AddEntry("NULL","Br(h#rightarrow#tau#tau)=6%","");
	leg->Draw();


	/*
	   TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
	   leg->SetFillColor(0);
	   leg->SetBorderSize(0);
	   leg->SetFillStyle(0);
	   TLegendEntry *entry;
	   entry=leg->AddEntry(hdata_obs,"observed","p");
	   entry=leg->AddEntry(fullMC2,"bckg. uncertainty","fl");
	//entry=leg->AddEntry(hSMHWWHIGGS,"SM HWW","f");
	entry=leg->AddEntry(hSMHIGGS,"SM H","f");
	eblindBy=leg->AddEntry(hZTauTau,"Z+#tau#tau (embedd.)","f");
	eblindBy=leg->AddEntry(hDY,"EWK","f");
	entry=leg->AddEntry(hFAKES,"Fakes","f");
	entry=leg->AddEntry(hSignal,"LFV Higgs, (B=0.9%)","l");
	//        entry=leg->AddEntry("NULL","Br(h#rightarrow#mu#tau)=1%","");
	//        entry=leg->AddEntry("NULL","Br(h#rightarrow#tau#tau)=6%","");
	 */


	leg->Draw();

	CMS_lumi( Pad1, iPeriod, iPos );
	//cmsPrelim(Lumi);

	Pad1->SetLogy(setLogY);



	c1->cd(); TPad *Pad2= new TPad("pad2","",0,0,1,0.23); Pad2->Draw(); Pad2->cd();  Pad2->SetGridy();
	Pad2->SetLeftMargin(0.2147651);
	Pad2->SetRightMargin(0.06543624);
	Pad2->SetTopMargin(0.0);
	Pad2->SetBottomMargin(0.38);
	Pad2->SetFillStyle(0);

	TH1F * Ratio=hdata_obs->Clone(); Ratio->SetName("Ratio");
	Ratio->Add(fullMC2,-1);
	double dataRatio[16];
	double mcRatio[16];
	double errordataUpRatio[16];
	double errordataDownRatio[16];
	double xbinsRatio[16];
	double xerrorbinsRatio[16];
	Ratio->Divide(fullMC2);

	TH1F* RatioError = Ratio->Clone(); RatioError->SetName("RatioError");

	for (int i=0; i<RatioError->GetNbinsX()+1; i++){
		double error=fullMC2->GetBinError(i)*hdata_obs->GetBinContent(i)/fullMC2->GetBinContent(i)/fullMC2->GetBinContent(i);
		//double error=fullMC2->GetBinError(i)/fullMC2->GetBinContent(i);
		RatioError->SetBinContent(i,0);
		RatioError->SetBinError(i,error);
	}


	for (int j=0; j<16; j++){
		xbinsRatio[j]=300./15*(j-1)+10;
		xerrorbinsRatio[j]=10;
		dataRatio[j]=hdata_obs->GetBinContent(j);
		errordataUpRatio[j]=hdata_obs->GetBinError(j);
		errordataDownRatio[j]=hdata_obs->GetBinError(j);
		if(dataRatio[j]==0) {errordataUpRatio[j]=1.7; errordataDownRatio[j]=0;}
		mcRatio[j]=fullMC2->GetBinContent(j);
		dataRatio[j]-=mcRatio[j];
		if(mcRatio[j]!=0) {
			dataRatio[j]=dataRatio[j]/mcRatio[j];
			errordataUpRatio[j]=errordataUpRatio[j]/mcRatio[j];
			errordataDownRatio[j]=errordataDownRatio[j]/mcRatio[j];
		}else{
			dataRatio[j]=0;
			errordataUpRatio[j]=0;
			errordataDownRatio[j]=0;
		}
		double error=0;
		if(fullMC2->GetBinContent(j)!=0) error=fullMC2->GetBinError(j)*hdata_obs->GetBinContent(j)/fullMC2->GetBinContent(j)/fullMC2->GetBinContent(j);

		cout<<hdata_obs->GetBinContent(j)<<" "<<mcRatio[j]<<"  "<<hdata_obs->GetBinError(j)<<" "<<fullMC2->GetBinError(j)<<"  "<<dataRatio[j]<<"  "<<errordataUpRatio[j]<<"  "<<error<<"  "<<Ratio->GetBinError(j)<<"   "<<sqrt(error*error+errordataUpRatio[j]*errordataUpRatio[j])<<endl;

	}

	TGraphAsymmErrors* dataGraphRatio=new TGraphAsymmErrors(16, xbinsRatio, dataRatio,xerrorbinsRatio,xerrorbinsRatio,errordataDownRatio,errordataUpRatio);

	Ratio->Draw("");

	Ratio->GetXaxis()->SetLabelFont(42);
	Ratio->GetXaxis()->SetTitleFont(42);
	Ratio->GetYaxis()->SetNdivisions(505);
	Ratio->GetYaxis()->SetLabelFont(42);
	Ratio->GetYaxis()->SetLabelSize(0.122);
	Ratio->GetYaxis()->SetRangeUser(ymin,ymax);
	Ratio->GetXaxis()->SetRangeUser(xmin,xmax);
	Ratio->GetXaxis()->SetLabelSize(0.12);
	Ratio->GetXaxis()->SetLabelFont(42);
	Ratio->SetYTitle("#frac{Data-Bkgd (fit)  }{Bkgd (fit)}");
	Ratio->SetXTitle(Xaxis);
	Ratio->GetXaxis()->SetNdivisions(505);
	Ratio->GetYaxis()->CenterTitle(true);
	Ratio->GetYaxis()->SetTitleOffset(0.4);
	Ratio->GetYaxis()->SetTitleSize(0.11);
	Ratio->GetXaxis()->SetTitleOffset(0.8);
	Ratio->GetXaxis()->SetTitleSize(0.20);
	Ratio->SetMarkerSize(1.);


	RatioError->Draw("sames,E2"); RatioError->SetFillStyle(3002); RatioError->SetFillColor(kGray+2); RatioError->SetMarkerSize(0);

	//	dataGraphRatio->Draw("sames,p");

	TCanvas *c2 = new TCanvas("canvas_"+name+"_2","canvas_"+name+"_2");
	TH1F* SUBTRACTEDMCERROR=fullMC2->Clone(); SUBTRACTEDMCERROR->SetName("SUBTRACTEDMCERROR");
	for (int i=0; i<SUBTRACTEDMCERROR->GetNbinsX()+1; i++) SUBTRACTEDMCERROR->SetBinContent(i,0);
	SUBTRACTEDMCERROR->SetFillColor(kYellow+4);
	SUBTRACTEDMCERROR->SetFillStyle(3004);
	SUBTRACTEDMCERROR->SetLineWidth(2);
	TH1F* SUBTRACTED=hdata_obs->Clone(); SUBTRACTED->SetName("SUBTRACTED");

	//	const int entriesD=(const)SUBTRACTEDMCERROR->GetNbinsX();
	double data[16];
	double mc[16];
	double errordataUp[16];
	double errordataDown[16];
	double xbins[16];
	double xerrorbins[16];

	for (int j=0; j<16; j++){
		xbins[j]=300./15*(j-1)+10;
		xerrorbins[j]=10;
		data[j]=SUBTRACTED->GetBinContent(j);
		errordataUp[j]=SUBTRACTED->GetBinError(j);
		errordataDown[j]=SUBTRACTED->GetBinError(j);
		if(data[j]==0) {errordataUp[j]=1.7; errordataDown[j]=0;}
		mc[j]=fullMC2->GetBinContent(j);
		data[j]-=mc[j];
	}

	TGraphAsymmErrors* dataGraph=new TGraphAsymmErrors(16, xbins, data,xerrorbins,xerrorbins,errordataDown,errordataUp);
	//dataGraph->SetMarkerColor(kRed);	

	SUBTRACTED->Add(fullMC2,-1);
	for (int i=0; i<SUBTRACTED->GetNbinsX()+1; i++) SUBTRACTED->SetBinError(i,hdata_obs->GetBinError(i));
	TH1F *hSignalFill=hSignal->Clone(); hSignalFill->SetName("hSignalFill");
	hSignalFill->SetFillColor(kBlue-10);
	hSignalFill->SetFillStyle(1001);
	hSignalFill->SetLineWidth(2);
	hSignalFill->Draw("hist");
        hSignalFill->SetLineStyle(1);

	hSignalFill->SetXTitle(Xaxis);
	SUBTRACTED->SetXTitle(Xaxis);
	SUBTRACTED->SetYTitle(Yaxis);
	hSignalFill->SetYTitle(Yaxis);

	hSignalFill->GetXaxis()->SetRangeUser(xmin,xmax);
	SUBTRACTED->GetXaxis()->SetRangeUser(xmin,xmax);
	SUBTRACTEDMCERROR->GetXaxis()->SetRangeUser(xmin,xmax);
	SUBTRACTEDMCERROR->SetXTitle(Xaxis);
	SUBTRACTEDMCERROR->SetYTitle(Yaxis);
	//hSignalFill->SetYTitle(Yaxis);
	SUBTRACTEDMCERROR->Draw("sames,E2");
	//SUBTRACTED->Draw("sames");
	dataGraph->Draw("sames,p");
	SUBTRACTEDMCERROR->GetXaxis()->SetNdivisions(505);
	SUBTRACTED->GetXaxis()->SetNdivisions(505);
	hSignalFill->GetXaxis()->SetNdivisions(505);
	SUBTRACTEDMCERROR->GetXaxis()->SetLabelSize(0.04);
	SUBTRACTED->GetXaxis()->SetLabelSize(0.04);
	hSignalFill->GetXaxis()->SetLabelSize(0.04);
	SUBTRACTEDMCERROR->GetYaxis()->SetLabelSize(0.04);
	SUBTRACTED->GetYaxis()->SetLabelSize(0.04);
	hSignalFill->GetYaxis()->SetLabelSize(0.04);
	SUBTRACTEDMCERROR->GetYaxis()->SetTitleSize(0.05);
	SUBTRACTED->GetYaxis()->SetTitleSize(0.05);
	hSignalFill->GetYaxis()->SetTitleSize(0.05);

	if(minsubs==-1)
		minsubs=TMath::Min(hSignalFill->GetMinimum(),SUBTRACTED->GetMinimum())*2.5;
	if(maxsubs==-1)
		maxsubs=TMath::Max(hSignalFill->GetMaximum(),SUBTRACTED->GetMaximum())*1.2;
	hSignalFill->SetMaximum(maxsubs);
	hSignalFill->SetMinimum(minsubs);

	if(minsubs==-1)
		minsubs=TMath::Min(SUBTRACTEDMCERROR->GetMinimum(),SUBTRACTED->GetMinimum())*2.5;
	if(maxsubs==-1)
		maxsubs=TMath::Max(SUBTRACTEDMCERROR->GetMaximum(),SUBTRACTED->GetMaximum())*1.2;
	SUBTRACTEDMCERROR->SetMaximum(maxsubs);
	SUBTRACTEDMCERROR->SetMinimum(minsubs);
	SUBTRACTED->SetMaximum(maxsubs);
	SUBTRACTED->SetMinimum(minsubs);




	TLegend *leg2 = new TLegend(0.55,0.93,0.99,0.7,NULL,"brNDC");
	leg2->SetFillColor(0);
	leg2->SetBorderSize(0);
	leg2->SetFillStyle(0);
	TLegendEntry *entry;
	//	entry=leg2->AddEntry("NULL",channelName,"");
	entry=leg2->AddEntry(hSignalFill,"LFV H#rightarrow#mu#tau signal (B=0.9%)","f");
	entry=leg2->AddEntry(SUBTRACTEDMCERROR,"Bkgd. uncertainty","f");
	entry=leg2->AddEntry(SUBTRACTED,"Data-Bkgd","pl");

	leg2->Draw();

        CMS_lumi( c2, iPeriod, iPos );

	c2->SaveAs(name+"_Subtracted.png");
	c2->SaveAs(name+"_Subtracted.pdf");

	if(!setLogY){
		c1->SaveAs(name+".png");
		c1->SaveAs(name+".pdf");
	}
	else {
		c1->SaveAs(name+"_log.png");
		c1->SaveAs(name+"_log.pdf");
	}

}

void cmsPrelim( double intLumi ){  TLatex latex;
	latex.SetNDC();
	latex.SetTextSize(0.04);

	latex.SetTextAlign(31); // align right
	latex.DrawLatex(0.9,0.96,Form("%.1f fb^{-1}, #sqrt{s} = 8 TeV",intLumi/1000));
	//  if (intLumi > 0.) {
	//    latex.SetTextAlign(31); // align right
	//    latex.DrawLatex(0.9,0.9,Form("#int #font[12]{L} dt = %.1f fb^{-1}",intLumi));
	//  }

	latex.SetTextAlign(11); // align left
	latex.DrawLatex(0.25,0.96,"CMS preliminary");
}

void fillNewHisto(TH1F * histoOUT, TH1F* histoIN){
	cout << "filling histo" << endl;
	for (int j=0; j<histoOUT->GetNbinsX()+1; j++){
		double binContent=histoOUT->GetBinContent(j)+histoIN->GetBinContent(j);
		double binError=histoOUT->GetBinError(j)*histoOUT->GetBinError(j)+histoIN->GetBinError(j)*histoIN->GetBinError(j);
		binError=sqrt(binError);
		histoOUT->SetBinContent(j,binContent);
		histoOUT->SetBinError(j,binError);
	}
	cout << "filled histo" << endl;
}
