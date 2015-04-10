// Input: Limits from Combine, in per-one format

// NEW MET

double medianRLimit=0.746;;

double twoSigmaUpRLimit=1.5;
double oneSigmaUpRLimit=1.1;
double oneSigmaDownRLimit=0.5;
double twoSigmaDownRLimit=0.4;

double observedLimit=1.51;



/*
PAS
double medianRLimit=0.7500;;

double twoSigmaUpRLimit=1.4719;
double oneSigmaUpRLimit=1.0699;
double oneSigmaDownRLimit=0.5317;
double twoSigmaDownRLimit=0.3940;

double observedLimit=1.5744;
*/
/*
   -- Asymptotic -- 
   Expected  2.5%: r < 0.3508
   Expected 16.0%: r < 0.4747
   Expected 50.0%: r < 0.6777
   Expected 84.0%: r < 0.9776
   Expected 97.5%: r < 1.3711
 */
double ComputeSumYLimit(double BranchingRatio=0.1){
  //    cout<<"Computing Ratio for "<<BranchingRatio<<endl;
  if (BranchingRatio == 1) { cout<<"Branching Ratio cannot be 1"<<endl;  return 0;}

  // Higgs Mass
  double mh=125;

  // Higgs Width at 125 GeV is 4.1 MeV
  double gammah= 4.1/1000; //  gammah =  SM_Higgs_Width

  // Magic Formulas, #26 and #27 from
  // BR (h->mutau)  = Width(h->mutau) / ( Width (h->mutau) + SM_Higgs_Width)
  // Width (h->mutau) = mh/8Pi * (|Y(mutau)|**2 + |Y(taumu)|**2)
  // (|Y(mutau)|**2 + |Y(taumu)|**2) =  (BR * SM_Higgs_Width)  / ()*(1- BR)

  double LimitOnSumY = 8*TMath::Pi()/mh * BranchingRatio * gammah / (1 -BranchingRatio);
  //    cout<<sqrt(LimitOnSumY)<<endl;
  return LimitOnSumY;
}


void yukawa2(bool plotBand=true, bool plotDipole=false){

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




	TCanvas *c1 = new TCanvas("LimitsOnCouplings");
	c1->SetLogy(true);
	c1->SetLogx(true);
	c1->SetLeftMargin(0.16);
	c1->SetRightMargin(0.06);
	c1->SetTopMargin(0.05);
	c1->SetBottomMargin(0.16);
	c1->SetFrameFillStyle(0);
	c1->SetFrameLineWidth(2);
	c1->SetFrameBorderMode(0);
	c1->SetFrameFillStyle(0);
	c1->SetFrameLineWidth(2);
	c1->SetFrameBorderMode(0);


	TF2 *fullspace = new TF2("fullspace","x*x+y*y",0.0001,1.2,0.0001,1.2);
	fullspace->Draw();	
	fullspace->GetXaxis()->SetTitle("|Y_{#mu#tau}|   ");
	fullspace->GetYaxis()->SetTitle("|Y_{#tau#mu}|   ");
	//	fullspace->SetMaximum(0.1);
	fullspace->GetXaxis()->SetTitleOffset(1.2);
	fullspace->GetYaxis()->SetTitleOffset(1.2);
	fullspace->GetXaxis()->SetRangeUser(1e-4,1);
	fullspace->GetYaxis()->SetRangeUser(1e-4,1);


	double naturalnessLimit=0.1057 * 1.778 / 246 / 246 ;

	cout<<"Naturalness?"<<naturalnessLimit<<endl;
	
	TF1 * naturalness = new TF1("dipole","[0]/x",0.00001,2.);
	naturalness->SetParameter(0,naturalnessLimit);
	naturalness->SetLineWidth(2);
	naturalness->SetParName(0,"YLimit");
	naturalness->SetLineColor(kMagenta+2); //naturalness->SetLineStyle(kDashed);

	// from magnetic dipole

	TF1 * dipoleUpperBound = new TF1("dipole","[0]/x",0.00001,2.);
	dipoleUpperBound->SetParameter(0,0.065*0.065);
	dipoleUpperBound->SetLineWidth(2);
	dipoleUpperBound->SetParName(0,"YLimit");
	dipoleUpperBound->SetLineColor(kWhite);

	TF1 * dipole = new TF1("dipole","[0]/x",0.00001,2.);
	dipole->SetParameter(0,0.0027);
	dipole->SetLineWidth(2);
	dipole->SetParName(0,"YLimit");
	dipole->SetLineColor(kWhite);

	TF1 * dipole2 = new TF1("dipole2","[0]/x",0.00001,2.);
	dipole2->SetParameter(0,(0.0027+0.00075));
	dipole2->SetParName(0,"YLimit");
	dipole2->SetLineColor(kWhite);

	TF1 * dipoleup = new TF1("dipoleup","[0]/x",0.00001,2.);
	dipoleup->SetParameter(0,sqrt( (0.0027+0.00075)**2+1));
	dipoleup->SetParName(0,"YLimit");
	dipoleup->SetLineColor(kWhite);

	TF1 * dipoledown = new TF1("dipoledown","[0]/x",0.00001,2.);
	dipoledown->SetParameter(0,sqrt( (0.0027-0.00075)**2));;
	dipoledown->SetParName(0,"YLimit");
	dipoledown->SetLineColor(kWhite);

	if(plotDipole){
		dipoleUpperBound->Draw("sames");
		dipole->Draw("sames");
	}	


	// tau->3mu 
	const double YLimitTauTo3Mu = 0.25*0.25;
	cout<<" TauTo3Mu Limit:  "<<sqrt(YLimitTauTo3Mu)<<endl;
	TF1 * TauTo3MuLimitCombined = new TF1("TauTo3MuLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	TauTo3MuLimitCombined->SetParameter(0,YLimitTauTo3Mu);
	TauTo3MuLimitCombined->SetParName(0,"YLimit");
	TauTo3MuLimitCombined->Draw("sames");

	TauTo3MuLimitCombined->SetLineColor(kWhite); TauTo3MuLimitCombined->SetLineWidth(2);

	// tau --> mu gamma
	const double YLimitTauToMuGamma = 0.016*0.016;
	cout<<" TauToMuGamma Limit:  "<<sqrt(YLimitTauToMuGamma)<<endl;
	TF1 * TauToMuGammaLimitCombined = new TF1("TauToMuGammaLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	TauToMuGammaLimitCombined->SetParameter(0,YLimitTauToMuGamma);
	TauToMuGammaLimitCombined->SetParName(0,"YLimit");
	TauToMuGammaLimitCombined->Draw("sames");

	TauToMuGammaLimitCombined->SetLineColor(kWhite); TauToMuGammaLimitCombined->SetLineWidth(2);


	// LHC Limit by Rami & co from ATLAS
	double BRLimitIndirectATLAS= 13./100;
	const double YLimitIndirectATLAS = ComputeSumYLimit(BRLimitIndirectATLAS);
	cout<<" LHC Limit by Rami & co from ATLAS:  Br: "<<BRLimitIndirectATLAS<<"      -->    Y<"<<sqrt(YLimitIndirectATLAS)<<endl; 
	TF1 *H2TauIndirect = new TF1("H2TauIndirect","sqrt([0]-x*x)",0.00001,sqrt(YLimitIndirectATLAS)+0.001);
	H2TauIndirect->SetParameter(0,YLimitIndirectATLAS);
	H2TauIndirect->SetParName(0,"YLimit");
	H2TauIndirect->Draw("sames");

	H2TauIndirect->SetLineWidth(4); H2TauIndirect->SetLineColor(kYellow-7); 


	// Lines to guide the eye
	// Br = 0.99
	double BRLimit99PerCent= 0.99;
	const double YLimit99PerCent = ComputeSumYLimit(BRLimit99PerCent);
	//cout<<" 99PerCent Limit:  "<<BRLimit99PerCent<<"      -->    "<<YLimit99PerCent<<"  -->("<<sqrt(YLimit99PerCent)<<")"<<endl;
	TF1 * F99PerCentLimitCombined = new TF1("F99PerCentLimitCombined","sqrt([0]-x*x)",0.00001,1.);
	F99PerCentLimitCombined->SetParameter(0,YLimit99PerCent);
	F99PerCentLimitCombined->SetParName(0,"YLimit");
	F99PerCentLimitCombined->Draw("sames");

	F99PerCentLimitCombined->SetLineStyle(kDashed); F99PerCentLimitCombined->SetLineColor(kBlue+4); F99PerCentLimitCombined->SetLineWidth(2);

	// Br = 0.50 
	double BRLimit50PerCent= 0.5;
	const double YLimit50PerCent = ComputeSumYLimit(BRLimit50PerCent);
	//cout<<" 50PerCent Limit:  "<<BRLimit50PerCent<<"      -->    "<<YLimit50PerCent<<"  -->("<<sqrt(YLimit50PerCent)<<")"<<endl;
	TF1 * F50PerCentLimitCombined = new TF1("F50PerCentLimitCombined","sqrt([0]-x*x)",0.00001,0.1);
	F50PerCentLimitCombined->SetParameter(0,YLimit50PerCent);
	F50PerCentLimitCombined->SetParName(0,"YLimit");
	F50PerCentLimitCombined->Draw("sames");

	F50PerCentLimitCombined->SetLineStyle(kDashed); F50PerCentLimitCombined->SetLineColor(kBlue+4); F50PerCentLimitCombined->SetLineWidth(2);

	// Br = 0.10 (starting point)
	double BRLimit10PerCent= 0.1;
	const double YLimit10PerCent = ComputeSumYLimit(BRLimit10PerCent);
	//cout<<" 10PerCent Limit:  "<<BRLimit10PerCent<<"      -->    "<<YLimit10PerCent<<"  -->("<<sqrt(YLimit10PerCent)<<")"<<endl;
	TF1 * F10PerCentLimitCombined = new TF1("F10PerCentLimitCombined","sqrt([0]-x*x)",0.00001,0.2);
	F10PerCentLimitCombined->SetParameter(0,YLimit10PerCent);
	F10PerCentLimitCombined->SetParName(0,"YLimit");
	F10PerCentLimitCombined->Draw("sames");

	F10PerCentLimitCombined->SetLineStyle(kDashed); F10PerCentLimitCombined->SetLineColor(kBlue+4); F10PerCentLimitCombined->SetLineWidth(2);

	// Br = 0.01 (reasonable outlook for now)
	double BRLimit1PerCent= 0.01;
	const double YLimit1PerCent = ComputeSumYLimit(BRLimit1PerCent);
	//cout<<" 1PerCent Limit:  "<<BRLimit1PerCent<<"      -->    "<<YLimit1PerCent<<"  -->("<<sqrt(YLimit1PerCent)<<")"<<endl;
	TF1 * F1PerCentLimitCombined = new TF1("F1PerCentLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	F1PerCentLimitCombined->SetParameter(0,YLimit1PerCent);
	F1PerCentLimitCombined->SetParName(0,"YLimit");
	F1PerCentLimitCombined->Draw("sames");

	F1PerCentLimitCombined->SetLineStyle(kDashed); F1PerCentLimitCombined->SetLineColor(kBlue+4); F1PerCentLimitCombined->SetLineWidth(2);

	// Br = 0.001 (maybe the future)
	double BRLimit1PerMil= 0.1/100;
	const double YLimit1PerMil = ComputeSumYLimit(BRLimit1PerMil);        
	//cout<<" 1PerMil Limit:  "<<BRLimit1PerMil<<"      -->    "<<YLimit1PerMil<<"  -->("<<sqrt(YLimit1PerMil)<<")"<<endl;
	TF1 * F1PerMilLimitCombined = new TF1("F1PerMilLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	F1PerMilLimitCombined->SetParameter(0,YLimit1PerMil);
	F1PerMilLimitCombined->SetParName(0,"YLimit");
	F1PerMilLimitCombined->Draw("sames");

	F1PerMilLimitCombined->SetLineStyle(kDashed); F1PerMilLimitCombined->SetLineColor(kBlue+4); F1PerMilLimitCombined->SetLineWidth(2);


	// Actual expected limits from combine:

	double BRLimitExpected= medianRLimit/100;
	const double YLimitExpected = ComputeSumYLimit(BRLimitExpected); 
	cout<<" Our Expected Limit:  Br<"<<BRLimitExpected<<"      -->    Y<"<<sqrt(YLimitExpected)<<endl;
	TF1 * ExpectedLimitCombined = new TF1("ExpectedLimitCombined","sqrt([0]-x*x)",0.00001,sqrt(YLimitExpected)+0.1);
	ExpectedLimitCombined->SetParameter(0,YLimitExpected);
	ExpectedLimitCombined->SetParName(0,"YLimit");
	ExpectedLimitCombined->Draw("sames,f");

	ExpectedLimitCombined->SetLineWidth(4); ExpectedLimitCombined->SetLineColor(kPink); 
	if(plotBand) {ExpectedLimitCombined->SetLineColor(kPink);  ExpectedLimitCombined->SetLineWidth(2);}  // This is to allow a lightweight version without the yellow/green band

	double BRLimitExpectedPlusOneSigma= oneSigmaUpRLimit/100;
	const double YLimitExpectedPlusOneSigma = ComputeSumYLimit(BRLimitExpectedPlusOneSigma);
	cout<<" Our ExpectedPlusOneSigma Limit:  "<<BRLimitExpectedPlusOneSigma<<"  -->"<<sqrt(YLimitExpectedPlusOneSigma)<<endl;
	TF1 * ExpectedPlusOneSigmaLimitCombined = new TF1("ExpectedPlusOneSigmaLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	ExpectedPlusOneSigmaLimitCombined->SetParameter(0,YLimitExpectedPlusOneSigma);
	ExpectedPlusOneSigmaLimitCombined->SetParName(0,"YLimit");
	ExpectedPlusOneSigmaLimitCombined->SetLineWidth(4); ExpectedPlusOneSigmaLimitCombined->SetLineColor(kYellow);

	double BRLimitExpectedMinusOneSigma= oneSigmaDownRLimit/100;
	const double YLimitExpectedMinusOneSigma = ComputeSumYLimit(BRLimitExpectedMinusOneSigma);
	cout<<" Our ExpectedMinusOneSigma Limit:  "<<BRLimitExpectedMinusOneSigma<<"  -->"<<sqrt(YLimitExpectedMinusOneSigma)<<endl;
	TF1 * ExpectedMinusOneSigmaLimitCombined = new TF1("ExpectedMinusOneSigmaLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	ExpectedMinusOneSigmaLimitCombined->SetParameter(0,YLimitExpectedMinusOneSigma);
	ExpectedMinusOneSigmaLimitCombined->SetParName(0,"YLimit");
	ExpectedMinusOneSigmaLimitCombined->SetLineWidth(4); ExpectedMinusOneSigmaLimitCombined->SetLineColor(kGreen);

	double BRLimitExpectedPlusTwoSigma= twoSigmaUpRLimit/100;
	const double YLimitExpectedPlusTwoSigma = ComputeSumYLimit(BRLimitExpectedPlusTwoSigma);
	cout<<" Our ExpectedPlusTwoSigma Limit:  "<<BRLimitExpectedPlusTwoSigma<<"  -->"<<sqrt(YLimitExpectedPlusTwoSigma)<<endl;
	TF1 * ExpectedPlusTwoSigmaLimitCombined = new TF1("ExpectedPlusTwoSigmaLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	ExpectedPlusTwoSigmaLimitCombined->SetParameter(0,YLimitExpectedPlusTwoSigma);
	ExpectedPlusTwoSigmaLimitCombined->SetParName(0,"YLimit");
	ExpectedPlusTwoSigmaLimitCombined->SetLineWidth(4); ExpectedPlusTwoSigmaLimitCombined->SetLineColor(kYellow);

	double BRLimitExpectedMinusTwoSigma= twoSigmaDownRLimit/100;
	const double YLimitExpectedMinusTwoSigma = ComputeSumYLimit(BRLimitExpectedMinusTwoSigma);
	cout<<" Our ExpectedMinusTwoSigma Limit:  "<<BRLimitExpectedMinusTwoSigma<<"  -->"<<sqrt(YLimitExpectedMinusTwoSigma)<<endl;
	TF1 * ExpectedMinusTwoSigmaLimitCombined = new TF1("ExpectedMinusTwoSigmaLimitCombined","sqrt([0]-x*x)",0.00001,2.);
	ExpectedMinusTwoSigmaLimitCombined->SetParameter(0,YLimitExpectedMinusTwoSigma);
	ExpectedMinusTwoSigmaLimitCombined->SetParName(0,"YLimit");
	ExpectedMinusTwoSigmaLimitCombined->SetLineWidth(4); ExpectedMinusTwoSigmaLimitCombined->SetLineColor(kGreen);



	// Observed

	double BRLimitObserved= observedLimit/100;
	const double YLimitObserved = ComputeSumYLimit(BRLimitObserved);
	cout<<endl<<endl<<" Observed Limit:  Br<"<<BRLimitObserved<<"  --> Y<"<<sqrt(YLimitObserved)<<endl;
	TF1 * ObservedLimitCombined = new TF1("ObservedLimitCombined","sqrt([0]-x*x)",0.00001,sqrt(YLimitObserved)+0.0001);
	ObservedLimitCombined->SetParameter(0,YLimitObserved);
	ObservedLimitCombined->SetParName(0,"YLimit");
	ObservedLimitCombined->Draw("sames,f");

	ObservedLimitCombined->SetLineWidth(4); ObservedLimitCombined->SetLineColor(kBlack);




	// Lets plot!

	// cmsPrelim(19717);
        CMS_lumi(c1, iPeriod, iPos );

	const Int_t npf = 10000;

	//fill area between TauTo2Mu and TauToMuGamma limits
	Double_t xf[2*npf+1], yf[2*npf+1];
	Double_t xfmin = 1e-4; Double_t xfmax = 2;
	Double_t dxf = (xfmax-xfmin)/(npf-1);
	for (Int_t i=0;i<npf;i++) {
		xf[i] = xfmin + dxf*i;
		yf[i] = 2;
		xf[npf+i] = xfmax - dxf*i;
		yf[npf+i] = TauToMuGammaLimitCombined->Eval(xf[npf+i]);
	}
	xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
	TGraph *grf = new TGraph(2*npf+1,xf,yf);
	grf->SetFillColor(kCyan+4);
	grf->Draw("lf");


	//fill area between TauTo2Mu and TauToMuGamma limits
	Double_t xf[2*npf+1], yf[2*npf+1];
	Double_t xfmin = 1e-4; Double_t xfmax = 2;
	Double_t dxf = (xfmax-xfmin)/(npf-1);
	for (Int_t i=0;i<npf;i++) {
		xf[i] = xfmin + dxf*i;
		yf[i] = TauTo3MuLimitCombined->Eval(xf[i]);
		xf[npf+i] = xfmax - dxf*i;
		yf[npf+i] = TauToMuGammaLimitCombined->Eval(xf[npf+i]);
	}
	xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
	TGraph *grf = new TGraph(2*npf+1,xf,yf);
	grf->SetFillColor(kCyan+3);
	grf->Draw("lf");


	//fill area between TauToMuGamma and INDIRECT limits
	Double_t xf[2*npf+1], yf[2*npf+1];
	Double_t xfmin = 1e-4; Double_t xfmax = 2;
	Double_t dxf = (xfmax-xfmin)/(npf-1);
	for (Int_t i=0;i<npf;i++) {
		xf[i] = xfmin + dxf*i;
		yf[i] = TauToMuGammaLimitCombined->Eval(xf[i]);
		xf[npf+i] = xfmax - dxf*i;
		yf[npf+i] = H2TauIndirect->Eval(xf[npf+i]);
	}
	xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
	TGraph *grf = new TGraph(2*npf+1,xf,yf);
	grf->SetFillColor(kCyan+1);
	grf->Draw("lf");



	//fill area between DIRECT and INDIRECT limits
	Double_t xf[2*npf+1], yf[2*npf+1];
	Double_t xfmin = 1e-4; Double_t xfmax = 2;
	Double_t dxf = (xfmax-xfmin)/(npf-1);
	for (Int_t i=0;i<npf;i++) {
		xf[i] = xfmin + dxf*i;
		yf[i] = H2TauIndirect->Eval(xf[i]);
		xf[npf+i] = xfmax - dxf*i;
		yf[npf+i] = ExpectedLimitCombined->Eval(xf[npf+i]);
	}
	xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
	TGraph *grf = new TGraph(2*npf+1,xf,yf);
	grf->SetFillColor(kCyan-9);
	grf->Draw("lf");


	// fill currently allowed area 
	Double_t x[npf+3], y[npf+3];
	Double_t xmin = 1e-4; Double_t xmax = 2;
	Double_t dx = (xmax-xmin)/(npf-1);

	for (Int_t i=0;i<npf;i++) {
		x[i] = xmin + dx*i;
		y[i] = ExpectedLimitCombined->Eval(x[i]);
	}
	x[npf]   = x[npf-1]; y[npf]   = c1->GetUymin();
	x[npf+1] = x[0];    y[npf+1] = y[npf];
	x[npf+2] = x[0];    y[npf+2] = y[0];
	TGraph *gr = new TGraph(npf+3,x,y);
	gr->SetFillColor(kWhite);
	gr->Draw("lf");



	if (plotDipole){

		// results from (g-2) and EDM 
		Double_t xf[2*npf+1], yf[2*npf+1];
		Double_t xfmin = 1e-4; Double_t xfmax = 2;
		Double_t dxf = (xfmax-xfmin)/(npf-1);
		for (Int_t i=0;i<npf;i++) {
			xf[i] = xfmin + dxf*i;
			yf[i] = dipoledown->Eval(xf[i]);
			xf[npf+i] = xfmax - dxf*i;
			yf[npf+i] = dipoleup->Eval(xf[npf+i]);
		}
		xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
		TGraph *grf = new TGraph(2*npf+1,xf,yf);
		grf->SetFillStyle(3002);
		grf->SetFillColor(kGreen);
		grf->Draw("lf");


		// only from (g-2), assuming Im(YmtYtm)==0
		Double_t xf[2*npf+1], yf[2*npf+1];
		Double_t xfmin = 1e-4; Double_t xfmax = 2;
		Double_t dxf = (xfmax-xfmin)/(npf-1);
		for (Int_t i=0;i<npf;i++) {
			xf[i] = xfmin + dxf*i;
			yf[i] = dipoledown->Eval(xf[i]);
			xf[npf+i] = xfmax - dxf*i;
			yf[npf+i] = dipole2->Eval(xf[npf+i]);
		}
		xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
		TGraph *grf = new TGraph(2*npf+1,xf,yf);
		grf->SetFillStyle(3001);
		grf->SetFillColor(kGreen);
		grf->Draw("lf");

	}

	if(plotBand){

		//fill 2 SIGMA Area 
		Double_t xf[2*npf+1], yf[2*npf+1];
		Double_t xfmin = 1e-4; Double_t xfmax = 2;
		Double_t dxf = (xfmax-xfmin)/(npf-1);
		for (Int_t i=0;i<npf;i++) {
			xf[i] = xfmin + dxf*i;
			yf[i] = ExpectedPlusTwoSigmaLimitCombined->Eval(xf[i]);
			xf[npf+i] = xfmax - dxf*i;
			yf[npf+i] = ExpectedMinusTwoSigmaLimitCombined->Eval(xf[npf+i]);
		}
		xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
		TGraph *grf = new TGraph(2*npf+1,xf,yf);
		grf->SetFillColor(kGreen);
		grf->Draw("lf");

		//fill 1 SIGMA Area
		Double_t xf[2*npf+1], yf[2*npf+1];
		Double_t xfmin = 1e-4; Double_t xfmax = 1;
		Double_t dxf = (xfmax-xfmin)/(npf-1);
		for (Int_t i=0;i<npf;i++) {
			xf[i] = xfmin + dxf*i;
			yf[i] = ExpectedPlusOneSigmaLimitCombined->Eval(xf[i]);
			xf[npf+i] = xfmax - dxf*i;
			yf[npf+i] = ExpectedMinusOneSigmaLimitCombined->Eval(xf[npf+i]);
		}
		xf[2*npf] = xf[0]; yf[2*npf] = yf[0];
		TGraph *grf = new TGraph(2*npf+1,xf,yf);
		grf->SetFillColor(kYellow);
		grf->Draw("lf");
	}


	// Draw Curves

	TauTo3MuLimitCombined->Draw("sames");
	TauToMuGammaLimitCombined->Draw("sames");
	H2TauIndirect->Draw("sames");
	F50PerCentLimitCombined->Draw("sames");
	//F99PerCentLimitCombined->Draw("sames");
	F10PerCentLimitCombined->Draw("sames");
	F1PerCentLimitCombined->Draw("sames");
	F1PerMilLimitCombined->Draw("sames");
	ExpectedLimitCombined->Draw("sames");

	naturalness->Draw("sames");

	if(plotDipole){
		//   dipoleUpperBound->Draw("sames");	
		dipole2->Draw("sames");  
		dipoleup->Draw("sames");  
		dipoledown->Draw("sames");  
	}


	ObservedLimitCombined->Draw("sames");


	// Draw Text

	TLatex *tt = new TLatex(sqrt(YLimit1PerMil)+0.0001,0.00040,"BR<0.1%");
	tt->SetTextAlign(11); tt->SetTextSize(0.027);
	tt->SetTextColor(kBlue+4);
	tt->SetTextAngle(-90);
	tt->Draw();

	tt = new TLatex(sqrt(YLimit1PerCent)+0.0001,0.00040,"BR<1%");
	//   tt = new TLatex(sqrt(YLimit1PerCent)+0.0001,0.001,"BR(H#rightarrow#mu#tau)<1%");
	tt->SetTextAlign(11); tt->SetTextSize(0.027);
	tt->SetTextColor(kBlue+4);
	tt->SetTextAngle(-90);
	tt->Draw();

	tt = new TLatex(sqrt(YLimit10PerCent)-0.002,0.00040,"BR<10%");
	tt->SetTextAlign(11); tt->SetTextSize(0.027);
	tt->SetTextColor(kBlue+4);
	tt->SetTextAngle(-90);
	tt->Draw();

	tt = new TLatex(sqrt(YLimit50PerCent)-0.006,0.00040,"BR<50%");
	tt->SetTextAlign(11); tt->SetTextSize(0.027);
	tt->SetTextColor(kBlue+4);
	tt->SetTextAngle(-90);
	tt->Draw();

	tt = new TLatex(sqrt(YLimit99PerCent)-0.1,0.001,"BR(H#rightarrow#mu#tau)<99%");
	tt->SetTextAlign(11); tt->SetTextSize(0.027);
	tt->SetTextColor(kBlue+4);
	tt->SetTextAngle(-90);
	//  tt->Draw();

	tt = new TLatex(0.0008,sqrt(YLimitIndirectATLAS)+0.0008,"ATLAS H#rightarrow#tau#tau");
	tt->SetTextAlign(11); tt->SetTextSize(0.03);
	tt->SetTextColor(kYellow-7);
	tt->Draw();

	tt = new TLatex(0.00012,sqrt(YLimitObserved)+0.0006,"observed");
	tt->SetTextAlign(11); tt->SetTextSize(0.03);
	tt->SetTextColor(kBlack);
	tt->Draw();

	tt = new TLatex(0.00012,sqrt(YLimitExpected)-0.0007,"expected");
	tt->SetTextAlign(11); tt->SetTextSize(0.03);
	tt->SetTextColor(kPink);
	if(plotBand) tt->SetTextColor(kPink);
	tt->Draw();
	tt = new TLatex(0.00012,sqrt(YLimitExpected)-0.0012,"H#rightarrow#mu#tau");
	tt->SetTextAlign(11); tt->SetTextSize(0.03);
	tt->SetTextColor(kPink);
	if(plotBand) tt->SetTextColor(kPink);
	tt->Draw();

	tt = new TLatex(0.00012,sqrt(YLimitTauTo3Mu)+0.01,"#tau#rightarrow 3#mu");
	tt->SetTextAlign(11); tt->SetTextSize(0.04);
	tt->SetTextColor(kWhite);
	tt->Draw();

	tt = new TLatex(0.00012,sqrt(YLimitTauToMuGamma)+0.0015,"#tau#rightarrow #mu #gamma");
	tt->SetTextAlign(11); tt->SetTextSize(0.04);
	tt->SetTextColor(kWhite);
	tt->Draw();


	tt = new TLatex(0.0012,0.0075,"|Y_{#mu#tau}Y_{#tau#mu}|=m_{#mu}m_{#tau}/v^{2}");
	tt->SetTextAlign(11); tt->SetTextSize(0.03);
	tt->SetTextColor(kMagenta+2);
	tt->SetTextAngle(-45);
	tt->Draw();


	if(plotDipole){

		tt = new TLatex(0.0025,1.7,"(g-2)_{#mu} (Im(Y_{#mu#tau}Y_{#tau#mu})=0)");
		tt->SetTextAlign(11); tt->SetTextSize(0.03);
		tt->SetTextColor(kWhite);
		tt->SetTextAngle(-45);
		tt->Draw();

		tt = new TLatex(0.28,0.12,"(g-2)_{#mu} and EDM");
		tt->SetTextAlign(11); tt->SetTextSize(0.03);
		tt->SetTextColor(kWhite);
		tt->SetTextAngle(45);
		tt->Draw();

		TArrow *arrow = new TArrow(0.003,0.7,0.004,0.9,0.01,"<>");
		arrow->SetLineColor(kWhite);
		arrow->SetFillStyle(1001);
		arrow->SetLineWidth(2);
		arrow->Draw();

		TArrow *arrow = new TArrow(0.045,0.045,0.9,0.9,0.01,"<>");
		arrow->SetLineColor(kWhite);
		arrow->SetFillStyle(1001);
		arrow->SetLineWidth(3);
		arrow->Draw();
	}


	TLegend *leg = new TLegend(0.5536913,0.7255245,0.9328859,0.9353147,NULL,"brNDC");
	leg->SetTextFont(62);
	leg->SetLineColor(1);
	leg->SetLineStyle(1);
	leg->SetLineWidth(1);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	TLegendEntry *entry;
	entry=leg->AddEntry("TauTo3MuLimitCombined","#tau#rightarrow3#mu","l");
	entry=leg->AddEntry("TauToMuGammaLimitCombined","#tau#rightarrow#mu#gamma","l");
	entry=leg->AddEntry("H2TauIndirect","H#rightarrow#tau#mu INDIRECT, LHC","l");
	entry=leg->AddEntry("ExpectedLimitCombined","H#rightarrow#mu#tau,CMS EXPECTED","l");
	entry=leg->AddEntry("ObservedLimitCombined","H#rightarrow#mu#tau, CMS OBSERVED","l");
	//   leg->Draw();	

	gPad->RedrawAxis();

}



void cmsPrelim( double intLumi ){  TLatex latex;
	latex.SetNDC();
	latex.SetTextSize(0.04);

	latex.SetTextAlign(31); // align right
	latex.DrawLatex(0.95,0.96,Form("%.1f fb^{-1}, #sqrt{s} = 8 TeV",intLumi/1000));

	latex.SetTextAlign(11); // align left
	latex.DrawLatex(0.17,0.96,"CMS preliminary");
}



