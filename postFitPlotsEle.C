#include "tdrstyle.C"
#include "CMS_lumi.C"

void postFitPlotsEle(TString name="collMass",TString dirData = "", TString fileData="fit2_signalV5_collMass_type1.root", TString file="fit2_signalV5_collMass_type1.root", TString dir="filesBoosted", TString dirInternalData="filesBoosted", TString dirInternal="ggmutau",bool postfit=true,double blindA=100, double blindB=160, bool blind=false, TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", TString Tex = "",double xmin=200, double xmax=500, double ymin=-2, double ymax=2, int rebinning=1, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1, double MIN=-1, double scaleSignal=1.0, bool skipDY=false){

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


        TFile *_file= new TFile(dirData+"/"+fileData);
        TString finddata="/data_obs";
        TH1F* hdata_obsNoErrFix=_file->Get(dirInternalData+finddata);
        TH1F* hdata_obs = hdata_obsNoErrFix->Clone();
        std::cout << hdata_obsNoErrFix->GetEntries() << std::endl;
        for (i = 1; i <= hdata_obs->GetNbinsX(); i++){
                if (hdata_obs->GetBinContent(i) == 0){
                        hdata_obs->SetBinContent(i,0.0);
                        hdata_obs->SetBinError(i,1.8);
                }
        }

        hdata_obs->SetName("data_obs");
        cout<<hdata_obs->GetNbinsX()<<endl;

        TFile *_fileMC= new TFile(dir+"/"+file);

	TString dyfile="/Fakes";
	bool ifDYOther=false;
	if(_fileMC->Get(dirInternal+"/DYnoTauTau")) {dyfile="/DYnoTauTau"; ifDYOther=true;}
	TH1F *hDY_2=_fileMC->Get(dirInternal+dyfile); hDY_2->SetName("hDY_2");
	if(!ifDYOther) hDY_2->Scale(0);
        TH1F *hWW_2=_fileMC->Get(dirInternal+"/WW"); 
	
	TString wg="/Fakes";
	bool ifWG=false;
	if(_fileMC->Get(dirInternal+"/WG")) { wg="/WG"; ifWG=true;}
        TH1F *hWG_2=_fileMC->Get(dirInternal+wg); hWG_2->SetName("hWG_2");
	if(!ifWG) hWG_2->Scale(0.);

        TString wgstar="/Fakes";
        bool ifWGStar=false;
        if(_fileMC->Get(dirInternal+"/WGStar")) { wgstar="/WGStar"; ifWGStar=true;}
        TH1F *hWGStar_2=_fileMC->Get(dirInternal+wgstar);   hWGStar_2->SetName("hWGStar_2");
        if(!ifWGStar) hWGStar_2->Scale(0.);

	hWG_2->Add(hWGStar_2);

        TH1F *hFAKES_2=_fileMC->Get(dirInternal+"/Fakes");
        TH1F *hTOP_2=_fileMC->Get(dirInternal+"/TOP"); 
        TH1F *hTT_2=_fileMC->Get(dirInternal+"/TT"); 
        TH1F *hZTauTau_2=_fileMC->Get(dirInternal+"/ZTauTau"); 

        TH1F *hLFVVBF126_2=_fileMC->Get(dirInternal+"/LFVVBF"); hLFVVBF126_2->SetName("buh");
        TH1F *hLFVGG126_2=_fileMC->Get(dirInternal+"/LFVGG");

        TH1F *hSMVBF126_2=_fileMC->Get(dirInternal+"/vbfHTauTau"); 
        TH1F *hSMGG126_2=_fileMC->Get(dirInternal+"/ggHTauTau"); 
        TH1F *hSMHWWVBF126_2=_fileMC->Get(dirInternal+"/vbfHWW");
        TH1F *hSMHWWGG126_2=_fileMC->Get(dirInternal+"/ggHWW");

	TH1F *hFAKES=hdata_obs->Clone(); hFAKES->SetName("fakesLepton"); 
        TH1F *hDY=hdata_obs->Clone(); hDY->SetName("DY"); 
        TH1F *hWW=hdata_obs->Clone(); hWW->SetName("WW"); 
        TH1F *hWG=hdata_obs->Clone(); hWG->SetName("WG");
        TH1F *hTOP=hdata_obs->Clone(); hTOP->SetName("TOP"); 
        TH1F *hTT=hdata_obs->Clone(); hTT->SetName("TT"); 
        TH1F *hZTauTau=hdata_obs->Clone(); hZTauTau->SetName("ZTauTau"); 
	TH1F *hLFVVBF126=hdata_obs->Clone(); hLFVVBF126->SetName("LFVVBF126");
        TH1F *hLFVGG126=hdata_obs->Clone(); hLFVGG126->SetName("LFVGG126");
        TH1F *hSMVBF126=hdata_obs->Clone(); hSMVBF126->SetName("SMVBF126");
        TH1F *hSMGG126=hdata_obs->Clone(); hSMGG126->SetName("SMGG126");
        TH1F *hSMHWWVBF126=hdata_obs->Clone(); hSMHWWVBF126->SetName("SMHWWVBF126");
        TH1F *hSMHWWGG126=hdata_obs->Clone(); hSMHWWGG126->SetName("SMHWWGG126");

	for (int i=0; i<hFAKES_2->GetNbinsX(); i++) {
			hFAKES->SetBinContent(i,hFAKES_2->GetBinContent(i));
                        hFAKES->SetBinError(i,hFAKES_2->GetBinError(i));

                        hDY->SetBinContent(i,hDY_2->GetBinContent(i));
                        hDY->SetBinError(i,hDY_2->GetBinError(i));

                        hWW->SetBinContent(i,hWW_2->GetBinContent(i));
                        hWW->SetBinError(i,hWW_2->GetBinError(i));

                        hWG->SetBinContent(i,hWG_2->GetBinContent(i));
                        hWG->SetBinError(i,hWG_2->GetBinError(i));

                        hTOP->SetBinContent(i,hTOP_2->GetBinContent(i));
                        hTOP->SetBinError(i,hTOP_2->GetBinError(i));

                        hTT->SetBinContent(i,hTT_2->GetBinContent(i));
                        hTT->SetBinError(i,hTT_2->GetBinError(i));

                        hZTauTau->SetBinContent(i,hZTauTau_2->GetBinContent(i));
                        hZTauTau->SetBinError(i,hZTauTau_2->GetBinError(i));

                        hLFVVBF126->SetBinContent(i,hLFVVBF126_2->GetBinContent(i));
                        hLFVVBF126->SetBinError(i,hLFVVBF126_2->GetBinError(i));

                        hLFVGG126->SetBinContent(i,hLFVGG126_2->GetBinContent(i));
                        hLFVGG126->SetBinError(i,hLFVGG126_2->GetBinError(i));

                        hSMVBF126->SetBinContent(i,hSMVBF126_2->GetBinContent(i));
                        hSMVBF126->SetBinError(i,hSMVBF126_2->GetBinError(i));

                        hSMGG126->SetBinContent(i,hSMGG126_2->GetBinContent(i));
                        hSMGG126->SetBinError(i,hSMGG126_2->GetBinError(i));

                        hSMHWWVBF126->SetBinContent(i,hSMHWWVBF126_2->GetBinContent(i));
                        hSMHWWVBF126->SetBinError(i,hSMHWWVBF126_2->GetBinError(i));

                        hSMHWWGG126->SetBinContent(i,hSMHWWGG126_2->GetBinContent(i));
                        hSMHWWGG126->SetBinError(i,hSMHWWGG126_2->GetBinError(i));

	}

	TH1F *hSMHIGGS=(TH1F*) hSMVBF126->Clone();hSMHIGGS->SetName("hSMHIGGS");
	hSMHIGGS->Add(hSMGG126);
	hSMHIGGS->Add(hSMHWWGG126); hSMHIGGS->Add(hSMHWWVBF126);

        TH1F* hSignal=(TH1F*)hLFVGG126->Clone(); hSignal->SetName("hSignal");
        hSignal->Add(hLFVVBF126);


        hFAKES->SetFillColor(kMagenta-10); hFAKES->SetLineColor(kMagenta+4); hFAKES->SetLineWidth(1);
        hZTauTau->SetFillColor(kOrange-4); hZTauTau->SetLineColor(kOrange+4); hZTauTau->SetLineWidth(1);

        hDY->SetFillColor(kAzure+3); hDY->SetLineColor(kAzure+4); hDY->SetLineWidth(1);
        hWW->SetFillColor(kAzure+3); hWW->SetLineColor(kAzure+3); hWW->SetLineWidth(1);
        hWG->SetFillColor(kAzure+3); hWG->SetLineColor(kAzure+3); hWG->SetLineWidth(1);

        hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hTT->SetFillColor(kGreen-2); hTT->SetLineColor(kGreen-2); hTT->SetLineWidth(1);

	hSMHIGGS->SetFillColor(kMagenta); hSMHIGGS->SetLineColor(kMagenta+1); hSMHIGGS->SetLineWidth(1);

        hLFVGG126->SetLineColor(kBlue);  hLFVGG126->SetLineWidth(3);
        hLFVVBF126->SetLineColor(kBlue+3); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);
        hSMVBF126->SetLineColor(kMagenta+3); hSMVBF126->SetLineWidth(3); 
        hSMGG126->SetLineColor(kMagenta); hSMGG126->SetLineWidth(3); 

        hSignal->SetLineColor(kBlue);  hSignal->SetLineWidth(3);
        hSignal->SetLineStyle(2);

	hdata_obs->SetMarkerSize(1); // Closer to Daniel's

/*	
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

*/
	
// PLOT

	TCanvas *c1 = new TCanvas("canvas_"+name);   
        TPad *Pad1= new TPad("pad1","",0,0.2,1,1); Pad1->Draw(); Pad1->cd();;
        Pad1->SetLeftMargin(0.2147651);
        Pad1->SetRightMargin(0.06543624);
        Pad1->SetTopMargin(0.07);
        Pad1->SetBottomMargin(0.04);

        TH1F* fullMC2=hFAKES->Clone();  fullMC2->Add(hZTauTau); fullMC2->Add(hTT); fullMC2->Add(hWG); fullMC2->Add(hWW);
        fullMC2->Add(hDY); fullMC2->Add(hTOP); fullMC2->Add(hSMHIGGS); 
                fullMC2->SetFillColorAlpha(kGray+2, 0.35);  //fullMC2->SetFillStyle(3002); 
        fullMC2->SetMarkerSize(0); fullMC2->SetLineWidth(0);
        fullMC2->Draw("hist");

        fullMC2->GetXaxis()->SetTitle("");
        fullMC2->GetYaxis()->SetTitle(Yaxis);
        fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
        fullMC2->GetYaxis()->SetTitleOffset(1.2);
        fullMC2->GetYaxis()->SetTitleSize(0.05);
        fullMC2->GetXaxis()->SetNdivisions(505);
        fullMC2->GetYaxis()->SetLabelSize(0.04);
 	fullMC2->GetXaxis()->SetLabelSize(0.0);

	THStack* stack = new THStack("stack","");
        stack->Add(hFAKES);
        stack->Add(hWG);
        stack->Add(hWW);
        stack->Add(hDY);
        stack->Add(hTT);
        stack->Add(hTOP);
        stack->Add(hZTauTau);
        stack->Add(hSMHIGGS);;
        stack->Add(hSignal);;

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

//        hSignal->Draw("sameshist");

        double maxData=hdata_obs->GetMaximum();
        double maxMC=stack->GetMaximum()*1.2;
	double maxLFV=hLFVGG126->GetMaximum();
        double maxLFV2=hLFVVBF126->GetMaximum();
        double minMC=stack->GetMinimum();

        if(maxData>maxMC) {maxMC=1.2*maxData;}
	if(maxLFV>maxMC) {maxMC=1.2*maxLFV;}
        if(maxLFV2>maxMC) {maxMC=1.2*maxLFV2;}
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
   entry=leg->AddEntry(hdata_obs,"Data, #mu#tau_{e}","p");
   entry=leg->AddEntry(fullMC2,"Bkgd. uncertainty","f");
   entry=leg->AddEntry(hSMHIGGS,"SM Higgs","f");
   eblindBy=leg->AddEntry(hZTauTau,"Z#rightarrow#tau#tau","f");
        entry=leg->AddEntry(hDY,"Other","f");
        entry=leg->AddEntry(hTOP,"t#bar{t}, t, #bar{t}","f");
   entry=leg->AddEntry(hFAKES,"Misidentified leptons","f");
        if(postfit) entry=leg->AddEntry(hSignal,"LFV Higgs (B=0.84%)","l");
        else entry=leg->AddEntry(hSignal,"LFV Higgs (B=1%)","l");
//        entry=leg->AddEntry("NULL","Br(h#rightarrow#mu#tau)=1%","");
//        entry=leg->AddEntry("NULL","Br(h#rightarrow#tau#tau)=6%","");



   leg->Draw();

   TLatex latex;
   latex.SetNDC();
   latex.SetTextAngle(0);
   latex.SetTextColor(kBlack);

   latex.SetTextFont(42);
   latex.SetTextAlign(31);
   latex.SetTextSize(.05);
   latex.DrawLatex(0.39,0.8,Tex);

   if(blind){	
                   TPave *pave = new TPave(blindA,0,blindB,MAX,4,"br");
                   pave->SetFillColor(kGray+1);
                   pave->SetFillStyle(3002);
                   pave->SetDrawOption(0);
                   pave->SetBorderSize(0);
                   pave->Draw();
   }


   CMS_lumi( Pad1, iPeriod, iPos );
   //cmsPrelim(Lumi);

        Pad1->SetLogy(setLogY);
 	gPad->RedrawAxis();


        c1->cd(); gPad->RedrawAxis(); TPad *Pad2= new TPad("pad2","",0,0,1,0.23); Pad2->Draw(); Pad2->cd();  Pad2->SetGridy();
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
	if(!postfit)        Ratio->SetYTitle("#frac{Data-Bkgd  }{Bkgd}");
	else 		    Ratio->SetYTitle("#frac{Data-Bkgd (fit)  }{Bkgd (fit)}");	
        Ratio->SetXTitle(Xaxis);
        Ratio->GetXaxis()->SetNdivisions(505);
        Ratio->GetYaxis()->CenterTitle(true);
        Ratio->GetYaxis()->SetTitleOffset(0.4);
        Ratio->GetYaxis()->SetTitleSize(0.11);
        Ratio->GetXaxis()->SetTitleOffset(0.75);
        Ratio->GetXaxis()->SetTitleSize(0.20);
        Ratio->SetMarkerSize(1.);

        TH1F* RatioError = Ratio->Clone(); RatioError->SetName("RatioError");

        for (int i=0; i<RatioError->GetNbinsX()+1; i++){
//                        double error=fullMC2->GetBinError(i)*hdata_obs->GetBinContent(i)/fullMC2->GetBinContent(i)/fullMC2->GetBinContent(i);
			double error=fullMC2->GetBinError(i)/fullMC2->GetBinContent(i);
                        RatioError->SetBinContent(i,0);
                        RatioError->SetBinError(i,error);
        }

        RatioError->Draw("E2"); //RatioError->SetFillStyle(3002); 
        RatioError->SetFillColorAlpha(kGray+2, 0.35); RatioError->SetMarkerSize(0);

        if(!blind) //Ratio->Draw("samesE0"); //errorbarswithoutdatapoints
		   Ratio->Draw("sames");
        else {
                int findBinA=Ratio->FindBin(blindA);
                int findBinB=Ratio->FindBin(blindB);
                for (int i=findBinA; i<findBinB; i++) Ratio->SetBinContent(i,-100);
                Ratio->Draw("sames");

                   TPave *pave = new TPave(blindA,ymin,blindB,ymax,4,"br");
                   pave->SetFillColor(kGray+1);
                   pave->SetFillStyle(3002);
                   pave->SetDrawOption(0);
                   pave->SetBorderSize(0);
                   pave->Draw();

                for (int i=findBinA; i<findBinB; i++) hdata_obs->SetBinContent(i,-100);

        }
       gPad->RedrawAxis();
       if(!setLogY){	
       		//c1->SaveAs(name+"ErrorBarsWithoutDataPoints.png");
       		//c1->SaveAs(name+"ErrorBarsWithoutDataPoints.pdf");
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


