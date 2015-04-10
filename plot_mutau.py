
from sys import argv, stdout, stderr
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
		print qcd_antiiso_ss.Integral()
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
	print "qcd test:"
	print zjets_pre.Integral()
	print ttbar_pre.Integral()
	print ww_pre.Integral()
	print wjets_pre
	print data_ss_inc.Integral()
	return qcd_ss_inc

	
## return w+jets MC estimation
def get_w(var,ss_ntuple_spot, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, wjetsFiltered_norm, zjets_norm, ttbar_semi_norm, ttbar_full_norm, ww_norm):

	if ss_ntuple_spot == "highMtssvbf":
		ss_highmt_ntuple_spot = "highMtssvbf"
	elif ss_ntuple_spot == "highMtssgg":
		ss_highmt_ntuple_spot = "highMtssgg"
	else:
		ss_highmt_ntuple_spot = "highMt"+ss_ntuple_spot
	#print ss_highmt_ntuple_spot
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
	print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets2_mc_ss_highmt)
	print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets3_mc_ss_highmt)
	print wjets_mc_ss_highmt.Integral()
	wjets_mc_ss_highmt.Add(wjets4_mc_ss_highmt)
	wjets_mc_ss_highmt.Add(wjetsFiltered_mc_ss_highmt)
	print wjets_mc_ss_highmt.Integral()
        if "gg0" in ss_ntuple_spot:
                wjets_mc_ss_highmt.Scale(0.8585376)
		print wjets_mc_ss_highmt.Integral()

	
	#print wjets_mc_ss_highmt.Integral()
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

	#print wjets_mc_ss.Integral()
	wjets_ss_inc = (data_ss_highmt.Integral() - zjets_ss_highmt.Integral() - ttbar_ss_highmt.Integral()-ww_ss_highmt.Integral())*wjets_mc_ss.Integral()/wjets_mc_ss_highmt.Integral()  #compute wjets from data in highmt sideband wjets control region. Multiply by ss/highMtss yield from MC
	#print (data_ss_highmt.Integral() - zjets_ss_highmt.Integral() - ttbar_ss_highmt.Integral()-ww_ss_highmt.Integral())
	if channel == "highMtssvbf":
		return wjets_mc_ss_highmt.Integral()
	else:
		return wjets_mc_ss.Integral()
	#return wjets_ss_inc



#########
##Style##
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
if len(argv) < 2:
	print "usage: python plot_mutau variable"
	sys.exit()
var = argv[1]
shape_norm = False
if shape_norm == False:
	ynormlabel = "Scaled to Data "
else:
	ynormlabel = "Normalized to 1 "
#predir = "zjets_embedded_sept9/" #directory with preselection files
#predir = "gg_maria_cmp/"
#predir = "zjets_control_regions_sept6/"
#predir = "200GeVtPt_sept12/"
#predir = "Optimized_VBF_Sept30_presel/"
#predir = "Presel_Oct_1_NewFakes/"
#predir = "Presel_Oct2_FakeRateNoRebin/"
#predir = "Presel_Nov12_FakeRateRebin/"
#predir = "Presel_Nov18_012Jets/"
predir = "presel_Dec12_synch1/"
#predir  = "presel_Jan1_MegaDataTest/"
#predir = "Presel_Nov6_FakeRate/"
#predir = "Presel_Oct31_2JetLooseVBF/"
#predir = "ztautau_control_attempt_sept24_m_t_DR/"
#predir = "ttbar_control_sept13/"
#predir = "control_regions_fakerate_sept12/"
#channel = "vbf" #channel (vbf or gg)
#channel = "ztautaucontrolvbf"
#channel = "highMtssvbf"
#channel = "vbf"
channel ="gg1"
#channel ="ssvbf"
#channel = "vbf"
jes = False #jes up or down
presel =  False #use preselection cuts or not
blind = True
systematics = True
fakeRate = False #apply fake rate method
zjetsEmbed = True #use embedded data samples for zjets
seperateSemiFull = False #seperate semi and fully leptonic ttbar
plotData=True
prelimColors=False
new_signal=True
logScale=False
if channel == "gg0" or channel == "gg1":
	fakeRate = False
#if systematics == True:
#	fakeRate = True
##savedir contains the root files for plotting
if presel:
        savedir = predir

else:
        #savedir = "vbf_fakerate_centralveto_aug19/"
        #savedir = "vbf_embedded_fakerate_aug27/"
	#savedir = "200GeVtPt_vbf_sept12/"
	#savedir = "Optimized_VBF_Sept30/"
	#savedir = "Signal_Oct_1_NewFakes/"
	#savedir = "JesPlusOptimized_Oct15/"
	#savedir = "jesminusNov10/"
	#savedir = "Optimized_Oct10/"
	#savedir = "Optimized_Nov12_FakeRateRebinning/"
	#savedir = "Optimized_Nov25_012Jets/"
	#savedir = "optimized_Dec12_synch1/"
	savedir = "reoptimized_Dec17/"
	#savedir = "singlet_Jan21_old_data/"
	#savedir = "jesnoneJan14/"
        #savedir = "control_regions_sept_2/"
##import parameters for input variable	
import mutau_vars
getVarParams = "mutau_vars."+var
varParams = eval(getVarParams)
xlabel = varParams[0]
if presel and var != "tMtToPfMet_Ty1" and var != "tPhiMETPhiType1":
	binwidth = 10
else:
	binwidth = varParams[1]
legend = eval(varParams[2])
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
		blindlow=0
		blindhigh=0
	elif var == "collMass_type1" and (channel == "gg1" or channel =="vbf"):
		blindlow = 110
		blindhigh = 140
	elif var == "tMtToPfMet_Ty1" and channel == "gg1":
		blindlow = 0
		blindhigh = 10
	#else:
	#	blind=False
if blindlow==blindhigh:
        blindlow = 0
	blindhigh = 500
isGeV = varParams[5]
canvas = ROOT.TCanvas("canvas","canvas",800,800)
if presel == True and plotData==True:
	p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0.22,1,1)
	p_lfv.SetBottomMargin(0.08)
	if logScale == True:
		p_lfv.SetLogy()
	p_lfv.Draw()
	p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.2)
	p_ratio.SetTopMargin(0.1)
	p_ratio.SetGrid()
	p_ratio.Draw()
	p_lfv.cd()
LFVStack = ROOT.THStack("stack","")
if new_signal == True:
	hgglfv_ntuple_file_str = 'LFV_GluGlu_Dec9.root'
	hvbflfv_ntuple_file_str='LFV_VBF_Dec9.root'
else:
	hgglfv_ntuple_file_str = 'LFV_GluGlu_H2Tau_M-126.root'
	hvbflfv_ntuple_file_str = 'LFV_VBF_H2Tau_M-126.root'
#hggsm_ntuple_file_str = 'GGH_H2Tau_M-125.root'
zjets_ntuple_file_str = 'Zjets_M50.root'
if zjetsEmbed:
	dataEmb_ntuple_file_str = 'dataEmbedded_2012.root'
	dy1jets_ntuple_file_str = 'DY1Jets_madgraph.root'
	dy2jets_ntuple_file_str = 'DY2Jets_madgraph.root'
	dy3jets_ntuple_file_str = 'DY3Jets_madgraph.root'
	dy4jets_ntuple_file_str = 'DY4Jets_madgraph.root'
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
#tt_ntuple_file_str = 'T_t-channel.root'
#tbart_ntuple_file_str = 'Tbar_t-channel.root'
#tw_ntuple_file_str = 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
#tbarw_ntuple_file_str = 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root'
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
#tt_ntuple_file = ROOT.TFile(savedir+tt_ntuple_file_str)
#tbart_ntuple_file = ROOT.TFile(savedir+tbart_ntuple_file_str)
#tw_ntuple_file = ROOT.TFile(savedir+tw_ntuple_file_str)
#tbarw_ntuple_file = ROOT.TFile(savedir+tbarw_ntuple_file_str)
data_ntuple_file = ROOT.TFile(savedir+data_ntuple_file_str)
hvbfsm_ntuple_file = ROOT.TFile(savedir+hvbfsm_ntuple_file_str)
#hggsm_ntuple_file = ROOT.TFile(savedir+hggsm_ntuple_file_str)

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
#tt_ntuple_file = ROOT.TFile(predir+tt_ntuple_file_str)
#tbart_ntuple_file = ROOT.TFile(predir+tbart_ntuple_file_str)
#tw_ntuple_file = ROOT.TFile(predir+tw_ntuple_file_str)
#tbarw_ntuple_file = ROOT.TFile(predir+tbarw_ntuple_file_str)

data_pre_ntuple_file = ROOT.TFile(predir+data_ntuple_file_str)

#get histograms
ntuple_spot = channel
hgglfv = hgglfv_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
hvbflfv = hvbflfv_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
hvbfsm = hvbfsm_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#hggsm = hggsm_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
zjetsMC = zjets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
if zjetsEmbed:
	dy1jets = dy1jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy2jets = dy2jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy3jets = dy3jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	dy4jets = dy4jets_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	zjets = dataEmb_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#if "gg0" in channel or "gg1" in channel:
	#	dy1other = dy1other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy2other = dy2other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy3other = dy3other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
	#	dy4other = dy4other_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
		
wjets1 = wjets1_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets2 = wjets2_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets3 = wjets3_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets4 = wjets4_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjetsFiltered = wjetsFiltered_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_semi = ttbar_semi_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ttbar_full = ttbar_full_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
ww = ww_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#tt = tt_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#tbart = tbart_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#tw = tbarw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
#tbarw = tw_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
data = data_ntuple_file.Get(ntuple_spot+"/"+var).Clone()


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
#tt_lumifile = lumidir + 'T_t-channel.lumicalc.sum'
#tbart_lumifile = lumidir + 'Tbar_t-channel.lumicalc.sum'
#tw_lumifile = lumidir + 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'
#tbarw_lumifile = lumidir + 'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'

if new_signal == True:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_Dec9.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_Dec9.lumicalc.sum'
else:
	hvbflfv_lumifile = lumidir + 'LFV_VBF_H2Tau_M-126.lumicalc.sum'
	hgglfv_lumifile = lumidir + 'LFV_GluGlu_H2Tau_M-126.lumicalc.sum'
hvbfsm_lumifile = lumidir + 'VBF_H2Tau_M-125.lumicalc.sum'
#hggsm_lumifile = lumidir + 'GGH_H2Tau_M-125.lumicalc.sum'



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

f = open(hvbflfv_lumifile).read().splitlines()
hvbflfv_efflumi = float(f[0])

f = open(hgglfv_lumifile).read().splitlines()
hgglfv_efflumi = float(f[0])

f = open(hvbfsm_lumifile).read().splitlines()
hvbfsm_efflumi = float(f[0])

#f = open(#hggsm_lumifile).read().splitlines()
#hggsm_efflumi = float(f[0])

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


if fakeRate == False:


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
	print "qcd norm" + str(qcd_norm)
	if qcd_norm < 0:  #if approximately no qcd
		qcd.Scale(0)
	else:
		qcd.Scale(qcd_norm/qcd.Integral()) #normalized qcd shape
#correct for using looser vbf Cuts for qcd shape
	if var == "vbfMass":
		for x in range(0,500):
			qcd.SetBinContent(x,0)
	elif var == "vbfDeta":
		xbin = qcd.GetXaxis().FindBin(3.5)
		for x in range(0,xbin):
			qcd.SetBinContent(x,0)

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
	hgglfv_norm = lumi/hgglfv_efflumi
	hvbflfv_norm = lumi/hvbflfv_efflumi
	hvbfsm_norm = lumi/hvbfsm_efflumi
	#hggsm_norm = lumi/hggsm_efflumi
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
		zjets.Scale(dyjets.Integral()/zjets.Integral())
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
	ttbar = ttbar_full.Clone()
	ttbar.Add(ttbar_semi)
	wjets_norm = 1/wjets.Integral()
	ttbar_norm = 1/ttbar.Integral()
	ww_norm = 1/ww.Integral()
	hgglfv_norm = 1/(hgglfv.Integral())
	hvbflfv_norm = 1/(hvbflfv.Integral())
	hvbfsm_norm = 1/(hvbfsm.Integral())
	#hggsm_norm = 1/(hggsm.Integral())
	qcd_norm = 1/(qcd.Integral())
	qcd.Scale(qcd_norm)
	wjets.Scale(wjets_norm)
	ttbar.Scale(ttbar_norm)
	ttbar_full.Scale(1/ttbar_full.Integral())
	ttbar_semi.Scale(1/ttbar_semi.Integral())
	if zjetsEmbed == False:
		zjets = zjetsMC.Clone()
	zjets_norm = 1/zjets.Integral()
	zjets.Scale(1/zjets.Integral())
		

ww.Scale(ww_norm)
hgglfv.Scale(hgglfv_norm)
hvbflfv.Scale(hvbflfv_norm)
hvbfsm.Scale(hvbfsm_norm)
#hggsm.Scale(hggsm_norm)
xbinLength = data.GetBinWidth(1)
isGeV = varParams[5]
widthOfBin = binwidth*xbinLength
if isGeV:
	ylabel = ynormlabel + " Events/" + str(widthOfBin) + " GeV"
else:
	ylabel = ynormlabel  + " Events/" + str(widthOfBin)
wjets.Rebin(binwidth)
zjets.Rebin(binwidth)
ttbar.Rebin(binwidth)
ttbar_full.Rebin(binwidth)
ttbar_semi.Rebin(binwidth)
ww.Rebin(binwidth)
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hvbfsm.Rebin(binwidth)
#hggsm.Rebin(binwidth)
data.Rebin(binwidth)
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

if systematics == True:
	if fakeRate == True:
		wjets = data_ntuple_file.Get(fakechannel+"/"+var).Clone()
		wjets.Rebin(binwidth)
        	fakesLow = data_ntuple_file.Get(fakechannel+"down/"+var).Clone()
        	fakesHigh = data_ntuple_file.Get(fakechannel+"up/"+var).Clone()
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
	print binwidth
	print "binLength" + str(binLength)
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0:
			if fakeRate == True:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)
			else:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+qcd.GetBinContent(i)
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
                        	eylUncert.append(wjetsBinContent-fakesLow.GetBinContent(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i))
				print wjets.GetBinContent(i)
				print fakesLow.GetBinContent(i)
				print fakesHigh.GetBinContent(i)
			#	eyhUncert.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
                        	eyhUncert.append(fakesHigh.GetBinContent(i) +zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i) - wjetsBinContent)
			else:
                                eylUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+qcd.GetBinError(i))
                                print wjets.GetBinContent(i)
                        #       eyhUncert.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
                                eyhUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+qcd.GetBinError(i))
	print "test error low" + str(zjets.GetBinError(2))
	print zjets.GetBinErrorUp(2)
	print xUncert
	print yUncert
	print exlUncert
	print exhUncert
	print eylUncert
	print eyhUncert
	xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
	yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
	yFakesNoStackVec = ROOT.TVectorF(len(yFakesNoStack),yFakesNoStack)
	exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
	exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
	eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
	eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)	
	systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)
	fakeErrorsNoStack =  ROOT.TGraphAsymmErrors(xUncertVec,yFakesNoStackVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)
'''
	if zjetsEmbed == False:
		zjetsFakes = zjets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		zjetsFakes.Scale(zjets_norm)
	else:
		zjetsFakes = dataEmb_ntuple_file.Get(fakechannel+"/"+var).Clone()
		zjetsFakes.Scale(dyjets.Integral()/zjets.Integral())

	zjets.Add(zjetsFakes) #zjetsFakes = actual_zjetsFakes*-1, will fix
	ttbar_full_fakes = ttbar_full_ntuple_file.Get(fakechannel+"/"+var).Clone()
	ttbar_full_fakes.Scale(ttbar_full_norm)
	ttbar_semi_fakes = ttbar_semi_ntuple_file.Get(fakechannel+"/"+var).Clone()
	ttbar_semi_fakes.Scale(ttbar_semi_norm)
	ttbar.Add(ttbar_full_fakes) #ttbar_full_fakes = actual ttbar_full_fakes*-1)
	ttbar.Add(ttbar_semi_fakes) #ttbar_semi_fakes = actual ttbar_semi_fakes*-1)
	ttbar_semi.Add(ttbar_semi_fakes)
	ttbar_full.Add(ttbar_full_fakes)
'''


outfile_name = savedir+"LFV"+"_"+channel+"_"+var
if fakeRate == True:
	outfile_name = outfile_name + "_fakeRate"
if zjetsEmbed == True:
	outfile_name = outfile_name +"_zjetsEmbed"
if new_signal == True:
	outfile_name = outfile_name +"_newSignal"
if logScale == True:
	outfile_name = outfile_name +"_log"

##create root file with yields for datacards
outfile = ROOT.TFile(outfile_name+".root","RECREATE")
outfile.mkdir("vbfmutau")
outfile.cd("vbfmutau/")
#wjets.Scale(5)
#zjets.Scale(5)
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
#	if "gg0" in channel or "gg1" in channel:
#		dyother.Write("zplusotherjets")

#ttbar.Scale(5)
#ww.Scale(5)
#data.Scale(5)
ttbar.Write("ttbar")
ttbar_semi.Write("ttbarsemi")
ttbar_full.Write("ttbarfull")
ww.Write("ww")
data.Write("data_obs")
#hvbflfv.Scale(6.75)
#hgglfv.Scale(6.5)
#hvbfsm.Scale(6.75)
hvbflfv.Write("LFVVBF126")
hgglfv.Write("LFVGG126")
hvbfsm.Write("SMVBF126")
#hggsm.Write("SMGG126")
hvbflfv.Write("LFVVBF")
hgglfv.Write("LFVGG")
hvbfsm.Write("SMVBF")
#hggsm.Write("SMGG")
outfile.Write()

if prelimColors == True:
	hgglfv.SetLineColor(ROOT.EColor.kBlue+2)
	hvbflfv.SetLineColor(ROOT.EColor.kRed+1)
	hvbfsm.SetLineColor(ROOT.EColor.kGreen+8)
	#hggsm.SetLineColor(ROOT.EColor.kOrange+5)
	wjets.SetFillColor(ROOT.EColor.kPink-4)
	zjets.SetFillColor(ROOT.EColor.kGreen+4)
	ttbar.SetFillColor(ROOT.EColor.kCyan-2)
	ttbar_full.SetFillColor(ROOT.EColor.kGreen+3)
	ttbar_semi.SetFillColor(ROOT.EColor.kCyan-6)
	ww.SetFillColor(ROOT.EColor.kCyan)
else:
        hgglfv.SetLineColor(ROOT.EColor.kBlue+2)
        hvbflfv.SetLineColor(ROOT.EColor.kRed+1)
        hvbfsm.SetLineColor(ROOT.EColor.kGreen+8)
	#hggsm.SetLineColor(ROTT.EColor.kOrange+5)
        wjets.SetFillColor(ROOT.EColor.kMagenta-10)
        zjets.SetFillColor(ROOT.EColor.kOrange-4)
        ttbar.SetFillColor(40)
        ttbar_full.SetFillColor(ROOT.EColor.kGreen+3)
        ttbar_semi.SetFillColor(ROOT.EColor.kCyan-6)
        ww.SetFillColor(ROOT.EColor.kCyan)
if fakeRate == False:
	qcd.SetFillColor(ROOT.EColor.kYellow-9)
	qcd.SetMarkerSize(0)
wjets.SetMarkerSize(0)
zjets.SetMarkerSize(0)
ttbar.SetMarkerSize(0)
ttbar_full.SetMarkerSize(0)
ttbar_semi.SetMarkerSize(0)
ww.SetMarkerSize(0)
hgglfv.SetMarkerSize(0)
hvbflfv.SetMarkerSize(0)
hvbfsm.SetMarkerSize(0)
#hggsm.SetMarkerSize(0)
hgglfv.SetLineWidth(3)
hvbflfv.SetLineWidth(3)
hvbfsm.SetLineWidth(3)
#hggsm.SetLineWidth(3)
#if zjetsEmbed == True and ("gg0" in channel or "gg1" in channel):
#	dyother.SetMarkerSize(0)
#	dyother.SetFillColor(ROOT.EColor.kSpring+1)
#	dyother.Rebin(binwidth)
#	legend.AddEntry(dyother,'Z+jets (other)')
legend.AddEntry(hgglfv,'GG LFV Higgs BR=0.10')
legend.AddEntry(hvbflfv, 'VBF LFV Higgs BR = 0.10')
legend.AddEntry(hvbfsm, 'VBF SM Higgs BR=0.060')
#legend.AddEntry(#hggsm, 'GG SM Higgs BR=0.060')
if fakeRate == False:
	legend.AddEntry(wjets,'W+Jets')
else:
	wjets.SetFillColor(ROOT.EColor.kBlue-5)
	legend.AddEntry(wjets, 'Fakes')
if zjetsEmbed == False: 
	legend.AddEntry(zjets,'Z+Jets')
else:
	legend.AddEntry(zjets, 'Z Tau Tau')
if seperateSemiFull == False:
	legend.AddEntry(ttbar,'TT+Jets')
else:
	legend.AddEntry(ttbar_full, 'TT Fully Leptonic')
	legend.AddEntry(ttbar_semi, 'TT Semi Leptonic')
legend.AddEntry(ww,'WW')
if fakeRate == False:
	legend.AddEntry(qcd,'QCD')
legend.SetFillColor(0)
legend.SetBorderSize(0)
if fakeRate == False:
	LFVStack.Add(qcd)
LFVStack.Add(ww)
if seperateSemiFull == False:
	LFVStack.Add(ttbar)
else:
	LFVStack.Add(ttbar_full)
	LFVStack.Add(ttbar_semi)
LFVStack.Add(zjets)
#if zjetsEmbed == True and ("gg0" in channel or "gg1" in channel):
#	LFVStack.Add(dyother)
LFVStack.Add(wjets)
maxLFVStack = LFVStack.GetMaximum()
maxhgglfv=hgglfv.GetMaximum()
maxhvbflfv=hvbflfv.GetMaximum()
maxhvbfsm = hvbfsm.GetMaximum()
#max#hggsm = hggsm.GetMaximum()
maxdata = data.GetMaximum()
print maxhvbflfv
#maxHist = max(maxLFVStack,maxhgglfv,maxhvbflfv,maxhvbfsm,max#hggsm,maxdata)
maxHist = max(maxLFVStack,maxhgglfv,maxhvbflfv,maxhvbfsm,maxdata)
print maxHist
LFVStack.SetMaximum(maxHist)
print LFVStack.GetMaximum()
LFVStack.Draw('hist')
hgglfv.Draw('sameshist')
hvbflfv.Draw('sameshist')
hvbfsm.Draw('sameshist')
#hggsm.Draw('sameshist')
if systematics == True:
	systErrors.SetFillStyle(3004)
	systErrors.Draw('sames2')
if presel == True and shape_norm == False and blind == False:
	if plotData == True:
		data.Draw("sames")
        	legend.AddEntry(data,'8 TeV Data')
if var == "collMass_type1":
        LFVStack.GetXaxis().SetRangeUser(0,500)
if var == "tMtToPfMet_Ty1":
	LFVStack.GetXaxis().SetRangeUser(0,40)
if var == "tPt":
	LFVStack.GetXaxis().SetRangeUser(0,100)
if blind == True and shape_norm == False:
	binblindlow = data.FindBin(blindlow)
	binblindhigh = data.FindBin(blindhigh)
	for x in range(binblindlow, binblindhigh):
		data.SetBinContent(x, -1000)
	if plotData == True:	
		data.Draw('sames')
		legend.AddEntry(data,'8 TeV Data')	
		pave = ROOT.TPave(blindlow,0,blindhigh,maxHist*1.05,4,"br")
		pave.SetFillColor(1)
		pave.SetFillStyle(3002)
		pave.SetBorderSize(0)
		pave.Draw('sameshist')
		legend.AddEntry(pave,'Blinded')
legend.SetTextSize(0.02)
legend.Draw('sames')
LFVStack.GetXaxis().SetTitle(xlabel)
LFVStack.GetXaxis().SetTitleOffset(0.95)
LFVStack.GetXaxis().SetLabelSize(0.035)
LFVStack.GetYaxis().SetTitle(ylabel)
LFVStack.GetYaxis().SetTitleOffset(1.35)
LFVStack.GetYaxis().SetLabelSize(0.035)
if var =="collMass_type1":
	LFVStack.GetYaxis().SetRangeUser(0,4.2)
else:
	LFVStack.GetYaxis().SetRangeUser(0,maxHist*1.05)
#data.GetXaxis().SetTitle(xlabel)
#data.GetYaxis().SetTitleOffset(1.2)
#data.GetYaxis().SetRangeUser(0,maxHist*1.05)
lumifb = '%.2f'%(lumi/1000)
title_str = "\sqrt{s} = 8 TeV   L = " + str(lumifb)+" fb^{-1}"
titleText = ROOT.TPaveText(0.2,0.91,0.7,0.99,"brNDC")
titleText.AddText(title_str)
titleText.SetFillStyle(0)
titleText.Draw('sames')
print title_str
#signal to background ratio
maxbin = hvbflfv.GetMaximumBin()
if fakeRate == False:
	#sbratio =hvbflfv.GetBinContent(maxbin)/(ww.GetBinContent(maxbin)+wjets.GetBinContent(maxbin)+zjets.GetBinContent(maxbin)+ttbar.GetBinContent(maxbin)+qcd.GetBinContent(maxbin))
	#sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+#hggsm.GetBinContent(maxbin))
        sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
else:
	#sbratio =hvbflfv.GetBinContent(maxbin)/(ww.GetBinContent(maxbin)+wjets.GetBinContent(maxbin)+zjets.GetBinContent(maxbin)+ttbar.GetBinContent(maxbin))
	#sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+#hggsm.GetBinContent(maxbin))
        sbratio = hvbflfv.GetBinContent(maxbin)/(LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
print "Signal to Background Ratio: " + str(sbratio)
#print (LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin)+#hggsm.GetBinContent(maxbin))
print (LFVStack.GetMaximum()+hvbfsm.GetBinContent(maxbin))
print hvbflfv.GetMaximum()
#p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.3)
#p_ratio.SetTopMargin(0.1)
#p_ratio.Draw()
if presel == True and plotData==True:
	p_ratio.cd()
	ratio = data.Clone()
	mc = wjets.Clone()
	mc.Add(zjets)
	mc.Add(ttbar)
	if fakeRate == False:
		mc.Add(qcd)
	ratio.Divide(mc)
	ratio.Draw()
	if var == "tPt":
		ratio.GetXaxis().SetRangeUser(0,100)
		lineOne = ROOT.TLine(0.0, 1.0, 100 + widthOfBin ,1.0)
	elif var == "tMtToPfMet_Ty1":
		ratio.GetXaxis().SetRangeUser(0,40)
		lineOne = ROOT.TLine(0.0, 1.0, 40.0 + widthOfBin,1.0)
	else:
        	lineOne = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1.0, ratio.GetXaxis().GetXmax(),1.0)
	
        lineOne.Draw('sames')
	if blind == True:
        	paveRatio = ROOT.TPave(blindlow,0.0,blindhigh,2.0,4,"br")
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
	print "binLength" + str(binLength)
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0:
			stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)
			wjetsBinContent = wjets.GetBinContent(i)
			ratioBinContent = ratio.GetBinContent(i)
			xRatio.append(wjets.GetBinCenter(i))
			yRatio.append(1.0)
			exlRatio.append(binLength/2)
			exhRatio.append(binLength/2)
			if fakeRate == True and systematics == True:
				eylRatio.append(1.0-(fakesLow.GetBinContent(i)-wjetsBinContent -zjets.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)+stackBinContent)/stackBinContent)
                        	eyhRatio.append((fakesHigh.GetBinContent(i)-wjetsBinContent+zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+stackBinContent)/stackBinContent-1.0)
			else:
                                eylRatio.append(1.0-(-wjets.GetBinError(i) -zjets.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)+stackBinContent)/stackBinContent)
                        	eyhRatio.append((wjets.GetBinError(i)+zjets.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+stackBinContent)/stackBinContent-1.0)

			print wjets.GetBinContent(i)
			#eyhFakes.append(fakesHigh.GetBinContent(i) - wjets.GetBinContent(i))
	if systematics == True:
		print "test error low" + str(zjets.GetBinError(2))
		print zjets.GetBinErrorUp(2)
		print xRatio
		print yRatio
		print exlRatio
		print exhRatio
		print eylRatio
		print eyhRatio
		xRatioVec = ROOT.TVectorF(len(xRatio),xRatio)
		yRatioVec = ROOT.TVectorF(len(yRatio),yRatio)
		exlRatioVec = ROOT.TVectorF(len(exlRatio),exlRatio)
		exhRatioVec = ROOT.TVectorF(len(exhRatio),exhRatio)
		eylRatioVec = ROOT.TVectorF(len(eylRatio),eylRatio)
		eyhRatioVec = ROOT.TVectorF(len(eyhRatio),eyhRatio)	
		ratioErrors = ROOT.TGraphAsymmErrors(xRatioVec,yRatioVec,exlRatioVec,exhRatioVec,eylRatioVec,eyhRatioVec)
		ratioErrors.SetFillStyle(3004)
        	ratioErrors.Draw('sames2')
	ratio.GetYaxis().SetTitle("Data MC Ratio")
	ratio.GetYaxis().SetTitleOffset(0.5)
	ratio.GetYaxis().SetTitleSize(0.1)
	ratio.GetYaxis().SetRangeUser(0.0,2.0)
	ratio.GetYaxis().SetNdivisions(4)
	ratio.GetYaxis().SetLabelSize(0.1)
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
if fakeRate == False:
	print "QCD Integral: " + str(qcd.Integral())
	print "W+jets Integral: " + str(wjets.Integral())
else:
	print "Fakes Integral: " + str(wjets.Integral())
	if systematics == True:
		print "Fakes Low Integral: " + str(fakesLow.Integral())
		print "Fakes High Integral: " + str(fakesHigh.Integral())
		print "(high-central)/central: " + str((fakesHigh.Integral() - wjets.Integral())/wjets.Integral())
		print "(central-low)/central: " + str((wjets.Integral() - fakesLow.Integral())/wjets.Integral())
lowbound = 60.1
highbound = 139.9
#print "Background:"+str(zjets.Integral(zjets.FindBin(lowbound),zjets.FindBin(highbound)) + ttbar.Integral(ttbar.FindBin(lowbound),ttbar.FindBin(highbound)) + ww.Integral(ww.FindBin(lowbound),ww.FindBin(highbound)) + hvbfsm.Integral(hvbfsm.FindBin(lowbound),hvbfsm.FindBin(highbound)) + #hggsm.Integral(hggsm.FindBin(lowbound),hggsm.FindBin(highbound))+ wjets.Integral(wjets.FindBin(lowbound),wjets.FindBin(highbound)))
print "Background:"+str(zjets.Integral(zjets.FindBin(lowbound),zjets.FindBin(highbound)) + ttbar.Integral(ttbar.FindBin(lowbound),ttbar.FindBin(highbound)) + ww.Integral(ww.FindBin(lowbound),ww.FindBin(highbound)) + hvbfsm.Integral(hvbfsm.FindBin(lowbound),hvbfsm.FindBin(highbound)) + wjets.Integral(wjets.FindBin(lowbound),wjets.FindBin(highbound)))
print "Signal:" + str(hvbflfv.Integral(hvbflfv.FindBin(lowbound),hvbflfv.FindBin(highbound))+hgglfv.Integral(hgglfv.FindBin(lowbound),hgglfv.FindBin(highbound)))
print "Z+jets Integral: " + str(zjets.Integral())
#if zjetsEmbed == True and ("gg0" in channel or "gg1" in channel):
#	print "Z+other Integral: " + str(dyother.Integral())
print "TTbar Integral: " + str(ttbar.Integral())
print "TTbar Full Integral: " + str(ttbar_full.Integral())
print "TTbar Semi Integral: " + str(ttbar_semi.Integral())
print "WW Integral: " + str(ww.Integral())
print "SM VBF Integral: " + str(hvbfsm.Integral())
#print "SS GG Integral: " + str(#hggsm.Integral())
print "Z+jets Entries: " + str(zjets.GetEntries())
print "TTbar Entries: " + str(ttbar.GetEntries())
print "TTbar Full Entries: " + str(ttbar_full.GetEntries())
print "TTbar Semi Entries: " + str(ttbar_semi.GetEntries())
print "WW Entries: " + str(ww.GetEntries())
print "data Entries: " + str(data.GetEntries())
print "wjets Entries: " + str(wjets.GetEntries())
