from sys import argv
import ROOT

channel = argv[1]

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)

data_file = ROOT.TFile("April22SSFakesSideband_Presel/data_2012.root") 


if "gg0" in channel:
	histSpotOSAntiIso = "antiisotaugg0/collMass"
	histSpotSSAntiIso = "antiisotaussgg0/collMass"
	osaiLegend = "0 Jet Region III"
	ssaiLegend = "0 Jet Region IV"
elif "gg1" in channel:
        histSpotOSAntiIso = "antiisotaugg1/collMass"
        histSpotSSAntiIso = "antiisotaussgg1/collMass"
        osaiLegend = "1 Jet Region III"
        ssaiLegend = "1 Jet Region IV"

elif "vbf" in channel:
        histSpotOSAntiIso = "antiisotauvbf/collMass"
        histSpotSSAntiIso = "antiisotaussvbf/collMass"
        osaiLegend = "2 Jet Region III"
        ssaiLegend = "2 Jet Region IV"


osai = data_file.Get(histSpotOSAntiIso)
ssai = data_file.Get(histSpotSSAntiIso)

osai.Scale(1/osai.Integral())
ssai.Scale(1/ssai.Integral())

osai.Rebin(10)
ssai.Rebin(10)

osai.SetLineWidth(3)
osai.SetLineColor(ROOT.EColor.kRed)
ssai.SetLineWidth(3)
ssai.SetLineColor(ROOT.EColor.kBlue)

osai.Draw("hist")
ssai.Draw("sameshist")

osaiMax = osai.GetMaximum()
ssaiMax = ssai.GetMaximum()

maxHist = max(osaiMax,ssaiMax)
maxHist = 1.5*maxHist

osai.GetYaxis().SetRangeUser(0,maxHist)

xvar = "collMass"
print xvar
osai.GetXaxis().SetTitle("CollMass_{#mu#tau_{h}} [GeV]")
osai.GetXaxis().SetLabelSize(0.04)
osai.GetXaxis().SetTitleSize(0.04)
osai.GetXaxis().SetTitleOffset(1.1)
osai.GetYaxis().SetLabelSize(0.03)
osai.GetYaxis().SetTitle("Normalized Events/10 GeV")
osai.GetYaxis().SetTitleSize(0.03)
osai.GetYaxis().SetTitleOffset(1.7)
osai.SetTitle("")

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

legend.AddEntry(osai,osaiLegend)
legend.AddEntry(ssai,ssaiLegend)

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)
legend.Draw("sames")

canvas.SaveAs("April22SSFakesSideband_Presel/Presel_RegionIIIvsIV_"+channel+".png")
