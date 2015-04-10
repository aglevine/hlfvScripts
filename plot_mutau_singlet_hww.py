from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import numpy
import makeOldQCD


##get qcd normalization (choose selections for qcd)

def yieldHisto(histo,xmin,xmax):
	binmin = int(histo.FindBin(xmin))
	binwidth = histo.GetBinWidth(binmin)
	binmax = int(xmax/binwidth)
	signal = histo.Integral(binmin,binmax)
	return signal
	

def make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file,wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm):

        qcd_os_inc = 1.06* get_ss_inc_qcd(var,channel, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm)  ##gets same sign inclusive qcd
        #factor of 1.06 for os inclusive qcd 
	
	if not presel: #get efficiency of vbf cuts
        	if channel == "highMtssvbf":
                	ssanti_iso_ntuple_spot = "highMtssantiisomuonvbf"
		else:
     			ssanti_iso_ntuple_spot = "ssantiisomuon" + channel ##channel = gg or vbf
        	qcd_antiiso_ss = data_ntuple_file.Get(ssanti_iso_ntuple_spot+"/"+var).Clone()
		#print qcd_antiiso_ss.Integral()
        	qcd_antiiso_ss_inc = data_pre_ntuple_file.Get(ssanti_iso_ntuple_spot+"/"+var).Clone()
		qcd_norm = qcd_os_inc*qcd_antiiso_ss.Integral()/qcd_antiiso_ss_inc.Integral()
	else:
		qcd_norm = qcd_os_inc
        return qcd_norm


#return same sign inclusive qcd normalization
def get_ss_inc_qcd(var,channel, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm):

	if channel == "highMtssvbf":
		ss_ntuple_spot = "highMtssvbf"
	elif channel == "highMtssgg":
		ss_ntuple_spot = "highMtssgg"
	elif channel == "highMtvbf":
		ss_ntuple_spot = "highMtssvbf"
	elif channel == "ssvbf":
		ss_ntuple_spot = "ssvbf"
	elif channel == "ssgg":
		ss_ntuple_spot = "ssgg"
	else:
		ss_ntuple_spot = "ss"+channel #channel = vbf or gg
	zjets_pre = zjets_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
	zjets_pre.Scale(zjets_norm)
	ttbar_semi_pre = ttbar_semi_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
        ttbar_full_pre = ttbar_full_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
        ttbar_semi_pre.Scale(ttbar_semi_norm)
        ttbar_full_pre.Scale(ttbar_full_norm)
	ttbar_pre = ttbar_full_pre.Clone()
        ttbar_pre.Add(ttbar_semi_pre)
	ww_pre = ww_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
	ww_pre.Scale(ww_norm)
	data_ss_inc = data_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
	wjets_pre = get_w(var,ss_ntuple_spot,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm) #returns integral of w+jets estimation
	qcd_ss_inc = data_ss_inc.Integral() - zjets_pre.Integral()-ttbar_pre.Integral() - ww_pre.Integral()-wjets_pre #subtract MC from data to get QCD
	#print "qcd test:"
	#print zjets_pre.Integral()
	#print ttbar_pre.Integral()
	#print ww_pre.Integral()
	#print wjets_pre
	#print data_ss_inc.Integral()
	return qcd_ss_inc

	
## return w+jets MC estimation
def get_w(var,ss_ntuple_spot, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm):

	if ss_ntuple_spot == "highMtssvbf":
		ss_highmt_ntuple_spot = "highMtssvbf"
	elif ss_ntuple_spot == "highMtssgg":
		ss_highmt_ntuple_spot = "highMtssgg"
	else:
		ss_highmt_ntuple_spot = "highMt"+ss_ntuple_spot
	##print ss_highmt_ntuple_spot
	data_ss_highmt = data_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone() #data_ss_highmt
        zjets_ss_highmt = zjets_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
	zjets_ss_highmt.Scale(zjets_norm)
        ttbar_semi_ss_highmt = ttbar_semi_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
        ttbar_full_ss_highmt = ttbar_full_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
	ttbar_semi_ss_highmt.Scale(ttbar_semi_norm)
	ttbar_full_ss_highmt.Scale(ttbar_full_norm)
	ttbar_ss_highmt = ttbar_full_ss_highmt.Clone()
	ttbar_ss_highmt.Add(ttbar_semi_ss_highmt)
	
        ww_ss_highmt = ww_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
	ww_ss_highmt.Scale(ww_norm)
	
	wjets1_mc_ss_highmt = wjets1_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
	wjets1_mc_ss_highmt.Scale(wjets1_norm)
        wjets2_mc_ss_highmt = wjets2_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
        wjets2_mc_ss_highmt.Scale(wjets2_norm)
        wjets3_mc_ss_highmt = wjets3_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
        wjets3_mc_ss_highmt.Scale(wjets3_norm)
        wjets4_mc_ss_highmt = wjets4_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
        wjets4_mc_ss_highmt.Scale(wjets4_norm)
	wjetsFiltered_mc_ss_highmt = wjetsFiltered_pre_ntuple_file.Get(ss_highmt_ntuple_spot+"/"+var).Clone()
	wjetsFiltered_mc_ss_highmt.Scale(wjetsFiltered_norm)
	wjets_mc_ss_highmt = wjets1_mc_ss_highmt.Clone()
	#print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets2_mc_ss_highmt)
	#print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets3_mc_ss_highmt)
	#print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets4_mc_ss_highmt)
	wjets_mc_ss_highmt.Add(wjetsFiltered_mc_ss_highmt)
	#print wjets_mc_ss_highmt.Integral()
        if "gg0" in ss_ntuple_spot:
                wjets_mc_ss_highmt.Scale(0.8585376)
		#print wjets_mc_ss_highmt.Integral()

	
	##print wjets_mc_ss_highmt.Integral()
	wjets1_mc_ss = wjets1_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
	wjets1_mc_ss.Scale(wjets1_norm)
        wjets2_mc_ss = wjets2_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
        wjets2_mc_ss.Scale(wjets2_norm)
        wjets3_mc_ss = wjets3_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
        wjets3_mc_ss.Scale(wjets3_norm)
        wjets4_mc_ss = wjets4_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
        wjets4_mc_ss.Scale(wjets4_norm)
	wjetsFiltered_mc_ss = wjetsFiltered_pre_ntuple_file.Get(ss_ntuple_spot+"/"+var).Clone()
	wjetsFiltered_mc_ss.Scale(wjetsFiltered_norm)
	wjets_mc_ss = wjets1_mc_ss.Clone()
	wjets_mc_ss.Add(wjets2_mc_ss)
	wjets_mc_ss.Add(wjets3_mc_ss)
	wjets_mc_ss.Add(wjets4_mc_ss)
	wjets_mc_ss.Add(wjetsFiltered_mc_ss)
        if "gg0" in ss_ntuple_spot:
                wjets_mc_ss.Scale(0.8585376)

	##print wjets_mc_ss.Integral()
	wjets_ss_inc = (data_ss_highmt.Integral() - zjets_ss_highmt.Integral() - ttbar_ss_highmt.Integral()-ww_ss_highmt.Integral())*wjets_mc_ss.Integral()/wjets_mc_ss_highmt.Integral()  #compute wjets from data in highmt sideband wjets control region. Multiply by ss/highMtss yield from MC
	#print (data_ss_highmt.Integral() - zjets_ss_highmt.Integral() - ttbar_ss_highmt.Integral()-ww_ss_highmt.Integral())
	if channel == "highMtssvbf":
		return wjets_mc_ss_highmt.Integral()
	else:
		return wjets_mc_ss.Integral()
	#return wjets_ss_inc


#########
##Style##
#ROOT.gROOT.LoadMacro("tdrstyle.C")
#ROOT.setTDRStyle()

#ROOT.gROOT.SetStyle("Plain")
#ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)
#if len(argv) < 2:
#	print "usage: python plot_mutau variable"
#	sys.exit()
var = "mPt"
predir = "presel_Feb16_jetPt/"
savedir = "tesup_signal_March9/"
channel = "vbf"
try:
        opts, args = getopt.getopt(sys.argv[1:],"ts:p:c:v:",["savedir=","predir=","channel=","var="])
except getopt.GetoptError:
        print 'plot_mutau_singlet.py -s <savedir> -p <predir> -c <channel> -v <var>'
        sys.exit(2)
for opt,arg in opts:
        #print "test     OOOOOOOOPPPPPPPPPPPPPPPPPPTTTTTTTTTTTTTTTSSSSS"
        #print opt
        if opt == "-t":
                print 'plot_mutau_singlet.py -s <savedir> -p <predir> -c <channel> -v <var>'
                sys.exit()
        elif opt in ("-s","--savedir"):
                savedir = arg
        elif opt in ("-p","--predir"):
                predir = arg
        elif opt in ("-c","--channel"):
                channel = arg
        elif opt in ("-v","--var"):
                var = arg

shape_norm = False
if shape_norm == False:
	ynormlabel = " "
else:
	ynormlabel = "Normalized to 1 "
if "jes" in savedir:
	jes = True #jes up or down
else:
	jes = False
if "ues" in savedir:
	ues = True
else:
	ues = False 
print "JJJJJJJEEEEEEEEESSSSSSSSSSS" + str(jes)
presel =  False #use preselection cuts or not
blind = False
if channel == "highMtssvbf":
	blind = False
systematics = True
if shape_norm == True:
	systematics = False
fakeRate = True #apply fake rate method
zjetsEmbed = True #use embedded data samples for zjets
DYShape = False
seperateSemiFull = False #seperate semi and fully leptonic ttbar
plotData=True
plotSave=True
prelimColors=False
new_signal=True
logScale=False
extraBackground = True
#if channel == "gg0" or channel == "gg1":
	#fakeRate = False
#if systematics == True:
#	fakeRate = True
##savedir contains the root files for plotting
if presel:
        savedir = predir
##import parameters for input variable	
import mutau_vars
print savedir
print predir
print channel
print var
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

if "jes" in predir and not ("jes" in savedir):
	print "Error: jes mismatch"
	sys.exit()
if "jes" in savedir and not ("jes" in predir):
        print "Error: jes mismatch"
        sys.exit()
if "jes_minus" in var and not ("jesminus" in savedir) or "jes_plus" in var and not ("jesplus" in savedir):
	print "Error: jes doesn't match"
	sys.exit()
if "ues" in predir and not ("ues" in savedir):
        print "Error: ues mismatch"
        sys.exit()
#if "ues" in savedir and not ("ues" in predir):
#        print "Error: ues mismatch"
#        sys.exit()
if "ues_minus" in var and not ("uesminus" in savedir) or "ues_plus" in var and not ("uesplus" in savedir):
        print "Error: ues doesn't match"
        sys.exit()
if var == "collMass_jes_minus" or var == "collMass_jes_plus" or var == "collMass_type1_ues_minus" or var == "collMass_type1_ues_plus":
	datavar = "collMass_type1"
if var == "collMass_type1":
	datavar = "collMass_type1"
elif var == "tMtToPfMet_ues":
	datavar = "tMtToPfMet_Ty1"
else:
	datavar = var
getVarParams = "mutau_vars."+var
varParams = eval(getVarParams)
xlabel = varParams[0]
if presel:
	binwidth = varParams[7]
else:
	binwidth = varParams[1]
if "collMass" in var and channel == "gg0":
	binwidth = 10
elif "collMass" in var and channel == "gg1":
	binwidth = 10
elif "ztautau" in channel and "collMass" in var:
	binwidth = 20
elif "intermediate" in savedir:
	binwidth = 20
if presel == False:
	legend = eval(varParams[2])
else:
	legend = eval(varParams[8])
#	print "test!!!!!!!!"
blindlow = varParams[3]
blindhigh = varParams[4]
if var == "m_t_Mass" and channel =="gg":
	blindhigh  = 120
if presel == True:
	if var == "fullMT_type1" and channel == "vbf":
		blindlow = 100
		blindhigh = 150
	elif var == "m_t_Mass" and (channel == "vbf" or channel == "gg1"):
		blindlow = 70
		blindhigh = 120
	elif var =="m_t_Mass" and channel == "ztautaucontrolvbf":
		blindlow = 80
		blindhigh = 110
	elif var == "m_t_Mass" and channel == "gg0":
		blindlow=80
		blindhigh=130
	elif var == "collMass_type1" and (channel == "gg1" or channel =="vbf"or channel == "gg0"):
		blindlow = 100
		blindhigh = 150
	elif var == "tMtToPfMet_Ty1" and channel == "gg1":
		blindlow = 0
		blindhigh = 10
	#else:
	#	blind=False
if blindlow==blindhigh:
        blind = False
isGeV = varParams[5]
xRange = varParams[6]
canvas = ROOT.TCanvas("canvas","canvas",800,800)
if plotData==True:
	p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
	#ROOT.gStyle.SetCanvasDefH(600)
	#ROOT.gStyle.SetCanvasDefW(600)
	#ROOT.gStyle.SetPadTopMargin(0.05)
	#ROOT.gStyle.SetPadRightMargin(0.03)
	#ROOT.gStyle.SetPadBottomMargin(0.3)
	p_lfv.SetLeftMargin(0.2147651)
	p_lfv.SetRightMargin(0.06543624)
	p_lfv.SetTopMargin(0.04895105)
	p_lfv.SetBottomMargin(0.305)
	if logScale == True:
		p_lfv.SetLogy()
	p_lfv.Draw()
	p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.295)
        p_ratio.SetLeftMargin(0.2147651)
        p_ratio.SetRightMargin(0.06543624)
        p_ratio.SetTopMargin(0.04895105)
        #p_ratio.SetBottomMargin(0.1311189)
	p_ratio.SetBottomMargin(0.295)
	p_ratio.SetGridy()
	p_ratio.Draw()
	#p_lfv.Draw()
	p_lfv.cd()
else:
	p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
        p_lfv.SetLeftMargin(0.2147651)
        p_lfv.SetRightMargin(0.06543624)
        p_lfv.SetTopMargin(0.04895105)
        p_lfv.SetBottomMargin(0.1311189)
        if logScale == True:
                p_lfv.SetLogy()
        p_lfv.Draw()
	p_lfv.cd()

LFVStack = ROOT.THStack("stack","")
if new_signal == True:
	hgglfv_ntuple_file_str = 'LFV_GluGlu_Dec9.root'
	hvbflfv_ntuple_file_str='LFV_VBF_Dec9.root'
else:
	hgglfv_ntuple_file_str = 'LFV_GluGlu_H2Tau_M-126.root'
	hvbflfv_ntuple_file_str = 'LFV_VBF_H2Tau_M-126.root'
hggsm_ntuple_file_str = 'GGH_H2Tau_M-125.root'
zjets_ntuple_file_str = 'Zjets_M50.root'
if zjetsEmbed:
	dataEmb_ntuple_file_str = 'dataEmbedded_2012.root'
	dy1jets_ntuple_file_str = 'DY1Jets_madgraph.root'
	dy2jets_ntuple_file_str = 'DY2Jets_madgraph.root'
	dy3jets_ntuple_file_str = 'DY3Jets_madgraph.root'
	dy4jets_ntuple_file_str = 'DY4Jets_madgraph.root'
	
	dy1other_ntuple_file_str = 'OtherDY1.root'
	dy2other_ntuple_file_str = 'OtherDY2.root'
	dy3other_ntuple_file_str = 'OtherDY3.root'
	dy4other_ntuple_file_str = 'OtherDY4.root'
	zjetsotherMC_ntuple_file_str = 'OtherM50.root'
	
	#if "gg0" in channel or "gg1" in channel:
	#	dy1other_ntuple_file_str = savedir+'DYAll/DY1Jets_madgraph.root'
	 #       dy2other_ntuple_file_str = savedir+'DYAll/DY2Jets_madgraph.root'
        #	dy3other_ntuple_file_str = savedir+'DYAll/DY3Jets_madgraph.root'
        #	dy4other_ntuple_file_str = savedir+'DYAll/DY4Jets_madgraph.root'
	#else:
         #       dy1jets_ntuple_file_str = 'DYAll/DY1Jets_madgraph.root'
          #      dy2jets_ntuple_file_str = 'DYAll/DY2Jets_madgraph.root'
           #     dy3jets_ntuple_file_str = 'DYAll/DY3Jets_madgraph.root'
            #    dy4jets_ntuple_file_str = 'DYAll/DY4Jets_madgraph.root'
wjets1_ntuple_file_str = 'Wplus1Jets.root'
wjets2_ntuple_file_str = 'Wplus2Jets.root'
wjets3_ntuple_file_str = 'Wplus3Jets.root'
wjets4_ntuple_file_str = 'Wplus4Jets_madgraph.root'
wjetsFiltered_ntuple_file_str = 'WplusJets_madgraph_filtered.root'
ttbar_semi_ntuple_file_str = 'TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.root'
ttbar_full_ntuple_file_str = 'TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.root'
ww_ntuple_file_str = 'WWJetsTo2L2Nu_TuneZ2_8TeV.root'
tt_ntuple_file_str = 'T_t-channel.root'
tbart_ntuple_file_str = 'Tbar_t-channel.root'
tw_ntuple_file_str = 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
#tbarw_ntuple_file_str = 'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
tbarw_ntuple_file_str = 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
data_ntuple_file_str = 'data_2012.root'
#data_ntuple_file_str = 'jesplusdata_2012.root'
hvbfsm_ntuple_file_str = 'VBF_H2Tau_M-125.root'
hvbfww_ntuple_file_str = 'HiggsToWWVBF125.root'
hggww_ntuple_file_str = 'HiggsToWWGG125.root'
if extraBackground == True:
	wwfull_ntuple_file_str = 'WWpythia.root'
	wz_ntuple_file_str = 'WZ.root'
	zz_ntuple_file_str = 'ZZ.root'
	vhsm_ntuple_file_str = 'VH_H2Tau_M-125.root'
	vhlfv_ntuple_file_str = 'LFV_VH_H2MuTau_LONG-MuTauMC.root'
	hwwvhtth_ntuple_file_str = 'HWWVHTTH125.root'

hgglfv_ntuple_file = ROOT.TFile(savedir+hgglfv_ntuple_file_str)
hvbflfv_ntuple_file = ROOT.TFile(savedir+hvbflfv_ntuple_file_str)
zjets_ntuple_file = ROOT.TFile(savedir+zjets_ntuple_file_str)
if zjetsEmbed:
	dataEmb_ntuple_file = ROOT.TFile(savedir+dataEmb_ntuple_file_str)
	dy1jets_ntuple_file = ROOT.TFile(savedir+dy1jets_ntuple_file_str)
	dy2jets_ntuple_file = ROOT.TFile(savedir+dy2jets_ntuple_file_str)
	dy3jets_ntuple_file = ROOT.TFile(savedir+dy3jets_ntuple_file_str)
	dy4jets_ntuple_file = ROOT.TFile(savedir+dy4jets_ntuple_file_str)
	dy1other_ntuple_file = ROOT.TFile(savedir+dy1other_ntuple_file_str)
	dy2other_ntuple_file = ROOT.TFile(savedir+dy2other_ntuple_file_str)
	dy3other_ntuple_file = ROOT.TFile(savedir+dy3other_ntuple_file_str)
	dy4other_ntuple_file = ROOT.TFile(savedir+dy4other_ntuple_file_str)
	zjetsotherMC_ntuple_file = ROOT.TFile(savedir+zjetsotherMC_ntuple_file_str)
	#if "gg0" in channel or "gg1" in channel:
	#	dy1other_ntuple_file = ROOT.TFile(dy1other_ntuple_file_str)
         #       dy2other_ntuple_file = ROOT.TFile(dy2other_ntuple_file_str)
          #      dy3other_ntuple_file = ROOT.TFile(dy3other_ntuple_file_str)
           #     dy4other_ntuple_file = ROOT.TFile(dy4other_ntuple_file_str)
wjets1_ntuple_file = ROOT.TFile(savedir+wjets1_ntuple_file_str)
wjets2_ntuple_file = ROOT.TFile(savedir+wjets2_ntuple_file_str)
wjets3_ntuple_file = ROOT.TFile(savedir+wjets3_ntuple_file_str)
wjets4_ntuple_file = ROOT.TFile(savedir+wjets4_ntuple_file_str)
wjetsFiltered_ntuple_file = ROOT.TFile(savedir+wjetsFiltered_ntuple_file_str)
ttbar_semi_ntuple_file = ROOT.TFile(savedir+ttbar_semi_ntuple_file_str)
ttbar_full_ntuple_file = ROOT.TFile(savedir+ttbar_full_ntuple_file_str)
ww_ntuple_file = ROOT.TFile(savedir+ww_ntuple_file_str)
tt_ntuple_file = ROOT.TFile(savedir+tt_ntuple_file_str)
tbart_ntuple_file = ROOT.TFile(savedir+tbart_ntuple_file_str)
tw_ntuple_file = ROOT.TFile(savedir+tw_ntuple_file_str)
tbarw_ntuple_file = ROOT.TFile(savedir+tbarw_ntuple_file_str)
data_ntuple_file = ROOT.TFile(savedir+data_ntuple_file_str)
hvbfsm_ntuple_file = ROOT.TFile(savedir+hvbfsm_ntuple_file_str)
hggsm_ntuple_file = ROOT.TFile(savedir+hggsm_ntuple_file_str)
hvbfww_ntuple_file = ROOT.TFile(savedir+hvbfww_ntuple_file_str)
hggww_ntuple_file = ROOT.TFile(savedir+hggww_ntuple_file_str)
if extraBackground == True:
	wwfull_ntuple_file = ROOT.TFile(savedir+wwfull_ntuple_file_str)
	wz_ntuple_file = ROOT.TFile(savedir+wz_ntuple_file_str)
	zz_ntuple_file = ROOT.TFile(savedir+zz_ntuple_file_str)
	vhsm_ntuple_file = ROOT.TFile(savedir+vhsm_ntuple_file_str)
	vhlfv_ntuple_file = ROOT.TFile(savedir+vhlfv_ntuple_file_str)
	hwwvhtth_ntuple_file = ROOT.TFile(savedir+hwwvhtth_ntuple_file_str)


hgglfv_pre_ntuple_file = ROOT.TFile(predir+hgglfv_ntuple_file_str)
hvbflfv_pre_ntuple_file = ROOT.TFile(predir+hvbflfv_ntuple_file_str)
zjets_pre_ntuple_file = ROOT.TFile(predir+zjets_ntuple_file_str)
wjets1_pre_ntuple_file = ROOT.TFile(predir+wjets1_ntuple_file_str)
wjets2_pre_ntuple_file = ROOT.TFile(predir+wjets2_ntuple_file_str)
wjets3_pre_ntuple_file = ROOT.TFile(predir+wjets3_ntuple_file_str)
wjets4_pre_ntuple_file = ROOT.TFile(predir+wjets4_ntuple_file_str)
wjetsFiltered_pre_ntuple_file = ROOT.TFile(predir+wjetsFiltered_ntuple_file_str)
ttbar_semi_pre_ntuple_file = ROOT.TFile(predir+ttbar_semi_ntuple_file_str)
ttbar_full_pre_ntuple_file = ROOT.TFile(predir+ttbar_full_ntuple_file_str)
ww_pre_ntuple_file = ROOT.TFile(predir+ww_ntuple_file_str)
tt_pre_ntuple_file = ROOT.TFile(predir+tt_ntuple_file_str)
tbart_pre_ntuple_file = ROOT.TFile(predir+tbart_ntuple_file_str)
tw_pre_ntuple_file = ROOT.TFile(predir+tw_ntuple_file_str)
tbarw_pre_ntuple_file = ROOT.TFile(predir+tbarw_ntuple_file_str)

data_pre_ntuple_file = ROOT.TFile(predir+data_ntuple_file_str)

#get histograms
ntuple_spot = channel
hgglfv = hgglfv_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
hvbflfv = hvbflfv_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
hvbfsm = hvbfsm_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#higgs->WW is very small, didn't rereun for jes and ues
hggww = hggww_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
hvbfww = hvbfww_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()

hggsm = hggsm_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
zjetsMC = zjets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
if zjetsEmbed:
	dy1jets = dy1jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy2jets = dy2jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy3jets = dy3jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy4jets = dy4jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy1other = dy1other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy2other = dy2other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy3other = dy3other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy4other = dy4other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	zjetsotherMC = zjetsotherMC_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#print datavar
	zjets = dataEmb_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
	print "ztautau1:"+str(zjets.Integral())
	#if "gg0" in channel or "gg1" in channel:
	#	dy1other = dy1other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy2other = dy2other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy3other = dy3other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy4other = dy4other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#changed w+jets to datavar to save time when running jes (w+jets MC not used in data driving fake rate estimation)
wjets1 = wjets1_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets2 = wjets2_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets3 = wjets3_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets4 = wjets4_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjetsFiltered = wjetsFiltered_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_semi = ttbar_semi_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_full = ttbar_full_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ww = ww_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tt = tt_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tbart = tbart_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tw = tw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tbarw = tbarw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
if extraBackground == True:
	wwfull = wwfull_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	wz = wz_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	zz =zz_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	vhsm = vhsm_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	vhlfv = vhlfv_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	hwwvhtth = hwwvhtth_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
data = data_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()


if jes==True:
	lumidir = 'lumicalc_jes/'
elif ues == True:
	lumidir = 'lumicalc_ues/'
else:
	lumidir = 'lumicalc_Jan17/'
#define lumicalc files
data1_lumifile = lumidir + 'data_SingleMu_Run2012A_22Jan2013_v1_2.lumicalc.sum'
data2_lumifile = lumidir + 'data_SingleMu_Run2012B_22Jan2013_v1_2.lumicalc.sum'
data3_lumifile = lumidir + 'data_SingleMu_Run2012C_22Jan2013_v1_2.lumicalc.sum'
data4_lumifile = lumidir + 'data_SingleMu_Run2012D_22Jan2013_v1.lumicalc.sum'
dataEmb1_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012A_v1.lumicalc.sum'
dataEmb2_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012B_v1.lumicalc.sum'
dataEmb3_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012C_v1.lumicalc.sum'
dataEmb4_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012D_v1.lumicalc.sum'
wjets_extension_lumifile = lumidir + 'WplusJets_madgraph_Extension.lumicalc.sum'
wjets1_lumifile = lumidir + 'Wplus1Jets_madgraph.lumicalc.sum'
wjets1_ext_lumifile = lumidir + 'Wplus1Jets_madgraph_extension.lumicalc.sum'
wjets2_lumifile = lumidir + 'Wplus2Jets_madgraph.lumicalc.sum'
wjets2_ext_lumifile = lumidir + 'Wplus2Jets_madgraph_extension.lumicalc.sum'
wjets3_lumifile = lumidir + 'Wplus3Jets_madgraph.lumicalc.sum'
wjets3_ext_lumifile = lumidir + 'Wplus3Jets_madgraph_extension.lumicalc.sum'
wjets4_lumifile = lumidir + 'Wplus4Jets_madgraph.lumicalc.sum'
wjetsFiltered_lumifile = lumidir + 'WplusJets_madgraph_filtered.lumicalc.sum'
dy1jets_lumifile = lumidir + 'DY1Jets_madgraph.lumicalc.sum'
dy2jets_lumifile = lumidir + 'DY2Jets_madgraph.lumicalc.sum'
dy3jets_lumifile = lumidir + 'DY3Jets_madgraph.lumicalc.sum'
dy4jets_lumifile = lumidir + 'DY4Jets_madgraph.lumicalc.sum'
zjets_lumifile = lumidir + 'Zjets_M50.lumicalc.sum'
ttbar_full_lumifile = lumidir + 'TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.lumicalc.sum'
ttbar_semi_lumifile = lumidir + 'TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.lumicalc.sum'
ww_lumifile = lumidir + 'WWJetsTo2L2Nu_TuneZ2_8TeV.lumicalc.sum'
tt_lumifile = lumidir + 'T_t-channel.lumicalc.sum'
tbart_lumifile = lumidir + 'Tbar_t-channel.lumicalc.sum'
tw_lumifile = lumidir + 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'
tbarw_lumifile = lumidir + 'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'
if extraBackground == True:
	wwfull_lumifile = lumidir + 'WWpythia.lumicalc.sum'
	wz_lumifile = lumidir + 'WZ.lumicalc.sum'
	zz_lumifile= lumidir + 'ZZ.lumicalc.sum'
	vhsm_lumifile = lumidir + 'VH_H2Tau_M-125.lumicalc.sum'
	vhlfv_lumifile = lumidir +'LFV_VH_H2MuTau_LONG-MuTauMC.lumicalc.sum'
	hwwvhtth_lumifile = lumidir+'HWWVHTTH125.lumicalc.sum'


if new_signal == True:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_Dec9.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_Dec9.lumicalc.sum'
else:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_H2Tau_M-126.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_H2Tau_M-126.lumicalc.sum'
hvbfsm_lumifile = lumidir + 'VBF_H2Tau_M-125.lumicalc.sum'
hggsm_lumifile = lumidir + 'GGH_H2Tau_M-125.lumicalc.sum'
hvbfww_lumifile = lumidir + 'HiggsToWWVBF125.lumicalc.sum'
hggww_lumifile = lumidir + 'HiggsToWWGG125.lumicalc.sum'



#read lumicalc files

f = open(wjets_extension_lumifile).read().splitlines()
wjets_extension_efflumi = float(f[0])

f = open(wjets1_lumifile).read().splitlines()
wjets1_efflumi = float(f[0])

f = open(wjets1_ext_lumifile).read().splitlines()
wjets1_ext_efflumi = float(f[0])

f = open(wjets2_lumifile).read().splitlines()
wjets2_efflumi = float(f[0])

f = open(wjets2_ext_lumifile).read().splitlines()
wjets2_ext_efflumi = float(f[0])

f = open(wjets3_lumifile).read().splitlines()
wjets3_efflumi = float(f[0])

f = open(wjets3_ext_lumifile).read().splitlines()
wjets3_ext_efflumi = float(f[0])

f = open(wjets4_lumifile).read().splitlines()
wjets4_efflumi = float(f[0])

f = open(wjetsFiltered_lumifile).read().splitlines()
wjetsFiltered_efflumi = float(f[0])

f = open(zjets_lumifile).read().splitlines()
zjets_efflumi = float(f[0])

f = open(ttbar_semi_lumifile).read().splitlines()
ttbar_semi_efflumi = float(f[0])

f = open(ttbar_full_lumifile).read().splitlines()
ttbar_full_efflumi = float(f[0])

f = open(ww_lumifile).read().splitlines()
ww_efflumi = float(f[0])

f = open(tt_lumifile).read().splitlines()
tt_efflumi = float(f[0])

f = open(tbart_lumifile).read().splitlines()
tbart_efflumi = float(f[0])

f = open(tw_lumifile).read().splitlines()
tw_efflumi = float(f[0])

f = open(tbarw_lumifile).read().splitlines()
tbarw_efflumi = float(f[0])

f = open(hvbflfv_lumifile).read().splitlines()
hvbflfv_efflumi = float(f[0])

f = open(hgglfv_lumifile).read().splitlines()
hgglfv_efflumi = float(f[0])

f = open(hvbfsm_lumifile).read().splitlines()
hvbfsm_efflumi = float(f[0])

f = open(hggsm_lumifile).read().splitlines()
hggsm_efflumi = float(f[0])

f = open(hvbfww_lumifile).read().splitlines()
hvbfww_efflumi = float(f[0])

f = open(hggww_lumifile).read().splitlines()
hggww_efflumi = float(f[0])

f = open(data1_lumifile).read().splitlines()
data1_lumi = float(f[0])

f = open(data2_lumifile).read().splitlines()
data2_lumi = float(f[0])

f = open(data3_lumifile).read().splitlines()
data3_lumi = float(f[0])

f = open(data4_lumifile).read().splitlines()
data4_lumi = float(f[0])

f = open(dataEmb1_lumifile).read().splitlines()
dataEmb1_lumi = float(f[0])

f = open(dataEmb2_lumifile).read().splitlines()
dataEmb2_lumi = float(f[0])

f = open(dataEmb3_lumifile).read().splitlines()
dataEmb3_lumi = float(f[0])

f = open(dataEmb4_lumifile).read().splitlines()
dataEmb4_lumi = float(f[0])

f = open(dy1jets_lumifile).read().splitlines()
dy1jets_efflumi = float(f[0])

f = open(dy2jets_lumifile).read().splitlines()
dy2jets_efflumi = float(f[0])

f = open(dy3jets_lumifile).read().splitlines()
dy3jets_efflumi = float(f[0])

#f = open(dy4jets_lumifile).read().splitlines()
f = open(dy3jets_lumifile).read().splitlines()
dy4jets_efflumi = float(f[0])

if extraBackground == True:

	f=open(wwfull_lumifile).read().splitlines()
	wwfull_efflumi = float(f[0])

	f=open(wz_lumifile).read().splitlines()
	wz_efflumi = float(f[0])

	f=open(zz_lumifile).read().splitlines()
	zz_efflumi = float(f[0])

	f=open(vhsm_lumifile).read().splitlines()
	vhsm_efflumi = float(f[0])
	
	f=open(vhlfv_lumifile).read().splitlines()
	vhlfv_efflumi = float(f[0])
	
	f=open(hwwvhtth_lumifile).read().splitlines()
	hwwvhtth_efflumi = float(f[0])

lumi = data1_lumi+data2_lumi+data3_lumi+data4_lumi
print "lumi: " + str(lumi)
lumiEmb = dataEmb1_lumi+dataEmb2_lumi+dataEmb3_lumi+dataEmb4_lumi
wjets1_total_efflumi = wjets1_efflumi+wjets1_ext_efflumi
wjets2_total_efflumi = wjets2_efflumi+wjets2_ext_efflumi
wjets3_total_efflumi = wjets3_efflumi+wjets3_ext_efflumi

#define normalzing factors to normalize MC to data
wjets1_datanorm = lumi/wjets1_total_efflumi
wjets2_datanorm = lumi/wjets2_total_efflumi
wjets3_datanorm = lumi/wjets3_total_efflumi
wjets4_datanorm = lumi/wjets4_efflumi
wjetsFiltered_datanorm = lumi/wjetsFiltered_efflumi
dy1jets_datanorm = lumi/dy1jets_efflumi
dy2jets_datanorm = lumi/dy2jets_efflumi
dy3jets_datanorm = lumi/dy3jets_efflumi
dy4jets_datanorm = lumi/dy4jets_efflumi
zjets_datanorm = lumi/zjets_efflumi
ttbar_semi_datanorm = lumi/ttbar_semi_efflumi
ttbar_full_datanorm = lumi/ttbar_full_efflumi
ww_datanorm = lumi/ww_efflumi
tt_datanorm = lumi/tt_efflumi
tbart_datanorm = lumi/tbart_efflumi
tw_datanorm = lumi/tw_efflumi
tbarw_datanorm = lumi/tbarw_efflumi
if extraBackground == True:
	wwfull_datanorm = lumi/wwfull_efflumi
	wz_datanorm = lumi/wz_efflumi
	zz_datanorm = lumi/zz_efflumi
	vhsm_datanorm = lumi/vhsm_efflumi
	vhlfv_datanorm = lumi/vhlfv_efflumi
	hwwvhtth_datanorm = lumi/hwwvhtth_efflumi


if fakeRate == False:

	print wjetsFiltered_pre_ntuple_file
#get qcd normalization (non fake rate method)
	qcd_norm = makeOldQCD.make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file, wjets1_datanorm, wjets2_datanorm, wjets3_datanorm, wjets4_datanorm, wjetsFiltered_datanorm, zjets_datanorm, ttbar_semi_datanorm, ttbar_full_datanorm, ww_datanorm)
	#qcd_norm = 0
	#print zjets.Integral(ust )
	if channel == "highMtssvbf":
		antiiso_ntuple_spot = "highMtssantiisomuonvbf"
	elif channel == "highMtvbf":
		antiiso_ntuple_spot = "highMtantiisomuonvbf"
	elif channel == "highMtssgg":
		antiiso_ntuple_spot = "highMtssantiisomuongg"
	elif channel == "ssvbf":
		antiiso_ntuple_spot = "ssantiisomuonvbf"
	elif channel == "ssgg":
		antiiso_ntuple_spot = "ssantiisomuongg"
	else:
		antiiso_ntuple_spot = "antiisomuon"+channel #channel = vbf or gg
	qcd = data_ntuple_file.Get(antiiso_ntuple_spot+"/"+var).Clone() #get antiisolated qcd shape
	#qcd = data_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#print "qcd norm" + str(qcd_norm)
	if qcd_norm < 0:  #if approximately no qcd
		qcd.Scale(0)
	else:
		qcd.Scale(qcd_norm/qcd.Integral()) #normalized qcd shape
#correct for using looser vbf Cuts for qcd shape
	#if var == "vbfMass":
#		for x in range(0,500):
#			qcd.SetBinContent(x,0)
#	elif var == "vbfDeta":
#		xbin = qcd.GetXaxis().FindBin(3.5)
#		for x in range(0,xbin):
#			qcd.SetBinContent(x,0)

if shape_norm == False: #normalize histos to data
	wjets1_norm = wjets1_datanorm
	wjets2_norm = wjets2_datanorm
	wjets3_norm = wjets3_datanorm
        wjets4_norm = wjets4_datanorm
	wjetsFiltered_norm = wjetsFiltered_datanorm
	zjets_norm = zjets_datanorm
	ztautau_norm = lumi/lumiEmb
	ttbar_semi_norm = ttbar_semi_datanorm
	ttbar_full_norm = ttbar_full_datanorm
	ww_norm = ww_datanorm
	tt_norm = tt_datanorm
	tbart_norm = tbart_datanorm
	tw_norm = tw_datanorm
	tbarw_norm = tbarw_datanorm
	if extraBackground == True:
        	wwfull_norm = wwfull_datanorm
 		wz_norm = wz_datanorm
		zz_norm = zz_datanorm
		vhsm_norm = vhsm_datanorm
		vhlfv_norm = vhlfv_datanorm
		hwwvhtth_norm = hwwvhtth_datanorm
	dy1jets_norm = dy1jets_datanorm
	dy2jets_norm = dy2jets_datanorm
	dy3jets_norm = dy3jets_datanorm
	dy4jets_norm = dy4jets_datanorm
	hgglfv_norm = lumi/hgglfv_efflumi
	hvbflfv_norm = lumi/hvbflfv_efflumi
	hvbfsm_norm = lumi/hvbfsm_efflumi
        hvbfww_norm = lumi/hvbfww_efflumi
	hggww_norm = lumi/hggww_efflumi
	#print lumi
	#print hggsm_efflumi
	hggsm_norm = lumi/hggsm_efflumi
	#print hggsm_norm
	wjets1.Scale(wjets1_norm)
	wjets2.Scale(wjets2_norm)
        wjets3.Scale(wjets3_norm)
        wjets4.Scale(wjets4_norm)
	wjetsFiltered.Scale(wjetsFiltered_norm)
	wjets = wjets1.Clone()
	wjets.Add(wjets2)
	wjets.Add(wjets3)
	wjets.Add(wjets4)
	wjets.Add(wjetsFiltered)
	tt.Scale(tt_norm)
	tbart.Scale(tbart_norm)
	tw.Scale(tw_norm)
	tbarw.Scale(tbarw_norm)
	singlet = tt.Clone()
	singlet.Add(tbart)
	singlet.Add(tw)
	singlet.Add(tbarw)
	print "testing singlet"
	print tt.Integral()
	print tbart.Integral()
	print tw.Integral()
	print tbarw.Integral()
	if presel == True and "gg0" in channel:
		wjets.Scale(0.8585376)
	ttbar_semi.Scale(ttbar_semi_norm)
	ttbar_full.Scale(ttbar_full_norm)
	ttbar = ttbar_full.Clone()
	ttbar.Add(ttbar_semi)
	zjetsMC.Scale(zjets_norm)
	if zjetsEmbed == False: #check whether or not to use embedded method
		zjets = zjetsMC.Clone()
	else:	
                dy1jets.Scale(dy1jets_datanorm)
                dy2jets.Scale(dy2jets_datanorm)
                dy3jets.Scale(dy3jets_datanorm)
                dy4jets.Scale(dy4jets_datanorm)
                dyjets = dy1jets.Clone()
                dyjets.Add(dy2jets)
                dyjets.Add(dy3jets)
                dyjets.Add(dy4jets)
		dyjets.Add(zjetsMC)
        	print "dyjets:" 
        	print dy1jets.Integral()
        	print dy2jets.Integral()
        	print dy3jets.Integral()
        	print dy4jets.Integral()
		print zjetsMC.Integral()
		#print "???????????????"
		#print zjetsMC.Integral()
		if DYShape == True:
			zjets = dyjets.Clone()
		else:	
			if zjets.Integral() != 0:
				zjets.Scale(dyjets.Integral()/zjets.Integral())
				print "ztautau2:"+str(zjets.Integral())
		dy1other.Scale(dy1jets_datanorm)
		dy2other.Scale(dy2jets_datanorm)
		dy3other.Scale(dy3jets_datanorm)
		dy4other.Scale(dy4jets_datanorm)
		zjetsotherMC.Scale(zjets_norm)
		zjetsother = dy1other.Clone()
		zjetsother.Add(dy2other)
		zjetsother.Add(dy3other)
		zjetsother.Add(dy4other)
		zjetsother.Add(zjetsotherMC)
		print "ZJETSOTERHEFFECTIVE SCALE FACTRAFASDFASFASDFASDFASDFASDF:" + str(zjetsother.Integral()/zjetsother.GetEffectiveEntries())

		
	
	#	if "gg0" in channel or "gg1" in channel:
         #       	dy1other.Scale(dy1jets_datanorm)
	#		dy1other.Add(dy1jets,-1)
         #       	dy2other.Scale(dy2jets_datanorm)
	#		dy2other.Add(dy2jets,-1)
         #       	dy3other.Scale(dy3jets_datanorm)
	#		dy3other.Add(dy3jets,-1)
         #       	dy4other.Scale(dy4jets_datanorm)
	#		dy4other.Add(dy4jets,-1)
	#		dyother = dy1other.Clone()
	#		dyother.Add(dy2other)
	#		dyother.Add(dy3other)
	#		dyother.Add(dy4other)
			
			

	
else:   	#normailze histos to 1
	wjets = wjets1.Clone()
	wjets.Add(wjets2)
	wjets.Add(wjets3)
	wjets.Add(wjets4)
	wjets.Add(wjetsFiltered)
	singlet = tt.Clone()
	singlet.Add(tbart)
	singlet.Add(tw)
	singlet.Add(tbarw)
	ttbar = ttbar_full.Clone()
	ttbar.Add(ttbar_semi)
	wjets_norm = 1/wjets.Integral()
	singlet_norm = 1/singlet.Integral()
	ttbar_norm = 1/ttbar.Integral()
	ww_norm = 1/ww.Integral()
	if extraBackground == True:
		wwfull_norm = 1/wwfull.Integral()
		wz_norm = 1/wz.Integral()
		zz_norm = 1/zz.Integral()
		vhsm_norm = 1/vhsm.Integral()
		vhlfv_norm = 1/vhlfv.Integral()
		hwwvhtth_norm = 1/hwwvhtth.Integral()
	hgglfv_norm = 1/(hgglfv.Integral())
	hvbflfv_norm = 1/(hvbflfv.Integral())
	hvbfsm_norm = 1/(hvbfsm.Integral())
	hggsm_norm = 1/(hggsm.Integral())
        hvbfww_norm = 1/(hvbfww.Integral())
        hggww_norm = 1/(hggww.Integral())
	if fakeRate == False:
		qcd_norm = 1/(qcd.Integral())
		qcd.Scale(qcd_norm)
	wjets.Scale(wjets_norm)
	singlet.Scale(singlet_norm)
	if zjetsEmbed == False:
		zjets = zjetsMC.Clone()
	zjets.Scale(1/zjets.Integral())
        zjetsotherMC.Scale(zjets_datanorm)
        zjetsother = dy1other.Clone()
        zjetsother.Add(dy2other)
        zjetsother.Add(dy3other)
        zjetsother.Add(dy4other)
        zjetsother.Add(zjetsotherMC)
	
	data.Scale(1/data.Integral())	

ww.Scale(ww_norm)
if extraBackground == True:
	wwfull.Scale(wwfull_norm)
	wz.Scale(wz_norm)
	zz.Scale(zz_norm)
	vhsm.Scale(vhsm_norm)
	vhlfv.Scale(vhlfv_norm)
	hwwvhtth.Scale(hwwvhtth_norm)
hgglfv.Scale(hgglfv_norm)
hvbflfv.Scale(hvbflfv_norm)
hvbfsm.Scale(hvbfsm_norm)
hggsm.Scale(hggsm_norm)
hvbfww.Scale(hvbfww_norm)
hggww.Scale(hggww_norm)
xbinLength = data.GetBinWidth(1)
isGeV = varParams[5]
widthOfBin = binwidth*xbinLength
if isGeV:
	ylabel = ynormlabel + " Events / " + str(int(widthOfBin)) + " GeV"
else:
	ylabel = ynormlabel  + " Events / " + str(widthOfBin)

if fakeRate == False:
	qcd.Rebin(binwidth)
if channel == "highMtssvbf":
	fakechannel = "highMtssantiisotauvbf"
elif channel == "highMtssgg":
	fakechannel = "highMtssantiisotaugg"
elif channel == "ttbarcontrolvbf":
	fakechannel = "antiisotauvbf"
else:
	fakechannel = "antiisotau"+channel
if fakeRate == True:
	wjets = data_ntuple_file.Get(fakechannel+"/"+datavar).Clone()
	print "fakes 1:" + str(wjets.Integral())
	if shape_norm == True:
		wjets.Scale(1/wjets.Integral())
	if zjetsEmbed == False:
		zjetsFakes = zjets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		zjetsFakes.Scale(-1*zjets_datanorm)
		zjets.Add(zjetsFakes)
	else:
		zjetsFakes = dataEmb_ntuple_file.Get(fakechannel+"/"+datavar).Clone()
		zjetsMCFakes = zjets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy1jetsFakes = dy1jets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy2jetsFakes = dy2jets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy3jetsFakes = dy3jets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy4jetsFakes = dy4jets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy1jetsFakes.Scale(dy1jets_datanorm)
		dy2jetsFakes.Scale(dy2jets_datanorm)
		dy3jetsFakes.Scale(dy3jets_datanorm)
		dy4jetsFakes.Scale(dy4jets_datanorm)
		zjetsMCFakes.Scale(zjets_datanorm)
		dyjetsFakes = dy1jetsFakes.Clone()
		dyjetsFakes.Add(dy2jetsFakes)
		dyjetsFakes.Add(dy3jetsFakes)
		dyjetsFakes.Add(dy4jetsFakes)
		dyjetsFakes.Add(zjetsMCFakes)
		if DYShape == True:
			zjetsFakes = dyjetsFakes.Clone()
		else:
			if zjetsFakes.Integral() != 0:
				zjetsFakes.Scale(-1*dyjetsFakes.Integral()/zjetsFakes.Integral())
		print "GET BINERROR TEST:"
		for i in range(1,wjets.GetNbinsX()+1):
			if wjets.GetBinError(i) > 3.0:
				print "fakes error before: " + str(wjets.GetBinError(i))
			if zjetsFakes.GetBinError(i) > 3.0:
				print "zjetsfakes error before: " + str(zjetsFakes.GetBinError(i))
		wjets.Add(zjetsFakes)
		print "fakes2:"+str(wjets.Integral())
		for i in range(1,wjets.GetNbinsX()+1):
			if wjets.GetBinError(i) > 3.0:
				print "fakes error after: " + str(wjets.GetBinError(i))
		dy1otherFakes = dy1other_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy2otherFakes = dy2other_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy3otherFakes = dy3other_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy4otherFakes = dy4other_ntuple_file.Get(fakechannel+"/"+var).Clone()
		zjetsotherMCFakes = zjetsotherMC_ntuple_file.Get(fakechannel+"/"+var).Clone()
		dy1otherFakes.Scale(dy1jets_datanorm)
		dy2otherFakes.Scale(dy2jets_datanorm)
		dy3otherFakes.Scale(dy3jets_datanorm)
		dy4otherFakes.Scale(dy4jets_datanorm)
		zjetsotherMCFakes.Scale(zjets_datanorm)
		zjetsotherFakes = dy1otherFakes.Clone()
		zjetsotherFakes.Add(dy2otherFakes)
		zjetsotherFakes.Add(dy3otherFakes)
		zjetsotherFakes.Add(dy4otherFakes)
		zjetsotherFakes.Add(zjetsotherMCFakes)
		zjetsotherFakes.Scale(-1)
		if shape_norm == False:
			zjetsother.Add(zjetsotherFakes)
		
	#print zjetsFakes.Integral()
	ttbar_full_fakes = ttbar_full_ntuple_file.Get(fakechannel+"/"+var).Clone()
	ttbar_semi_fakes = ttbar_semi_ntuple_file.Get(fakechannel+"/"+var).Clone()
	
	ttbar_full_fakes.Scale(-1*ttbar_full_datanorm)
	ttbar_semi_fakes.Scale(-1*ttbar_semi_datanorm)
	#print "ttbar fake integral"
	#print ttbar_full_fakes.Integral()
	#print ttbar_semi_fakes.Integral()
	ttbar.Add(ttbar_full_fakes)
	ttbar.Add(ttbar_semi_fakes)
	#wjets.Add(ttbar_full_fakes)
	#wjets.Add(ttbar_semi_fakes)
if shape_norm == True:
	wjets.Scale(1/wjets.Integral())
	ttbar.Scale(1/ttbar.Integral())
	zjetsother.Scale(1/zjetsother.Integral())
wjets.Rebin(binwidth)
zjets.Rebin(binwidth)
zjetsother.Rebin(binwidth)
ttbar.Rebin(binwidth)
ttbar_full.Rebin(binwidth)
ttbar_semi.Rebin(binwidth)
ww.Rebin(binwidth)
if extraBackground == True:
	wwfull.Rebin(binwidth)
	wz.Rebin(binwidth)
	zz.Rebin(binwidth)
	vhsm.Rebin(binwidth)
	vhlfv.Rebin(binwidth)
	hwwvhtth.Rebin(binwidth)
singlet.Rebin(binwidth)
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hvbfsm.Rebin(binwidth)
hggsm.Rebin(binwidth)
hvbfww.Rebin(binwidth)
hggww.Rebin(binwidth)
data.Rebin(binwidth)
if zjetsEmbed == False:
	zjetsother = zjets.Clone()
	zjetsother.Scale(0)

if systematics == True:
	if fakeRate == True:
        	#fakesLow = data_ntuple_file.Get(fakechannel+"down/"+var).Clone()
		#fakesLow.Add(zjetsFakes)
        	#fakesHigh = data_ntuple_file.Get(fakechannel+"up/"+var).Clone()
		#fakesHigh.Add(zjetsFakes)
		fakesLow = data_ntuple_file.Get(fakechannel+"/"+datavar).Clone()
		fakesLow.Add(zjetsFakes)
		fakesLow.Scale(0.8)
		fakesHigh = data_ntuple_file.Get(fakechannel+"/"+datavar).Clone()
		fakesHigh.Add(zjetsFakes)
		fakesHigh.Scale(1.2)
        	fakesLow.Rebin(binwidth)
        	fakesHigh.Rebin(binwidth)
	size = wjets.GetNbinsX()
	xUncert = array.array('f',[])
	yUncert = array.array('f',[])
	yFakesNoStack = array.array('f',[])
	exlUncert = array.array('f',[])
	exhUncert = array.array('f',[])
	eylUncert = array.array('f',[])
	eyhUncert = array.array('f',[])
	binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)
	#print binwidth
	#print "binLength" + str(binLength)
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0 or wjets.GetBinContent(i) == 0:
			if fakeRate == True:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)
				#if i == 1:
					#print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"
					#print stackBinContent
			else:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)+qcd.GetBinContent(i)
			wjetsBinContent = wjets.GetBinContent(i)
			xUncert.append(wjets.GetBinCenter(i))
			yUncert.append(stackBinContent)
			yFakesNoStack.append(wjetsBinContent)
			#exlUncert.append(wjets.GetBinCenter(i)-binLength/2)
			#exhUncert.append(wjets.GetBinCenter(i)+binLength/2)
			exlUncert.append(binLength/2)
			exhUncert.append(binLength/2)
			#exlUncert.append(0)
			#exhUncert.append(0)
			#eylUncert.append(wjets.GetBinContent(i)-fakesLow.GetBinContent(i))
			if fakeRate == True:
                        	eylUncert.append(wjetsBinContent-fakesLow.GetBinContent(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i))
			#	eyhUncert.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
                        	eyhUncert.append(fakesHigh.GetBinContent(i) +zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i) + singlet.GetBinError(i) - wjetsBinContent)
				#if i == 1:
					#print eylUncert
					#print eyhUncert
			else:
                                eylUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+ singlet.GetBinError(i) +qcd.GetBinError(i))
                                #print wjets.GetBinContent(i)
                        #       eyhUncert.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
                                eyhUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i)+ qcd.GetBinError(i))
	xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
	yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
	yFakesNoStackVec = ROOT.TVectorF(len(yFakesNoStack),yFakesNoStack)
	exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
	exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
	eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
	eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)	
	systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)
	fakeErrorsNoStack =  ROOT.TGraphAsymmErrors(xUncertVec,yFakesNoStackVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)


outfile_name = savedir+"LFV"+"_"+channel+"_"+var
if fakeRate == True:
	outfile_name = outfile_name + "_fakeRate"
if zjetsEmbed == True:
	outfile_name = outfile_name +"_zjetsEmbed"
if DYShape == True:
	outfile_name = outfile_name +"_dyshape"
if new_signal == True:
	outfile_name = outfile_name +"_newSignal"
if logScale == True:
	outfile_name = outfile_name +"_log"
if "jesnone" in savedir:
	outfile_name = outfile_name + "_jesnone"
elif "jesminus" in savedir:
	outfile_name = outfile_name + "_jesminus"
elif "jesplus" in savedir:
	outfile_name = outfile_name + "_jesplus"
outfile_name = outfile_name+"_singletfix"

##create root file with yields for datacards
outfile = ROOT.TFile(outfile_name+".root","RECREATE")
outfile.mkdir("vbfmutau")
outfile.cd("vbfmutau/")
if fakeRate == False:
	qcd.Write("qcd")
	wjets.Write("wjets")
else:
	wjets.Write("fakes")
	if systematics == True:
		fakeErrorsNoStack.Write("fake rate error graph")
if zjetsEmbed == False:
	zjets.Write("zjets")
else:
	zjets.Write("ztautau")
	zjetsother.Write("zjetsother")
#	if "gg0" in channel or "gg1" in channel:
#		dyother.Write("zplusotherjets")

ttbar.Write("ttbar")
ttbar_semi.Write("ttbarsemi")
ttbar_full.Write("ttbarfull")
ww.Write("ww")
singlet.Write("singlet")
data.Write("data_obs")
hvbflfvScaled = hvbflfv.Clone()
hvbflfvScaled.Scale(0.1)
hgglfvScaled = hgglfv.Clone()
hgglfvScaled.Scale(0.1)
hvbflfvScaled.Write("LFVVBF126")
hgglfvScaled.Write("LFVGG126")
hvbfsm.Write("SMVBF126")
hggsm.Write("SMGG126")
hvbfww.Write("WWVBF126")
hggww.Write("WWGG126")
hvbflfvScaled.Write("LFVVBF")
hgglfvScaled.Write("LFVGG")
hvbfsm.Write("SMVBF")
hggsm.Write("SMGG")
hvbfww.Write("WWVBF")
hggww.Write("WWGG")
if extraBackground == True:
	wz.Write("WZ")
	zz.Write("ZZ")
	vhsm.Write("VHSM")
	vhlfv.Write("VHLFV")
	hwwvhtth.Write("HWWVHTTH")
outfile.Write()
if (presel == True or plotData ==False) and ( channel == "vbf" and plotSave == True and shape_norm == False):
        hgglfv.Scale(10)
        hvbflfv.Scale(10)
	#print "test"
if prelimColors == True:
	hgglfv.SetLineColor(ROOT.EColor.kBlue+2)
	hvbflfv.SetLineColor(ROOT.EColor.kRed+1)
	hvbfsm.SetLineColor(ROOT.EColor.kGreen+8)
	hggsm.SetLineColor(ROOT.EColor.kOrange+5)
	wjets.SetFillColor(ROOT.EColor.kPink-4)
	zjets.SetFillColor(ROOT.EColor.kGreen+4)
	zjetsother.SetFillColor(ROOT.EColor.kAzure+3)
	ttbar.SetFillColor(ROOT.EColor.kCyan-2)
	ttbar_full.SetFillColor(ROOT.EColor.kGreen+3)
	ttbar_semi.SetFillColor(ROOT.EColor.kCyan-6)
	ww.SetFillColor(ROOT.EColor.kCyan)
	singlet.SetFillColor(ROOT.EColor.kMagenta-3)
else:
        hgglfv.SetLineColor(ROOT.EColor.kBlue)
        hvbflfv.SetLineColor(ROOT.EColor.kRed)
        hvbfsm.SetLineColor(ROOT.EColor.kMagenta)
	hggsm.SetLineColor(ROOT.EColor.kMagenta)
        hvbfww.SetLineColor(ROOT.EColor.kOrange+3)
        hggww.SetLineColor(ROOT.EColor.kOrange+3)
        wjets.SetFillColor(ROOT.EColor.kMagenta-10)
	wjets.SetLineColor(ROOT.EColor.kMagenta+4)
	wjets.SetLineWidth(1)
        zjets.SetFillColor(ROOT.EColor.kOrange-4)
	zjets.SetLineColor(ROOT.EColor.kOrange+4)
	zjets.SetLineWidth(1)
	zjetsother.SetFillColor(ROOT.EColor.kAzure+3)
	zjetsother.SetLineColor(ROOT.EColor.kAzure+4)
	zjetsother.SetLineWidth(1)
        ttbar.SetFillColor(40)
	ttbar.SetLineColor(ROOT.EColor.kBlack)
	ttbar.SetLineWidth(1)
        ttbar_full.SetFillColor(ROOT.EColor.kGreen+3)
        ttbar_semi.SetFillColor(ROOT.EColor.kCyan-6)
        ww.SetFillColor(ROOT.EColor.kRed+2)
	ww.SetLineColor(ROOT.EColor.kRed+4)
	ww.SetLineWidth(1)
	singlet.SetFillColor(ROOT.EColor.kGreen-2)
	singlet.SetLineColor(ROOT.EColor.kGreen+4)
	singlet.SetLineWidth(1)
if fakeRate == False:
	qcd.SetFillColor(ROOT.EColor.kCyan)
	qcd.SetLineColor(ROOT.EColor.kBlue+4)
	qcd.SetLineWidth(1)
	qcd.SetMarkerSize(0)
wjets.SetMarkerSize(0)
zjets.SetMarkerSize(0)
zjetsother.SetMarkerSize(0)
ttbar.SetMarkerSize(0)
ttbar_full.SetMarkerSize(0)
ttbar_semi.SetMarkerSize(0)
ww.SetMarkerSize(0)
singlet.SetMarkerSize(0)
hgglfv.SetMarkerSize(0)
hvbflfv.SetMarkerSize(0)
hvbfsm.SetMarkerSize(0)
hggsm.SetMarkerSize(0)
hvbfww.SetMarkerSize(0)
hggww.SetMarkerSize(0)
hgglfv.SetLineWidth(3)
hvbflfv.SetLineWidth(3)
hvbflfv.SetLineStyle(ROOT.kDashed)
hvbfsm.SetLineWidth(3)
hvbfsm.SetLineStyle(ROOT.kDashed)
hggsm.SetLineWidth(3)
hvbfww.SetLineWidth(3)
hvbfww.SetLineStyle(ROOT.kDashed)
hggww.SetLineWidth(3)
data.SetMarkerSize(1)
#if zjetsEmbed == True and ("gg0" in channel or "gg1" in channel):
#	dyother.SetMarkerSize(0)
#	dyother.SetFillColor(ROOT.EColor.kSpring+1)
#	dyother.Rebin(binwidth)
#	legend.AddEntry(dyother,'Z+jets (other)')
#print presel
#print channel
#print plotSave
#print shape_norm
if shape_norm == False and (presel == True or (presel==False and blind == True)):
        if plotData == True:
                data.Draw("sames,E1")
LFVStack.Add(wjets)
LFVStack.Add(ww)
if seperateSemiFull == False:
	LFVStack.Add(ttbar)
else:
	LFVStack.Add(ttbar_full)
	LFVStack.Add(ttbar_semi)

LFVStack.Add(singlet)
if zjetsEmbed == False:
	LFVStack.Add(zjets)
else:
	LFVStack.Add(zjetsother)
	LFVStack.Add(zjets)
if fakeRate == False:
	legend.AddEntry(qcd,'QCD',"f")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
if fakeRate == False:
	LFVStack.Add(qcd)
maxLFVStack = LFVStack.GetMaximum()
maxhgglfv=hgglfv.GetMaximum()
maxhvbflfv=hvbflfv.GetMaximum()
maxhvbfsm = hvbfsm.GetMaximum()
maxhggsm = hggsm.GetMaximum()
maxhvbfww = hvbfww.GetMaximum()
maxhggww = hggww.GetMaximum()
maxdata = data.GetMaximum()
#print maxhvbflfv
maxHist = max(maxLFVStack,maxhgglfv,maxhvbflfv,maxhvbfsm,maxhggsm,maxhvbfww,maxhggww,maxdata)
#print ":((((((((((((((((((((("
#print maxdata
#maxHist = max(maxLFVStack,maxhgglfv,maxhvbflfv,maxhvbfsm,maxdata)
#print maxHist
if var == "vbfj1eta" or var == "vbfj2eta":
	maxHist = maxHist*1.40/1.20
LFVStack.SetMaximum(maxHist*1.20)
#print LFVStack.GetMaximum()
hsm = hvbfsm.Clone()
hsm.Add(hggsm)
hsm.Add(hvbfww)
hsm.Add(hggww)
hsm.SetFillColor(ROOT.EColor.kMagenta)
hsm.SetLineColor(ROOT.EColor.kMagenta)
hsm.SetLineWidth(1)
LFVStack.Add(hsm)
LFVStack.Draw('hist')
#if shape_norm == False and (presel == True or (presel==False and blind == True)):
if shape_norm == False and plotData == True:
	data.Draw("sames,E1")
if xRange != 0:
        #print xRange
        #print ":KFJFKJFJFKJ:"
        LFVStack.GetXaxis().SetRangeUser(0,xRange)
hgglfv.Scale(0.1)
hvbflfv.Scale(0.1)
hgglfv.Draw('sameshist')
hvbflfv.Draw('sameshist')
#hvbfsm.Draw('sameshist')
#hggsm.Draw('sameshist')
#hvbfww.Draw('sameshist')
#hggww.Draw('sameshist')
if shape_norm == False and plotData == True:
	legend.AddEntry(data,'Observed',"p")
if systematics == True:
	systErrors.SetFillStyle(3001)
        systErrors.SetFillColor(ROOT.EColor.kGray+3)
        systErrors.SetMarkerSize(0)
        systErrors.Draw('sames,E2')
	legend.AddEntry(systErrors,'Bkg. Uncertainty')
legend.AddEntry(hsm,'SM Higgs')
if fakeRate == False:
        legend.AddEntry(wjets,'W+Jets','f')
else:
        legend.AddEntry(wjets, 'Fake(jet#rightarrow#tau)','f')
if zjetsEmbed == False:
        legend.AddEntry(zjets,'Z+Jets')
else:
        legend.AddEntry(zjets, 'Z#rightarrow#tau#tau (embedded)','f')
        legend.AddEntry(zjetsother, 'Z#rightarrowl^{+}l^{-}','f')
legend.AddEntry(singlet,'Single Top',"f")
if seperateSemiFull == False:
        legend.AddEntry(ttbar,'t#bar{t}')
else:
        legend.AddEntry(ttbar_full, 'TT Fully Leptonic')
        legend.AddEntry(ttbar_semi, 'TT Semi Leptonic')
legend.AddEntry(ww,'EWK Di-Boson',"f")
if (channel == "vbf" or channel == "ztautaucontrolvbf") and plotSave == True and shape_norm == False and ( presel == True or plotData == False):
        legend.AddEntry(hgglfv,'GG LFV Higgs BR=1.0')
        legend.AddEntry(hvbflfv, 'VBF LFV Higgs BR=1.0')
else:
        legend.AddEntry(hgglfv,'LFV GG Higgs')
        legend.AddEntry(hvbflfv, 'LFV VBF Higgs')
#legend.AddEntry(hggsm, 'SM GGF H#rightarrow#mu#tau')
#legend.AddEntry(hvbfsm, 'SM VBF H#rightarrow#mu#tau')
#legend.AddEntry(hggww, 'WW GGF H#rightarrow#mu#tau')
#legend.AddEntry(hvbfww, 'WW VBF H#rightarrow#mu#tau')
blind = False
if blind == True and shape_norm == False and plotData == True:
	binblindlow = data.FindBin(blindlow)
	binblindhigh = data.FindBin(blindhigh)
	#print binblindlow
	#print binblindhigh
	for x in range(binblindlow, binblindhigh+1):
		data.SetBinContent(x, -1000)
	pave = ROOT.TPave(blindlow,0,blindhigh,maxHist*1.25,4,"br")
	pave.SetFillColor(ROOT.kGray+1)
	pave.SetFillStyle(3003)
	pave.SetBorderSize(0)
	#pave.SetDrawOption(0)
	#pave.Draw('sameshist')
	#legend.AddEntry(pave,'Blinded')
if plotData == True:
	legend.SetTextSize(0.025)
else:
	legend.SetTextSize(0.024)
legend.Draw('sames')
LFVStack.GetXaxis().SetTitle(xlabel)
LFVStack.GetXaxis().SetNdivisions(510)
LFVStack.GetXaxis().SetTitleOffset(3.0)
LFVStack.GetXaxis().SetLabelOffset(3.0)
LFVStack.GetXaxis().SetLabelSize(0.035)
LFVStack.GetYaxis().SetTitle(ylabel)
LFVStack.GetYaxis().SetTitleOffset(1.40)
LFVStack.GetYaxis().SetLabelSize(0.035)

if var =="collMass_type1":
	LFVStack.GetYaxis().SetRangeUser(0,4.2)
#else:
	#if shape_norm == False:
#		LFVStack.GetYaxis().SetRangeUser(0,maxHist*1.05)
#	else:
#		LFVStack.GetYaxis().SetRangeUser(0,2)
#data.GetXaxis().SetTitle(xlabel)
#data.GetYaxis().SetTitleOffset(1.2)
#data.GetYaxis().SetRangeUser(0,maxHist*1.05)
#lumifb = '%.2f'%(lumi/1000)
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(31)
latexStr = "%.1f fb^{-1}, #sqrt{s} = 8 TeV"%(lumi/1000)
latex.DrawLatex(0.9,0.96,latexStr)
latex.SetTextAlign(11)
latex.DrawLatex(0.25,0.96,"CMS preliminary")
#title_str = "CMS Preliminary:  \sqrt{s} = 8 TeV   L = " + str(lumifb)+" fb^{-1}"
#titleText = ROOT.TPaveText(0.2,0.91,0.7,0.99,"brNDC")
#titleText.AddText(title_str)
#titleText.SetFillStyle(0)
#titleText.SetBorderSize(0)
#titleText.Draw('sames')
#print title_str
#signal to background ratio
maxbin = hvbflfv.GetMaximumBin()
if fakeRate == False:
	#sbratio =hvbflfv.GetBinContent(maxbin)/(ww.GetBinContent(maxbin)+wjets.GetBinContent(maxbin)+zjets.GetBinContent(maxbin)+ttbar.GetBinContent(maxbin)+qcd.GetBinContent(maxbin))
	sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+hggsm.GetBinContent(maxbin)+hvbfww.GetBinContent(maxbin)+hggww.GetBinContent(maxbin))
        #sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
else:
	#sbratio =hvbflfv.GetBinContent(maxbin)/(ww.GetBinContent(maxbin)+wjets.GetBinContent(maxbin)+zjets.GetBinContent(maxbin)+ttbar.GetBinContent(maxbin))
	sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+hggsm.GetBinContent(maxbin)+hvbfww.GetBinContent(maxbin)+hggww.GetBinContent(maxbin))
        #sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
print "Signal to Background Ratio: " + str(sbratio)
print (LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+hggsm.GetBinContent(maxbin))
print (LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
print hvbflfv.GetMaximum()
#p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.3)
#p_ratio.SetTopMargin(0.1)
#p_ratio.Draw()
if plotData==True:
	p_ratio.cd()
	ROOT.gROOT.LoadMacro("tdrstyle.C")
	ROOT.setTDRStyle()
	ratio = data.Clone()
	mc = wjets.Clone()
	mc.Add(zjets)
	if zjetsEmbed == True:
		mc.Add(zjetsother)
	mc.Add(ttbar)
	mc.Add(ww)
	mc.Add(singlet)
	if fakeRate == False:
		mc.Add(qcd)
	mc.Scale(-1)
	ratio.Add(mc)
	mc.Scale(-1)
	ratio.Divide(mc)
	ratio.Draw("E1")
	if xRange != 0:
		ratio.GetXaxis().SetRangeUser(0,xRange)
		lineOne = ROOT.TLine(0.0, 1.0, xRange +widthOfBin,1.0)
	else:
        	lineOne = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1.0, ratio.GetXaxis().GetXmax(),1.0)
	
        #lineOne.Draw('sames')
	if blind == True:
        	paveRatio = ROOT.TPave(blindlow,-1.0,blindhigh,1.0,4,"br")
        	paveRatio.SetFillColor(1)
        	paveRatio.SetFillStyle(3002)
        	paveRatio.SetBorderSize(0)
 	       	paveRatio.Draw('sameshist')

	size = wjets.GetNbinsX()
	xRatio = array.array('f',[])
	yRatio = array.array('f',[])
	exlRatio = array.array('f',[])
	exhRatio = array.array('f',[])
	eylRatio = array.array('f',[])
	eyhRatio = array.array('f',[])
	binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)
	print binwidth
	#print "binLength" + str(binLength)
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0:
			stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)
			if data.GetBinContent(i) != 0 and stackBinContent == 0:
				print "data but no MC!!"
				sys.exit(2)
			wjetsBinContent = wjets.GetBinContent(i)
			ratioBinContent = ratio.GetBinContent(i)
			xRatio.append(wjets.GetBinCenter(i))
			yRatio.append(0.0)
			exlRatio.append(binLength/2)
			exhRatio.append(binLength/2)
			if fakeRate == True and systematics == True:
				eylRatio.append(-(fakesLow.GetBinContent(i)-wjetsBinContent -zjets.GetBinError(i)-zjetsother.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)-singlet.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
                        	eyhRatio.append((fakesHigh.GetBinContent(i)-wjetsBinContent+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
			else:
                                eylRatio.append(-(-wjets.GetBinError(i) -zjets.GetBinError(i)-zjetsother.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)-singlet.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
                        	eyhRatio.append((wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))

			#print wjets.GetBinContent(i)
			#eyhFakes.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
	if systematics == True:
		#print "test error low" + str(zjets.GetBinError(2))
		#print zjets.GetBinErrorUp(2)
		#print xRatio
		#print yRatio
		#print exlRatio
		#print exhRatio
		#print eylRatio
		#print eyhRatio
		xRatioVec = ROOT.TVectorF(len(xRatio),xRatio)
		yRatioVec = ROOT.TVectorF(len(yRatio),yRatio)
		exlRatioVec = ROOT.TVectorF(len(exlRatio),exlRatio)
		exhRatioVec = ROOT.TVectorF(len(exhRatio),exhRatio)
		eylRatioVec = ROOT.TVectorF(len(eylRatio),eylRatio)
		eyhRatioVec = ROOT.TVectorF(len(eyhRatio),eyhRatio)	
		ratioErrors = ROOT.TGraphAsymmErrors(xRatioVec,yRatioVec,exlRatioVec,exhRatioVec,eylRatioVec,eyhRatioVec)
		ratioErrors.SetFillStyle(3002)
        	ratioErrors.Draw('sames,E2')
		ratioErrors.SetFillColor(ROOT.EColor.kGray+3)
	ratio.GetXaxis().SetTitle(xlabel)
	ratio.GetXaxis().SetTitleSize(0.12)
	ratio.GetXaxis().SetNdivisions(510)
	ratio.GetXaxis().SetTitleOffset(1.1)
	ratio.GetXaxis().SetLabelSize(0.12)
	ratio.GetXaxis().SetLabelFont(42)
	#ratio.GetXaxis().SetTitleFont(42)
	ratio.GetYaxis().SetNdivisions(505)
	ratio.GetYaxis().SetLabelFont(42)
	ratio.GetYaxis().SetLabelSize(0.1)
	ratio.GetYaxis().SetRangeUser(-1,1)
	#ratio.GetXaxis().SetLabelSize(0.1)
	#ratio.GetXaxis().SetLabelFont(42)
	ratio.GetYaxis().SetTitle("#frac{Data-Predicted}{Predicted}")
	ratio.GetYaxis().CenterTitle(1)
	ratio.GetYaxis().SetTitleOffset(0.4)
	ratio.GetYaxis().SetTitleSize(0.12)
	ratio.SetTitle("")
	#ratioText = ROOT.TPaveText(0.2,0.91,0.7,0.99,"brNDC")
	#ratioText.AddText("Data MC Ratio")
	#ratioText.SetFillStyle(0)
	#ratioText.Draw('sames')
if seperateSemiFull:
	outfile_name = outfile_name+"_semifull"
if shape_norm == False:
	canvas.SaveAs(outfile_name+".png")
else:
	canvas.SaveAs(outfile_name+"_shape.png")
if shape_norm == False and fakeRate == False and zjetsEmbed == True and new_signal == True and systematics == True and plotData == False and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "mPt":
		canvas.SaveAs(savedir+"muhad_VBF_muPt_After_Presel.pdf")
	elif var == "tPt":
		canvas.SaveAs(savedir+"muhad_VBF_tauPt_After_Presel.pdf")
	elif var == "tMtToPfMet_Ty1":
		canvas.SaveAs(savedir+"muhad_VBF_MT_After_Presel.pdf")
	elif var == "tPhiMETPhiType1":
		canvas.SaveAs(savedir+"muhad_VBF_dPhi_tau_met_After_Presel.pdf")
	elif var == "mPhiMETPhiType1":
		canvas.SaveAs(savedir+"muhad_VBF_dPhi_mu_met_After_Presel.pdf")
	elif var == "collMass_type1":
		canvas.SaveAs(savedir+"muhad_VBF_m_colinear_After_Presel.pdf")
        elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_dEta_jj_After_Presel.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_Mjj_After_Presel.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet1eta_After_Presel.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet2eta_After_Presel.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet1pt_After_Presel.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet2pt_After_Presel.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1" and blind == True:
		canvas.SaveAs(savedir+"muhad_VBF_m_colinear_After_Presel_WITHDATA.pdf")
        elif var == "mPt":
                canvas.SaveAs(savedir+"muhad_VBF_muPt_After_Presel_WITHDATA.pdf")
        elif var == "tPt":
                canvas.SaveAs(savedir+"muhad_VBF_tauPt_After_Presel_WITHDATA.pdf")
        elif var == "tMtToPfMet_Ty1":
                canvas.SaveAs(savedir+"muhad_VBF_MT_After_Presel_WITHDATA.pdf")
        elif var == "tPhiMETPhiType1":
                canvas.SaveAs(savedir+"muhad_VBF_dPhi_tau_met_After_Presel_WITHDATA.pdf")
        elif var == "mPhiMETPhiType1":
                canvas.SaveAs(savedir+"muhad_VBF_dPhi_mu_met_After_Presel_WITHDATA.pdf")
        elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_dEta_jj_After_Presel_WITHDATA.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_Mjj_After_Presel_WITHDATA.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet1eta_After_Presel_WITHDATA.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet2eta_After_Presel_WITHDATA.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet1pt_After_Presel_WITHDATA.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet2pt_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="gg1" and presel == True and DYShape == False and plotSave == True:
        if var == "collMass_type1" and blind == True:
                canvas.SaveAs(savedir+"muhad_Boost_m_colinear_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="gg0" and presel == True and DYShape == False and plotSave == True:
        if var == "collMass_type1" and blind == True:
                canvas.SaveAs(savedir+"muhad_GG_m_colinear_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="ztautaucontrolvbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1":
		canvas.SaveAs(savedir+"muhad_VBF_ztautau_control.pdf")
	elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_dEta_jj.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_Mjj.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet1eta.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet2eta.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet1pt.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet2pt.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == False and channel =="vbf" and presel == False and DYShape == False and plotSave == True and blind == False:
	if var == "collMass_type1":
		canvas.SaveAs(savedir + "muhad_VBF_m_colinear_After_Allsel.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="vbf" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_VBF_m_colinear_After_allsel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="gg1" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_Boost_m_colinear_After_Allsel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == True and plotData == True and channel =="gg0" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_GG_m_colinear_After_Allsel_WITHDATA.pdf")

if shape_norm == True and fakeRate == True and zjetsEmbed == True and new_signal == True and systematics == False and plotData == False and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1":
		canvas.SaveAs(savedir+"m_colinear_muhad_VBF_After_Presel_Shape.pdf")
if fakeRate == False:
	print "QCD Integral: " + str(qcd.Integral())
	print "W+jets Integral: " + str(wjets.Integral())
        print "Wplus1Jets Integral: " + str(wjets1.Integral())
        print "Wplus2Jets Integral: " + str(wjets2.Integral())
        print "Wplus3Jets Integral: " + str(wjets3.Integral())
        print "Wplus4Jets Integral: " + str(wjets4.Integral())
	print "WplusJetsFiltered Integral: " + str(wjetsFiltered.Integral())

else:
	print "Fakes Integral: " + str(wjets.Integral())
	if systematics == True:
		print "Fakes Low Integral: " + str(fakesLow.Integral())
		print "Fakes High Integral: " + str(fakesHigh.Integral())
		print "(high-central)/central: " + str((fakesHigh.Integral() - wjets.Integral())/wjets.Integral())
		print "(central-low)/central: " + str((wjets.Integral() - fakesLow.Integral())/wjets.Integral())
lowbound = 100
highbound = 150

wwYield = yieldHisto(ww,lowbound,highbound)
wwbinmin = ww.FindBin(lowbound)
wwbinwidth = ww.GetBinWidth(wwbinmin)
wwbinmax = highbound/binwidth
wwsignal = ww.Integral(wwbinmin,wwbinmax)
print "ww: " + str(wwsignal)
if extraBackground == True:
	wwfullYield = yieldHisto(wwfull,lowbound,highbound)
	wwfullbinmin = wwfull.FindBin(lowbound)
	wwfullbinwidth = wwfull.GetBinWidth(wwfullbinmin)
	wwfullbinmax = highbound/binwidth
	wwfullsignal = wwfull.Integral(wwfullbinmin,wwfullbinmax)
	print "ww full: " + str(wwfullsignal)
	wzYield = yieldHisto(wz,lowbound,highbound)
	wzbinmin = wz.FindBin(lowbound)
	wzbinwidth = wz.GetBinWidth(wzbinmin)
	wzbinmax = highbound/binwidth
	wzsignal = wz.Integral(wzbinmin,wzbinmax)
	print "wz: " + str(wzsignal)
	zzYield = yieldHisto(zz,lowbound,highbound)
	zzbinmin = zz.FindBin(lowbound)
	zzbinwidth = zz.GetBinWidth(zzbinmin)
	zzbinmax = highbound/binwidth
	zzsignal = zz.Integral(zzbinmin,zzbinmax)
	print "zz: " + str(zzsignal)
	vhsmYield = yieldHisto(vhsm,lowbound,highbound)
	vhsmbinmin = vhsm.FindBin(lowbound)
	vhsmbinwidth = vhsm.GetBinWidth(vhsmbinmin)
	vhsmbinmax = highbound/binwidth
	vhsmsignal = vhsm.Integral(vhsmbinmin,vhsmbinmax)
	print "vhsm: "+ str(vhsmsignal)
	vhlfvYield = yieldHisto(vhlfv,lowbound,highbound)
	vhlfvbinmin = vhlfv.FindBin(lowbound)
	vhlfvbinwidth = vhlfv.GetBinWidth(vhlfvbinmin)
	vhlfvbinmax = highbound/binwidth
	vhlfvsignal = vhlfv.Integral(vhlfvbinmin,vhlfvbinmax)
	print "vhlfv: "+ str(vhlfvsignal)



#print "Background:"+str(zjets.Integral(zjets.FindBin(lowbound),zjets.FindBin(highbound)) +zjetsother.Integral(zjetsother.FindBin(lowbound),zjetsother.FindBin(highbound))+ttbar.Integral(ttbar.FindBin(lowbound),ttbar.FindBin(highbound)) + ww.Integral(ww.FindBin(lowbound),ww.FindBin(highbound)) + hvbfsm.Integral(hvbfsm.FindBin(lowbound),hvbfsm.FindBin(highbound)) + hggsm.Integral(hggsm.FindBin(lowbound),hggsm.FindBin(highbound))+ wjets.Integral(wjets.FindBin(lowbound),wjets.FindBin(highbound)))
#print "Background:"+str(zjets.Integral(zjets.FindBin(lowbound),zjets.FindBin(highbound)) + ttbar.Integral(ttbar.FindBin(lowbound),ttbar.FindBin(highbound)) + ww.Integral(ww.FindBin(lowbound),ww.FindBin(highbound))+ singlet.Integral(singlet.FindBin(lowbound),singlet.FindBin(highbound)) + hvbfsm.Integral(hvbfsm.FindBin(lowbound),hvbfsm.FindBin(highbound)) + wjets.Integral(wjets.FindBin(lowbound),wjets.FindBin(highbound)))
#print "Signal:" + str(hvbflfv.Integral(hvbflfv.FindBin(lowbound),hvbflfv.FindBin(highbound))+hgglfv.Integral(hgglfv.FindBin(lowbound),hgglfv.FindBin(highbound)))
print "Background:"+str(zjets.GetBinContent(2) +zjetsother.GetBinContent(2)+ttbar.GetBinContent(2) + ww.GetBinContent(2) + hvbfsm.GetBinContent(2) + hggsm.GetBinContent(2)+ wjets.GetBinContent(2))
print "Signal:" + str(hvbflfv.GetBinContent(2)+hgglfv.GetBinContent(2))
print "Z+jets Integral: " + str(zjets.Integral())
print "Z+jets (other) Integral: " + str(zjetsother.Integral())
#if zjetsEmbed == True and ("gg0" in channel or "gg1" in channel):
#	print "Z+other Integral: " + str(dyother.Integral())
print "TTbar Integral: " + str(ttbar.Integral())
print "TTbar Full Integral: " + str(ttbar_full.Integral())
print "TTbar Semi Integral: " + str(ttbar_semi.Integral())
print "WW Integral: " + str(ww.Integral())
print "Single Top Integral: " + str(singlet.Integral())
print "T channel Integral: " + str(tt.Integral())
print "Tbar-t channel Integral: " + str(tbart.Integral()) 
print "T W channel Integral: " + str(tw.Integral())
print "Tbar W channel Integral: " + str(tbarw.Integral())
print "SM VBF Integral: " + str(hvbfsm.Integral())
print "SM GG Integral: " + str(hggsm.Integral())
print "LFV VBF Integral: " + str(hvbflfv.Integral())
print "LFV GG Integral: " + str(hgglfv.Integral())
print "Z+jets MC Integral: " + str(zjetsMC.Integral())
print "DY 1 Integral: " + str(dy1jets.Integral())
print "DY 2 Integral: " + str(dy2jets.Integral())
print "DY 3 Integral: " + str(dy3jets.Integral())
print "DY 4 Integral: " + str(dy4jets.Integral())
print "Zjets Fakes Integral: " + str(zjetsFakes.Integral())
print "Z+jets Entries: " + str(zjets.GetEntries())
print "TTbar Entries: " + str(ttbar.GetEntries())
print "TTbar Full Entries: " + str(ttbar_full.GetEntries())
print "TTbar Semi Entries: " + str(ttbar_semi.GetEntries())
print "WW Entries: " + str(ww.GetEntries())
print "Single Top Entries: " + str(singlet.GetEntries())
print "data Entries: " + str(data.GetEntries())
print "wjets Entires: " + str(wjets.GetEntries())
print "data scale factor = " + str(data.Integral()/data.GetEffectiveEntries())
if fakeRate == True:
	print "fakes scale factor = " + str(wjets.Integral()/data.GetEffectiveEntries())
if zjetsEmbed == True:
	print "z tau tau scale factor = " + str (zjets.Integral()/zjets.GetEffectiveEntries())
	print "z jets other scale factor = " + str(zjetsother.Integral()/zjetsother.GetEffectiveEntries())
print "ttbar scale factor = " + str (ttbar.Integral()/ttbar.GetEffectiveEntries())
print "ww scale factor = " + str (ww.Integral()/ww.GetEffectiveEntries())
print "singlet scale factor = " + str(singlet.Integral()/singlet.GetEffectiveEntries())
print "LFV VBF scale factor = " + str(hvbflfv.Integral()*0.1/hvbflfv.GetEffectiveEntries())
print "LFV GG scale factor = " + str(hgglfv.Integral()*0.1/hgglfv.GetEffectiveEntries())
print "SM GG scale factor = " + str (hggsm.Integral()*0.1/hggsm.GetEffectiveEntries())
print "SM VBF scale factor = " + str(hvbfsm.Integral()*0.1/hvbfsm.GetEffectiveEntries())
if hggww.GetEffectiveEntries() == 0:
	print "WW HGG scale factor = " + str(hggww_norm)
else:
	print "WW HGG scale factor = " + str (hggww.Integral()/hggww.GetEffectiveEntries())
print "WW HVBF scale factor = " + str(hvbfww.Integral()/hvbfww.GetEffectiveEntries())
print "WW HVBF test = " + str(lumi/hvbfww_efflumi)
if extraBackground == True:
	print "WZ scale factor = " + str(lumi/wz_efflumi)
	print "ZZ scale factor = " + str(lumi/zz_efflumi)
	print "VH SM scale factor = " + str(lumi/vhsm_efflumi)
	print "VH LFV scale factor = " + str(lumi/vhlfv_efflumi)
	print "HWWVHTTH scale factor = " + str(lumi/hwwvhtth_efflumi)
#print "WW HVBF norm = " +str(hvbfww_norm)
#print "WW HGG norm = " + str(hggww_norm)
#print "SM HVBF norm = " + str(0.1*hvbfsm_norm)
#print "SM HGG norm = " + str(0.1*hggsm_norm)
#print "LFV HVBF norm = " + str(0.1*hvbflfv_norm)
#print "LFV HGG norm = " + str(0.1*hgglfv_norm)
#print "singlet norm = " +str((tt_norm+tbart_norm+tw_norm+tbarw_norm/4))
#print "ww norm = " + str(ww_norm)
#print "ttbar norm = " + str((ttbar_full_norm+ttbar_semi_norm)/2)
#print "zjetsother norm = " + str((dy1jets_norm+dy2jets_norm+dy3jets_norm+dy4jets_norm/4))
#print "ztautau norm = " +str((dy1jets_norm+dy2jets_norm+dy3jets_norm+dy4jets_norm/4))
#print "fake norm = " + str(0.49)
print "ww entries: " + str(ww.GetEntries())
if extraBackground == True:
	print "ww full entries: " + str(wwfull.GetEntries())
wwYield = yieldHisto(ww,lowbound,highbound)
wwbinmin = ww.FindBin(lowbound)
wwbinwidth = ww.GetBinWidth(wwbinmin)
wwbinmax = highbound/binwidth
wwsignal = ww.Integral(wwbinmin,wwbinmax)
print "ww: " + str(wwsignal)
singletbinmin = singlet.FindBin(lowbound)
singletbinwidth = singlet.GetBinWidth(singletbinmin)
singletbinmax = highbound/binwidth
singletsignal = singlet.Integral(singletbinmin,singletbinmax)
print "singlet: " + str(singletsignal)

if extraBackground == True:
	wwfullYield = yieldHisto(wwfull,lowbound,highbound)
	wwfullbinmin = wwfull.FindBin(lowbound)
	wwfullbinwidth = wwfull.GetBinWidth(wwfullbinmin)
	wwfullbinmax = highbound/binwidth
	wwfullsignal = wwfull.Integral(wwfullbinmin,wwfullbinmax)
	print "ww full: " + str(wwfullsignal)
	wzYield = yieldHisto(wz,lowbound,highbound)
	wzbinmin = wz.FindBin(lowbound)
	wzbinwidth = wz.GetBinWidth(wzbinmin)
	wzbinmax = highbound/binwidth
	wzsignal = wz.Integral(wzbinmin,wzbinmax)
	print "wz: " + str(wzsignal)
	zzYield = yieldHisto(zz,lowbound,highbound)
	zzbinmin = zz.FindBin(lowbound)
	zzbinwidth = zz.GetBinWidth(zzbinmin)
	zzbinmax = highbound/binwidth
	zzsignal = zz.Integral(zzbinmin,zzbinmax)
	print "zz: " + str(zzsignal)
	vhsmYield = yieldHisto(vhsm,lowbound,highbound)
	vhsmbinmin = vhsm.FindBin(lowbound)
	vhsmbinwidth = vhsm.GetBinWidth(vhsmbinmin)
	vhsmbinmax = highbound/binwidth
	vhsmsignal = vhsm.Integral(vhsmbinmin,vhsmbinmax)
	print "vhtthsm: "+ str(vhsmsignal)
	vhlfvYield = yieldHisto(vhlfv,lowbound,highbound)
	vhlfvbinmin = vhlfv.FindBin(lowbound)
	vhlfvbinwidth = vhlfv.GetBinWidth(vhlfvbinmin)
	vhlfvbinmax = highbound/binwidth
	vhlfvsignal = vhlfv.Integral(vhlfvbinmin,vhlfvbinmax)
	print "vhtthlfv: "+ str(vhlfvsignal)
hggwwYield = yieldHisto(hggww,lowbound,highbound)
hggwwbinmin = hggww.FindBin(lowbound)
hggwwbinwidth = hggww.GetBinWidth(hggwwbinmin)
hggwwbinmax = highbound/binwidth
hggwwsignal = hggww.Integral(hggwwbinmin,hggwwbinmax)
print "hggww: "+ str(hggwwsignal)
if extraBackground == True:
	hwwvhtthYield = yieldHisto(hwwvhtth,lowbound,highbound)
	hwwvhtthbinmin = hwwvhtth.FindBin(lowbound)
	hwwvhtthbinwidth = hwwvhtth.GetBinWidth(hwwvhtthbinmin)
	hwwvhtthbinmax = highbound/binwidth
	hwwvhtthsignal = hwwvhtth.Integral(hwwvhtthbinmin,hwwvhtthbinmax)
	print "hwwvhtth: " +str(hwwvhtthsignal)
hvbfwwYield = yieldHisto(hvbfww,lowbound,highbound)
hvbfwwbinmin = hvbfww.FindBin(lowbound)
hvbfwwbinwidth = hvbfww.GetBinWidth(hvbfwwbinmin)
hvbfwwbinmax = highbound/binwidth
hvbfwwsignal = hvbfww.Integral(hvbfwwbinmin,hvbfwwbinmax)
print "hww vbf: " +str(hvbfwwsignal)
hggsmYield = yieldHisto(hggsm,lowbound,highbound)
hggsmbinmin = hggsm.FindBin(lowbound)
hggsmbinwidth = hggsm.GetBinWidth(hggsmbinmin)
hggsmbinmax = highbound/binwidth
hggsmsignal = hggsm.Integral(hggsmbinmin,hggsmbinmax)
print "h gg sm: " +str(hggsmsignal)
hvbfsmYield = yieldHisto(hvbfsm,lowbound,highbound)
hvbfsmbinmin = hvbfsm.FindBin(lowbound)
hvbfsmbinwidth = hvbfsm.GetBinWidth(hvbfsmbinmin)
hvbfsmbinmax = highbound/binwidth
hvbfsmsignal = hvbfsm.Integral(hvbfsmbinmin,hvbfsmbinmax)
print hvbfsmbinmin
print hvbfsmbinmax
print "h vbf sm: " +str(hvbfsmsignal)
hgglfvYield = yieldHisto(hgglfv,lowbound,highbound)
hgglfvbinmin = hgglfv.FindBin(lowbound)
hgglfvbinwidth = hgglfv.GetBinWidth(hgglfvbinmin)
hgglfvbinmax = highbound/binwidth
hgglfvsignal = hgglfv.Integral(hgglfvbinmin,hgglfvbinmax)
print "h gg lfv: " +str(hgglfvsignal)
hvbflfvYield = yieldHisto(hvbflfv,lowbound,highbound)
hvbflfvbinmin = hvbflfv.FindBin(lowbound)
hvbflfvbinwidth = hvbflfv.GetBinWidth(hvbflfvbinmin)
hvbflfvbinmax = highbound/binwidth
hvbflfvsignal = hvbflfv.Integral(hvbflfvbinmin,hvbflfvbinmax)
print hvbflfvbinmin
print hvbflfvbinmax
print "h vbf lfv: " +str(hvbflfvsignal)




if fakeRate == False:
	print "QCD Yield: " + str(yieldHisto(qcd,lowbound,highbound))
	print "W+jets Yield: " + str(yieldHisto(wjets,lowbound,highbound))
	print "Wplus1Jets Yield: " + str(yieldHisto(wjets1,lowbound,highbound))
	print "Wplus2Jets Yield: " + str(yieldHisto(wjets2,lowbound,highbound))
	print "Wplus3Jets Yield: " + str(yieldHisto(wjets3,lowbound,highbound))
	print "Wplus4Jets Yield: " + str(yieldHisto(wjets4,lowbound,highbound))
	print "WplusJetsFiltered Yield: " + str(yieldHisto(wjetsFiltered,lowbound,highbound))

else:
	print "Fakes Yield: " + str(yieldHisto(wjets,lowbound,highbound))
print "Data Yield: " + str(yieldHisto(data,lowbound,highbound))
if zjetsEmbed == True:
	print "ZTauTau Yield: " + str(yieldHisto(zjets,lowbound,highbound))
	print "Zjetsother Yield: " + str(yieldHisto(zjetsother,lowbound,highbound))
print "TTBar Yield: " + str(yieldHisto(ttbar,lowbound,highbound))
print "WW Yield: " + str(yieldHisto(ww,lowbound,highbound))
print "Singlet Yield: " + str(yieldHisto(singlet,lowbound,highbound))
print "LFV VBF Yield: " + str(yieldHisto(hvbflfv,lowbound,highbound))
print "LFV GG Yield: " + str(yieldHisto(hgglfv,lowbound,highbound))
print "SM GG Yield: " + str(yieldHisto(hggsm,lowbound,highbound))
print "WW HGG Yield: " +str(yieldHisto(hggww,lowbound,highbound))
print "WW HVBF Yield: " + str(yieldHisto(hvbfww,lowbound,highbound))
print "WW Full Yield: " + str(yieldHisto(wwfull,lowbound,highbound))
print "WZ Yield: " + str(yieldHisto(wz,lowbound,highbound))
print "ZZ Yield: " + str(yieldHisto(zz,lowbound,highbound))
print "VHSM Yield: " + str(yieldHisto(vhsm,lowbound,highbound))
print "VHLFV Yield: " + str(yieldHisto(vhlfv,lowbound,highbound))
print "HWWVHTTH Yield: " + str(yieldHisto(hwwvhtth,lowbound,highbound))
