void plote(){

	gROOT->LoadMacro("tdrstyle.C");
	setTDRStyle();
	gStyle->SetPalette(51);


        gROOT->LoadMacro("CMS_lumi.C");
        writeExtraText = false;
        int iPeriod = 2;
        // second parameter in example_plot is iPos, which drives the position of the CMS logo in the plot
        int iPos=0;
        // iPos=11: top-left, left-aligned
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




	TCanvas *PLOTMU = new TCanvas("PLOTMU", "BEST FIT",600,22,664,763);
	gStyle->SetOptFit(1);
	gStyle->SetOptStat(0);
	gStyle->SetOptTitle(0);
	PLOTMU->Range(-1.298202,-1.436207,2.706292,7.434483);
	PLOTMU->SetFillColor(0);
	PLOTMU->SetBorderMode(0);
	PLOTMU->SetBorderSize(2);
	PLOTMU->SetTickx(1);
	PLOTMU->SetTicky(1);
	PLOTMU->SetLeftMargin(0.2742424);
	PLOTMU->SetRightMargin(0.05151515);
	PLOTMU->SetTopMargin(0.04897959);
	PLOTMU->SetBottomMargin(0.1619048);
	PLOTMU->SetFrameFillStyle(0);
	PLOTMU->SetFrameLineWidth(2);
	PLOTMU->SetFrameBorderMode(0);
	PLOTMU->SetFrameFillStyle(0);
	PLOTMU->SetFrameLineWidth(2);
	PLOTMU->SetFrameBorderMode(0);

	const Int_t nx = 1;
	const Int_t ny = 7;
	char *month[nx]  = {"Best Fit"};
//mu/tau then mu/e
/*
	char *channels[ny]={"H#rightarrow#mu#tau", "#mu#tau_{e}, 2 Jets","#mu#tau_{e}, 1 Jet", "#mu#tau_{e}, 0 Jets","#mu#tau_{h}, 2 Jets","#mu#tau_{h}, 1 Jet", "#mu#tau_{h}, 0 Jets"};

        double      MU[7]={0.841981,0.0524171,0.813178,0.868633,1.48276,0.213705,0.405503};
        double ERRDOWN[7]={0.368479,0.97021,0.78162,0.624873,0.927777,1.09168,1.22005};
	double   ERRUP[7]={0.392093,1.58307,0.854759,0.658724,1.16189,1.03082,1.20483};
        double     MU2[7]={0.841981,-7,-7,-7,-7,-7,-7};
*/
//mu/e then mu/tau
        char *channels[ny]={"H#rightarrow#e#tau", "e#tau_{h}, 2 Jets","e#tau_{h}, 1 Jet", "e#tau_{h}, 0 Jets","e#tau_{#mu}, 2 Jets","e#tau_{#mu}, 1 Jet", "#e#tau_{#mu}, 0 Jets"};

        double      MU[7]={0.841981,1.48276,0.213705,0.405503,0.0524171,0.813178,0.868633};
        double ERRDOWN[7]={0.368479,0.927777,1.09168,1.22005,0.97021,0.78162,0.624873};
        double   ERRUP[7]={0.392093,1.16189,1.03082,1.20483,1.58307,0.854759,0.658724};
        double     MU2[7]={0.841981,-7,-7,-7,-7,-7,-7};
	TString channels2[7];

		for(int i=0; i<7; i++) channels2[i]=Form("#splitline{%s}{#scale[0.8]{%1.2f  #scale[0.7]{#splitline{+%1.2f}{-%1.2f}} %%}}",channels[i],MU[i],ERRUP[i],ERRDOWN[i]);
	
	double y[7]={0.5,1.5,2.5,3.5,4.5,5.5,6.5};
	double erry[7]={0,0,0,0,0,0,0};

	TH2F *h = new TH2F("h","test",1,-1.5,2.5,7,0,7);
	for (int j=0; j<ny; j++)      h->Fill(1,channels2[j],0);
	h->SetXTitle("Best fit to B(H#rightarrow#e#tau), %");
        h->GetXaxis()->SetTitleSize(0.05);
	h->GetXaxis()->SetTitleOffset(1.1);
	//   h->LabelsDeflate("X");
	// h->LabelsDeflate("Y");
	// h->LabelsOption("v");
	h->Draw();

	for(int i=0; i<7; i++) printf(" %s --> %4.2f (-%4.2f, +%4.2f)  \n",channels[i],MU[i],ERRDOWN[i],ERRUP[i]);

	TGraphAsymmErrors *GRAPHMU=new TGraphAsymmErrors(7,MU,y,ERRDOWN,ERRUP,erry,erry);
        TGraphAsymmErrors *GRAPHMU2=new TGraphAsymmErrors(7,MU2,y,ERRDOWN,ERRUP,erry,erry);

	GRAPHMU2->SetMarkerColor(kRed); GRAPHMU2->SetLineColor(kRed);

	GRAPHMU->Draw("P,sames");
        GRAPHMU2->Draw("P,sames");

	TLine  *line1 = new TLine(1,0,1,7);
	line1->SetLineStyle(kDashed);
        line1->SetLineColor(kGray);
	line1->Draw();	

	TLine  *line0 = new TLine(0,0,0,7);
	line0->SetLineStyle(kDashed);
	line0->SetLineColor(kGray);
	line0->Draw();


        TLine  *lineH = new TLine(-1.5,1,2.5,1);
	lineH->SetLineWidth(2);
        lineH->Draw();


        CMS_lumi( PLOTMU, iPeriod, iPos );
	PLOTMU->SaveAs("LFVBRETau.pdf");

}


void cmsPrelim( double intLumi ){  TLatex latex;
	latex.SetNDC();
	latex.SetTextSize(0.04);

	latex.SetTextAlign(31); // align right
	latex.DrawLatex(0.95,0.96,Form("%.1f fb^{-1}, #sqrt{s} = 8 TeV",intLumi/1000));

	latex.SetTextAlign(11); // align left
	latex.DrawLatex(0.25,0.96,"CMS preliminary");
}

