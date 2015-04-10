#include <TString.h>
#include <TFile.h>
#include <TH1.h>


void getYields(TString name,TString dir, double xmin, double xmax, bool, VBF, bool GG);
double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error);

void printYieldsMuEle(){

	printf("GG category \n"); 
	//getYields("mlfit.root","shapes_fit_s/datacard_MuEle_0Jet","mueledatacards_June6/GGF_rootfile.root","GGF",10,15,false,true);
	getYields("outCombinedFitsAll/mlfit.root","shapes_fit_s/datacard_MuEle_0Jet","mueledatacards_June6/GGF_rootfile.root","GGF",10,15,false,true);
        printf("\n\n");

        printf("Boost category \n");
        //getYields("outCombinedFitsAll/mlfit.root","shapes_fit_s/datacard_MuEle_1Jet","mueledatacards_June6/Boost_rootfile.root","Boost",10,15,false,false);
	getYields("outCombinedFitsAll/mlfit.root","shapes_fit_s/datacard_MuEle_1Jet","mueledatacards_June6/Boost_rootfile.root","Boost",10,15,false,false);
        printf("\n\n");

        printf("VBF category \n");
        //getYields("mlfit.root","shapes_fit_s/datacard_MuEle_2Jet","mueledatacards_June6/VBF_rootfile.root","VBF",5,8,true,false);
	getYields("outCombinedFitsAll/mlfit.root","shapes_fit_s/datacard_MuEle_2Jet","mueledatacards_June6/VBF_rootfile.root","VBF",5,8,true,false);
        printf("\n\n");

}

void getYields(TString name,TString dir, TString dataName, TString dirData, double xmin, double xmax, bool VBF, bool GG){

	TFile *fileMuTauGG = new TFile(name,"READONLY");
	TFile *fileMuTauData = new TFile(dataName, "READONLY");

	TString samplesName[19]={"                  Fake leptons",
                                 "          Z#rightarrow#tau#tau",
				 "                            VV",
                                 "                        WGamma",
                                 "                       WGamma*",
				 "                WGamma,WGamma*",
                                 "                     Drell-Yan",
                                 "                      t#bar{t}",
                                 "                    t, #bar{t}",
				 "   SM H#rightarrow#tau#tau, GG",
				 "  SM H#rightarrow#tau#tau, VBF",
                                 "        SM H#rightarrow WW, GG",
                                 "       SM H#rightarrow WW, VBF",
				 "                      SM Higgs",			
				 "                           BG ",
				 "   LFV H#rightarrow#mu#tau, GG",
				 "  LFV H#rightarrow#mu#tau, VBF",
                                 "      LFV  H#rightarrow#mu#tau",
				 "                          data"};

	double theoErrorGG=sqrt(0.08*0.08+0.10*0.10+0.04*0.04);
		if(VBF) theoErrorGG=sqrt(0.08*0.08+0.30*0.30+0.04*0.04);
	double theoErrorVBF=sqrt(0.08*0.08+0.04*0.04+0.04*0.04);

	TString samples[19]={"Fakes","ZTauTau","WW","WG","WGStar","","DYnoTauTau","TT","TOP","ggHTauTau","vbfHTauTau","ggHWW","vbfHWW","","","LFVGG","LFVVBF","","data_obs"};
	double errorFactor[19]={0.4,0.03,0.15,1,1,0,0.1,0.1,0.1,theoErrorGG,theoErrorVBF,theoErrorGG,theoErrorVBF,0,0,theoErrorGG,theoErrorVBF,0,0};

	double error[19]; 
        double errorStat[19];
        double errorSyst[19];

	double yield[19];

	for (int i=0; i<19; i++){
			if(i==14){
				yield[i]=0; error[i]=0; errorSyst[i]=0; errorStat[i]=0; 
				for (int j=0; j<13; j++) {
					if (j != 5){
						if ((VBF && (j != 3 && j!= 4 && j!= 6)) || !VBF){
							yield[i]+=yield[j]; errorSyst[i]+=errorSyst[j]*errorSyst[j]; errorStat[i]+=errorStat[j]*errorStat[j];
						}
					}
				}
				errorStat[i]=sqrt(errorStat[i]);
                                errorSyst[i]=sqrt(errorSyst[i]);

			}
			else if (i==17){
                                yield[i]=yield[i-1]+ yield[i-2];
				errorStat[i]=sqrt(errorStat[i-1]**2+errorStat[i-2]**2);
				errorSyst[i]=sqrt(errorSyst[i-1]**2+errorSyst[i-2]**2);
                        }
                        else if (i==13){
                                yield[i]=yield[i-1]+ yield[i-2]+yield[i-3]+yield[i-4];
                                errorStat[i]=sqrt(errorStat[i-1]**2+errorStat[i-2]**2+errorStat[i-3]**2+errorStat[i-4]**2);
                                errorSyst[i]=sqrt(errorSyst[i-1]**2+errorSyst[i-2]**2+errorSyst[i-3]**2+errorSyst[i-4]**2);
                        }
			else if (i == 5){
				if (!VBF){
					if (!GG){
                                		yield[i]=yield[i-1]+ yield[i-2];
                                		errorStat[i]=sqrt(errorStat[i-1]**2+errorStat[i-2]**2);
                                		errorSyst[i]=sqrt(errorSyst[i-1]**2+errorSyst[i-2]**2);
					}
					else {
                                                yield[i]=yield[i-1];
                                                errorStat[i]=sqrt(errorStat[i-1]**2);
                                                errorSyst[i]=sqrt(errorSyst[i-1]**2);
					}
				}
			}
			else if(i==3 || i == 4 || i == 6){
				if (!VBF){
					if (!GG && i == 3){
	                                	yield[i]=yieldHisto(fileMuTauGG,dir+"/"+samples[i],xmin,xmax,errorStat[i]);
                                		errorSyst[i]=yield[i]*errorFactor[i];
					}
					else if (i == 4 || i == 6){	
                                                yield[i]=yieldHisto(fileMuTauGG,dir+"/"+samples[i],xmin,xmax,errorStat[i]);
                                                errorSyst[i]=yield[i]*errorFactor[i];
					}
				}
			}
					
			else{
				if (i!=18){
					yield[i]=yieldHisto(fileMuTauGG,dir+"/"+samples[i],xmin,xmax,errorStat[i]);
				}
				else{
					if (VBF){
                                        	
						//yield[i]=yieldHisto(fileMuTauData,dirData+"/"+samples[i],100,160,errorStat[i]);
						yield[i]=yieldHisto(fileMuTauData,dirData+"/"+samples[i],100,160,errorStat[i]);		
			                }
					else{
						//yield[i]=yieldHisto(fileMuTauData,dirData+"/"+samples[i],100,150,errorStat[i]);
						yield[i]=yieldHisto(fileMuTauData,dirData+"/"+samples[i],100,150,errorStat[i]);
					}
				}
				if(i==15||i==16) {
						 yield[i]=yield[i];
						 errorStat[i]=errorStat[i];
						 }
				errorSyst[i]=yield[i]*errorFactor[i];
			}
                                error[i]=sqrt(errorStat[i]*errorStat[i]+errorSyst[i]*errorSyst[i]);

			//if(i==0||i==9 || i==14 || i==18) printf("------------------------------------------------------------------------------------------\n");
			//if(i==13||i==17) printf("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n"); 
//			printf("2.0%d  %s \t ->  %8.3f +- %5.3f (%5.3f,%5.3f)\n",i+1,samplesName[i].Data(),yield[i], error[i],errorStat[i],errorSyst[i]);		  
			if(error[i] < 0.1 && error[i] > 0){
				error[i] = 0.1;
			}
			if  (yield[i] < 0.1 && yield[i] > 0){
				yield[i] = 0.1; 
			}
                       	printf("2.0%d  %s \t ->     $%8.3f \\pm %5.3f$ \n",i+1,samplesName[i].Data(),yield[i], error[i]);
			//if(i==14 || i==17) printf("------------------------------------------------------------------------------------------\n");
			//if(i==14) printf("------------------------------------------------------------------------------------------\n");
	}

}

double yieldHisto(TFile* file, TString name,double xmin, double xmax, double &error){
	TH1F* histo=(TH1F*)file->Get(name); 
	int binmin=histo->FindBin(xmin);
	double binwidth = histo->GetBinWidth(binmin);
	int binmax = xmax/binwidth;
        //int binmax=histo->FindBin(xmax);
	
	
	

	//printf("%3i", binmax);
	double yield=histo->IntegralAndError(binmin,binmax,error);

	return yield;
}


