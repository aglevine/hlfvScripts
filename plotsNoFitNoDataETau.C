#include "tdrstyle.C"
#include "CMS_lumi.C"

void plotsNoFitNoDataETau(bool mine=false,TString name="collMass",TString file="LFV_vbf_collMass_fakeRate_zjetsEmbed_newSignal.root", TString dir="preselectionMetFix_Nov2", TString dirInternal="vbfmutau",double blindA=100, double blindB=160, bool blind=false, TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", TString Tex="#mu#tau_{h} 0 Jet", double xmin=0, double xmax=300, int rebinning=1, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1, double MIN=-1, double CORRFR=1., double scaleSignal=1.0, double ymin=-0.95, double ymax=0.95){

  //gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  //gROOT->LoadMacro("CMS_lumi.C");
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



  double kForPlotting=1;
  double branchingratioTauTau=0.063;
  double branchingratioTauMu=0.1;
  double Lumi=19717;

 // Get Plots

 // Get Plots
	std::cout << dir << file << dirInternal <<std::endl;
        TFile *_file0= new TFile(dir+"/"+file);
	TString find="zjetsother";
	if(!mine) find="zjetsother";
        TH1F *hDY=_file0->Get(dirInternal+find); hDY->SetName("DY");
	find="diboson";
	if(!mine) find="ww";
        TH1F *hWW=_file0->Get(dirInternal+find); hWW->SetName("WW");
	find="singlet";
	if(!mine) find="singlet";
        if(_file0->Get(dirInternal+find)){
        	TH1F *hTOP=_file0->Get(dirInternal+find); hTOP->SetName("TOP");
	}
	else{
		TH1F *hTOP=_file0->Get(dirInternal+"LFVGG"); hTOP->SetName("TOP"); hTOP->Scale(0);
	}
	find="ttbar";
	if(!mine) find="ttbar";
        TH1F *hTT=_file0->Get(dirInternal+find); hTT->SetName("TT");
	find="ztautau";
	if(!mine) find="ztautau";
        TH1F *hZTauTau=_file0->Get(dirInternal+find); hZTauTau->SetName("ZTauTau");
	find="fakes";
	if(!mine) find="fakes";
        TH1F *hFAKES=_file0->Get(dirInternal+find); hFAKES->SetName("fakes");
                hFAKES->Scale(CORRFR);
        TH1F *hLFVVBF126=_file0->Get(dirInternal+"LFVVBF"); hLFVVBF126->SetName("LFVVBF126");
        TH1F *hSMVBF126=_file0->Get(dirInternal+"SMVBF126"); hSMVBF126->SetName("SMVBF126");
        TH1F *hLFVGG126=_file0->Get(dirInternal+"LFVGG"); hLFVGG126->SetName("LFVGG126");
        TH1F *hSMGG126=_file0->Get(dirInternal+"SMGG126"); hSMGG126->SetName("SMGG126");

	find="Observed";


        TH1F* hSMHIGGS=hSMGG126->Clone(); hSMHIGGS->SetName("HIGGSSM");
        hSMHIGGS->Add(hSMVBF126);

        // For the Control plots only we want signal to be scaled to 100% Br
        hLFVVBF126->Scale(scaleSignal);
        hLFVGG126->Scale(scaleSignal);

// From the fit
/*	hDY->Scale(1.122280);
	hWW->Scale(1.254172);
	hTOP->Scale(1.348162);
	hTT->Scale(1.082784);
	hZTauTau->Scale(1.157596);
	hFAKES->Scale(0.901000);
*/
	
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

        hDY->SetFillColor(kAzure+3); hDY->SetLineColor(kAzure+4); hDY->SetLineWidth(1);
        hWW->SetFillColor(kAzure+3); hWW->SetLineColor(kAzure+3); hWW->SetLineWidth(1);

        hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hTT->SetFillColor(kGreen-2); hTT->SetLineColor(kGreen-2); hTT->SetLineWidth(1);

        hLFVGG126->SetLineColor(kBlue+1);  hLFVGG126->SetLineWidth(3);
        hLFVVBF126->SetLineColor(kBlue+1); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);
        hSMVBF126->SetLineColor(kMagenta); hSMVBF126->SetLineWidth(3); hSMVBF126->SetLineStyle(kDashed); 
        hSMGG126->SetLineColor(kMagenta); hSMGG126->SetLineWidth(3); 
        hSMHIGGS->SetFillColor(kMagenta); hSMHIGGS->SetLineColor(kMagenta+1); hSMHIGGS->SetLineWidth(1);


 // Rebin

	hFAKES->Rebin(rebinning);
	hZTauTau->Rebin(rebinning);
        hDY->Rebin(rebinning);
        hTOP->Rebin(rebinning);
	hTT->Rebin(rebinning);
	hWW->Rebin(rebinning);
	hLFVGG126->Rebin(rebinning);
	hLFVVBF126->Rebin(rebinning);
	hSMVBF126->Rebin(rebinning);
        hSMGG126->Rebin(rebinning);
	hSMHIGGS->Rebin(rebinning);

// PLOT

        TCanvas *c1 = new TCanvas("canvas_"+name);
        TPad *Pad1= new TPad("pad1","",0,0,1,1); Pad1->Draw(); Pad1->cd();;
        Pad1->SetLeftMargin(0.2147651);
        Pad1->SetRightMargin(0.06543624);
        Pad1->SetTopMargin(0.07);
        Pad1->SetBottomMargin(0.2);


        for (int i=0; i<hFAKES->GetNbinsX()+1; i++){
                double content=hFAKES->GetBinContent(i);
                double contentErr=0;//sqrt(content);//hFAKES->GetBinError(i);
		double err=sqrt(0.3*0.3*content*content+contentErr*contentErr);
                hFAKES->SetBinError(i,err);
        }

        TH1F* fullMC2=hZTauTau->Clone();  fullMC2->Add(hFAKES); fullMC2->Add(hTT); fullMC2->Add(hWW);
        fullMC2->Add(hDY); fullMC2->Add(hTOP);
        fullMC2->SetFillColorAlpha(kGray+2, 0.35); 
        //fullMC2->SetFillStyle(3002); 
        fullMC2->SetMarkerSize(0);
	fullMC2->Draw("hist");

        fullMC2->GetYaxis()->SetTitle(Yaxis);
        fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
        fullMC2->GetYaxis()->SetTitleOffset(1.2);
        fullMC2->GetYaxis()->SetTitleSize(0.05);
        fullMC2->GetXaxis()->SetNdivisions(505);
        fullMC2->GetYaxis()->SetLabelSize(0.04);
	fullMC2->GetXaxis()->SetLabelSize(0);
        fullMC2->GetXaxis()->SetLabelFont(42);
        fullMC2->GetXaxis()->SetTitleFont(42);
        fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
        fullMC2->GetXaxis()->SetLabelSize(0.04);
        fullMC2->GetXaxis()->SetLabelFont(42);
        fullMC2->SetXTitle(Xaxis);
        fullMC2->GetXaxis()->SetNdivisions(505);
        fullMC2->GetXaxis()->SetTitleOffset(1.1);
        fullMC2->GetXaxis()->SetTitleSize(0.05);

	THStack* stack = new THStack("stack","");
        stack->Add(hFAKES);
        stack->Add(hWW);
        stack->Add(hDY);
        stack->Add(hTT);
        stack->Add(hTOP);
        stack->Add(hZTauTau);
        stack->Add(hSMHIGGS);

	cout<<"Yields"<<endl;
	cout<<"VV " <<hWW->Integral()<<endl;
        cout<<"TOP " <<hTOP->Integral()<<endl;
        cout<<"TT " <<hTT->Integral()<<endl;
        cout<<"DY " <<hDY->Integral()<<endl;
        cout<<"ZTauTau " <<hZTauTau->Integral()<<endl;
        cout<<"FAKES " <<hFAKES->Integral()<<endl;
        cout<<"LFVGG126 " <<hLFVGG126->Integral()<<endl;
        cout<<"LFVVBF126 " <<hLFVVBF126->Integral()<<endl;

	stack->Draw("samehist");
	fullMC2->Draw("sames,E2");

        hLFVVBF126->Draw("sameshist");
        hLFVGG126->Draw("sameshist");

        double maxMC=stack->GetMaximum()*1.2;
	double maxLFV=hLFVGG126->GetMaximum();
        double maxLFV2=hLFVVBF126->GetMaximum();
        double minMC=stack->GetMinimum();

	if(maxLFV>maxMC) {maxMC=1.2*maxLFV;}
        if(maxLFV2>maxMC) {maxMC=1.2*maxLFV2;}
	if(MAX!=-1) {maxMC=MAX;}

	stack->SetMaximum(maxMC);
	stack->GetYaxis()->SetRangeUser(minMC,maxMC);
        fullMC2->SetMaximum(maxMC);
        fullMC2->GetYaxis()->SetRangeUser(minMC,maxMC);

	if(setLogY){fullMC2->SetMinimum(0.1); fullMC2->GetYaxis()->SetRangeUser(1,maxMC*1000);}



   TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
   leg->SetFillColor(0);
   leg->SetBorderSize(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry;
   entry=leg->AddEntry(fullMC2,"Bkgd. uncertainty","f");
   entry=leg->AddEntry(hSMHIGGS,"SM Higgs","f");
   eblindBy=leg->AddEntry(hZTauTau,"Z#rightarrow#tau#tau","f");
        entry=leg->AddEntry(hTOP,"t#bar{t}, t, #bar{t}","f");
        entry=leg->AddEntry(hDY,"Other","f");
   entry=leg->AddEntry(hFAKES,"MisID'd #tau","f");
   entry=leg->AddEntry(hLFVGG126,"LFV GG Higgs (B=100%)","l");
   entry=leg->AddEntry(hLFVVBF126,"LFV VBF Higgs (B=100%)","l");
   


   leg->Draw();


    CMS_lumi( Pad1, iPeriod, iPos );

    TLatex latex;
    latex.SetNDC();
    latex.SetTextAngle(0);
    latex.SetTextColor(kBlack);

    latex.SetTextFont(42);
    latex.SetTextAlign(31);
    latex.SetTextSize(.05);
    latex.DrawLatex(0.39,0.8,Tex);

   //cmsPrelim(Lumi);
	
        Pad1->SetLogy(setLogY);
	gPad->RedrawAxis();

       if(!setLogY){	
       	//	c1->SaveAs(name+"ErrorBarsWithoutDataPoints.png");
       	//	c1->SaveAs(name+"ErrorBarsWithoutDataPoints.pdf");
              c1->SaveAs(name+".png");
              c1->SaveAs(name+".pdf");

	}
	else {
       		c1->SaveAs(name+"_log.png");
       		c1->SaveAs(name+"_log.pdf");
        }  

}


