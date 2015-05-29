nclude <TFile.h>
#include <TH1.h>


void getYields(TString name,TString dir, double xmin, double xmax, bool VBF);
double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error);

void printYieldsMuTauPresel(){

        printf("GG category \n");
        //getYields("MuTauPresel_June9/GG_collMass_PRESEL.root","ggmutau",50,300,false);
	getYields("preselection_Nov9_SSFakes/LFV_gg0_collMass_fakeRate_zjetsEmbed_newSignal.root","vbfmutau",0,100,true);
        printf("\n\n");

        printf("Boosted category \n");
        //getYields("MuTauPresel_June9/Boosted_collMass_PRESEL.root","ggmutau",50,300,false);
        getYields("preselection_Nov9_SSFakes/LFV_gg1_collMass_fakeRate_zjetsEmbed_newSignal.root","vbfmutau",0,100,true);
        printf("\n\n");

        printf("VBF category \n");
        //getYields("MuTauPresel_June9/LFV_vbf_collMass_type1_fakeRate_zjetsEmbed_newSignal_PRESEL.root","vbfmutau",50,300,true);
        getYields("preselection_Nov9_SSFakes/LFV_vbf_collMass_fakeRate_zjetsEmbed_newSignal.root","vbfmutau",0,100,true);

}

void getYields(TString name,TString dir, double xmin, double xmax, bool VBF){

	TFile *fileMuTauGG = new TFile(name,"READONLY");

/*
        TH1F* hFAKES=(TH1F*)fileMuTauGG->Get(dir+"/FAKES"); hFAKES->SetName("hFAKES");
	TH1F* hVV=(TH1F*)fileMuTauGG->Get(dir+"/VV"); hVV->SetName("hVV");
        TH1F* hTOP=(TH1F*)fileMuTauGG->Get(dir+"/TOP"); hTOP->SetName("hTOP");
        TH1F* hTT=(TH1F*)fileMuTauGG->Get(dir+"/TT"); hTT->SetName("hTT");
        TH1F* hZTauTau=(TH1F*)fileMuTauGG->Get(dir+"/ZTauTau"); hZTauTau->SetName("hZTauTau");
        TH1F* hDY=(TH1F*)fileMuTauGG->Get(dir+"/DY"); hDY->SetName("hDY");
        TH1F* hLFVVBF126=(TH1F*)fileMuTauGG->Get(dir+"/LFVVBF126"); hLFVVBF126->SetName("hLFVVBF126");
        TH1F* hLFVGG126=(TH1F*)fileMuTauGG->Get(dir+"/LFVVBF126"); hLFVVBF126->SetName("hLFVVBF126");
        TH1F* hSMVBF126=(TH1F*)fileMuTauGG->Get(dir+"/SMVBF126"); hSMVBF126->SetName("hSMVBF126");
        TH1F* hSMGG126=(TH1F*)fileMuTauGG->Get(dir+"/SMVBF126"); hSMVBF126->SetName("hSMVBF126");
        TH1F* hdata_obs=(TH1F*)fileMuTauGG->Get(dir+"/data_obs"); hdata_obs->SetName("hdata_obs");
*/

	TString samplesName[16]={"Fake #tau (jet#rightarrow#tau)",
                                 "          Z#rightarrow#tau#tau",
				 "                            VV",
                                 "                     Drell-Yan",
                                 "                      t#bar{t}",
				 "                    t, #bar{t}",
				 "   SM H#rightarrow#tau#tau, GG",
				 "  SM H#rightarrow#tau#tau, VBF",
                                 "        SM H#rightarrow WW, GG",
                                 "        SM H#rightarrow WW, VBF",
				 " 	 SM H#rightarrow#tau#tau",			
				 "                           BG ",
				 "   LFV H#rightarrow#mu#tau, GG",
				 "  LFV H#rightarrow#mu#tau, VBF",
                                 "      LFV  H#rightarrow#mu#tau",
				 "                          data"};

	double theoErrorGG=sqrt(0.08*0.08+0.10*0.10+0.04*0.04);
		if(VBF) theoErrorGG=sqrt(0.08*0.08+0.30*0.30+0.04*0.04);
	double theoErrorVBF=sqrt(0.08*0.08+0.04*0.04+0.04*0.04);
	if (VBF){
        	TString samples[16]={"fakes","ztautau","ww","zjetsother","ttbar","singlet","SMGG126","SMVBF126","","","","","LFVGG","LFVVBF","","data_obs"};
	}
	else{	
		TString samples[16]={"FAKES","ZTauTau","VV","DY","TT","TOP","SMGG126","SMVBF126","WWGG126","WWVBF126","","","LFVGG126","LFVVBF126","","data_unblind"};
	}
	double errorFactor[16]={0.3,0.03,0.15,0.1,0.1,0.1,theoErrorGG,theoErrorVBF,0,0,0,0,theoErrorGG,theoErrorVBF,0,0};

	double error[16]; 
        double errorStat[16];
        double errorSyst[16];

	double yield[16];

	for (int i=0; i<16; i++){
			if((i == 8 || i ==9)&& VBF){}
			else if(i==11){
                                yield[i]=0; error[i]=0; errorSyst[i]=0; errorStat[i]=0;
				for (int j=0; j<10; j++) {yield[i]+=yield[j]; errorSyst[i]+=errorSyst[j]*errorSyst[j]; errorStat[i]+=errorStat[j]*errorStat[j];}
				errorStat[i]=sqrt(errorStat[i]);
                                errorSyst[i]=sqrt(errorSyst[i]);
			}
			else if (i==14) {
                                yield[i]=yield[i-1]+ yield[i-2];
				errorStat[i]=sqrt(errorStat[i-1]**2+errorStat[i-2]**2);
				errorSyst[i]=sqrt(errorSyst[i-1]**2+errorSyst[i-2]**2);
			}
			else if (i==10&& !VBF){
                                yield[i]=yield[i-1]+ yield[i-2]+yield[i-3]+yield[i-4];
                                errorStat[i]=sqrt(errorStat[i-1]**2+errorStat[i-2]**2+errorStat[i-3]**2+errorStat[i-4]**2);
                                errorSyst[i]=sqrt(errorSyst[i-1]**2+errorSyst[i-2]**2+errorSyst[i-3]**2+errorSyst[i-4]**2);			
			}
			else if (i==10 && VBF){
                                yield[i]=yield[i-3]+ yield[i-4];
                                errorStat[i]=sqrt(errorStat[i-3]**2+errorStat[i-4]**2);
                                errorSyst[i]=sqrt(errorSyst[i-3]**2+errorSyst[i-4]**2);
                        }
			else{
                                if(i == 15){
                                }
				yield[i]=yieldHisto(fileMuTauGG,dir+"/"+samples[i],xmin,xmax,errorStat[i]);
				if(yield[i]<0) yield[i]=0;
				if(i==12||i==13) {
						 yield[i]=yield[i];
						 errorStat[i]=errorStat[i];
						 }
				errorSyst[i]=yield[i]*errorFactor[i];
			}
                                error[i]=sqrt(errorStat[i]*errorStat[i]+errorSyst[i]*errorSyst[i]);
				if(i == 15){
				}

			if(i==0||i==6 || i==11 || i==15) printf("------------------------------------------------------------------------------------------\n");
			if(i==10||i==14) printf("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n"); 
//			printf("%2.0d  %s \t ->  %8.2f +- %5.2f (%5.2f,%5.2f)\n",i+1,samplesName[i].Data(),yield[i], error[i],errorStat[i],errorSyst[i]);	
                        printf("2.0%d  %s \t ->     $%8.2f \\pm %5.2f$ \n",i+1,samplesName[i].Data(),yield[i], error[i]);
			if(i==11 || i==14) printf("------------------------------------------------------------------------------------------\n");
			if(i==11) printf("------------------------------------------------------------------------------------------\n");
	}

}

double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error){
	TH1F* histo=(TH1F*)file->Get(name); 
	int binmin=histo->FindBin(xmin);
        double binwidth = histo->GetBinWidth(binmin);
	int binmax = xmax/binwidth;

	double yield=histo->IntegralAndError(binmin,binmax,error);

	return yield;
}
