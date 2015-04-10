nclude <TFile.h>
#include <TH1.h>


void getYields(TString name,TString dir, double xmin, double xmax, bool VBF);
double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error);

void printYieldsMuTauDataPresel(){
        printf("GG category \n");
        getYields("presel_Feb16_jetPt/data_2012.root","gg0",50,300,false);
        printf("\n\n");

        printf("Boosted category \n");
        getYields("presel_Feb16_jetPt/data_2012.root","gg1",50,300,false);
        printf("\n\n");

        printf("VBF category \n");
        getYields("presel_Feb16_jetPt/data_2012.root","vbf",50,300,true);

}

void getYields(TString name,TString dir, double xmin, double xmax, bool VBF){

	TFile *fileMuTauGG = new TFile(name,"READONLY");

	TString samplesName[1]={
				 "                          data"};

	TString samples[1]={"collMass_type1"};
	double errorFactor[1]={0};

	double error[1]; 
        double errorStat[1];
        double errorSyst[1];

	double yield[1];

	for (int i=0; i<1; i++){
			yield[i]=yieldHisto(fileMuTauGG,dir+"/"+samples[i],xmin,xmax,errorStat[i]);
			if(yield[i]<0) yield[i]=0;
			errorSyst[i]=yield[i]*errorFactor[i];
                        error[i]=sqrt(errorStat[i]*errorStat[i]+errorSyst[i]*errorSyst[i]);
                        printf("2.0%d  %s \t ->     $%8.2f \\pm %5.2f$ \n",i+1,samplesName[i].Data(),yield[i], error[i]);
	
	}

}

double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error){
	TH1F* histo=(TH1F*)file->Get(name); 
	int binmin=histo->FindBin(xmin);
        int binmax=histo->FindBin(xmax);

	double yield=histo->IntegralAndError(binmin,binmax,error);

	return yield;
}
