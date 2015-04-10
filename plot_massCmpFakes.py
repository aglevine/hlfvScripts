from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import numpy

##get qcd normalization (choose selections for qcd)

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
ROOT.gStyle.SetOptStat(0)
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

ynormlabel = "Normalized to 1 "
if "jes" in predir:
	jes = True #jes up or down
else:
	jes = False
print "JJJJJJJEEEEEEEEESSSSSSSSSSS" + str(jes)
presel =  False #use preselection cuts or not
blind = True
if channel == "highMtssvbf":
	blind = False
systematics = True
fakeRate = False #apply fake rate method
zjetsEmbed = True #use embedded data samples for zjets
seperateSemiFull = False #seperate semi and fully leptonic ttbar
plotData=True
plotSave=True
prelimColors=False
new_signal=True
logScale=False

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

if "jes" in predir and not ("jes" in savedir):
	print "Error: jes mismatch"
	sys.exit()
if "jes" in savedir and not ("jes" in predir):
        print "Error: jes mismatch"
        sys.exit()
if "jes_minus" in var and not ("jesminus" in savedir) or "jes_plus" in var and not ("jesplus" in savedir):
	print "Error: jes doesn't match"
	sys.exit()
if var == "collMass_jes_minus" or var == "collMass_jes_plus":
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
tbarw_ntuple_file_str = 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
data_ntuple_file_str = 'data_2012.root'
#data_ntuple_file_str = 'jesplusdata_2012.root'
hvbfsm_ntuple_file_str = 'VBF_H2Tau_M-125.root'

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
	#if "gg0" in channel or "gg1" in channel:
	#	dy1other = dy1other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy2other = dy2other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy3other = dy3other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy4other = dy4other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#changed w+jets to datavar to save time when running jes (w+jets MC not used in data driving fake rate estimation)
wjets1 = wjets1_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
wjets2 = wjets2_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
wjets3 = wjets3_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
wjets4 = wjets4_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()
wjetsFiltered = wjetsFiltered_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_semi = ttbar_semi_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_full = ttbar_full_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ww = ww_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tt = tt_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tbart = tbart_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tw = tbarw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
tbarw = tw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
data = data_ntuple_file.Get(ntuple_spot+"/"+datavar).Clone()


if jes==False:
	lumidir = 'lumicalc_Jan17/'
else:
	lumidir = 'lumicalc_jes/'
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

if new_signal == True:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_Dec9.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_Dec9.lumicalc.sum'
else:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_H2Tau_M-126.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_H2Tau_M-126.lumicalc.sum'
hvbfsm_lumifile = lumidir + 'VBF_H2Tau_M-125.lumicalc.sum'
hggsm_lumifile = lumidir + 'GGH_H2Tau_M-125.lumicalc.sum'



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

f = open(dy3jets_lumifile).read().splitlines()
dy4jets_efflumi = float(f[0])

lumi = data1_lumi+data2_lumi+data3_lumi+data4_lumi
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





#get qcd normalization (non fake rate method)
qcd_norm = make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file, wjets1_datanorm, wjets2_datanorm, wjets3_datanorm, wjets4_datanorm, wjetsFiltered_datanorm, zjets_datanorm, ttbar_semi_datanorm, ttbar_full_datanorm, ww_datanorm)
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
dy1jets_norm = dy1jets_datanorm
dy2jets_norm = dy2jets_datanorm
dy3jets_norm = dy3jets_datanorm
dy4jets_norm = dy4jets_datanorm
hgglfv_norm = lumi/hgglfv_efflumi
hvbflfv_norm = lumi/hvbflfv_efflumi
hvbfsm_norm = lumi/hvbfsm_efflumi
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
	#print "???????????????"
	#print zjetsMC.Integral()
	if zjets.Integral() != 0:
		zjets.Scale(dyjets.Integral()/zjets.Integral())
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

ww.Scale(ww_norm)
hgglfv.Scale(hgglfv_norm)
hvbflfv.Scale(hvbflfv_norm)
hvbfsm.Scale(hvbfsm_norm)
hggsm.Scale(hggsm_norm)
xbinLength = data.GetBinWidth(1)
isGeV = varParams[5]
widthOfBin = binwidth*xbinLength
if isGeV:
	ylabel = ynormlabel + " Events / " + str(int(widthOfBin)) + " GeV"
else:
	ylabel = ynormlabel  + " Events / " + str(widthOfBin)

if channel == "highMtssvbf":
	fakechannel = "highMtssantiisotauvbf"
elif channel == "highMtssgg":
	fakechannel = "highMtssantiisotaugg"
elif channel == "ttbarcontrolvbf":
	fakechannel = "antiisotauvbf"
else:
	fakechannel = "antiisotau"+channel
fakes = data_ntuple_file.Get(fakechannel+"/"+datavar).Clone()
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
	if zjetsFakes.Integral() != 0:
		zjetsFakes.Scale(-1*dyjetsFakes.Integral()/zjetsFakes.Integral())
	print "GET BINERROR TEST:"
	for i in range(1,wjets.GetNbinsX()):
		if wjets.GetBinError(i) > 3.0:
			print "fakes error before: " + str(wjets.GetBinError(i))
		if zjetsFakes.GetBinError(i) > 3.0:
			print "zjetsfakes error before: " + str(zjetsFakes.GetBinError(i))
	fakes.Add(zjetsFakes)
	for i in range(1,wjets.GetNbinsX()):
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
	zjetsother.Add(zjetsotherFakes)
		
	
ttbar_full_fakes = ttbar_full_ntuple_file.Get(fakechannel+"/"+var).Clone()
ttbar_semi_fakes = ttbar_semi_ntuple_file.Get(fakechannel+"/"+var).Clone()

ttbar_full_fakes.Scale(-1*ttbar_full_datanorm)
ttbar_semi_fakes.Scale(-1*ttbar_semi_datanorm)
#print "ttbar fake integral"
#print ttbar_full_fakes.Integral()
#print ttbar_semi_fakes.Integral()
ttbar.Add(ttbar_full_fakes)
ttbar.Add(ttbar_semi_fakes)
wjets.Add(qcd)
wjets.Scale(1/wjets.Integral())
fakes.Scale(1/fakes.Integral())
ttbar.Scale(1/ttbar.Integral())
zjetsother.Scale(1/zjetsother.Integral())

	

	
fakesLow = fakes.Clone()
fakesLow.Scale(0.7)
fakesHigh = fakes.Clone()
fakesHigh.Scale(1.3)
fakesLow.Rebin(binwidth)
fakesHigh.Rebin(binwidth)
fakes.Rebin(binwidth)
wjets.Rebin(binwidth)
qcd.Rebin(binwidth)
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
		stackBinContent = fakes.GetBinContent(i)
		xUncert.append(wjets.GetBinCenter(i))
		yUncert.append(stackBinContent)
		exlUncert.append(binLength/2)
		exhUncert.append(binLength/2)
                eylUncert.append(stackBinContent-fakesLow.GetBinContent(i))
                eyhUncert.append(fakesHigh.GetBinContent(i)-stackBinContent)

xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)
systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)
	

zjets.Rebin(binwidth)
zjetsother.Rebin(binwidth)
ttbar.Rebin(binwidth)
ttbar_full.Rebin(binwidth)
ttbar_semi.Rebin(binwidth)
ww.Rebin(binwidth)
singlet.Rebin(binwidth)
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hvbfsm.Rebin(binwidth)
hggsm.Rebin(binwidth)
data.Rebin(binwidth)
if zjetsEmbed == False:
	zjetsother = zjets.Clone()
	zjetsother.Scale(0)

outfile_name = savedir+"LFV"+"_"+channel+"_fakescmp.png"

wjets.SetLineColor(ROOT.EColor.kBlue+2)
fakes.SetLineColor(ROOT.EColor.kRed+1)
wjets.SetMarkerSize(0)
fakes.SetMarkerSize(0)
wjets.SetLineWidth(3)
fakes.SetLineWidth(3)

legend.AddEntry(wjets,'W+Jets,QCD')
legend.AddEntry(fakes,'Fakes')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
maxLFVStack = LFVStack.GetMaximum()
maxhgglfv=hgglfv.GetMaximum()
maxhvbflfv=hvbflfv.GetMaximum()
maxhvbfsm = hvbfsm.GetMaximum()
maxhggsm = hggsm.GetMaximum()
maxdata = data.GetMaximum()
maxHist = max(wjets.GetMaximum(),fakes.GetMaximum())
wjets.SetMaximum(maxHist*1.20)
if xRange != 0:
	wjets.GetXaxis().SetRangeUser(0,xRange)
wjets.Draw('hist')
fakes.Draw('sameshist')
legend.Draw('sames')
#print LFVStack.GetMaximum()
wjets.GetXaxis().SetTitle(xlabel)
wjets.GetXaxis().SetNdivisions(510)
wjets.GetXaxis().SetTitleOffset(3.0)
wjets.GetXaxis().SetLabelOffset(3.0)
wjets.GetXaxis().SetLabelSize(0.035)
wjets.GetYaxis().SetTitle(ylabel)
wjets.GetYaxis().SetTitleOffset(1.40)
wjets.GetYaxis().SetLabelSize(0.035)
wjets.GetYaxis().SetTitleSize(0.04)

systErrors.SetFillStyle(3001)
systErrors.SetFillColor(ROOT.EColor.kGray+3)
systErrors.SetMarkerSize(0)
systErrors.Draw('sames,E2')
legend.AddEntry(systErrors,'Bkg. Uncertainty')

#if var =="collMass_type1":
#	wjets.GetYaxis().SetRangeUser(0,4.2)
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
p_ratio.cd()
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ratio = wjets.Clone()
denom = fakes.Clone()
ratio.Divide(denom)
ratio.Draw("E1")
if xRange != 0:
	ratio.GetXaxis().SetRangeUser(0,xRange)
size = wjets.GetNbinsX()
xRatioUncert = array.array('f',[])
yRatioUncert = array.array('f',[])
exlRatioUncert = array.array('f',[])
exhRatioUncert = array.array('f',[])
eylRatioUncert = array.array('f',[])
eyhRatioUncert = array.array('f',[])
binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)
#print binwidth
#print "binLength" + str(binLength)
for i in range(1,size+1):
        if fakes.GetBinContent(i) != 0:
                stackRatioBinContent = wjets.GetBinContent(i)/fakes.GetBinContent(i)
		print "stackRatioBinContent:"
		print stackRatioBinContent
		stackRatioBinContentLow = wjets.GetBinContent(i)/fakesHigh.GetBinContent(i)
                stackRatioBinContentHigh = wjets.GetBinContent(i)/fakesLow.GetBinContent(i)
	else:
                stackRatioBinContent = 0
                print "stackRatioBinContent:"
                print stackRatioBinContent
                stackRatioBinContentLow = 0
                stackRatioBinContentHigh = 0
        xRatioUncert.append(wjets.GetBinCenter(i))
        yRatioUncert.append(stackRatioBinContent)
        exlRatioUncert.append(binLength/2)
        exhRatioUncert.append(binLength/2)
        eylRatioUncert.append(stackRatioBinContent-stackRatioBinContentLow)
        eyhRatioUncert.append(stackRatioBinContentHigh-stackRatioBinContent)
xRatioUncertVec = ROOT.TVectorF(len(xRatioUncert),xRatioUncert)
yRatioUncertVec = ROOT.TVectorF(len(yRatioUncert),yRatioUncert)
exlRatioUncertVec = ROOT.TVectorF(len(exlRatioUncert),exlRatioUncert)
exhRatioUncertVec = ROOT.TVectorF(len(exhRatioUncert),exhRatioUncert)
eylRatioUncertVec = ROOT.TVectorF(len(eylRatioUncert),eylRatioUncert)
eyhRatioUncertVec = ROOT.TVectorF(len(eyhRatioUncert),eyhRatioUncert)
systRatioErrors = ROOT.TGraphAsymmErrors(xRatioUncertVec,yRatioUncertVec,exlRatioUncertVec,exhRatioUncertVec,eylRatioUncertVec,eyhRatioUncertVec)
systRatioErrors.SetFillStyle(3002)
systRatioErrors.SetFillColor(ROOT.EColor.kGray+3)
systRatioErrors.SetMarkerSize(0)
systRatioErrors.Draw('sames,E2')

ratio.GetXaxis().SetTitle(xlabel)
ratio.GetXaxis().SetTitleSize(0.12)
ratio.GetXaxis().SetNdivisions(510)
ratio.GetXaxis().SetTitleOffset(1.1)
ratio.GetXaxis().SetLabelSize(5)
ratio.GetXaxis().SetLabelFont(42)
#ratio.GetXaxis().SetTitleFont(42)
ratio.GetYaxis().SetNdivisions(505)
ratio.GetYaxis().SetLabelFont(42)
ratio.GetYaxis().SetLabelSize(0.1)
ratio.GetYaxis().SetRangeUser(0,2)
#ratio.GetXaxis().SetLabelSize(0.1)
#ratio.GetXaxis().SetLabelFont(42)
ratio.GetYaxis().SetTitle("#frac{W+Jets,QCD}{Fakes}")
ratio.GetYaxis().CenterTitle(1)
ratio.GetYaxis().SetTitleOffset(0.4)
ratio.GetYaxis().SetTitleSize(0.12)
ratio.SetTitle("")
#ratioText = ROOT.TPaveText(0.2,0.91,0.7,0.99,"brNDC")
#ratioText.AddText("Data MC Ratio")
#ratioText.SetFillStyle(0)
#ratioText.Draw('sames')
canvas.SaveAs(outfile_name)
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
highbound = 200
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
print "Z+jets Entries: " + str(zjets.GetEntries())
print "TTbar Entries: " + str(ttbar.GetEntries())
print "TTbar Full Entries: " + str(ttbar_full.GetEntries())
print "TTbar Semi Entries: " + str(ttbar_semi.GetEntries())
print "WW Entries: " + str(ww.GetEntries())
print "Single Top Entries: " + str(singlet.GetEntries())
print "data Entries: " + str(data.GetEntries())
print "wjets Entires: " + str(wjets.GetEntries())
