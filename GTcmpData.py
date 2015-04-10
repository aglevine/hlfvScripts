from sys import argv
import ROOT


ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)

gt_dir_new = "dataGTcmpNew/"
gt_dir_old = "dataGTcmpOld/"
gt_dir_save = "dataGTcmpPlots/"

gt27_file_str = "data_2012_newGT.root"
gt23_file_str = "data_2012oldGT.root"

file27 = ROOT.TFile(gt_dir_new+gt27_file_str) 
file23 = ROOT.TFile(gt_dir_old+gt23_file_str)


histSpotOld = "gtTest/collMass"
histSpotNew = "gtTest/collMass_type1"

gt23 = file23.Get(histSpotOld)
gt27 = file27.Get(histSpotNew)

gt23.Scale(1/gt23.Integral())
gt27.Scale(1/gt27.Integral())

gt23.Rebin(10)
gt27.Rebin(10)

gt23.SetLineWidth(3)
gt23.SetLineColor(ROOT.EColor.kRed)
gt27.SetLineWidth(3)
gt27.SetLineColor(ROOT.EColor.kBlue)

gt23.Draw("hist")
gt27.Draw("sameshist")

gt23Max = gt23.GetMaximum()
gt27Max = gt27.GetMaximum()

maxHist = max(gt23Max,gt27Max)
maxHist = 1.5*maxHist

gt23.GetYaxis().SetRangeUser(0,maxHist)

xvar = "collMass"
print xvar
gt23.GetXaxis().SetTitle(xvar)

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

legend.AddEntry(gt23,"GT 23 (note tau ID different as well)")
legend.AddEntry(gt27,"GT 27 (note tau ID different as well)")

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)
legend.Draw("sames")

canvas.SaveAs(gt_dir_save+"GTcmp.png")
