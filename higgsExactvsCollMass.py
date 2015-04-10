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
legend = ROOT.TLegend(0.55,0.45,0.79,0.97,' ','brNDC')


canvas = ROOT.TCanvas("canvas","canvas",800,800)
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

savedir = "FullHiggsMass_July24/"
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

if channel == "gg0" or channel == "gg1":
	hlfv_ntuple_file_str = hgglfv_ntuple_file_str
else:
	hlfv_ntuple_file_str = hvbflfv_ntuple_file_str

hlfv_ntuple_file = ROOT.TFile(savedir+hlfv_ntuple_file_str+'.root')
hlfvCollMass = hlfv_ntuple_file.Get(channel+"/collMass_type1")
hlfv_lumifile = 'lumicalc_Jan17/'+hlfv_ntuple_file_str+'.lumicalc.sum'
f = open(hlfv_lumifile).read().splitlines()
hlfv_efflumi = float(f[0])
hlfvCollMass.Scale(lumi/hlfv_efflumi)
hlfvCollMass.SetLineColor(ROOT.EColor.kRed)
hlfvCollMass.SetLineWidth(3)
hlfvCollMass.SetMarkerSize(0)
hlfvCollMass.Rebin(binwidth)
hlfvCollMass.Scale(0.1)
hlfvCollMass.Draw("hist")
hlfvCollMass.GetXaxis().SetTitle("M_{#mu#tau} [GeV] ")
yTitle = "Events/"+str(binwidth) +" GeV"
if channel == "gg0":
	legendStr = "0 Jet GGF"
elif channel == "gg1":
	legendStr = "1 Jet GGF"
elif channel == "vbf":
	legendStr = "2 Jet VBF"
hlfvCollMass.GetYaxis().SetTitle(yTitle)
hlfvCollMass.GetXaxis().SetNdivisions(510)
hlfvCollMass.GetXaxis().SetTitleOffset(0.8)
hlfvCollMass.GetXaxis().SetLabelSize(0.035)
hlfvCollMass.GetYaxis().SetTitleOffset(0.8)
hlfvCollMass.GetYaxis().SetLabelSize(0.035)
hlfvCollMass.GetYaxis().SetLabelSize(0.035)
hlfvCollMass.GetXaxis().SetRangeUser(0,300)
legend.AddEntry(hlfvCollMass,legendStr+" LFV CollMass")

hlfvExactMass = hlfv_ntuple_file.Get(channel+"/higgsMass")
hlfvExactMass.Scale(lumi/hlfv_efflumi)
hlfvExactMass.SetLineColor(ROOT.EColor.kBlue)
hlfvExactMass.SetLineWidth(3)
hlfvExactMass.SetMarkerSize(0)
hlfvExactMass.Rebin(binwidth)
hlfvExactMass.Scale(0.1)
hlfvExactMass.Draw("sameshist")
hlfvExactMass.GetXaxis().SetTitle("[GeV] ")
hlfvExactMass.GetXaxis().SetNdivisions(510)
hlfvExactMass.GetXaxis().SetTitleOffset(0.8)
hlfvExactMass.GetXaxis().SetLabelSize(0.035)
hlfvExactMass.GetYaxis().SetLabelSize(0.035)
hlfvExactMass.GetXaxis().SetRangeUser(0,300)
legend.AddEntry(hlfvExactMass,legendStr + " LFV ExactMass")

legend.SetTextSize(0.03)
legend.Draw("sames")
canvas.SaveAs(savedir+"ExactvsCollMass_"+channel+".png")


