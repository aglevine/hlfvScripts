#include "tdrstyle.C"
#include "CMS_lumi.C"

void plotsNoFitEleBand(TString name="collMass",TString fileData="fit2_signalV5_collMass_type1.root", TString file="fit2_signalV5_collMass_type1.root", TString dir="filesBoosted", TString dirInternalData="filesBoosted", TString dirInternal="ggmutau",bool postfit=true,double blindA=100, double blindB=160, bool blind=false, TString Xaxis="M_{#mu,#tau}_{coll} [GeV]", TString Yaxis="Events / 20 GeV", double xmin=200, double xmax=500, double ymin=-2, double ymax=2, int rebinning=1, bool setLogY=false, double legx1=0.6, double legy1=0.9, double legx2=0.9, double legy2=0.5, double MAX=-1, double MIN=-1, double scaleSignal=1.0, bool skipDY=false){
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




        TFile *_file= new TFile(dir+"/"+fileData);
        TString finddata="/data_obs";
        TH1F* hdata_obs=_file->Get(dirInternalData+finddata);
        hdata_obs->SetName("data_obs");
        cout<<hdata_obs->GetNbinsX()<<endl;

        TFile *_fileMC= new TFile(dir+"/"+file);

	TString dyfile="/Fakes";
	bool ifDYOther=false;
	if(_fileMC->Get(dirInternal+"/DYnoTauTau")) {dyfile="/DYnoTauTau"; ifDYOther=true;}
	TH1F *hDY=_fileMC->Get(dirInternal+dyfile); hDY->SetName("hDY");
	if(!ifDYOther) hDY->Scale(0);
        TH1F *hWW=_fileMC->Get(dirInternal+"/WW"); 
	
	TString wg="/Fakes";
	bool ifWG=false;
	if(_fileMC->Get(dirInternal+"/WG")) { wg="/WG"; ifWG=true;}
        TH1F *hWG=_fileMC->Get(dirInternal+wg); hWG->SetName("hWG");
	if(!ifWG) hWG->Scale(0.);

        TString wgstar="/Fakes";
        bool ifWGStar=false;
        if(_fileMC->Get(dirInternal+"/WGStar")) { wgstar="/WGStar"; ifWGStar=true;}
        TH1F *hWGStar=_fileMC->Get(dirInternal+wgstar);   hWGStar->SetName("hWGStar");
        if(!ifWGStar) hWGStar->Scale(0.);

	hWG->Add(hWGStar);

        TH1F *hFAKES=_fileMC->Get(dirInternal+"/Fakes");
        TH1F *hTOP=_fileMC->Get(dirInternal+"/TOP"); 
        TH1F *hTT=_fileMC->Get(dirInternal+"/TT"); 
        TH1F *hZTauTau=_fileMC->Get(dirInternal+"/ZTauTau"); 

        TH1F *hLFVVBF126=_fileMC->Get(dirInternal+"/LFVVBF"); hLFVVBF126->SetName("buh");
        TH1F *hLFVGG126=_fileMC->Get(dirInternal+"/LFVGG");

	hLFVVBF126->Scale(10);
	hLFVGG126->Scale(10);

	TH1F *hSMHIGGS=(TH1F*) hFAKES->Clone();hSMHIGGS->SetName("hSMHIGGS"); hSMHIGGS->Scale(0);

        hFAKES->SetFillColor(kMagenta-10); hFAKES->SetLineColor(kMagenta+4); hFAKES->SetLineWidth(1);
        //hZTauTau->SetFillColor(kOrange-4); hZTauTau->SetLineColor(kOrange+4); hZTauTau->SetLineWidth(1);
        //hZTauTau->SetFillColor(kAzure+3); hZTauTau->SetLineColor(kAzure+2); hZTauTau->SetLineWidth(1);
        hZTauTau->SetFillColor(kCyan+2); hZTauTau->SetLineColor(kCyan+2); hZTauTau->SetLineWidth(1);

        hDY->SetFillColor(kCyan+2); hDY->SetLineColor(kCyan+2); hDY->SetLineWidth(1);
        hWW->SetFillColor(kCyan+2); hWW->SetLineColor(kCyan+2); hWW->SetLineWidth(1);
        hWG->SetFillColor(kCyan+2); hWG->SetLineColor(kCyan+2); hWG->SetLineWidth(1);
        hTOP->SetFillColor(kCyan+2); hTOP->SetLineColor(kCyan+2); hTOP->SetLineWidth(1);
        hTT->SetFillColor(kCyan+2); hTT->SetLineColor(kCyan+2); hTT->SetLineWidth(1);

        hSMHIGGS->SetFillColor(kAzure+3); hSMHIGGS->SetLineColor(kAzure+3); hSMHIGGS->SetLineWidth(1);

        /*hTOP->SetFillColor(kGreen-2); hTOP->SetLineColor(kGreen+4); hTOP->SetLineWidth(1);
        hTT->SetFillColor(kGreen-2); hTT->SetLineColor(kGreen-2); hTT->SetLineWidth(1);

	hSMHIGGS->SetFillColor(kMagenta); hSMHIGGS->SetLineColor(kMagenta+1); hSMHIGGS->SetLineWidth(1);
*/

        hLFVGG126->SetLineColor(kBlue);  hLFVGG126->SetLineWidth(3);
        hLFVVBF126->SetLineColor(kBlue); hLFVVBF126->SetLineWidth(3); hLFVVBF126->SetLineStyle(kDashed);

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
	Pad1->SetLogy(setLogY);
        TH1F* hFAKESERROR=hFAKES->Clone(); hFAKESERROR->SetName("hFAKESERROR");

        for (int i=0; i<hFAKES->GetNbinsX()+1; i++){
                double content=hFAKES->GetBinContent(i);
                double contentErr=hFAKES->GetBinError(i);
                double err=sqrt(0.4*0.4*content*content+contentErr*contentErr);
                hFAKESERROR->SetBinError(i,err);
        }

        TH1F* fullMC3=hFAKESERROR->Clone();  fullMC3->Add(hZTauTau); fullMC3->Add(hTT); fullMC3->Add(hWG); fullMC3->Add(hWW);
        fullMC3->Add(hDY); fullMC3->Add(hTOP); fullMC3->Add(hSMHIGGS);
                fullMC3->SetFillColorAlpha(kGray+2,0.35); //fullMC3->SetFillStyle(3013); 
        fullMC3->SetMarkerSize(0); fullMC3->SetLineWidth(0); fullMC3->SetLineColor(kBlack);


        TH1F* fullMC2=hFAKES->Clone();  fullMC2->Add(hZTauTau); fullMC2->Add(hTT); fullMC2->Add(hWG); fullMC2->Add(hWW);
        fullMC2->Add(hDY); fullMC2->Add(hTOP); fullMC2->Add(hSMHIGGS); 
                fullMC2->SetFillColorAlpha(kBlack,0.45); //fullMC2->SetFillStyle(3002); 
        fullMC2->SetMarkerSize(0); fullMC2->SetLineWidth(0); fullMC2->SetLineColor(kBlack);
	fullMC2->SetMinimum(0.01);
	fullMC2->Draw("hist");
        fullMC2->GetXaxis()->SetTitle("");
        fullMC2->GetYaxis()->SetTitle(Yaxis);
        fullMC2->GetXaxis()->SetRangeUser(xmin,xmax);
        fullMC2->GetYaxis()->SetTitleOffset(1.2);
        fullMC2->GetYaxis()->SetTitleSize(0.05);
        fullMC2->GetXaxis()->SetLabelSize(0.0);
        fullMC2->GetXaxis()->SetNdivisions(505);
        fullMC2->GetYaxis()->SetLabelSize(0.04);

	THStack* stack = new THStack("stack","");
	stack->Add(hFAKES);
        stack->Add(hWG);
        stack->Add(hWW);
        stack->Add(hDY);

        stack->Add(hTT);
        stack->Add(hTOP);

        stack->Add(hZTauTau);
        stack->Add(hSMHIGGS);;
        //stack->Add(hLFVGG126);;
        //stack->Add(hLFVVBF126);;

	cout<<"Yields"<<endl;
	cout<<"VV " <<hWW->Integral()<<endl;
        cout<<"TOP " <<hTOP->Integral()<<endl;
        cout<<"TT " <<hTT->Integral()<<endl;
        cout<<"DY " <<hDY->Integral()<<endl;
        cout<<"ZTauTau " <<hZTauTau->Integral()<<endl;
        cout<<"FAKES " <<hFAKES->Integral()<<endl;
        cout<<"LFVGG126 " <<hLFVGG126->Integral()<<endl;
        cout<<"LFVVBF126 " <<hLFVVBF126->Integral()<<endl;

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
        stack->Draw("sameshist");
	stack->SetMaximum(maxMC);
	stack->GetYaxis()->SetRangeUser(minMC,maxMC);
        fullMC2->SetMaximum(maxMC);
        fullMC2->GetYaxis()->SetRangeUser(minMC,maxMC);
        if(setLogY){fullMC2->SetMinimum(0.01); fullMC2->GetYaxis()->SetRangeUser(0.1,maxMC*1000);stack->GetYaxis()->SetRangeUser(0.1,maxMC*1000);}
        stack->Draw("samehist");
        fullMC3->Draw("sames,E2");
        fullMC2->Draw("sames,E2");

        hLFVVBF126->Draw("sameshist");
        hLFVGG126->Draw("sameshist");
        TH1F* histoDataUnblindedV4=hdata_obs->Clone(); histoDataUnblindedV4->SetName("data_unblinded");
        for (int i = 0; i<=hdata_obs->GetNbinsX();i++){
                cout << hdata_obs->GetBinContent(i) << endl;
        }
	cout << blind << endl;
        if(!blind){
		hdata_obs->SetMinimum(0.01);
		hdata_obs->Draw("sames");
	}
        else {
                int findBinA=hdata_obs->FindBin(blindA);
                int findBinB=hdata_obs->FindBin(blindB);
                for (int i=findBinA; i<findBinB; i++) hdata_obs->SetBinContent(i,-1000);
                hdata_obs->Draw("sames");
        }


   TLegend *leg = new TLegend(legx1,legy1,legx2,legy2,NULL,"brNDC");
   leg->SetFillColor(0);
   leg->SetBorderSize(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry;
   entry=leg->AddEntry(hdata_obs,"Data, #mu#tau_{e}","p");
   entry=leg->AddEntry(fullMC2,"Bkgd. stat. uncertainty","f");
   entry=leg->AddEntry(fullMC3,"Bkgd. syst. uncertainty","f");
   entry=leg->AddEntry(hFAKES,"Misidentified leptons","f");
   entry=leg->AddEntry(hZTauTau,"True leptons", "f");
   //entry=leg->AddEntry(hSMHIGGS,"SM Higgs","f");
   //eblindBy=leg->AddEntry(hZTauTau,"Z#rightarrow#tau#tau","f");
   //     entry=leg->AddEntry(hDY,"Other","f");
   //     entry=leg->AddEntry(hTOP,"t#bar{t}, t, #bar{t}","f");
   entry=leg->AddEntry(hLFVGG126,"LFV GG Higgs (B=100%)","l");
   entry=leg->AddEntry(hLFVVBF126,"LFV VBF Higgs (B=100%)","l");
   leg->Draw();
   CMS_lumi( Pad1, iPeriod, iPos );
   //cmsPrelim(Lumi);

        //Pad1->SetLogy(set
        cout << "log?" << endl;
        hdata_obs->Draw("sames");
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
	if(!postfit)        Ratio->SetYTitle("#frac{Data-Bkgd}{Bkgd}");
	else 		    Ratio->SetYTitle("#frac{Data-Bkgd (fit)}{Bkgd (fit)}");	
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
                        double error2=0.4+error;//fullMC3->GetBinError(i)*hdata_obs->GetBinContent(i)/fullMC3->GetBinContent(i)/fullMC3->GetBinContent(i);
                        RatioError->SetBinContent(i,0);
                        RatioError->SetBinError(i,error);
                        RatioError2->SetBinContent(i,0);
                        RatioError2->SetBinError(i,error2);
        }
         RatioError2->Draw("E2");//RatioError2->SetFillStyle(3013); 
        RatioError2->SetFillColorAlpha(kGray+2,0.35); 
        RatioError2->SetMarkerSize(0); RatioError2->SetLineWidth(2);
        RatioError->Draw("E2,sames"); //RatioError->SetFillStyle(3002); 
        RatioError->SetFillColorAlpha(kBlack,0.45); RatioError->SetMarkerSize(0);
	Ratio->Draw("sames");
        hdata_obs->Draw("sames");
        cout << "log?" << endl;

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


