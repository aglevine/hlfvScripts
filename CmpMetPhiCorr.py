from sys import argv, stdout, stderr
import getopt
import ROOT


channel = argv[1]
var = argv[2]

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)
if "gg" in channel:
	signalFile_str= "LFV_GluGlu_Dec9"
	binWidth = 10
elif "vbf" in channel:
	signalFile_str = "LFV_VBF_Dec9"
	binWidth = 50
oldir = "jespfMetOct7/"
newdir = "newMetPhiCorr/"


signalOldFile = ROOT.TFile(oldir+signalFile_str+".root")
signalNewFile = ROOT.TFile(newdir+signalFile_str+".root")

signalOld = signalOldFile.Get(channel+"/"+var).Clone()
signalNew = signalNewFile.Get(channel+"/"+var).Clone()

lumidirOld = "lumicalc_jes/"
lumidirNew = "lumicalc_newMETPhiCorr/"

lumi_str = signalFile_str

lumifileOld = lumidirOld+lumi_str+".lumicalc.sum"
lumifileNew = lumidirNew+lumi_str+".lumicalc.sum"

f= open(lumifileOld).read().splitlines()
efflumiOld = float(f[0])

u = open(lumifileNew).read().splitlines()
efflumiNew = float(u[0])
lumi = 19712.0604555


signalOld.Scale(lumi/efflumiOld)
signalNew.Scale(lumi/efflumiNew)

signalOld.Rebin(binWidth)
signalNew.Rebin(binWidth)

signalOld.Draw("hist")
signalNew.Draw("sameshist")

signalOld.SetLineWidth(3)
signalOld.SetLineColor(ROOT.EColor.kRed)
signalNew.SetLineWidth(3)
signalNew.SetLineColor(ROOT.EColor.kBlue)

signalOldMax = signalOld.GetMaximum()
signalNewMax = signalNew.GetMaximum()

signalMax = max(signalOldMax,signalNewMax)
signalMax = signalMax*1.5

signalOld.GetYaxis().SetRangeUser(0,signalMax)

signalNew.GetXaxis().SetTitle(var)

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

legend.AddEntry(signalNew,"LFV"+channel+"After Met x-y Fix")
legend.AddEntry(signalOld,"LFV"+channel+"Before Met x-y Fix")

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

legend.Draw("sames")

canvas.SaveAs("newMetPhiCorr/NewPhiCorrVsOld_"+channel+"_"+var+".png")






















