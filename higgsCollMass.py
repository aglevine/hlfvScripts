from sys import argv, stdout, stderr
import ROOT
import sys
import math
import array
import numpy

def draw_histo(histo_file_name,histo_name,channel,color,legend,savedir):

	histo_file = ROOT.TFile(savedir+histo_file_name+'.root')
	histo = histo_file.Get(channel+"/collMass_type1")
	histo_lumifile = 'lumicalc_Jan17/'+histo_file_name+'.lumicalc.sum'
	
	f = open(histo_lumifile).read().splitlines()
	histo_efflumi = float(f[0])
	lumi = 19712.0604555
	histo.Scale(lumi/histo_efflumi)
	#colorString = "ROOT.EColor.k"+color
	#color_t = (Color_t) colorString
	histo.SetLineColor(ROOT.EColor.kRed)
	histo.SetLineWidth(3)
	histo.SetMarkerSize(0)
	legend.AddEntry(histo)
	print histo.GetEntries()
	print histo.Integral()
	histo.Rebin(10)
	histo.Draw("sameshist")
	

	


ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

channel = argv[1]
doLog = True
legend = ROOT.TLegend(0.65,0.45,0.89,0.97,' ','brNDC')


canvas = ROOT.TCanvas("canvas","canvas",800,800)
if doLog == True:
	canvas.SetLogy()
hgglfv_ntuple_file_str = 'LFV_GluGlu_Dec9'
hvbflfv_ntuple_file_str = 'LFV_VBF_Dec9'
hggsm_ntuple_file_str = 'GGH_H2Tau_M-125'
hvbfsm_ntuple_file_str = 'VBF_H2Tau_M-125'
hvbfww_ntuple_file_str = 'HiggsToWWVBF125'
hggww_ntuple_file_str = 'HiggsToWWGG125'
vhsm_ntuple_file_str = 'VH_H2Tau_M-125'
vhlfv_ntuple_file_str = 'LFV_VH_H2MuTau_LONG-MuTauMC'
hwwvhtth_ntuple_file_str = 'HWWVHTTH125'

binning = [5,100,150]
lumi = 19712.0604555
if channel == "gg0" or channel == "gg1":
        binwidth = 10
else:
        binwidth = 50

#frame = ROOT.TH1F('frame','frame',*binning)
#frame.Draw()
#frame.SetTitle('')
savedir = "jesnonesignalJune18_VHVV/"
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

hgglfv_ntuple_file = ROOT.TFile(savedir+hgglfv_ntuple_file_str+'.root')
hgglfv = hgglfv_ntuple_file.Get(channel+"/collMass_type1")
hgglfv_lumifile = 'lumicalc_Jan17/'+hgglfv_ntuple_file_str+'.lumicalc.sum'
f = open(hgglfv_lumifile).read().splitlines()
hgglfv_efflumi = float(f[0])
hgglfv.Scale(lumi/hgglfv_efflumi)
hgglfv.SetLineColor(ROOT.EColor.kRed)
hgglfv.SetLineWidth(3)
hgglfv.SetMarkerSize(0)
hgglfv.Rebin(binwidth)
hgglfv.Scale(0.1)
hgglfv.Draw("hist")
hgglfv.GetXaxis().SetTitle("Coll Mass_{#mu#tau_{h}} [GeV]")
hgglfv.GetXaxis().SetNdivisions(510)
hgglfv.GetXaxis().SetTitleOffset(0.8)
hgglfv.GetXaxis().SetLabelSize(0.035)
hgglfv.GetYaxis().SetLabelSize(0.035)
hgglfv.GetXaxis().SetRangeUser(0,300)
legend.AddEntry(hgglfv,"GGF LFV Higgs")

hvbflfv_ntuple_file = ROOT.TFile(savedir+hvbflfv_ntuple_file_str+'.root')
hvbflfv = hvbflfv_ntuple_file.Get(channel+"/collMass_type1")
hvbflfv_lumifile = 'lumicalc_Jan17/'+hvbflfv_ntuple_file_str+'.lumicalc.sum'
f = open(hvbflfv_lumifile).read().splitlines()
hvbflfv_efflumi = float(f[0])
hvbflfv.Scale(lumi/hvbflfv_efflumi)
hvbflfv.SetLineColor(ROOT.EColor.kGray+3)
hvbflfv.SetLineWidth(3)
hvbflfv.SetMarkerSize(0)
hvbflfv.Rebin(binwidth)
hvbflfv.Scale(0.1)
hvbflfv.Draw("sameshist")
legend.AddEntry(hvbflfv,"VBF LFV Higgs")

maxHisto = max(hgglfv.GetMaximum(),hvbflfv.GetMaximum())
hgglfv.SetMaximum(1.1*maxHisto)

hggsm_ntuple_file = ROOT.TFile(savedir+hggsm_ntuple_file_str+'.root')
hggsm = hggsm_ntuple_file.Get(channel+"/collMass_type1")
hggsm_lumifile = 'lumicalc_Jan17/'+hggsm_ntuple_file_str+'.lumicalc.sum'
f = open(hggsm_lumifile).read().splitlines()
hggsm_efflumi = float(f[0])
hggsm.Scale(lumi/hggsm_efflumi)
hggsm.SetLineColor(ROOT.EColor.kBlue)
hggsm.SetLineWidth(3)
hggsm.SetMarkerSize(0)
hggsm.Rebin(binwidth)
hggsm.Draw("sameshist")
legend.AddEntry(hggsm,"GGF H #rightarrow #tau#tau")

hvbfsm_ntuple_file = ROOT.TFile(savedir+hvbfsm_ntuple_file_str+'.root')
hvbfsm = hvbfsm_ntuple_file.Get(channel+"/collMass_type1")
hvbfsm_lumifile = 'lumicalc_Jan17/'+hvbfsm_ntuple_file_str+'.lumicalc.sum'
f = open(hvbfsm_lumifile).read().splitlines()
hvbfsm_efflumi = float(f[0])
hvbfsm.Scale(lumi/hvbfsm_efflumi)
hvbfsm.SetLineColor(ROOT.EColor.kCyan-3)
hvbfsm.SetLineWidth(3)
hvbfsm.SetMarkerSize(0)
hvbfsm.Rebin(binwidth)
hvbfsm.Draw("sameshist")
legend.AddEntry(hvbfsm,"VBF H #rightarrow #tau#tau")

hvbfww_ntuple_file = ROOT.TFile(savedir+hvbfww_ntuple_file_str+'.root')
hvbfww = hvbfww_ntuple_file.Get(channel+"/collMass_type1")
hvbfww_lumifile = 'lumicalc_Jan17/'+hvbfww_ntuple_file_str+'.lumicalc.sum'
f = open(hvbfww_lumifile).read().splitlines()
hvbfww_efflumi = float(f[0])
hvbfww.Scale(lumi/hvbfww_efflumi)
hvbfww.SetLineColor(ROOT.EColor.kGreen-3)
hvbfww.SetLineWidth(3)
hvbfww.SetMarkerSize(0)
hvbfww.Rebin(binwidth)
hvbfww.Draw("sameshist")
legend.AddEntry(hvbfww,"VBF H #rightarrow WW")

hggww_ntuple_file = ROOT.TFile(savedir+hggww_ntuple_file_str+'.root')
hggww = hggww_ntuple_file.Get(channel+"/collMass_type1")
hggww_lumifile = 'lumicalc_Jan17/'+hggww_ntuple_file_str+'.lumicalc.sum'
f = open(hggww_lumifile).read().splitlines()
hggww_efflumi = float(f[0])
hggww.Scale(lumi/hggww_efflumi)
hggww.SetLineColor(ROOT.EColor.kMagenta+3)
hggww.SetLineWidth(3)
hggww.SetMarkerSize(0)
hggww.Rebin(binwidth)
hggww.Draw("sameshist")
legend.AddEntry(hggww,"GG H #rightarrow WW")

vhsm_ntuple_file = ROOT.TFile(savedir+vhsm_ntuple_file_str+'.root')
vhsm = vhsm_ntuple_file.Get(channel+"/collMass_type1")
vhsm_lumifile = 'lumicalc_Jan17/'+vhsm_ntuple_file_str+'.lumicalc.sum'
f = open(vhsm_lumifile).read().splitlines()
vhsm_efflumi = float(f[0])
vhsm.Scale(lumi/vhsm_efflumi)
vhsm.SetLineColor(ROOT.EColor.kYellow+3)
vhsm.SetLineWidth(3)
vhsm.SetMarkerSize(0)
vhsm.Rebin(binwidth)
vhsm.SetLineStyle(ROOT.kDashed)
vhsm.Draw("sameshist")
legend.AddEntry(vhsm,"WH/ZH/TTH #rightarrow #tau#tau")

vhlfv_ntuple_file = ROOT.TFile(savedir+vhlfv_ntuple_file_str+'.root')
vhlfv = vhlfv_ntuple_file.Get(channel+"/collMass_type1")
vhlfv_lumifile = 'lumicalc_Jan17/'+vhlfv_ntuple_file_str+'.lumicalc.sum'
f = open(vhlfv_lumifile).read().splitlines()
vhlfv_efflumi = float(f[0])
vhlfv.Scale(lumi/vhlfv_efflumi)
vhlfv.SetLineColor(ROOT.EColor.kViolet-3)
vhlfv.SetLineWidth(3)
vhlfv.SetMarkerSize(0)
vhlfv.Rebin(binwidth)
vhlfv.SetLineStyle(ROOT.kDashed)
vhlfv.Draw("sameshist")
legend.AddEntry(vhlfv,"LFV VH")

hwwvhtth_ntuple_file = ROOT.TFile(savedir+hwwvhtth_ntuple_file_str+'.root')
hwwvhtth = hwwvhtth_ntuple_file.Get(channel+"/collMass_type1")
hwwvhtth_lumifile = 'lumicalc_Jan17/'+hwwvhtth_ntuple_file_str+'.lumicalc.sum'
f = open(hwwvhtth_lumifile).read().splitlines()
hwwvhtth_efflumi = float(f[0])
hwwvhtth.Scale(lumi/hwwvhtth_efflumi)
hwwvhtth.SetLineColor(ROOT.EColor.kOrange+3)
hwwvhtth.SetLineWidth(3)
hwwvhtth.SetMarkerSize(0)
hwwvhtth.Rebin(binwidth)
hwwvhtth.Draw("sameshist")
legend.AddEntry(hwwvhtth,"WH/ZH/TTH #rightarrow WW")

legend.Draw("sames")
if doLog == False:
	canvas.SaveAs(savedir+"Higgs_Masses_"+channel+"_noLog.png")
else:
   	canvas.SaveAs(savedir+"Higgs_Masses_"+channel+".png")


