from sys import argv, stdout, stderr
import ROOT
import sys

##Style##
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

if len(argv) < 2:
        print "usage: python plot_mutau variable"
        sys.exit()
var = argv[1]


canvas = ROOT.TCanvas("canvas","canvas",800,800)
tightIso_ntuple_file = ROOT.TFile("MuMuTau_Jan27_Hdfspresel/mmt/preselection/isofalse/AnalyzeMuMuTauTight/datammt_2012.root")
looseIso_ntuple_file = ROOT.TFile("MuMuTau_Jan27_LooseMuIso/mmt/preselection/isofalse/AnalyzeMuMuTauTight/datammt_2012.root")
noIso_ntuple_file = ROOT.TFile("MuMuTau_Jan27_Redo/mmt/preselection/isofalse/AnalyzeMuMuTauTight/datammt_2012.root")

bNum_ntuple_file = ROOT.TFile("MuMuTau_Jan29_tFlavorTest/mmt/preselection/isotrue/AnalyzeMuMuTauTight/Zjetsmmtvbf.root")
bDenom_ntuple_file = ROOT.TFile("MuMuTau_Jan29_tFlavorTest/mmt/preselection/isofalse/AnalyzeMuMuTauTight/Zjetsmmtvbf.root")

bNum = bNum_ntuple_file.Get("vbf/"+var).Clone()
bDenom = bDenom_ntuple_file.Get("vbf/"+var).Clone()

tightIso = tightIso_ntuple_file.Get("vbf/m1_m2_Mass").Clone()
looseIso = looseIso_ntuple_file.Get("vbf/m1_m2_Mass").Clone()
#noIso = noIso_ntuple_file.Get("vbf/m1_m2_Mass").Clone()
noIso = noIso_ntuple_file.Get("vbf/m1_m2_Mass").Clone()

#print noIso.Integral(noIso.FindBin(0.12),noIso.FindBin(1.0))

#tightIso.Scale(1/tightIso.Integral())
#looseIso.Scale(1/looseIso.Integral())
#noIso.Scale(1/noIso.Integral())

tightIso.SetLineColor(ROOT.EColor.kBlue+1)
looseIso.SetLineColor(ROOT.EColor.kGreen+1)
noIso.SetLineColor(ROOT.EColor.kRed+1)
bDenom.SetLineColor(ROOT.EColor.kBlue+1)
bNum.SetLineColor(ROOT.EColor.kRed+1)
bDenom.SetLineWidth(3)
bNum.SetLineWidth(3)
bDenom.SetMarkerSize(0)
bNum.SetMarkerSize(0)
tightIso.SetMarkerSize(0)
looseIso.SetMarkerSize(0)
noIso.SetMarkerSize(0)

#bDenom.Scale(1/bDenom.Integral())
#bNum.Scale(1/bNum.Integral())
bRatio = bNum.Clone()
bRatio.Divide(bDenom)
print bRatio.Integral()/bRatio.GetEntries()
#bRatio.Rebin(11)
#noIso.Draw('hist')
#tightIso.Draw('sameshist')
#looseIso.Draw('sameshist')

#bNum.Draw('histo')
#bDenom.Draw('sameshist')
bRatio.Draw('histo')

#noIso.GetXaxis().SetRangeUser(I0,.0)
noIso.GetXaxis().SetTitle(var)
noIso.GetYaxis().SetLabelSize(0.04)

legend = ROOT.TLegend(0.75,0.6,0.8,0.9,'','brNDC')
legend.SetTextSize(0.02)
#legend.AddEntry(tightIso,"0.12 Mu Isolation")
#legend.AddEntry(looseIso,"0.2 Mu Isolation")
#legend.AddEntry(noIso,"No Mu Isolation")

#legend.AddEntry(bDenom,"IsoFalse")
#legend.AddEntry(bNum,"IsoTrue")
legend.AddEntry(bRatio,"Ratio")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.Draw('sames')

canvas.SaveAs(var+"cmpRatio.png")
