
from sys import argv, stdout, stderr
import ROOT
import sys

##get qcd (choose selections for qcd)

def make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file,wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, zjets_norm, ttbar_norm, ww_norm):

        qcd_norm_histo = get_ss_inc_qcd(var,channel, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, zjets_norm, ttbar_norm, ww_norm)  ##gets same sign inclusive qcd
        qcd_norm_histo.Scale(1.06) ##os inclusive qcd 
	if not presel: #get efficiency of vbf cuts
     		ssanti_iso_ntuple_spot = "ssantiisomuon"+channel
        	data_ntuple_file.cd(ssanti_iso_ntuple_spot)
        	qcd_antiiso_ss = ROOT.gDirectory.Get(var).Clone()
        	data_pre_ntuple_file.cd(ssanti_iso_ntuple_spot)
        	qcd_antiiso_ss_inc = ROOT.gDirectory.Get(var).Clone()
        	qcd_norm_histo.Multiply(qcd_antiiso_ss)
        	qcd_norm_histo.Divide(qcd_antiiso_ss_inc)

        return qcd_norm_histo



def get_ss_inc_qcd(var,channel, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, zjets_norm, ttbar_norm, ww_norm):

	ss_ntuple_spot = "ss"+channel
	zjets_pre_ntuple_file.cd(ss_ntuple_spot)
	zjets_pre = ROOT.gDirectory.Get(var).Clone()
	print zjets.Integral()
	zjets_pre.Scale(zjets_norm)
	print zjets.Integral()
	ttbar_pre_ntuple_file.cd(ss_ntuple_spot)
	ttbar_pre = ROOT.gDirectory.Get(var).Clone()
        ttbar_pre.Scale(ttbar_norm)
	ww_pre_ntuple_file.cd(ss_ntuple_spot)
	ww_pre = ROOT.gDirectory.Get(var).Clone()
	ww_pre.Scale(ww_norm)
	data_pre_ntuple_file.cd(ss_ntuple_spot)
	qcd_ss_inc = ROOT.gDirectory.Get(var).Clone()
	qcd_ss_inc.Add(zjets_pre,-1)
	qcd_ss_inc.Add(ttbar_pre,-1)
	qcd_ss_inc.Add(ww_pre,-1)
	wjets_pre = get_w(var,ss_ntuple_spot,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, zjets_norm, ttbar_norm, ww_norm) #returns w+jets estimation
	qcd_ss_inc.Add(wjets_pre,-1)
	return qcd_ss_inc

	

def get_w(var,ss_ntuple_spot, wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file, wjets1_norm, wjets2_norm, wjets3_norm, wjets4_norm, zjets_norm, ttbar_norm, ww_norm):

	ss_highmt_ntuple_spot = "highMt"+ss_ntuple_spot
	data_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
	wjets_ss_inc = ROOT.gDirectory.Get(var).Clone() #data_ss_highmt
	zjets_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        zjets_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	zjets_ss_highmt.Scale(zjets_norm)
	ttbar_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        ttbar_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	ttbar_ss_highmt.Scale(ttbar_norm)
	
        ww_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        ww_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	ww_ss_highmt.Scale(ww_norm)
	
	wjets1_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
	wjets_mc_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	wjets_mc_ss_highmt.Scale(wjets1_norm)
	wjets2_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        wjets2_mc_ss_highmt = ROOT.gDirectory.Get(var).Clone()
        wjets2_mc_ss_highmt.Scale(wjets2_norm)
        wjets3_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        wjets3_mc_ss_highmt = ROOT.gDirectory.Get(var).Clone()
        wjets3_mc_ss_highmt.Scale(wjets3_norm)
        wjets4_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        wjets4_mc_ss_highmt = ROOT.gDirectory.Get(var).Clone()
        wjets4_mc_ss_highmt.Scale(wjets4_norm)	
	wjets_mc_ss_highmt.Add(wjets2_mc_ss_highmt)
	wjets_mc_ss_highmt.Add(wjets3_mc_ss_highmt)
	wjets_mc_ss_highmt.Add(wjets4_mc_ss_highmt)

	wjets1_pre_ntuple_file.cd(ss_ntuple_spot)
	wjets_mc_ss = ROOT.gDirectory.Get(var).Clone()
	wjets_mc_ss.Scale(wjets1_norm)
        wjets2_pre_ntuple_file.cd(ss_ntuple_spot)
        wjets2_mc_ss = ROOT.gDirectory.Get(var).Clone()
        wjets2_mc_ss.Scale(wjets2_norm)
        wjets3_pre_ntuple_file.cd(ss_ntuple_spot)
        wjets3_mc_ss = ROOT.gDirectory.Get(var).Clone()
        wjets3_mc_ss.Scale(wjets3_norm)
        wjets4_pre_ntuple_file.cd(ss_ntuple_spot)
        wjets4_mc_ss = ROOT.gDirectory.Get(var).Clone()
        wjets4_mc_ss.Scale(wjets4_norm)

	wjets_mc_ss.Add(wjets2_mc_ss)
	wjets_mc_ss.Add(wjets3_mc_ss)
	wjets_mc_ss.Add(wjets4_mc_ss)

	wjets_ss_inc.Add(zjets_ss_highmt,-1)
	wjets_ss_inc.Add(ttbar_ss_highmt,-1)
	wjets_ss_inc.Add(ww_ss_highmt,-1) ##w_data_ss_highmt
	wjets_ss_inc.Multiply(wjets_mc_ss)
	wjets_ss_inc.Divide(wjets_mc_ss_highmt)
	return wjets_ss_inc 

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
	ynormlabel = "Normalized to Data "
else:
	ynormlabel = "Normalized to 1 "
binwidth = 5  #define rebinning
#specify plotting schemes for individual variables
#if blindlow = blindhigh, then blind=False (no unblinding of area outside of signal region)
blindlow = 0
blindhigh = 0
if var == "mPt":
	xlabel = "#mu P_{T} (GeV)"
	binwidth = 10
	legend =ROOT.TLegend(0.55,0.45,0.8,0.85,'','brNDC')
	ylabel = ynormlabel +" 10 GeV binning"
	blindlow = 40
	blindhigh = 40
elif var == "tPt":
	xlabel = "#tau P_{T} (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 5 GeV binning"
	blindlow = 20
	blindhigh = 60
elif var == "mEta":
	xlabel = "#mu #eta"
	legend =ROOT.TLegend(0.2,0.6,0.4,0.8,'','brNDC')
	binwidth = 10
	ylabel = ynormlabel
	blindlow = -1.5
	blindhigh = -1.5
elif var == "tEta":
	xlabel = "#tau #eta"
	legend =ROOT.TLegend(0.7,0.65,0.9,0.88,'','brNDC')
	binwidth = 10
	ylabel = ynormlabel
	blindlow = -1.5
	blindhigh = 1.5
elif var == "mMtToPfMet_Ty1":
	xlabel = "#mu M_{T} Ty1 (GeV)"
	binwidth = 20
	ylabel = ynormlabel + " 20 GeV binning"
	legend =ROOT.TLegend(0.55,0.6,0.8,0.8,'','brNDC')
	blindlow = 30
	blindhigh = 100
elif var == "tMtToPfMet_Ty1":
	xlabel = "#tau M_{T} Ty1 (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 5 GeV binning"
	blindlow = 20
	blindhigh = 100
elif var == "vbfDeta":
	xlabel = "#Delta#eta_{jj}"
	legend =ROOT.TLegend(0.6,0.6,0.9,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 3.5
	blindhigh = 7
elif var == "vbfDijetrap":
	xlabel ="Rapidity_{jj}"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 0
	blindhigh = 1
elif var == "vbfDphihjnomet":
	xlabel = "#Delta#phi_{Hj} (no MET)"
	legend =ROOT.TLegend(0.2,0.6,0.5,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 2.5
	blindhigh = 3.25
elif var == "vbfDphihj":
	xlabel = "#Delta#phi_{Hj}"
	legend =ROOT.TLegend(0.2,0.6,0.5,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 2.75
	blindhigh = 3.25
elif var == "vbfHrap":
	xlabel = "Rapidity_{H}"
	legend =ROOT.TLegend(0.4,0.6,0.89,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 0
	blindhigh = 1.5
elif var == "vbfj1eta":
	xlabel = "#eta_{j1}"
	binwidth = 10
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	blindlow=0
	blindhigh=0
elif var == "vbfj2eta":
	xlabel = "#eta_{j2}"
	binwidth = 10
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	blindlow=0
	blindhigh=0
elif var == "vbfMass":
	xlabel = "M_{jj} (GeV)"
	binwidth = 10
	legend =ROOT.TLegend(0.15,0.6,0.45,0.8,'','brNDC')
	ylabel = ynormlabel + " 50 GeV binning"
	blindlow = 500
	blindhigh = 800
elif var == "vbfMVA":
	xlabel = "MVAMET (GeV)"
	ylabel = ynormlabel
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
elif var == "vbfVispt":
	xlabel = "Visible P_{T} (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 10 GeV binning"
	blindlow = 20
	blindhigh = 140
elif var == "m_t_Mass":
	xlabel = "Visible Mass (GeV)"
	legend =ROOT.TLegend(0.48,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + "20 GeV binning"
	binwidth = 20
	blindlow = 60
	blindhigh = 120
elif var == "m_t_DPhi":
	xlabel = "#mu #tau #Delta#phi"
	legend = ROOT.TLegend(0.25,0.6,0.6,0.8,'','brNDC')
	ylabel = ynormlabel
	blindlow = 2.6
	blindhigh = 3.2
elif var == "m_t_Pt":
	xlabel = "Visible P_{T} (GeV)"
	legend = ROOT.TLegend(0.45,0.5,0.85,0.8,'','brNDC')
	ylabel = ynormlabel + "10 GeV binning"
	binwidth = 10
	blindlow = 20
	blindhigh = 140
elif var == "m_t_DR":
	xlabel = "#mu #tau #DeltaR"
	legend = ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	blindlow = 1.0
	blindhigh = 3.5
elif var == "m_t_ToMETDPhi_Ty1":
	xlabel = "#Delta#phi (MET , #mu#tau)"
	legend = ROOT.TLegend(0.15,0.7,0.4,0.87,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
	blindlow = 0
	blindhigh = 1.5
elif var == "fullMT_type1":
	xlabel = "Full M_{T} (GeV)"
	ylabel = ynormlabel +"  40 GeV Binning"
	legend = ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC') 
	binwidth = 40
	blindlow = 60
	blindhigh = 160
elif var == "fullPT_type1":
	xlabel = "Full P_{T} (GeV)"
	ylabel = ynormlabel + " 20 GeV Binning"
	legend = ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	binwidth = 20
	blindlow = 20
	blindhigh = 240
elif var == "jetVeto30":
	xlabel  = "Number of P_{T} > 30 GeV Jets"
	ylabel = ynormlabel
	legend = ROOT.TLegend(0.45,0.4,0.87,0.8,'','brNDC')
	binwidth = 1
else:
	xlabel = var
	binwidth = 5
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	

predir = "presel_2jets/" #directory with preselection files
channel = "vbf" #channel (vbf or gg)
presel = True #use preselection cuts or not
blind = True
#blindlow = 1000
#blindhigh = 1001
if blindlow==blindhigh:
	blind = False
##savedir contains the root files for plotting
if presel:
	savedir = predir
	
else:
	savedir = "vbf_2jets/"
	

canvas = ROOT.TCanvas("canvas","canvas",800,800)
p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0.3,1,1)
p_lfv.SetBottomMargin(0.08)
p_lfv.Draw()
p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.3)
p_ratio.SetTopMargin(0.1)
p_ratio.Draw()
#p_ratio.cd()
p_lfv.cd()
LFVStack = ROOT.THStack("stack","")
hgglfv_ntuple_file_str = 'LFV_GluGlu_H2Tau_M-126.root'
hggsm_ntuple_file = ''
hvbflfv_ntuple_file_str = 'LFV_VBF_H2Tau_M-126.root'
zjets_ntuple_file_str = 'Zjets_M50.root'
#wjets_ntuple_file_str = 'WJets.root'
wjets1_ntuple_file_str = 'Wplus1Jets_madgraph.root'
wjets2_ntuple_file_str = 'Wplus2Jets_madgraph.root'
wjets3_ntuple_file_str = 'Wplus3Jets_madgraph.root'
wjets4_ntuple_file_str = 'Wplus4Jets_madgraph.root'

ttbar_ntuple_file_str = 'TTplusJets_madgraph.root'
ww_ntuple_file_str = 'WWJetsTo2L2Nu_TuneZ2_8TeV.root'
data_ntuple_file_str = 'data_2012.root'
hvbfsm_ntuple_file_str = 'VBF_H2Tau_M-125.root'

hgglfv_ntuple_file = ROOT.TFile(savedir+hgglfv_ntuple_file_str)
hvbflfv_ntuple_file = ROOT.TFile(savedir+hvbflfv_ntuple_file_str)
zjets_ntuple_file = ROOT.TFile(savedir+zjets_ntuple_file_str)
wjets1_ntuple_file = ROOT.TFile(savedir+wjets1_ntuple_file_str)
wjets2_ntuple_file = ROOT.TFile(savedir+wjets2_ntuple_file_str)
wjets3_ntuple_file = ROOT.TFile(savedir+wjets3_ntuple_file_str)
wjets4_ntuple_file = ROOT.TFile(savedir+wjets4_ntuple_file_str)
ttbar_ntuple_file = ROOT.TFile(savedir+ttbar_ntuple_file_str)
ww_ntuple_file = ROOT.TFile(savedir+ww_ntuple_file_str)
data_ntuple_file = ROOT.TFile(savedir+data_ntuple_file_str)
hvbfsm_ntuple_file = ROOT.TFile(savedir+hvbfsm_ntuple_file_str)

hgglfv_pre_ntuple_file = ROOT.TFile(predir+hgglfv_ntuple_file_str)
hvbflfv_pre_ntuple_file = ROOT.TFile(predir+hvbflfv_ntuple_file_str)
zjets_pre_ntuple_file = ROOT.TFile(predir+zjets_ntuple_file_str)
wjets1_pre_ntuple_file = ROOT.TFile(predir+wjets1_ntuple_file_str)
wjets2_pre_ntuple_file = ROOT.TFile(predir+wjets2_ntuple_file_str)
wjets3_pre_ntuple_file = ROOT.TFile(predir+wjets3_ntuple_file_str)
wjets4_pre_ntuple_file = ROOT.TFile(predir+wjets4_ntuple_file_str)
ttbar_pre_ntuple_file = ROOT.TFile(predir+ttbar_ntuple_file_str)
ww_pre_ntuple_file = ROOT.TFile(predir+ww_ntuple_file_str)
data_pre_ntuple_file = ROOT.TFile(predir+data_ntuple_file_str)





#get histograms
ntuple_spot = channel
hgglfv_ntuple_file.cd(ntuple_spot)
hgglfv = ROOT.gDirectory.Get(var).Clone()
hvbflfv_ntuple_file.cd(ntuple_spot)
hvbflfv = ROOT.gDirectory.Get(var).Clone()
#hggsm_ntuple_file.cd(hggsm_ntuple_spot)
hvbfsm_ntuple_file.cd(ntuple_spot)
hvbfsm = ROOT.gDirectory.Get(var).Clone()
zjets_ntuple_file.cd(ntuple_spot)
zjets = ROOT.gDirectory.Get(var).Clone()
print zjets.Integral()
wjets1_ntuple_file.cd(ntuple_spot)
wjets1 = ROOT.gDirectory.Get(var).Clone()
wjets2_ntuple_file.cd(ntuple_spot)
wjets2 = ROOT.gDirectory.Get(var).Clone()
wjets3_ntuple_file.cd(ntuple_spot)
wjets3 = ROOT.gDirectory.Get(var).Clone()
wjets4_ntuple_file.cd(ntuple_spot)
wjets4 = ROOT.gDirectory.Get(var).Clone()
ttbar_ntuple_file.cd(ntuple_spot)
ttbar = ROOT.gDirectory.Get(var).Clone()
ww_ntuple_file.cd(ntuple_spot)
ww = ROOT.gDirectory.Get(var).Clone()
data_ntuple_file.cd(ntuple_spot)
data = ROOT.gDirectory.Get(var).Clone()


#define lumicalc files
data1_lumifile = 'lumicalc/data_SingleMu_Run2012A_13Jul2012_v1.lumicalc.sum'
data2_lumifile = 'lumicalc/data_SingleMu_Run2012A_recover_06Aug2012_v1.lumicalc.sum'
data3_lumifile = 'lumicalc/data_SingleMu_Run2012B_22Jan2013_v1.lumicalc.sum'
data4_lumifile = 'lumicalc/data_SingleMu_Run2012C_24Aug2012_v1.lumicalc.sum'
data5_lumifile = 'lumicalc/data_SingleMu_Run2012C_PromptReco_v2.lumicalc.sum'
data6_lumifile = 'lumicalc/data_SingleMu_Run2012D_PromptReco_v1.lumicalc.sum'
wjets_filtered_lumifile = 'lumicalc/WplusJets_madgraph_filtered.lumicalc.sum'
wjets_extension_lumifile = 'lumicalc/WplusJets_madgraph_Extension.lumicalc.sum'
wjets1_lumifile = 'lumicalc/Wplus1Jets_madgraph.lumicalc.sum'
wjets1_ext_lumifile = 'lumicalc/Wplus1Jets_madgraph_extension.lumicalc.sum'
wjets2_lumifile = 'lumicalc/Wplus2Jets_madgraph.lumicalc.sum'
wjets2_ext_lumifile = 'lumicalc/Wplus2Jets_madgraph_extension.lumicalc.sum'
wjets3_lumifile = 'lumicalc/Wplus3Jets_madgraph.lumicalc.sum'
wjets3_ext_lumifile = 'lumicalc/Wplus3Jets_madgraph_extension.lumicalc.sum'
wjets4_lumifile = 'lumicalc/Wplus4Jets_madgraph.lumicalc.sum'
zjets_lumifile = 'lumicalc/Zjets_M50.lumicalc.sum'
tt_lumifile = 'lumicalc/TTplusJets_madgraph.lumicalc.sum'
ww_lumifile = 'lumicalc/WWJetsTo2L2Nu_TuneZ2_8TeV.lumicalc.sum'
hvbflfv_lumifile = 'lumicalc/LFV_VBF_H2Tau_M-126.lumicalc.sum'
hgglfv_lumifile = 'lumicalc/LFV_GluGlu_H2Tau_M-126.lumicalc.sum'
hvbfsm_lumifile = 'lumicalc/VBF_H2Tau_M-125.lumicalc.sum'



#read lumicalc files
f = open(wjets_filtered_lumifile).read().splitlines()
wjets_filtered_efflumi = float(f[0])

f = open(wjets_extension_lumifile).read().splitlines()
wjets_extension_efflumi = float(f[0])

f = open(wjets1_lumifile).read().splitlines()
wjets1_efflumi = float(f[0])

f = open(wjets2_lumifile).read().splitlines()
wjets2_efflumi = float(f[0])

f = open(wjets3_lumifile).read().splitlines()
wjets3_efflumi = float(f[0])

f = open(wjets4_lumifile).read().splitlines()
wjets4_efflumi = float(f[0])

f = open(zjets_lumifile).read().splitlines()
zjets_efflumi = float(f[0])
#print zjets_efflumi

f = open(tt_lumifile).read().splitlines()
tt_efflumi = float(f[0])

f = open(ww_lumifile).read().splitlines()
ww_efflumi = float(f[0])

f = open(hvbflfv_lumifile).read().splitlines()
hvbflfv_efflumi = float(f[0])

f = open(hgglfv_lumifile).read().splitlines()
hgglfv_efflumi = float(f[0])

f = open(hvbfsm_lumifile).read().splitlines()
hvbfsm_efflumi = float(f[0])

f = open(data1_lumifile).read().splitlines()
data1_lumi = float(f[0])

f = open(data2_lumifile).read().splitlines()
data2_lumi = float(f[0])

f = open(data3_lumifile).read().splitlines()
data3_lumi = float(f[0])

f = open(data4_lumifile).read().splitlines()
data4_lumi = float(f[0])

f = open(data5_lumifile).read().splitlines()
data5_lumi = float(f[0])

f = open(data6_lumifile).read().splitlines()
data6_lumi = float(f[0])

lumi = data1_lumi+data2_lumi+data3_lumi+data4_lumi+data5_lumi+data6_lumi
print "lumi:"
print lumi
#print lumi
#print zjets_efflumi
#wjets_efflumi = wjets_filtered_efflumi+wjets1_efflumi+wjets2_efflumi+wjets3_efflumi+wjets4_efflumi
#wjets_efflumi = wjets_extension_efflumi
#wjets_efflumi = wjets_extension_efflumi
#wjets_efflumi= 1580.01
#wjets_efflumi = wjets_extension_efflumi+wjets1_efflumi+wjets2_efflumi+wjets3_efflumi+wjets4_efflumi
#zjets_efflumi = 8505.626
#tt_efflumi = 30529.576
#ww_efflumi = 332328.452161#xsection = 5.82 pb
#smgg_higgs_efflumi = 784763.11 #xsection = 1.23 pb
#hgglfv_efflumi= 509885.536
#hvbflvf_efflumi = 6369426.75159
#lumi = 18025.9 #inverse picobarns

#print lumi
wjets1_datanorm = lumi/wjets1_efflumi
wjets2_datanorm = lumi/wjets2_efflumi
wjets3_datanorm = lumi/wjets3_efflumi
wjets4_datanorm = lumi/wjets4_efflumi
#wjets_datanorm = lumi/wjets_efflumi
zjets_datanorm = lumi/zjets_efflumi
tt_datanorm = lumi/tt_efflumi
ww_datanorm = lumi/ww_efflumi

#print zjets_datanorm
qcd_norm_histo = make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file, wjets1_datanorm, wjets2_datanorm, wjets3_datanorm, wjets4_datanorm, zjets_datanorm, tt_datanorm, ww_datanorm)
#print zjets.Integral()
antiiso_ntuple_spot = "antiisomuon"+channel
data_ntuple_file.cd(antiiso_ntuple_spot)
qcd = ROOT.gDirectory.Get(var).Clone() #get antiisolated qcd shape
if qcd_norm_histo.Integral() < 0:
	qcd.Scale(0)
else:
	qcd.Scale(qcd_norm_histo.Integral()/qcd.Integral()) #normalized qcd shape

if shape_norm == False: #normalize histos to data
	wjets1_norm = wjets1_datanorm
	wjets2_norm = wjets2_datanorm
	wjets3_norm = wjets3_datanorm
        wjets4_norm = wjets4_datanorm
	zjets_norm = zjets_datanorm
	#ttbar_norm = tt_datanorm
	ttbar_norm = tt_datanorm
	ww_norm = ww_datanorm
	#smgg_higgs_norm = lumi/smgg_higgs_efflumi
	hgglfv_norm = lumi/hgglfv_efflumi
	hvbflfv_norm = lumi/hvbflfv_efflumi
	hvbfsm_norm = lumi/hvbfsm_efflumi
	hgglfv.Scale(hgglfv_norm)
	hvbflfv.Scale(hvbflfv_norm)
	hvbfsm.Scale(hvbfsm_norm)
	wjets1.Scale(wjets1_norm)
	wjets2.Scale(wjets2_norm)
        wjets3.Scale(wjets3_norm)
        wjets4.Scale(wjets4_norm)
	wjets1.Add(wjets2)
	wjets1.Add(wjets3)
	wjets1.Add(wjets4)
	ttbar.Scale(ttbar_norm)
        tt_total_norm = ttbar.Integral()
	#ttbar.Add(ttbar_full)
	#ttbar.Scale(tt_total_norm/ttbar.Integral())	
	
else:   	#normailze histos to 1
	wjets1.Add(wjets2)
	wjets1.Add(wjets3)
	wjets1.Add(wjets4)
	wjets_norm = 1/wjets1.Integral()
	zjets_norm = 1/zjets.Integral()
	ttbar_norm = 1/ttbar.Integral()
	ww_norm = 1/ww.Integral()
	hgglfv_norm = 1/(hgglfv.Integral())
	hvbflfv_norm = 1/(hvbflfv.Integral())
	hvbfsm_norm = 1/(hvbfsm.Integral())
	hvbfsm.Scale(hvbfsm_norm)
	hgglfv.Scale(hgglfv_norm)
	hvbflfv.Scale(hvbflfv_norm)
	qcd_norm = 1/(qcd.Integral())
	qcd.Scale(qcd_norm)
	wjets1.Scale(wjets_norm)
	ttbar.Scale(ttbar_norm)

zjets.Scale(zjets_norm)
ww.Scale(ww_norm)

#wjets cross section (cmssw) = 37509.0 pb
#zjets cross section (cmssw) = 3503 pb
#tt cross section (cmssw) = 225.197 pb
#data_vbf.Scale(1.0/data_vbf.Integral())
#data_vbf.SetLineColor(ROOT.EColor.kBlue)
#signal_mc_vbf.SetLineColor(ROOT.EColor.kRed)
hgglfv.SetLineColor(ROOT.EColor.kGreen+3)
hvbflfv.SetLineColor(ROOT.EColor.kRed)
hvbfsm.SetLineColor(ROOT.EColor.kBlue)
wjets1.SetFillColor(ROOT.EColor.kRed-5)
zjets.SetFillColor(ROOT.EColor.kGreen+6)
ttbar.SetFillColor(ROOT.EColor.kOrange-3)
ww.SetFillColor(ROOT.EColor.kYellow-2)
qcd.SetFillColor(ROOT.EColor.kMagenta+3)
wjets1.SetMarkerSize(0)
zjets.SetMarkerSize(0)
ttbar.SetMarkerSize(0)
ww.SetMarkerSize(0)
qcd.SetMarkerSize(0)
hgglfv.SetMarkerSize(0)
hvbflfv.SetMarkerSize(0)
hvbfsm.SetMarkerSize(0)
hgglfv.SetLineWidth(3)
hvbflfv.SetLineWidth(3)
hvbfsm.SetLineWidth(3)
wjets1.Rebin(binwidth)
zjets.Rebin(binwidth)
ttbar.Rebin(binwidth)
ww.Rebin(binwidth)
qcd.Rebin(binwidth)
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hvbfsm.Rebin(binwidth)
data.Rebin(binwidth)
#legend.AddEntry(data_vbf,'Data')
#legend.AddEntry(signal_mc_vbf),'VBF LFV MC')
if shape_norm == False:
	if "gg" in channel:
		legend.AddEntry(hgglfv,'GG LFV Higgs')
	if "vbf" in channel:
		legend.AddEntry(hvbflfv, 'VBF LFV Higgs')
		legend.AddEntry(hvbfsm, 'VBF SM Higgs')

else:
        if "gg" in channel:
                legend.AddEntry(hgglfv,'GG LFV Higgs')
        if "vbf" in channel:
                legend.AddEntry(hvbflfv, 'VBF LFV Higgs')
		legend.AddEntry(hvbfsm, 'VBF SM Higgs')	
legend.AddEntry(wjets1,'W+Jets')
legend.AddEntry(zjets,'Z+Jets')
legend.AddEntry(ttbar,'TT+Jets')
legend.AddEntry(ww,'WW')
legend.AddEntry(qcd,'QCD')
legend.SetFillColor(0)
legend.SetBorderSize(0)
LFVStack.Add(zjets)
LFVStack.Add(ttbar)
#LFVStack.Add(hgglfv)
LFVStack.Add(wjets1)
LFVStack.Add(ww)
LFVStack.Add(qcd)
LFVStack.Draw('hist')
if "gg" in channel:
	hgglfv.Draw('sameshist')
if "vbf" in channel:
	hvbflfv.Draw('sameshist')
	hvbfsm.Draw('sameshist')

maxMC = LFVStack.GetMaximum()
maxData = data.GetMaximum()
if maxData>maxMC and shape_norm == False:
	maxHist = maxData
else:
	maxHist = maxMC
LFVStack.SetMaximum(maxHist*1.05)
print maxHist

if presel == True and shape_norm == False:
	data.Draw("sames")
        legend.AddEntry(data,'8 TeV Data')
elif blind == True and shape_norm == False:
	binblindlow = data.FindBin(blindlow)
	binblindhigh = data.FindBin(blindhigh)
	for x in range(binblindlow, binblindhigh):
		data.SetBinContent(x, -1000)
		
	data.Draw('sames')
	legend.AddEntry(data,'8 TeV Data')	
	pave = ROOT.TPave(blindlow,0,blindhigh,maxHist*1.1,4,"br")
	pave.SetFillColor(1)
	pave.SetFillStyle(3002)
	#pave.SetDrawOption(0)
	pave.SetBorderSize(0)
	pave.Draw()
	
legend.Draw('sames')
LFVStack.GetXaxis().SetTitle(xlabel)
LFVStack.GetYaxis().SetTitleOffset(1.2)
lumifb = '%.2f'%(lumi/1000)
title_str = "\sqrt{8} TeV Collisions  L = " + str(lumifb)+" fb^{-1}      "+ylabel
print title_str
LFVStack.SetTitle(title_str)

#signal to background ratio
maxbin = hvbflfv.GetMaximumBin()
sbratio =hvbflfv.GetBinContent(maxbin)/(ww.GetBinContent(maxbin)+wjets1.GetBinContent(maxbin)+zjets.GetBinContent(maxbin)+ttbar.GetBinContent(maxbin))
print "Signal to Background Ratio: " + str(sbratio)
#p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.3)
#p_ratio.SetTopMargin(0.1)
#p_ratio.Draw()
p_ratio.cd()
ratio = data.Clone()
mc = wjets1.Clone()
mc.Add(zjets)
mc.Add(ttbar)
mc.Add(qcd)
ratio.Divide(mc)
if blindlow != blindhigh:
	ratio.Draw()
ratio.SetTitle("Data:MC Ratio")
ratio.GetYaxis().SetRangeUser(0,5)
if shape_norm == False:
	canvas.SaveAs(savedir+"LFV"+var+".png")
else:
	canvas.SaveAs(savedir+"LFV"+var+"_shape.png")
print "QCD Integral: " + str(qcd.Integral())
print "Z+jets Integral: " + str(zjets.Integral())
print "W+jets Integral: " + str(wjets1.Integral())
