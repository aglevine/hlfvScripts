'''
Makes Gen Level LFV plots
Author: Aaron Levine
'''
from sys import argv, stdout, stderr
import ROOT
import sys
plotReco = True
ntupleStr = argv[1]
var = argv[2]
if "GGF" in ntupleStr:
	channel = "GGF"
if "VBF" in ntupleStr:
	channel = "VBF"
if "VH" in ntupleStr:
	channel = "VH"
if "ele" in var:
	cutStr = "((pdgId==11 && motherPdgId==15)||(pdgId==-11 && motherPdgId==-15))&&(status==1)" #electron from tau
if "mu" in var:
	cutStr = "(abs(pdgId)==13 && motherPdgId==25 && status == 1)" #muon from higgs
if "tau" in var: 
	cutStr = "(abs(pdgId)==15 && motherPdgId==25 && status == 2)" #tau from Higgs
if "higgs" in var:
	cutStr = "(pdgId==25&&status==62)" #higgs from ggf/vbf/vh
if "Pt" in var:
	varKin = "pt"
	binning = [20,0,500]
if "Eta" in var:
	varKin = "eta"
	binning = [24,-6,6]
if "Phi" in var:
	varKin = "phi"
	binning = [14,-3.5,3.5]
if plotReco == False:
	saveStr = "GenLevelFiles_Feb10/GENCmp_HToMuTau_"+channel+"_"+var
else:
	saveStr = "GenLevelFiles_Feb10/GENtoRECOCmp_HToMuTau_"+channel+"_"+var

ntuple_file13 = ROOT.TFile(ntupleStr+"_13TeV.root")
ntuple_file13_reco = ROOT.TFile(ntupleStr+"_13TeVRECO.root")
ntuple_file8 = ROOT.TFile(ntupleStr+"_8TeV.root")
ntuple_spot = 'BasicGenInfo/Ntuple'

ntuple13 = ntuple_file13.Get(ntuple_spot)
ntuple13reco = ntuple_file13_reco.Get(ntuple_spot)
ntuple8 = ntuple_file8.Get(ntuple_spot)

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

tex = ROOT.TLatex()
tex.SetTextSize(0.07)
tex.SetTextAlign(11)
tex.SetNDC(True)

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)

drawStr = "%s >>htemp(%s)" % (varKin, ", ".join(str(x) for x in binning))

ntuple13.Draw(drawStr, cutStr, "goff")
histo13 = ROOT.gDirectory.Get("htemp").Clone()
histo13.GetXaxis().SetTitle(var)

ntuple13reco.Draw(drawStr, cutStr, "goff")
histo13reco = ROOT.gDirectory.Get("htemp").Clone()
histo13reco.GetXaxis().SetTitle(var)

ntuple8.Draw(drawStr, cutStr, "goff")
histo8 = ROOT.gDirectory.Get("htemp").Clone()
histo8.GetXaxis().SetTitle(var)

histo13.Sumw2()
histo13reco.Sumw2()
histo8.Sumw2()

histo13.Scale(1/histo13.Integral())
histo13reco.Scale(1/histo13reco.Integral())
histo8.Scale(1/histo8.Integral())

max13 = histo13.GetMaximum()
max13reco = histo13reco.GetMaximum()
max8 = histo8.GetMaximum()

if plotReco == False:
	maxHisto = max(max13,max8)
else:
	maxHisto = max(max13,max13reco)

histo13.SetLineColor(ROOT.EColor.kBlue)
histo13.SetLineWidth(2)
histo13.Draw("histE1")
histo13.GetYaxis().SetRangeUser(0,1.1*maxHisto)
if plotReco == False:
	histo13.SetTitle("13 TeV vs 8 TeV MuTau"+channel)
else:
	histo13.SetTitle("13 TeV: Gen vs Reco MuTau"+channel)

histo13reco.SetLineColor(ROOT.EColor.kRed)
histo13reco.SetLineWidth(2)


histo8.SetLineColor(ROOT.EColor.kRed)
histo8.SetLineWidth(2)

if plotReco==False:
	histo8.Draw("sameshistE1")
else:
	histo13reco.Draw("sameshistE1")



legend = ROOT.TLegend(0.65,0.55,0.85,0.65,'','brNDC')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)

legend.AddEntry(histo13,"13 TeV")
if plotReco == False:
	legend.AddEntry(histo8,"8 TeV")
else:
	legend.AddEntry(histo13reco,"13 TeV Reco")

legend.Draw("sames")

canvas.SaveAs(saveStr+".png")



