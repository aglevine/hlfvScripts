
from sys import argv, stdout, stderr
import ROOT
import sys

##get qcd (choose selections for qcd)

def make_qcd(presel, var, predir, savedir, channel ,wjets_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file):

        qcd_final = get_ss_inc_qcd(var,channel, wjets_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file)  ##gets same sign inclusive qcd
        qcd_final.Scale(1.06) ##os inclusive qcd 
	print qcd_final.Integral()
	if not presel:
     		ssanti_iso_ntuple_spot = "ssantiisomuon"+channel
        	data_ntuple_file.cd(ssanti_iso_ntuple_spot)
        	qcd_antiiso_ss = ROOT.gDirectory.Get(var).Clone()
        	data_pre_ntuple_file.cd(ssanti_iso_ntuple_spot)
        	qcd_antiiso_ss_inc = ROOT.gDirectory.Get(var).Clone()
        	qcd_final.Multiply(qcd_antiiso_ss)
        	qcd_final.Divide(qcd_antiiso_ss_inc)
		print "wtf"

        return qcd_final



def get_ss_inc_qcd(var,channel, wjets_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file):

	ss_ntuple_spot = "ss"+channel
	zjets_pre_ntuple_file.cd(ss_ntuple_spot)
	zjets_pre = ROOT.gDirectory.Get(var).Clone()
	ttbar_pre_ntuple_file.cd(ss_ntuple_spot)
	ttbar_pre = ROOT.gDirectory.Get(var).Clone()
	ww_pre_ntuple_file.cd(ss_ntuple_spot)
	ww_pre = ROOT.gDirectory.Get(var).Clone()
	data_pre_ntuple_file.cd(ss_ntuple_spot)
	qcd_ss_inc = ROOT.gDirectory.Get(var).Clone()
	qcd_ss_inc.Add(zjets_pre,-1)
	qcd_ss_inc.Add(ttbar_pre,-1)
	qcd_ss_inc.Add(ww_pre,-1)
	wjets_pre = get_w(var,ss_ntuple_spot,wjets_pre_ntuple_file,zjets_pre_ntuple_file,ttbar_pre_ntuple_file,ww_pre_ntuple_file,data_pre_ntuple_file) #returns w+jets estimation
	print wjets_pre.Integral()
	qcd_ss_inc.Add(wjets_pre,-1)
	print qcd_ss_inc.Integral()
	return qcd_ss_inc

	

def get_w(var,ss_ntuple_spot, wjets_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file):

	ss_highmt_ntuple_spot = "highMt"+ss_ntuple_spot
	data_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
	wjets_ss_inc = ROOT.gDirectory.Get(var).Clone() #data_ss_highmt
	zjets_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        zjets_ss_highmt = ROOT.gDirectory.Get(var).Clone()
        ttbar_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        ttbar_ss_highmt = ROOT.gDirectory.Get(var).Clone()
        ww_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
        ww_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	wjets_pre_ntuple_file.cd(ss_highmt_ntuple_spot)
	wjets_mc_ss_highmt = ROOT.gDirectory.Get(var).Clone()
	wjets_pre_ntuple_file.cd(ss_ntuple_spot)
	wjets_mc_ss = ROOT.gDirectory.Get(var).Clone()
	
	wjets_ss_inc.Add(zjets_ss_highmt,-1)
	wjets_ss_inc.Add(ttbar_ss_highmt,-1)
	wjets_ss_inc.Add(ww_ss_highmt,-1) ##w_data_ss_highmt_
	wjets_ss_inc.Multiply(wjets_mc_ss)
	wjets_ss_inc.Divide(wjets_mc_ss_highmt)
	print wjets_ss_inc.Integral()
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
## axis labels
binwidth = 5
if var == "mPt":
	xlabel = "#mu P_{T} (GeV)"
	binwidth = 10
	legend =ROOT.TLegend(0.55,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel +" 10 GeV binning"
elif var == "tPt":
	xlabel = "#tau P_{T} (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 5 GeV binning"
elif var == "mEta":
	xlabel = "#mu #eta"
	legend =ROOT.TLegend(0.2,0.6,0.4,0.8,'','brNDC')
	binwidth = 10
	ylabel = ynormlabel
elif var == "tEta":
	xlabel = "#tau #eta"
	legend =ROOT.TLegend(0.7,0.65,0.9,0.88,'','brNDC')
	binwidth = 10
	ylabel = ynormlabel
elif var == "mMtToPfMet_Ty1":
	xlabel = "#mu M_{T} Ty1 (GeV)"
	binwidth = 10
	ylabel = ynormlabel + " 10 GeV binning"
	legend =ROOT.TLegend(0.55,0.6,0.8,0.8,'','brNDC')
elif var == "tMtToPfMet_Ty1":
	xlabel = "#tau M_{T} Ty1 (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 5 GeV binning"
elif var == "vbfDeta":
	xlabel = "#Delta#eta_{jj}"
	legend =ROOT.TLegend(0.6,0.6,0.9,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
elif var == "vbfDijetrap":
	xlabel ="Rapidity_{jj}"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
elif var == "vbfDphihjnomet":
	xlabel = "#Delta#phi_{Hj} (no MET)"
	legend =ROOT.TLegend(0.2,0.6,0.5,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
elif var == "vbfDphihj":
	xlabel = "#Delta#phi_{Hj}"
	legend =ROOT.TLegend(0.2,0.6,0.5,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
elif var == "vbfHrap":
	xlabel = "Rapidity_{H}"
	legend =ROOT.TLegend(0.4,0.6,0.89,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
elif var == "vbfj1eta":
	xlabel = "#eta_{j1}"
	binwidth = 10
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
elif var == "vbfj2eta":
	xlabel = "#eta_{j2}"
	binwidth = 10
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
elif var == "vbfMass":
	xlabel = "M_{jj} (GeV)"
	binwidth = 10
	legend =ROOT.TLegend(0.15,0.6,0.45,0.8,'','brNDC')
	ylabel = ynormlabel + " 50 GeV binning"
elif var == "vbfMVA":
	xlabel = "MVAMET (GeV)"
	ylabel = ynormlabel
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
elif var == "vbfVispt":
	xlabel = "Visible P_{T} (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + " 10 GeV binning"
elif var == "m_t_Mass":
	xlabel = "Visible Mass (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + "10 GeV binning"
	binwidth = 10
elif var == "m_t_DPhi":
	xlabel = "#mu #tau #Delta#phi"
	legend = ROOT.TLegend(0.25,0.6,0.6,0.8,'','brNDC')
	ylabel = ynormlabel
elif var == "m_t_Pt":
	xlabel = "Visible P_{T} (GeV)"
	legend = ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + "10 GeV binning"
	binwidth = 10
elif var == "m_t_DR":
	xlabel = "#mu #tau #DeltaR"
	legend = ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
elif var == "m_t_ToMETDPhi_Ty1":
	xlabel = "#Delta#phi (MET , #mu#tau)"
	legend = ROOT.TLegend(0.15,0.7,0.4,0.87,'','brNDC')
	ylabel = ynormlabel
	binwidth = 10
else:
	xlabel = var
	binwidth = 5
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
predir = "presel_highmt/"
channel = "vbf"
presel = False
if presel:
	savedir = predir
else:
	savedir = "vbf_qcd/"

canvas = ROOT.TCanvas("canvas","canvas",800,800)
LFVStack = ROOT.THStack("stack","")
gg_lfv_higgs_ntuple_file_str = 'LFV_GluGlu_H2Tau_M-126.root'
gg_sm_higgs_ntuple_file = ''
vbf_lfv_higgs_ntuple_file_str = 'LFV_VBF_H2Tau_M-126.root'
zjets_ntuple_file_str = 'Zjets_M50.root'
wjets_ntuple_file_str = 'WplusJets_madgraph_Extension.root'
ttbar_ntuple_file_str = 'TTplusJets_madgraph.root'
ww_ntuple_file_str = 'WWJetsTo2L2Nu_TuneZ2_8TeV.root'
data_ntuple_file_str = 'data_2012.root'

gg_lfv_higgs_ntuple_file = ROOT.TFile(savedir+gg_lfv_higgs_ntuple_file_str)
vbf_lfv_higgs_ntuple_file = ROOT.TFile(savedir+vbf_lfv_higgs_ntuple_file_str)
zjets_ntuple_file = ROOT.TFile(savedir+zjets_ntuple_file_str)
wjets_ntuple_file = ROOT.TFile(savedir+wjets_ntuple_file_str)
ttbar_ntuple_file = ROOT.TFile(savedir+ttbar_ntuple_file_str)
ww_ntuple_file = ROOT.TFile(savedir+ww_ntuple_file_str)
data_ntuple_file = ROOT.TFile(savedir+data_ntuple_file_str)
gg_lfv_higgs_pre_ntuple_file = ROOT.TFile(predir+gg_lfv_higgs_ntuple_file_str)
vbf_lfv_higgs_pre_ntuple_file = ROOT.TFile(predir+vbf_lfv_higgs_ntuple_file_str)
zjets_pre_ntuple_file = ROOT.TFile(predir+zjets_ntuple_file_str)
wjets_pre_ntuple_file = ROOT.TFile(predir+wjets_ntuple_file_str)
ttbar_pre_ntuple_file = ROOT.TFile(predir+ttbar_ntuple_file_str)
ww_pre_ntuple_file = ROOT.TFile(predir+ww_ntuple_file_str)
data_pre_ntuple_file = ROOT.TFile(predir+data_ntuple_file_str)

qcd = make_qcd(presel, var, predir, savedir, channel ,wjets_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file)
qcd.Scale(1.06)
print qcd.Integral()

ntuple_spot = channel
gg_lfv_higgs_ntuple_file.cd(ntuple_spot)
gg_lfv_higgs = ROOT.gDirectory.Get(var).Clone()
vbf_lfv_higgs_ntuple_file.cd(ntuple_spot)
vbf_lfv_higgs = ROOT.gDirectory.Get(var).Clone()
#gg_sm_higgs_ntuple_file.cd(gg_sm_higgs_ntuple_spot)
zjets_ntuple_file.cd(ntuple_spot)
zjets = ROOT.gDirectory.Get(var).Clone()
wjets_ntuple_file.cd(ntuple_spot)
wjets = ROOT.gDirectory.Get(var).Clone()
ttbar_ntuple_file.cd(ntuple_spot)
ttbar = ROOT.gDirectory.Get(var).Clone()
ww_ntuple_file.cd(ntuple_spot)
ww = ROOT.gDirectory.Get(var).Clone()

data_ntuple_file.cd(ntuple_spot)
data = ROOT.gDirectory.Get(var).Clone()

wjets_efflumi= 1580.01
zjets_efflumi = 8505.626
tt_efflumi = 30529.576
ww_efflumi = 332328.452161#xsection = 5.82 pb
smgg_higgs_efflumi = 784763.11 #xsection = 1.23 pb
gg_lfv_higgs_efflumi= 509885.536
vbf_lfv_higgs_efflumi = 6369426.75159
lumi = 18025.9 #inverse picobarns
if shape_norm == False:
	wjets_norm = lumi/wjets_efflumi
	zjets_norm = lumi/zjets_efflumi
	tt_norm = lumi/tt_efflumi
	ww_norm = lumi/ww_efflumi
	smgg_higgs_norm = lumi/smgg_higgs_efflumi
	gg_lfv_higgs_norm = lumi/gg_lfv_higgs_efflumi
	vbf_lfv_higgs_norm = lumi/vbf_lfv_higgs_efflumi
	gg_lfv_higgs.Scale(0.5*gg_lfv_higgs_norm)
	vbf_lfv_higgs.Scale(0.5*vbf_lfv_higgs_norm)
else:
	wjets_norm = 1/wjets.Integral()
	zjets_norm = 1/zjets.Integral()
	tt_norm = 1/ttbar.Integral()
	ww_norm = 1/ww.Integral()
	gg_lfv_higgs_norm = 1/(gg_lfv_higgs.Integral())
	vbf_lfv_higgs_norm = 1/(vbf_lfv_higgs.Integral())
	gg_lfv_higgs.Scale(gg_lfv_higgs_norm)
	vbf_lfv_higgs.Scale(vbf_lfv_higgs_norm)
	qcd_norm = 1/(qcd.Integral())
	qcd.Scale(qcd_norm)

zjets.Scale(zjets_norm)
wjets.Scale(wjets_norm)
ttbar.Scale(tt_norm)
ww.Scale(ww_norm)

#wjets cross section (cmssw) = 37509.0 pb
#zjets cross section (cmssw) = 3503 pb
#tt cross section (cmssw) = 225.197 pb
#data_vbf.Scale(1.0/data_vbf.Integral())
#data_vbf.SetLineColor(ROOT.EColor.kBlue)
#signal_mc_vbf.SetLineColor(ROOT.EColor.kRed)
gg_lfv_higgs.SetLineColor(ROOT.EColor.kBlue)
vbf_lfv_higgs.SetLineColor(ROOT.EColor.kRed)
wjets.SetFillColor(ROOT.EColor.kRed-5)
zjets.SetFillColor(ROOT.EColor.kGreen+6)
ttbar.SetFillColor(ROOT.EColor.kOrange-3)
ww.SetFillColor(ROOT.EColor.kYellow-2)
qcd.SetFillColor(ROOT.EColor.kMagenta+3)
wjets.SetMarkerSize(0)
zjets.SetMarkerSize(0)
ttbar.SetMarkerSize(0)
ww.SetMarkerSize(0)
qcd.SetMarkerSize(0)
gg_lfv_higgs.SetMarkerSize(0)
vbf_lfv_higgs.SetMarkerSize(0)
gg_lfv_higgs.SetLineWidth(3)
vbf_lfv_higgs.SetLineWidth(3)
wjets.Rebin(binwidth)
zjets.Rebin(binwidth)
ttbar.Rebin(binwidth)
ww.Rebin(binwidth)
qcd.Rebin(binwidth)
gg_lfv_higgs.Rebin(binwidth)
vbf_lfv_higgs.Rebin(binwidth)
data.Rebin(binwidth)
#legend.AddEntry(data_vbf,'Data')
#legend.AddEntry(signal_mc_vbf),'VBF LFV MC')
if shape_norm == False:
	if "gg" in channel:
		legend.AddEntry(gg_lfv_higgs,'5 X GG LFV Higgs')
	if "vbf" in channel:
		legend.AddEntry(vbf_lfv_higgs, '5 X VBF LFV Higgs')
else:
        if "gg" in channel:
                legend.AddEntry(gg_lfv_higgs,'GG LFV Higgs')
        if "vbf" in channel:
                legend.AddEntry(vbf_lfv_higgs, 'VBF LFV Higgs')	
legend.AddEntry(wjets,'W+Jets')
legend.AddEntry(zjets,'Z+Jets')
legend.AddEntry(ttbar,'TT+Jets')
legend.AddEntry(ww,'WW')
legend.AddEntry(qcd,'QCD')
if presel == True:
	legend.AddEntry(data,'Data')
legend.SetFillColor(0)
legend.SetBorderSize(0)
LFVStack.Add(zjets)
LFVStack.Add(ttbar)
#LFVStack.Add(gg_lfv_higgs)
LFVStack.Add(wjets)
LFVStack.Add(ww)
LFVStack.Add(qcd)
LFVStack.Draw('hist')
if presel == True:
	data.Draw('sames')
#gg_lfv_higgs.Draw('lSames')
#wjets.Draw('lsames')
#zjets.Draw('lsames')
#ttbar.Draw('lsames')
#data.Draw('sames')
if "gg" in channel:
	gg_lfv_higgs.Draw('sameshist')
if "vbf" in channel:
	vbf_lfv_higgs.Draw('sameshist')
legend.Draw('sames')
LFVStack.GetXaxis().SetTitle(xlabel)
LFVStack.GetYaxis().SetTitleOffset(1.2)
LFVStack.SetTitle("\sqrt{8} TeV Collisions  L = 18.03 fb^{-1}      "+ylabel)
#LFVStack.GetYaxis().SetTitle(ylabel)
if shape_norm == False:
	canvas.SaveAs(savedir+"/LFV"+var+".png")
else:
	canvas.SaveAs(savedir+"/LFV"+var+"_shape.png")

