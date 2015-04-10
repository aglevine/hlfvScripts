from sys import argv
import ROOT

channel = argv[1]
sample = argv[2]

ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


canvas = ROOT.TCanvas("canvas","canvas",800,800)

after_dir = "jespfMetOct7/"
#afterFile_str = nonefile_str = "LFV_" + channel+"_collMass_fakeRate_zjetsEmbed_newSignal.root"
afterFile_str = nonefile_str = "LFV_" + channel+"_pfMetEt_fakeRate_zjetsEmbed_newSignal.root"

before_dir = "jesnonesignalJune18_VHVV/"
#beforeFile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone_singletfix.root"
beforeFile_str = "LFV_" + channel+"_type1_pfMetEt_fakeRate_zjetsEmbed_newSignal_jesnone.root"

afterFile = ROOT.TFile(after_dir+afterFile_str)
beforeFile = ROOT.TFile(before_dir+beforeFile_str)

histSpot = "vbfmutau/"+sample

afterSample = afterFile.Get(histSpot)
beforeSample = beforeFile.Get(histSpot)

afterSample.Scale(1/afterSample.Integral())
beforeSample.Scale(1/beforeSample.Integral())

afterSample.Draw("hist")
beforeSample.Draw("sameshist")

afterSample.SetLineWidth(3)
afterSample.SetLineColor(ROOT.EColor.kRed)
beforeSample.SetLineWidth(3)
beforeSample.SetLineColor(ROOT.EColor.kBlue)

afterSampleMax =  afterSample.GetMaximum()
beforeSampleMax = beforeSample.GetMaximum()

maxHist = max(afterSampleMax, beforeSampleMax)
maxHist = maxHist*1.5
afterSample.GetYaxis().SetRangeUser(0,maxHist)
#if channel == "vbf":
#	afterSample.GetYaxis().SetRangeUser(0,0.75)
#else:
#	afterSample.GetYaxis().SetRangeUser(0,0.25)
#afterSample.GetXaxis().SetTitle("Collinear Mass [GeV]")
afterSample.GetXaxis().SetTitle("PF MET [GeV]")

legend = ROOT.TLegend(0.43,0.60,0.93,0.97,' ','brNDC')

if channel == "vbf":
	channel_str = "2 Jet"
elif channel == "gg1":
	channel_str = "1 Jet"
elif channel == "gg0":
	channel_str = "0 Jet"

legend.AddEntry(afterSample,sample+" After MET Fix, "+channel_str)
legend.AddEntry(beforeSample,sample+" Before MET Fix, "+channel_str)

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)
legend.Draw("sames")

canvas.SaveAs("jespfMetOct7/METBeforeAfterCmp_pfMet_"+sample+"_"+channel+"_.png")
#canvas.SaveAs("jespfMetOct7/METBeforeAfterCmp_collMass_"+sample+"_"+channel+"_.png")


