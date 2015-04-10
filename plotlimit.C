void plotlimit(){

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
/*	char *channels[ny]={"H#rightarrow#mu#tau", "#mu#tau_{e}, 2 Jets","#mu#tau_{e}, 1 Jet", "#mu#tau_{e}, 0 Jets","#mu#tau_{h}, 2 Jets","#mu#tau_{h}, 1 Jet", "#mu#tau_{h}, 0 Jets"};

	double SIGMA[7]=  {  0.4, 1.92127, 0.849027, 0.671648, 1.17987, 1.0563, 1.19183};
	double ERR2DOWN[7]={ 0.4, 1.6475, 0.8613, 0.6968, 1.0795, 1.1039, 1.2364};
	double ERRDOWN[7]= {0.5, 2.3839, 1.1623, 0.9340, 1.5274, 1.4741, 1.6616};
	double MEDIAN[7]= { 0.746, 3.7652, 1.6641, 1.3164, 2.3125, 2.0703, 2.3359};
	double ERRUP[7]={   1.1, 6.1972, 2.4269, 1.8884, 3.5938, 2.9698, 3.3695};
	double ERR2UP[7]=  {  1.5, 9.8500, 3.4658, 2.6400, 5.3935, 4.1260, 4.6967};
	double OBSERVED[7]=  { 1.51, 3.8383, 2.3809, 2.0370, 3.6818, 2.2204, 2.6055};

	//        double OBSERVED[7]=  { -10,-10,-10,-10,-10,-10,-10};

	double R2DOWN[7]={ 0.3940, 1.6475, 0.8613, 0.6968, 0.9233, 1.1288, 1.2447};
	double RDOWN[7]= {0.5317, 2.3839, 1.1623, 0.9340, 1.3025, 1.5050, 1.6727};
	double RUP[7]={   1.0699, 6.1972, 2.4269, 1.8884, 3.0386, 2.9979, 3.3920};
	double R2UP[7]=  {  1.4719, 9.8500, 3.4658, 2.6400, 4.5894, 4.1774, 4.7281};
*/
//mu/e then mu/tau
        char *channels[ny]={"H#rightarrow#mu#tau", "#mu#tau_{h}, 2 Jets","#mu#tau_{h}, 1 Jet", "#mu#tau_{h}, 0 Jets","#mu#tau_{e}, 2 Jets","#mu#tau_{e}, 1 Jet", "#mu#tau_{e}, 0 Jets"};

        double SIGMA[7]=  {  0.4, 1.17987, 1.0563, 1.19183, 1.92127, 0.849027, 0.671648};
        double ERR2DOWN[7]={ 0.4, 1.0795, 1.1039, 1.2364, 1.6475, 0.8613, 0.6968};
        double ERRDOWN[7]= {0.5, 1.5274, 1.4741, 1.6616, 2.3839, 1.1623, 0.9340};
        double MEDIAN[7]= { 0.746, 2.3125, 2.0703, 2.3359, 3.7652, 1.6641, 1.3164};
        double ERRUP[7]={   1.1, 3.5938, 2.9698, 3.3695, 6.1972, 2.4269, 1.8884};
        double ERR2UP[7]=  {  1.5, 5.3935, 4.1260, 4.6967, 9.8500, 3.4658, 2.6400};
        double OBSERVED[7]=  { 1.51, 3.6818, 2.2204, 2.6055, 3.8383, 2.3809, 2.0370};

        //        double OBSERVED[7]=  { -10,-10,-10,-10,-10,-10,-10};

        double R2DOWN[7]={ 0.3940, 0.9233, 1.1288, 1.2447, 1.6475, 0.8613, 0.6968};
        double RDOWN[7]= {0.5317, 1.3025, 1.5050, 1.6727, 2.3839, 1.1623, 0.9340};
        double RUP[7]={   1.0699, 3.0386, 2.9979, 3.3920, 6.1972, 2.4269, 1.8884};
        double R2UP[7]=  {  1.4719, 4.5894, 4.1774, 4.7281, 9.8500, 3.4658, 2.6400};



	for (int i=0; i<7; i++){
		ERR2DOWN[i]=-ERR2DOWN[i]+MEDIAN[i];
		ERRDOWN[i]=-ERRDOWN[i]+MEDIAN[i];
		ERRUP[i]=ERRUP[i]-MEDIAN[i];
		ERR2UP[i]=ERR2UP[i]-MEDIAN[i];
	}


	TString channels2[7];
	for(int i=0; i<7; i++) {
		//		channels2[i]=Form("#splitline{%s}{ #scale[0.8]{Median=%1.2f, #sigma=%1.2f}}",channels[i],MEDIAN[i],SIGMA[i]);
		channels2[i]=Form("#splitline{%s}{ #scale[0.8]{ #splitline{%1.2f%% (exp.)}{%1.2f%% (obs.)}}}",channels[i],MEDIAN[i],OBSERVED[i]);
		cout<<channels[i]<<"  --> \t"<<R2DOWN[i]<<"\t"<<RDOWN[i]<<"\t"<<MEDIAN[i]<<"\t"<<RUP[i]<<"\t"<<R2UP[i]<<"       ("<<SIGMA[i]<<")   --->"<<OBSERVED[i]<<endl;
		//		cout<<MEDIAN[i]<<"   "<<SIGMA[i]<<"     -->"<<(R2UP[i]-MEDIAN[i])/2<<"   "<<RUP[i]-MEDIAN[i]<<"   "<<(-R2DOWN[i]+MEDIAN[i])/2<<"   "<<-RDOWN[i]+MEDIAN[i]<<"   "<<(R2UP[i]-R2DOWN[i])/4<<"   "<<(RUP[i]-RDOWN[i])/2<<endl;
	}

	double y[7]={0.5,1.5,2.5,3.5,4.5,5.5,6.5};
	double erry[7]={0,0,0,0,0,0,0};

	TH2F *h = new TH2F("h","test",1,-1.5,10,7,0,7);
	for (int j=0; j<ny; j++)      h->Fill(1,channels2[j],0);
	h->SetXTitle("95% CL limit on B(H#rightarrow#mu#tau), %");
	h->GetXaxis()->SetLabelSize(0.04);
        h->GetXaxis()->SetTitleSize(0.05);
	//   h->LabelsDeflate("X");
	// h->LabelsDeflate("Y");
	// h->LabelsOption("v");
	h->Draw();

	for (int i=0; i<7; i++){
		TPave *pave = new TPave(R2DOWN[i],i+0.75,R2UP[i],i+0.25,4,"br");
		pave->Draw();
		pave->SetBorderSize(0);
		pave->SetFillColor(kYellow);
		TPave *pave2 = new TPave(RDOWN[i],i+0.75,RUP[i],i+0.25,4,"br");
		pave2->Draw();
		pave2->SetBorderSize(0);
		pave2->SetFillColor(kGreen);
	}


	TGraphAsymmErrors *GRAPHMEDIAN=new TGraphAsymmErrors(7,MEDIAN,y,0,0,erry,erry);
	TGraphAsymmErrors *GRAPHOBSERVED=new TGraphAsymmErrors(7,OBSERVED,y,0,0,erry,erry);

	GRAPHMEDIAN->SetLineColor(kBlue); GRAPHMEDIAN->SetMarkerStyle(5); GRAPHMEDIAN->SetMarkerColor(kBlue+2); GRAPHMEDIAN->SetMarkerSize(1.5); GRAPHMEDIAN->SetLineWidth(1);

	GRAPHMEDIAN->Draw("P,sames");
	GRAPHOBSERVED->Draw("P,sames");

	TLine  *line0 = new TLine(0,0,0,7);
	line0->SetLineStyle(kDashed);
	line0->SetLineColor(kGray);
	line0->Draw();


	TLine  *lineH = new TLine(-1.5,1,10,1);
	lineH->SetLineWidth(2);
	lineH->Draw();

	TLegend *leg = new TLegend(0.6424242,0.7148997,0.9045455,0.9255014,NULL,"brNDC");
	leg->SetFillColor(0);
	leg->SetBorderSize(0);
	TLegendEntry *entry;
	entry=leg->AddEntry(GRAPHOBSERVED,"Observed","p");
	entry=leg->AddEntry(GRAPHMEDIAN,"Expected","p");
	entry=leg->AddEntry("NULL","Expected #pm 1#sigma","f");
	entry->SetFillColor(kGreen);
	entry->SetFillStyle(1001);
	entry->SetLineStyle(1);
	entry=leg->AddEntry("NULL","Expected #pm 2#sigma","f");
	entry->SetFillColor(kYellow);
	entry->SetFillStyle(1001);
	entry->SetLineStyle(1);

	leg->Draw();

        CMS_lumi( PLOTMU, iPeriod, iPos );
	PLOTMU->SaveAs("NewMETLimits.png");
	PLOTMU->SaveAs("NewMETLimits.pdf");
	//cmsPrelim(19700);

}


void cmsPrelim( double intLumi ){  TLatex latex;
	latex.SetNDC();
	latex.SetTextSize(0.04);

	latex.SetTextAlign(31); // align right
	latex.DrawLatex(0.95,0.96,Form("%.1f fb^{-1}, #sqrt{s} = 8 TeV",intLumi/1000));

	latex.SetTextAlign(11); // align left
	latex.DrawLatex(0.25,0.96,"CMS preliminary");
}

