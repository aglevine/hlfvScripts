from sys import argv
import ROOT

channel = argv[1]
sample = "fakes"

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)

signal_dir = "jesnonesignalJune18_VHVV/"
signalFile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone.root" 

#signal_dir = "jespfMetOct7/"
#signalFile_str = "LFV_" + channel+"_collMass_fakeRate_zjetsEmbed_newSignal.root"

before_dir_down = "fakeShapeShiftDown_May7/"
#before_dir_down = "FakesLowFixedMetjes_Oct20/"
beforeDownFile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal.root"
#beforeDownFile_str = "LFV_" + channel+"_collMass_fakeRate_zjetsEmbed_newSignal.root"

before_dir_up ="fakeShapeShiftUp_May7/"
#before_dir_up = "FakesHighFixedMetjes_Oct20/"
beforeUpFile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal.root"
#beforeUpFile_str = "LFV_" + channel+"_collMass_fakeRate_zjetsEmbed_newSignal.root"

signalFile = ROOT.TFile(signal_dir+signalFile_str)
beforeDownFile = ROOT.TFile(before_dir_down+beforeDownFile_str)
beforeUpFile = ROOT.TFile(before_dir_up+beforeUpFile_str)

histSpot = "vbfmutau/"+sample

signalSample = signalFile.Get(histSpot)
beforeDownSample = beforeDownFile.Get(histSpot)
beforeUpSample = beforeUpFile.Get(histSpot)

signalSample.Scale(1/signalSample.Integral())
beforeDownSample.Scale(1/beforeDownSample.Integral())
beforeUpSample.Scale(1/beforeUpSample.Integral())

signalSample.Draw("hist")
beforeDownSample.Draw("sameshist")
beforeUpSample.Draw("sameshist")

signalSample.SetLineWidth(3)
signalSample.SetLineColor(ROOT.EColor.kRed)
beforeDownSample.SetLineWidth(3)
beforeDownSample.SetLineColor(ROOT.EColor.kBlue)
beforeUpSample.SetLineWidth(3)
beforeUpSample.SetLineColor(ROOT.EColor.kGreen+3)

signalSampleMax =  signalSample.GetMaximum()
beforeDownSampleMax = beforeDownSample.GetMaximum()
beforeUpSampleMax = beforeUpSample.GetMaximum()

maxHist = max(signalSampleMax, beforeDownSampleMax, beforeUpSampleMax)
maxHist = maxHist*1.5
signalSample.GetYaxis().SetRangeUser(0,maxHist)
#if channel == "vbf":
#	afterSample.GetYaxis().SetRangeUser(0,0.75)
#else:
#	afterSample.GetYaxis().SetRangeUser(0,0.25)
signalSample.GetXaxis().SetTitle("Type 1 CollMass [GeV]")

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

legend.AddEntry(signalSample,sample+" Before MET Fix, "+channel)
legend.AddEntry(beforeDownSample,sample+" Down Before MET Fix, "+channel)
legend.AddEntry(beforeUpSample,sample+" Up Before MET Fix, "+channel)

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

legend.Draw("sames")

canvas.SaveAs("jespfMetOct7/METBeforeBeforeFakeShapeCmp_"+sample+"_"+channel+"_.png")


