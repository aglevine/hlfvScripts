void plotsANMCOnly(TString name="collMass",TString file="fit2_signalV5_collMass_type1.root", TString dir="filesBoosted", double blindA=100, double blindB=160, bool blind=false, TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", double xmin=200, double xmax=500, int rebinning=1, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1){


  gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  double kForPlotting=1;
  double branchingratioTauTau=0.063;
  double branchingratioTauMu=0.1;
  double Lumi=19717;
  TString dirInternal="ggmutau";

 // Get Plots

	TFile *_file0= new TFile(dir+"/"+file);
        TH1F *hQCD=_file0->Get(dirInternal+"/QCD"); hQCD->SetName("QCD");
        TH1F *hDY=_file0->Get(dirInternal+"/DY"); hDY->SetName("DY");
        TH1F *hWW=_file0->Get(dirInternal+"/WW"); hWW->SetName("WW");
        TH1F *hTOP=_file0->Get(dirInternal+"/TOP"); hTOP->SetName("TOP");
        TH1F *hTT=_file0->Get(dirInternal+"/TT"); hTT->SetName("TT");
        TH1F *hZTauTau=_file0->Get(dirInternal+"/ZTauTau"); hZTauTau->SetName("ZTauTau");
        TH1F *hFAKES=_file0->Get(dirInternal+"/MCFAKES"); hFAKES->SetName("fakes");
        TH1F *hLFVVBF126=_file0->Get(dirInternal+"/LFVVBF126"); hLFVVBF126->SetName("LFVVBF126");
        TH1F *hSMVBF126=_file0->Get(dirInternal+"/SMVBF126"); hSMVBF126->SetName("SMVBF126");
        TH1F *hLFVGG126=_file0->Get(dirInternal+"/LFVGG126"); hLFVGG126->SetName("LFVGG126");
        TH1F *hSMGG126=_file0->Get(dirInternal+"/SMGG126"); hSMGG126->SetName("SMGG126");

 // Daniel's Colors
/*
WGammaStar=kCyan
ZTauTauEmbedded=kOrange-4
ZLL_residual=kAzure+3
TTBar=40
SingleTop=kGreen-2
EWKDiBoson=kRed+2
WJets/QCD Multijets=kMagenta-10
SMHToTauTau=kMagenta
*/
        hFAKES->SetFillColor(kMagenta-10); hFAKES->SetLineColor(kMagenta+4); hFAKES->SetLineWidth(1);
        hZTauTau->SetFillColor(kOrange-4); hZTauTau->SetLineColor(kOrange+4); hZTauTau->SetLineWidth(1);
        hTT->SetFillColor(40); hTT->SetLineColor(kBlack); hTT->SetLineWidth(1);;  hTT->SetLineWidth(1);
        hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hDY->SetFillColor(kAzure+3); hDY->SetLineColor(kAzure+4); hDY->SetLineWidth(1);
        hQCD->SetFillColor(kCyan); hQCD->SetLineColor(kBlue+4); hQCD->SetLineWidth(1);
        hWW->SetFillColor(kRed+2); hWW->SetLineColor(kRed+4); hWW->SetLineWidth(1);

        hLFVGG126->SetLineColor(kBlue);  hLFVGG126->SetLineWidth(3);
        hLFVVBF126->SetLineColor(kBlue); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);
        hSMVBF126->SetLineColor(kMagenta); hSMVBF126->SetLineWidth(3); hSMVBF126->SetLineStyle(kDashed); 
        hSMGG126->SetLineColor(kMagenta); hSMGG126->SetLineWidth(3); 


 // Rebin

	hFAKES->Rebin(rebinning);
	hZTauTau->Rebin(rebinning);
	hQCD->Rebin(rebinning);
        hDY->Rebin(rebinning);
        hTOP->Rebin(rebinning);
	hTT->Rebin(rebinning);
	hWW->Rebin(rebinning);
	hLFVGG126->Rebin(rebinning);
	hLFVVBF126->Rebin(rebinning);
	hSMVBF126->Rebin(rebinning);
        hSMGG126->Rebin(rebinning);

// PLOT


	TCanvas *c1 = new TCanvas("canvas_"+name);   
	TPad *Pad1= new TPad("pad1","",0,0.,1,1); Pad1->Draw(); Pad1->cd();;
   	Pad1->SetLeftMargin(0.2147651);
   	Pad1->SetRightMargin(0.06543624);
   	Pad1->SetTopMargin(0.04895105);
   	Pad1->SetBottomMargin(0.1311189);
	Pad1->SetLogy(setLogY);

	THStack* stack = new THStack("stack","");
        stack->Add(hQCD);
        stack->Add(hWW);
        stack->Add(hTOP);
        stack->Add(hTT);
        stack->Add(hDY);
        stack->Add(hZTauTau);
        stack->Add(hFAKES);
        stack->Draw("hist");

        TH1F* fullMC2=hFAKES->Clone();  fullMC2->Add(hZTauTau); fullMC2->Add(hTT); fullMC2->Add(hWW); 
	fullMC2->Add(hQCD); fullMC2->Add(hDY); fullMC2->Add(hTOP);
	fullMC2->Add(hSMGG126); fullMC2->Add(hSMVBF126);
        fullMC2->SetFillColor(kGray+3); fullMC2->SetFillStyle(3001); fullMC2->SetMarkerSize(0);
        stack->GetXaxis()->SetTitle(Xaxis);
        stack->GetYaxis()->SetTitle(Yaxis);
        stack->GetXaxis()->SetRangeUser(xmin,xmax);
        stack->GetXaxis()->SetNdivisions(505);

	stack->GetYaxis()->SetTitleOffset(1.8);

	stack->Draw("hist");
	fullMC2->Draw("sames,E2");

        hLFVVBF126->Draw("sameshist");
        hLFVGG126->Draw("sameshist");
        hSMVBF126->Draw("sameshist");
        hSMGG126->Draw("sameshist");

        double maxMC=stack->GetMaximum();
	 double maxLFV=hLFVGG126->GetMaximum();
         double maxLFV2=hLFVVBF126->GetMaximum();

	if(maxLFV>maxMC) {maxMC=maxLFV;}
        if(maxLFV2>maxMC) {maxMC=maxLFV2;}
	if(MAX!=-1) maxMC=MAX;

	stack->SetMaximum(maxMC*1.05);


   TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
   leg->SetFillColor(0);
   leg->SetBorderSize(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry;
   entry=leg->AddEntry(hFAKES,"W+jets","f");
   eblindBy=leg->AddEntry(hZTauTau,"Z+#tau#tau (embedded)","f");
   eblindBy=leg->AddEntry(hDY,"Z+l^{+}l^{-}","f");
   entry=leg->AddEntry(hTT,"t#bar{t}","f");
   entry=leg->AddEntry(hTOP,"Single Top","f");
   entry=leg->AddEntry(hWW,"EWK Dibosons","f");
   entry=leg->AddEntry(hQCD,"QCD","f");
      /*  entry=leg->AddEntry(hLFVGG126,Form("LFV GG Higgs    (BR= %1.2f)",branchingratioTauMu),"l");
        entry=leg->AddEntry(hLFVVBF126,Form("LFV VBF Higgs    (BR= %1.2f)",branchingratioTauMu),"l");
        entry=leg->AddEntry(hSMVBF126,Form("SM VBF Higgs     (BR= %1.2f)",branchingratioTauTau),"l");
	*/
	entry=leg->AddEntry(hLFVGG126,"LFV GG Higgs","l");
        entry=leg->AddEntry(hLFVVBF126,"LFV VBF Higgs","l");
        entry=leg->AddEntry(hSMVBF126,"SM VBF Higgs","l");
        entry=leg->AddEntry(hSMGG126,"SM GG Higgs","l");


   leg->Draw();


   cmsPrelim(Lumi);

       if(!setLogY){	
       		c1->SaveAs(dir+"/"+name+"_MCONLY.png");
       		c1->SaveAs(dir+"/"+name+"_MCONLY.pdf");
	}
	else {
       		c1->SaveAs(dir+"/"+name+"_MCONLY_log.png");
       		c1->SaveAs(dir+"/"+name+"_MCONLY_log.pdf");
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


