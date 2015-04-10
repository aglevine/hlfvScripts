from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import numpy
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

fileFit = ROOT.TFile("ForAaron_fakes_tJetPt.root")
ntupleFit = fileFit.Get("datacorHisto_Ratio").Clone()
fit = ntupleFit.Fit("pol1","","",30.0,230.0)
canvas = ROOT.TCanvas("canvas","canvas",800,800)
ntupleFit.GetYaxis().SetTitle("Fake Rate Factor")
ntupleFit.GetYaxis().SetTitleOffset(0.9)
ntupleFit.GetYaxis().SetLabelSize(0.035)
ntupleFit.GetYaxis().SetTitleSize(0.05)
ntupleFit.GetXaxis().SetTitleOffset(0.9)
ntupleFit.GetXaxis().SetLabelSize(0.035)
ntupleFit.GetXaxis().SetTitleSize(0.05)
ntupleFit.GetXaxis().SetTitle("Tau Jet Pt")
ntupleFit.Draw()
canvas.SaveAs("FakeFitLine.png")
