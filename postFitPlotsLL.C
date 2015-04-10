void postFitPlotsLL(TString name="collMass",TString fileData="dataALL.root", TString file="mlfit20.root", TString dirInternal="shapes_fit_s", TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", double xmin=200, double xmax=300, double ymin=-2, double ymax=2, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MIN=-1,double MAX=-1, bool mutau0=true, bool mutau1=true, bool mutau2=true, bool muele0=true, bool muele1=true, bool muele2=true, bool REBIN=true, bool weightSOverSB=true,TString channelName="#mu#tau", double minsubs=-1, double maxsubs=-1){


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

	const int nbins=18;
	double binsLog[19]={-3,-2,-1.75,-1.5,-1.4,-1.3,-1.2,-1.1,-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,0};	
	//	const int nbins=22;
	//	double binsLog[23]={-2,-1.5,-1.25,-1.1,-1.05,-1,-0.95,-0.9,-0.85,-0.8,-0.75,-0.7,-0.65,-0.6,-0.55,-0.5,-0.45,-0.4,-0.2,-0.1,0};

	TFile *_fileMC= new TFile("UnblindNEW/"+file);
	TFile *_fileData= new TFile("UnblindNEW/"+fileData);

	TString dirInternalAllMU[3]={dirInternal+"/datacard_MuTau_0Jet_new",dirInternal+"/datacard_MuTau_1Jet_new", dirInternal+"/datacard_MuTau_2Jet_new"};
	TString dirInternalAllELE[3]={dirInternal+"/datacard_MuEle_0Jet",dirInternal+"/datacard_MuEle_1Jet", dirInternal+"/datacard_MuEle_2Jet"};

	double weightMuTau[3]={1,1,1};
	double weightMuEle[3]={1,1,1};

	TString dirInternalDataAllMU[3]={"gg0mutau","boostmutau","vbfmutau"};
	TString dirInternalDataAllELE[3]={"GGF","Boost","VBF"};

	TH1F* hLOGMu[3];
	TH1F* hLOGDATAMu[3]; 
	TH1F* hLOGEle[3]; 
	TH1F* hLOGDATAEle[3]; 
	TH1F* hLOGSIGNALMu[3];
	TH1F* hLOGSIGNALEle[3];
	TH1F* hLOGDATA=new TH1F("LOGDATA","",nbins,binsLog);
	TH1F* hLOGSIGNAL=new TH1F("LOGSIGNAL","",nbins,binsLog);
	TH1F* hLOGMuUP[3];
	TH1F* hLOGEleUP[3];
	TH1F* hLOGMuDOWN[3];
	TH1F* hLOGEleDOWN[3];
	TH1F* hLOGUP=new TH1F("LOGUP","",nbins,binsLog);
	TH1F  *hLOGDOWN=new TH1F("LOGDOWN","",nbins,binsLog);

	for (int i=0; i<3; i++){
		hLOGMu[i]=new TH1F("LOGMu_"+dirInternalDataAllMU[i],"",nbins,binsLog);
		hLOGDATAMu[i]=new TH1F("LOGDATAMu_"+dirInternalDataAllMU[i],"",nbins,binsLog);
		hLOGSIGNALMu[i]=new TH1F("LOGSIGNALMu_"+dirInternalDataAllMU[i],"",nbins,binsLog);
		hLOGMuUP[i]=new TH1F("LOGMuUP_"+dirInternalDataAllMU[i],"",nbins,binsLog);
		hLOGMuDOWN[i]=new TH1F("LOGMuDOWN_"+dirInternalDataAllMU[i],"",nbins,binsLog);

		if(muonchannels[i]!=true) continue;

		cout<<endl<<dirInternalDataAllMU[i]<<endl;


		TH1F *hdata_obs_2=(TH1F*)_fileData->Get(dirInternalDataAllMU[i]+"/data_obs");
		hdata_obs_2->SetName("hdata_obs_2");

		TH1F* hDUMMY = (TH1F*)hdata_obs_2->Clone(); hDUMMY->SetName("DUMMY_"+dirInternalAllMU[i]); hDUMMY->Scale(0);	

		TH1F *hFAKES_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+"/fakes");hFAKES_2->SetName("fakesHisto");
		TString Extra="/zjetsother";

		if(i==2) Extra="/fakes"; // in the postfit directory the DY for VBF is not saved, since it has 0 events
		TH1F *hDY_2=(TH1F*)_fileMC->Get(dirInternalAllMU[i]+Extra); hDY_2->SetName("dyHisto");
		if(i==2) hDY_2->Scale(0);		

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

		// WEIGHT

		weightHistosSignificance(hFAKES_2,hDY_2,hWW_2,hDUMMY,hDUMMY,hTOP_2,hTT_2,hZTauTau_2,hLFVVBF126_2,hLFVGG126_2,hSMVBF126_2,hSMGG126_2,hSMHWWVBF126_2,hSMHWWGG126_2,hdata_obs_2,hLOGMu[i],hLOGDATAMu[i],hLOGSIGNALMu[i], hLOGMuUP[i], hLOGMuDOWN[i]);

		hDUMMY->Delete();

	}

	for (int i=0; i<3; i++){
		hLOGEle[i]=new TH1F("LOGEle_"+dirInternalDataAllELE[i],"",nbins,binsLog);
		hLOGDATAEle[i]=new TH1F("LOGDATAEle_"+dirInternalDataAllELE[i],"",nbins,binsLog);
		hLOGSIGNALEle[i]=new TH1F("LOGSIGNALEle_"+dirInternalDataAllELE[i],"",nbins,binsLog);
		hLOGEleDOWN[i]=new TH1F("LOGEleDOWN_"+dirInternalDataAllELE[i],"",nbins,binsLog);
		hLOGEleUP[i]=new TH1F("LOGEleUP_"+dirInternalDataAllELE[i],"",nbins,binsLog);

		if(elechannels[i]!=true) continue;
		cout<<endl<<dirInternalDataAllELE[i]<<endl;

		TH1F *hdata_obs_2=(TH1F*)_fileData->Get(dirInternalDataAllELE[i]+"/data_obs");
		hdata_obs_2->SetName("hdata_obs_2");

		TH1F *hFAKESLEPTON_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/Fakes"); hFAKESLEPTON_2->SetName("hFAKESLEPTON_2");

		TString Extra="/DYnoTauTau";
		if(i==2) Extra="/Fakes"; // in the postfit directory the DY for VBF is not saved, since it has 0 events
		TH1F *hDY_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra);
		if(i==2) hDY_2->Scale(0);

		TH1F *hWW_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/WW");

		Extra="/WG";
		if(i!=1) Extra="/Fakes";
		TH1F *hWGamma_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra); hWGamma_2->SetName("hWGamma_2");
		if(i!=0) hWGamma_2->Scale(0);
		Extra="/WGStar";
		if(i==2) Extra="/Fakes";
		TH1F *hWGammaStar_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+Extra); hWGammaStar_2->SetName("hWGammaStar_2");
		if(i==2) hWGammaStar_2->Scale(0);

		TH1F *hTOP_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/TOP");
		TH1F *hTT_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/TT");
		TH1F *hZTauTau_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ZTauTau");
		TH1F *hLFVVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/LFVVBF");
		TH1F *hLFVGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/LFVGG");
		TH1F *hSMGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ggHTauTau");
		TH1F *hSMVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/vbfHTauTau");
		TH1F *hSMHWWGG126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/ggHWW");
		TH1F *hSMHWWVBF126_2=(TH1F*)_fileMC->Get(dirInternalAllELE[i]+"/vbfHWW");

		weightHistosSignificance(hFAKESLEPTON_2,hDY_2,hWW_2,hWGammaStar_2,hWGamma_2,hTOP_2,hTT_2,hZTauTau_2,hLFVVBF126_2,hLFVGG126_2,hSMVBF126_2,hSMGG126_2,hSMHWWVBF126_2,hSMHWWGG126_2,hdata_obs_2,hLOGEle[i],hLOGDATAEle[i],hLOGSIGNALEle[i],hLOGEleUP[i],hLOGEleDOWN[i]);


	}

	THStack* stack = new THStack("stack","");

	TH1F* hLOG=(TH1F*)hLOGDATA->Clone(); hLOG->SetName("hLOG");

	for(int i=0; i<3; i++){
		if(elechannels[i]!=true) continue;
		double mix=hLOGEle[i]->GetBinContent(-1)+hLOGEle[i]->GetBinContent(0);
		hLOGEle[i]->SetBinContent(1,mix);
		hLOGEle[i]->SetFillColor(kMagenta-10+i);
		hLOG->Add(hLOGEle[i]);
		stack->Add(hLOGEle[i]);
		mix=hLOGDATAEle[i]->GetBinContent(-1)+hLOGDATAEle[i]->GetBinContent(0);
		hLOGDATAEle[i]->SetBinContent(1,mix);
		hLOGDATA->Add(hLOGDATAEle[i]);
		mix=hLOGEleUP[i]->GetBinContent(-1)+hLOGEleUP[i]->GetBinContent(0);
		hLOGEleUP[i]->SetBinContent(1,mix);
		hLOGUP->Add(hLOGEleUP[i]);
		mix=hLOGEleDOWN[i]->GetBinContent(-1)+hLOGEleDOWN[i]->GetBinContent(0);
		hLOGEleDOWN[i]->SetBinContent(1,mix);
		hLOGDOWN->Add(hLOGEleDOWN[i]);
	}
	for(int i=0; i<3; i++){
		if(muonchannels[i]!=true) continue;
		double mix=hLOGMu[i]->GetBinContent(-1)+hLOGMu[i]->GetBinContent(0);
		hLOGMu[i]->SetBinContent(1,mix);
		hLOGMu[i]->SetFillColor(kCyan-10+i);
		stack->Add(hLOGMu[i]);
		hLOG->Add(hLOGMu[i]);
		mix=hLOGDATAMu[i]->GetBinContent(-1)+hLOGDATAMu[i]->GetBinContent(0);
		hLOGDATAMu[i]->SetBinContent(1,mix);
		hLOGDATA->Add(hLOGDATAMu[i]);
		mix=hLOGMuUP[i]->GetBinContent(-1)+hLOGMuUP[i]->GetBinContent(0);
		hLOGMuUP[i]->SetBinContent(1,mix);
		hLOGUP->Add(hLOGMuUP[i]);
		mix=hLOGMuDOWN[i]->GetBinContent(-1)+hLOGMuDOWN[i]->GetBinContent(0);
		hLOGMuDOWN[i]->SetBinContent(1,mix);
		hLOGDOWN->Add(hLOGMuDOWN[i]);
	}
	for(int i=0; i<3; i++){
		if(muonchannels[i]==true) {
			double mix=hLOGSIGNALMu[i]->GetBinContent(-1)+hLOGSIGNALMu[i]->GetBinContent(0);
			hLOGSIGNALMu[i]->SetBinContent(1,mix);
			hLOGSIGNAL->Add(hLOGSIGNALMu[i]);	
		}
		if(elechannels[i]==true) {
			mix=hLOGSIGNALEle[i]->GetBinContent(-1)+hLOGSIGNALEle[i]->GetBinContent(0);
			hLOGSIGNALEle[i]->SetBinContent(1,mix);
			hLOGSIGNAL->Add(hLOGSIGNALEle[i]);
		}
	}

	hLOGSIGNAL->SetFillColor(kBlue);
	hLOGSIGNAL->SetLineColor(kBlue);
	hLOGSIGNAL->SetFillStyle(3004);
	hLOGSIGNAL->SetLineWidth(1);

	stack->Add(hLOGSIGNAL);

	for (int i=0; i<hLOG->GetNbinsX(); i++){
		double error=hLOGUP->GetBinContent(i)-hLOGDOWN->GetBinContent(i);
		error=error/2;
		hLOG->SetBinError(i,error);
	}

	hLOG->SetFillStyle(3001);
	hLOG->SetFillColor(kGray+3);
	hLOG->SetMarkerStyle(1);

	TCanvas *c=new TCanvas(name);
	c->SetLogy(setLogY);
	stack->Draw();
	stack->GetXaxis()->SetTitle(Xaxis);
	stack->GetYaxis()->SetTitle(Yaxis);
	hLOGSIGNAL->GetXaxis()->SetTitle(Xaxis);
	hLOGSIGNAL->GetYaxis()->SetTitle(Yaxis);
	if(MAX!=-1) stack->SetMaximum(MAX);
	if(MIN!=-1) stack->SetMinimum(MIN);
	hLOG->Draw("sames,E2");

	hLOGDATA->Draw("sames,p,E");
	TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
	leg->SetFillColor(0);
	leg->SetBorderSize(0);
	TLegendEntry *entry;
	entry=leg->AddEntry(hLOGDATA,"observed data","p");
	entry=leg->AddEntry(hLOGEle[0],"#mu#tau_{e},0Jet","f");
	entry=leg->AddEntry(hLOGEle[1],"#mu#tau_{e},1Jet","f");
	entry=leg->AddEntry(hLOGEle[2],"#mu#tau_{e},2Jet","f");
	entry=leg->AddEntry(hLOGMu[0],"#mu#tau_{h},0Jet","f");
	entry=leg->AddEntry(hLOGMu[1],"#mu#tau_{h},1Jet","f");
	entry=leg->AddEntry(hLOGMu[2],"#mu#tau_{h},2Jet","f");
	entry=leg->AddEntry(hLOG,"bckg uncertainty","f");
	entry=leg->AddEntry(hLOGSIGNAL,"LFV h#rightarrow#mu#tau, 125 GeV","f");

	leg->Draw();

	//cmsPrelim(19700);
	CMS_lumi(c, iPeriod, iPos );

	c->SaveAs(name+".pdf");
	c->SaveAs(name+".png");




	//	_fileMC->Close();
	//	_fileData->Close();

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
	for (int j=0; j<histoOUT->GetNbinsX()+1; j++){
		double binContent=histoOUT->GetBinContent(j)+histoIN->GetBinContent(j);
		double binError=histoOUT->GetBinError(j)*histoOUT->GetBinError(j)+histoIN->GetBinError(j)*histoIN->GetBinError(j);
		binError=sqrt(binError);
		histoOUT->SetBinContent(j,binContent);
		histoOUT->SetBinError(j,binError);
	}
}

void weightHistosSignificance(TH1F* hFAKES_2,TH1F* hDY_2,TH1F* hWW_2,TH1F* hWGammaStar_2, TH1F* hWGamma_2,TH1F* hTOP_2,TH1F* hTT_2,TH1F* hZTauTau_2,TH1F* hLFVVBF126_2,TH1F* hLFVGG126_2,TH1F* hSMVBF126_2,TH1F* hSMGG126_2,TH1F* hSMHWWVBF126_2,TH1F* hSMHWWGG126_2,TH1F* hdata_obs_2, TH1F* log, TH1F* logData, TH1F* logSignal, TH1F* logUp, TH1F* logDown){

	for (int j=0; j<hFAKES_2->GetNbinsX()+1; j++){
		double weightBin=0;
		double weightDataBin=0;
		double signalBin=0;
		double bckgBin=0;
		double signalDataBin=0;

		TH1F* suma=(TH1F*)hFAKES_2->Clone();  suma->SetName("suma");
		suma->Add(hDY_2); suma->Add(hWW_2); suma->Add(hTOP_2); suma->Add(hTT_2); //suma->Add(hWGamma_2); suma->Add(hWGammaStar_2); 
		suma->Add(hZTauTau_2); suma->Add(hSMVBF126_2); suma->Add(hSMGG126_2); suma->Add(hSMHWWVBF126_2); suma->Add(hSMHWWGG126_2);

		bckgBin=suma->GetBinContent(j);
		errBin=suma->GetBinError(j);
		signalBin+=hLFVGG126_2->GetBinContent(j)+hLFVVBF126_2->GetBinContent(j);

		if(bckgBin<1e-5) continue;

		signalDataBin=hdata_obs_2->GetBinContent(j)-bckgBin;
		if(signalDataBin<0) signalDataBin=0;

		if(signalBin+bckgBin>0) weightBin=signalBin/(signalBin+bckgBin);
		if(signalDataBin+bckgBin>0) weightDataBin=signalDataBin/(signalDataBin+bckgBin);

		cout<<bckgBin<<"(+-"<<errBin<<")   "<<signalBin<<"    --> "<<weightBin<<"   "<<TMath::Log10(weightBin)<<"   -->"<<hdata_obs_2->GetBinContent(j)<<endl;
		log->Fill(TMath::Log10(weightBin),bckgBin);
		logUp->Fill(TMath::Log10(weightBin),bckgBin+errBin);
		logDown->Fill(TMath::Log10(weightBin),bckgBin-errBin);
		logData->Fill(TMath::Log10(weightBin),hdata_obs_2->GetBinContent(j));
		logSignal->Fill(TMath::Log10(weightBin),signalBin);

		double binContent=hFAKES_2->GetBinContent(j)*weightBin;
		double binError=hFAKES_2->GetBinError(j)*weightBin;
		hFAKES_2->SetBinContent(j,binContent);
		hFAKES_2->SetBinError(j,binError);

		binContent=hDY_2->GetBinContent(j)*weightBin;
		binError=hDY_2->GetBinError(j)*weightBin;
		hDY_2->SetBinContent(j,binContent);
		hDY_2->SetBinError(j,binError);

		binContent=hWW_2->GetBinContent(j)*weightBin;
		binError=hWW_2->GetBinError(j)*weightBin;
		hWW_2->SetBinContent(j,binContent);
		hWW_2->SetBinError(j,binError);

		binContent=hWGammaStar_2->GetBinContent(j)*weightBin;
		binError=hWGammaStar_2->GetBinError(j)*weightBin;
		hWGammaStar_2->SetBinContent(j,binContent);
		hWGammaStar_2->SetBinError(j,binError);

		binContent=hWGamma_2->GetBinContent(j)*weightBin;
		binError=hWGamma_2->GetBinError(j)*weightBin;
		hWGamma_2->SetBinContent(j,binContent);
		hWGamma_2->SetBinError(j,binError);

		binContent=hTOP_2->GetBinContent(j)*weightBin;
		binError=hTOP_2->GetBinError(j)*weightBin;
		hTOP_2->SetBinContent(j,binContent);
		hTOP_2->SetBinError(j,binError);

		binContent=hTT_2->GetBinContent(j)*weightBin;
		binError=hTT_2->GetBinError(j)*weightBin;
		hTT_2->SetBinContent(j,binContent);
		hTT_2->SetBinError(j,binError);

		binContent=hZTauTau_2->GetBinContent(j)*weightBin;
		binError=hZTauTau_2->GetBinError(j)*weightBin;
		hZTauTau_2->SetBinContent(j,binContent);
		hZTauTau_2->SetBinError(j,binError);

		binContent=hLFVVBF126_2->GetBinContent(j)*weightBin;
		binError=hLFVVBF126_2->GetBinError(j)*weightBin;
		hLFVVBF126_2->SetBinContent(j,binContent);
		hLFVVBF126_2->SetBinError(j,binError);

		binContent=hLFVGG126_2->GetBinContent(j)*weightBin;
		binError=hLFVGG126_2->GetBinError(j)*weightBin;
		hLFVGG126_2->SetBinContent(j,binContent);
		hLFVGG126_2->SetBinError(j,binError);

		binContent=hSMVBF126_2->GetBinContent(j)*weightBin;
		binError=hSMVBF126_2->GetBinError(j)*weightBin;
		hSMVBF126_2->SetBinContent(j,binContent);
		hSMVBF126_2->SetBinError(j,binError);

		binContent=hSMGG126_2->GetBinContent(j)*weightBin;
		binError=hSMGG126_2->GetBinError(j)*weightBin;
		hSMGG126_2->SetBinContent(j,binContent);
		hSMGG126_2->SetBinError(j,binError);

		binContent=hSMHWWVBF126_2->GetBinContent(j)*weightBin;
		binError=hSMHWWVBF126_2->GetBinError(j)*weightBin;
		hSMHWWVBF126_2->SetBinContent(j,binContent);
		hSMHWWVBF126_2->SetBinError(j,binError);

		binContent=hSMHWWGG126_2->GetBinContent(j)*weightBin;
		binError=hSMHWWGG126_2->GetBinError(j)*weightBin;
		hSMHWWGG126_2->SetBinContent(j,binContent);
		hSMHWWGG126_2->SetBinError(j,binError);


		binContent=hdata_obs_2->GetBinContent(j)*weightBin;
		binError=hdata_obs_2->GetBinError(j)*weightBin;
		hdata_obs_2->SetBinContent(j,binContent);
		hdata_obs_2->SetBinError(j,binError);

	}	

}
