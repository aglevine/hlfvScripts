#include "tdrstyle.C"
#include "CMS_lumi.C"

void plotsNoFitBand(bool mine=true,TString name="collMass",TString file="fit2_signalV5_collMass_type1.root", TString dir="filesBoosted", TString dirInternal="ggmutau",double blindA=100, double blindB=160, bool blind=false, TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", double xmin=200, double xmax=500, int rebinning=1, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1, double MIN=-1, double CORRFR=1., double scaleSignal=10.0, double ymin=-0.95, double ymax=0.95){

  //gROOT->LoadMacro("tdrstyle.C");
  setTDRStyle();
  double kForPlotting=1;
  double branchingratioTauTau=0.063;
  double branchingratioTauMu=0.1;
  double Lumi=19717;
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



 // Get Plots

 // Get Plots

        TFile *_file0= new TFile(dir+"/"+file);
	TString find="/DY";
	if(!mine) find="/zjetsother";
        TH1F *hDY=_file0->Get(dirInternal+find); hDY->SetName("DY");
	find="/VV";
	if(!mine) find="/ww";
        TH1F *hWW=_file0->Get(dirInternal+find); hWW->SetName("WW");
	find="/TOP";
	if(!mine) find="/singlet";
        TH1F *hTOP=_file0->Get(dirInternal+find); hTOP->SetName("TOP");
	find="/TT";
	if(!mine) find="/ttbar";
        TH1F *hTT=_file0->Get(dirInternal+find); hTT->SetName("TT");
	find="/ZTauTau";
	if(!mine) find="/ztautau";
        TH1F *hZTauTau=_file0->Get(dirInternal+find); hZTauTau->SetName("ZTauTau");
	find="/FAKES";
	if(!mine) find="/fakes";
        TH1F *hFAKES=_file0->Get(dirInternal+find); hFAKES->SetName("fakes");
                hFAKES->Scale(CORRFR);
        TH1F *hLFVVBF126=_file0->Get(dirInternal+"/LFVVBF126"); hLFVVBF126->SetName("LFVVBF126");
        TH1F *hSMVBF126=_file0->Get(dirInternal+"/SMVBF126"); hSMVBF126->SetName("SMVBF126");
        TH1F *hLFVGG126=_file0->Get(dirInternal+"/LFVGG126"); hLFVGG126->SetName("LFVGG126");
        TH1F *hSMGG126=_file0->Get(dirInternal+"/SMGG126"); hSMGG126->SetName("SMGG126");

	find="/data_unblind";
	if(!mine) find="/data_obs";
        TH1F *hdata_obs=_file0->Get(dirInternal+find); 
	hdata_obs->SetName("data_obs");


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
        hTT->SetFillColor(40); hTT->SetLineColor(kBlue+4); hTT->SetLineWidth(1);;  hTT->SetLineWidth(1);
        hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hDY->SetFillColor(kAzure+3); hDY->SetLineColor(kAzure+4); hDY->SetLineWidth(1);
        hWW->SetFillColor(kRed+2); hWW->SetLineColor(kRed+4); hWW->SetLineWidth(1);

        hLFVGG126->SetLineColor(kBlue);  hLFVGG126->SetLineWidth(3);
        hLFVVBF126->SetLineColor(kBlue); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);
        hSMVBF126->SetLineColor(kMagenta); hSMVBF126->SetLineWidth(3); hSMVBF126->SetLineStyle(kDashed); 
        hSMGG126->SetLineColor(kMagenta); hSMGG126->SetLineWidth(3); 
        hSMHIGGS->SetFillColor(kMagenta); hSMHIGGS->SetLineColor(kMagenta+1); hSMHIGGS->SetLineWidth(1);



	hdata_obs->SetMarkerSize(1); // Closer to Daniel's

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
	hdata_obs->Rebin(rebinning);
	hSMHIGGS->Rebin(rebinning);

// PLOT

        TCanvas *c1 = new TCanvas("canvas_"+name);
        TPad *Pad1= new TPad("pad1","",0,0.2,1,1); Pad1->Draw(); Pad1->cd();;
        Pad1->SetLeftMargin(0.2147651);
        Pad1->SetRightMargin(0.06543624);
        Pad1->SetTopMargin(0.07);
        Pad1->SetBottomMargin(0.04);

	TH1F* hFAKESERROR=hFAKES->Clone(); hFAKESERROR->SetName("hFAKESERROR");

        for (int i=0; i<hFAKES->GetNbinsX()+1; i++){
                double content=hFAKES->GetBinContent(i);
                double contentErr=hFAKES->GetBinError(i);
		double err=sqrt(0.3*0.3*content*content+contentErr*contentErr);
                hFAKESERROR->SetBinError(i,err);
        }

        TH1F* fullMC2=hFAKES->Clone(); fullMC2->SetName("fullMC2");  
	//fullMC2->Add(hZTauTau); fullMC2->Add(hTT); fullMC2->Add(hWW);
        //fullMC2->Add(hDY); fullMC2->Add(hTOP);
        fullMC2->SetFillColorAlpha(kBlack, 0.45); //fullMC2->SetFillStyle(3002); 
        fullMC2->SetMarkerSize(0); fullMC2->SetLineWidth(0); fullMC2->SetLineColor(kBlack);
	fullMC2->Draw("hist");

        TH1F* fullMC3=hFAKESERROR->Clone();  fullMC3->SetName("fullMC3"); 
	//fullMC3->Add(hZTauTau); fullMC3->Add(hTT); fullMC3->Add(hWW);
        //fullMC3->Add(hDY); fullMC3->Add(hTOP);
        fullMC3->SetFillColorAlpha(kGray+2, 0.35); 
        //fullMC3->SetFillStyle(3013); 
        fullMC3->SetMarkerSize(0); fullMC3->SetLineWidth(0); fullMC3->SetLineColor(kBlack);

        fullMC2->GetXaxis()->SetTitle("");
        fullMC2->GetYaxis()->SetTitle(Yaxis);
        fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
        fullMC2->GetYaxis()->SetTitleOffset(1.2);
        fullMC2->GetYaxis()->SetTitleSize(0.05);
        fullMC2->GetXaxis()->SetNdivisions(505);
	fullMC2->GetXaxis()->SetLabelSize(0.0);
        fullMC2->GetYaxis()->SetLabelSize(0.04);

	THStack* stack = new THStack("stack","");
        /*stack->Add(hWW);
        stack->Add(hTT);
        stack->Add(hTOP);
        stack->Add(hDY);
        stack->Add(hZTauTau);
	*/
        stack->Add(hFAKES);
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
        fullMC3->Draw("sames,E2");
	fullMC2->Draw("sames,E2");

        hLFVVBF126->Draw("sameshist");
        hLFVGG126->Draw("sameshist");

        double maxData=hdata_obs->GetMaximum();
        double maxMC=stack->GetMaximum()*1.2;
	double maxLFV=hLFVGG126->GetMaximum();
        double maxLFV2=hLFVVBF126->GetMaximum();
        double minMC=stack->GetMinimum();

        if(maxData>maxMC) {maxMC=1.2*maxData;}
	if(maxLFV>maxMC) {maxMC=1.2*maxLFV;}
        if(maxLFV2>maxMC) {maxMC=1.2*maxLFV2;}
	if(MAX!=-1) {maxMC=MAX;}

	stack->SetMaximum(maxMC);
	stack->GetYaxis()->SetRangeUser(minMC,maxMC);
        fullMC2->SetMaximum(maxMC);
        fullMC2->GetYaxis()->SetRangeUser(minMC,maxMC);

	if(setLogY){fullMC2->SetMinimum(0.01); fullMC2->GetYaxis()->SetRangeUser(0.1,maxMC*1000);}

        TH1F* histoDataUnblindedV4=hdata_obs->Clone(); histoDataUnblindedV4->SetName("data_unblinded");

        if(!blind) hdata_obs->Draw("sames");
        else {
                int findBinA=hdata_obs->FindBin(blindA);
                int findBinB=hdata_obs->FindBin(blindB);
                for (int i=findBinA; i<findBinB; i++) hdata_obs->SetBinContent(i,-1000);
                hdata_obs->Draw("sames");
/*                   TPave *pave = new TPave(blindA,minMC,blindB,maxMC,4,"br");
                   pave->SetFillColor(kGray+1);
                   pave->SetFillStyle(3003);
                   pave->SetDrawOption(0);
                   pave->SetBorderSize(0);
                   pave->Draw();
*/
        }


   TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
   leg->SetFillColor(0);
   leg->SetBorderSize(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry;
   entry=leg->AddEntry(hdata_obs,"Data, #mu#tau_{h}","p");
   entry=leg->AddEntry(fullMC2,"Bkgd. stat. uncertainty","f");
   entry=leg->AddEntry(fullMC3,"Bkgd. syst. uncertainty","f");
   entry=leg->AddEntry(hFAKES,"Misidentified #tau","f");
   entry=leg->AddEntry(hLFVGG126,"LFV GG Higgs (B=100%)","l");
   entry=leg->AddEntry(hLFVVBF126,"LFV VBF Higgs (B=100%)","l");
   

   leg->Draw();

   CMS_lumi( Pad1, iPeriod, iPos );
   //cmsPrelim(Lumi);
	
        Pad1->SetLogy(setLogY);
	gPad->RedrawAxis();

        c1->cd(); TPad *Pad2= new TPad("pad2","",0,0,1,0.23); Pad2->Draw(); Pad2->cd();  Pad2->SetGridy();
        Pad2->SetLeftMargin(0.2147651);
        Pad2->SetRightMargin(0.06543624);
        Pad2->SetTopMargin(0.0);
        Pad2->SetBottomMargin(0.37);
        Pad2->SetFillStyle(0);



        TH1F * Ratio=hdata_obs->Clone(); Ratio->SetName("Ratio");
        Ratio->Add(fullMC2,-1);

        Ratio->Divide(fullMC2);
        Ratio->GetXaxis()->SetLabelFont(42);
        Ratio->GetXaxis()->SetTitleFont(42);
        Ratio->GetYaxis()->SetNdivisions(505);
        Ratio->GetYaxis()->SetLabelFont(42);
        Ratio->GetYaxis()->SetLabelSize(0.122);
        Ratio->GetYaxis()->SetRangeUser(ymin,ymax);
        Ratio->GetXaxis()->SetRangeUser(xmin,xmax);
        Ratio->GetXaxis()->SetLabelSize(0.12);
        Ratio->GetXaxis()->SetLabelFont(42);
        Ratio->SetYTitle("#frac{Data-Bkgd}{Bkgd}");
        Ratio->SetXTitle(Xaxis);
        Ratio->GetXaxis()->SetNdivisions(505);
        Ratio->GetYaxis()->CenterTitle(true);
        Ratio->GetYaxis()->SetTitleOffset(0.4);
        Ratio->GetYaxis()->SetTitleSize(0.11);
        Ratio->GetXaxis()->SetTitleOffset(0.75);
        Ratio->GetXaxis()->SetTitleSize(0.20);
        Ratio->SetMarkerSize(1.);


        TH1F* RatioError = Ratio->Clone(); RatioError->SetName("RatioError");
        TH1F* RatioError2 = Ratio->Clone(); RatioError2->SetName("RatioError2");

        for (int i=0; i<RatioError->GetNbinsX()+1; i++){
                        double error=fullMC2->GetBinError(i)*hdata_obs->GetBinContent(i)/fullMC2->GetBinContent(i)/fullMC2->GetBinContent(i);
                        double error2=0.3+error;//fullMC3->GetBinError(i)*hdata_obs->GetBinContent(i)/fullMC3->GetBinContent(i)/fullMC3->GetBinContent(i);
                        RatioError->SetBinContent(i,0);
                        RatioError->SetBinError(i,error);
                        RatioError2->SetBinContent(i,0);
                        RatioError2->SetBinError(i,error2);
        }
	 RatioError2->Draw("E2");//RatioError2->SetFillStyle(3013); 
         RatioError2->SetFillColorAlpha(kGray+2, 0.35); RatioError2->SetMarkerSize(0); RatioError2->SetLineWidth(2);
         RatioError->Draw("E2,sames"); RatioError->SetFillColorAlpha(kBlack, 0.45); 
         //RatioError->SetFillStyle(3002); 
         RatioError->SetMarkerSize(0);

        if(!blind) Ratio->Draw("sames");
        else {
                int findBinA=Ratio->FindBin(blindA);
                int findBinB=Ratio->FindBin(blindB);
                for (int i=findBinA; i<findBinB; i++) Ratio->SetBinContent(i,-100);
                Ratio->Draw("sames");

                   TPave *pave = new TPave(blindA,-0.5,blindB,0.5,4,"br");
                   pave->SetFillColor(1);
                   //pave->SetFillStyle(3003);
                   pave->SetFillStyle(3021);
                   pave->SetDrawOption(0);
                   pave->SetBorderSize(0);
                   pave->Draw();
        }

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


