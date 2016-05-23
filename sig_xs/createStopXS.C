// This script to plot stop pair Xsec and stop-bino Xsec for 13 TeV
// in root, .x createStopXS.C

void createStopXS() {

  TFile * fOut = new TFile("stop-bino_xsecs.root", "RECREATE");

    Double_t mst_bins[29] = {110, 160, 185, 210, 235, 260, 285, 310, 335, 360, 385, 410, 460, 510, 560, 610, 660, 710, 810, 910, 1010, 1110, 1210, 1310, 1410, 1510, 1710, 2010, 5010};
   Double_t mBino_bins[31] = {25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 375, 425, 475, 525, 575, 625, 675, 725, 825, 925, 1025, 1125, 1225, 1325, 1425, 1525, 1725, 2025};

   Double_t xbins[31];
   xbins[0] = 0;
   xbins[1] = 55;
  for(int i = 1; i < 29; i++) xbins[i+1] = (mst_bins[i] + mst_bins[i-1])/2.;
  xbins[30] = 6510;

   Double_t ybins[33];
  ybins[0] = 0;
  ybins[1] = 12.5;
  for(int i = 1; i < 31; i++) ybins[i+1] = (mBino_bins[i] + mBino_bins[i-1])/2.;
  ybins[32] = 2175;

  //TH2D * h_real_xsec = new TH2D("real_xsec", "real_xsec", 30, xbins, 32, ybins);
  //h_real_xsec->Sumw2();

  //TH2D * h_real_errors = (TH2D*)h_real_xsec->Clone("real_errors");

  TH1D * h_xsec8 = new TH1D("xsec8", "stop_xsec8", 380, 100, 2000);
  h_xsec8->Sumw2();
  TH1D * h_xsec13 = new TH1D("xsec13", "stop_xsec13", 380, 100, 2000);
  h_xsec13->Sumw2();

  TH2D * h2_xsec8 = new TH2D("h2_xsec8","stop_bino_xs8",380,100,2000,200,0,1000);
  h2_xsec8->Sumw2();
  TH2D * h2_xsec13 = new TH2D("h2_xsec13","stop_bino_xs13",380,100,2000,200,0,1000);
  h2_xsec13->Sumw2();
  TH1D * h_errors8 = (TH1D*)h_xsec8->Clone("errors");
  TH1D * h_errors13 = (TH1D*)h_xsec13->Clone("errors");

  ifstream fin8;
  fin8.open("xsec/stop_pair_8TeVxs.dat");
  ifstream fin13;
  fin13.open("xsec/stop_pair_13TeVxs.dat");

  while(1) {
    int mStop;
    int mBino;
    double xsec, xsecErr;

    fin13 >> mStop >> xsec >> xsecErr;
    
    if(!fin13.good()) break;

    h_xsec13->SetBinContent(h_xsec13->FindBin(mStop), xsec);
    h_xsec13->SetBinError(h_xsec13->FindBin(mStop), xsec*xsecErr*0.01);
    h_errors13->SetBinContent(h_errors13->FindBin(mStop), xsecErr);
  
    for(mBino=0;mBino<mStop;mBino+=5)
      {h2_xsec13->SetBinContent(h2_xsec13->FindBin(mStop,mBino),xsec);
	if(mBino>1000) break;}

  }
while(1) {
    int mStop;
    int mBino;
    double xsec, xsecErr;
    fin8 >> mStop >> xsec >> xsecErr;
    
    if(!fin8.good()) break;

    h_xsec8->SetBinContent(h_xsec8->FindBin(mStop), xsec);
    h_xsec8->SetBinError(h_xsec8->FindBin(mStop), xsec*xsecErr*0.01);
    h_errors8->SetBinContent(h_errors8->FindBin(mStop), xsecErr);
  
    for(mBino=0;mBino<mStop;mBino+=5)
      {h2_xsec8->SetBinContent(h2_xsec8->FindBin(mStop,mBino),xsec);
	if(mBino>1000) break;}

  }
  
 //  gStyle->SetOptStat(0)
  //gPad->SetLogy()

  fin8.close();
  fin13.close();
  TCanvas *c=new TCanvas("c","c",1000,800);
  TLine * virtualLine = new TLine(100, 100, 1000, 1000);
  virtualLine->SetLineStyle(2);
  virtualLine->SetLineWidth(2);
  TLatex * nlspComment = new TLatex(250, 260, "mStop < mBino");
  nlspComment->SetTextAngle(49);
  nlspComment->SetTextSize(0.02);

  TPaveText *Header13 = new TPaveText(0.1, 0.901, 0.45, 0.94, "NDC");
  Header13->SetFillColor(0);
  Header13->SetFillStyle(0);
  Header13->SetLineColor(0);
  Header13->SetBorderSize(0);
  Header13->AddText("pp  #sqrt{s} = 13 TeV  NLO-NLL  ");

  TPaveText *Header8 = new TPaveText(0.1, 0.901, 0.45, 0.94, "NDC");
  Header8->SetFillColor(0);
  Header8->SetFillStyle(0);
  Header8->SetLineColor(0);
  Header8->SetBorderSize(0);
  Header8->AddText("pp  #sqrt{s} = 8 TeV  NLO-NLL  ");

  c->SetRightMargin(0.14);
  h2_xsec13->Draw("colz");
  h2_xsec13->SetTitle(";m_{Stop}[GeV];m_{Bino}[GeV];Cross Section [pb]");
  h2_xsec13->SetMinimum(0.000008);
  h2_xsec13->SetMaximum(2000);
  h2_xsec13->GetXaxis()->SetRangeUser(100,1400);
  h2_xsec13->GetXaxis()->SetLabelSize(0.025);
  h2_xsec13->GetYaxis()->SetTitleOffset(1.2);
  h2_xsec13->GetYaxis()->SetLabelSize(0.025);
  h2_xsec13->GetZaxis()->SetTitleOffset(1.0);
  h2_xsec13->GetZaxis()->SetLabelSize(0.02);
  gStyle->SetOptStat(0);
  gPad->SetLogz();
  virtualLine->Draw("same");
  nlspComment->Draw("same");
  Header13->Draw("same");
  c->Print("xsec.pdf(");

  c->Clear();
  gPad->SetLogy();
  gPad->SetGrid();
  TH1D * h_xsec13_2=(TH1D*)h_xsec13->Clone("sec");
  h_xsec13->Draw("E4");
  h_xsec13->SetMaximum(3000);
  h_xsec13->SetFillColor(kBlue-10);
 

  h_xsec13_2->Draw("Hist C same");
  h_xsec13_2->SetLineColor(kBlue);

  h_xsec13->GetXaxis()->SetTitleOffset(1.2);
  h_xsec13->GetYaxis()->SetTitleOffset(1.2);
  h_xsec13->SetTitle(";m_{Stop}[GeV];Stop pair production #sigma [pb]");

  Header13->Draw("same");
  c->Print("xsec.pdf");


  c->Clear();
  c->SetRightMargin(0.14);
  gPad->SetLogy(0);
  gPad->SetGrid(0,0);
  h2_xsec8->Draw("colz");
  h2_xsec8->SetTitle(";m_{Stop}[GeV];m_{Bino}[GeV];Cross Section [pb]");
  h2_xsec8->SetMinimum(0.000008);
  h2_xsec8->SetMaximum(2000);
  h2_xsec8->GetXaxis()->SetRangeUser(100,1400);
  h2_xsec8->GetXaxis()->SetLabelSize(0.025);
  h2_xsec8->GetYaxis()->SetTitleOffset(1.2);
  h2_xsec8->GetYaxis()->SetLabelSize(0.025);
  h2_xsec8->GetZaxis()->SetTitleOffset(1.0);
  h2_xsec8->GetZaxis()->SetLabelSize(0.02);
  gStyle->SetOptStat(0);
  gPad->SetLogz();
  virtualLine->Draw("same");
  nlspComment->Draw("same");
  Header8->Draw("same");
  c->Print("xsec.pdf");

  c->Clear();
  gPad->SetLogy();
  gPad->SetGrid();
  TH1D * h_xsec8_2=(TH1D*)h_xsec8->Clone("sec");
  h_xsec8->Draw("E4");
  h_xsec8->SetMaximum(3000);
  h_xsec8->SetFillColor(kRed-10);
 

  h_xsec8_2->Draw("Hist C same");
  h_xsec8_2->SetLineColor(kRed);

  h_xsec8->GetXaxis()->SetTitleOffset(1.2);
  h_xsec8->GetYaxis()->SetTitleOffset(1.2);
  h_xsec8->SetTitle(";m_{Stop}[GeV];Stop pair production #sigma [pb]");

  Header8->Draw("same");
  c->Print("xsec.pdf");

  //combine 8 and 13 TeV cross section
  c->Clear();
  TLegend *leg=new TLegend(0.7,0.75,0.85,0.9);

  gPad->SetLogy();
  gPad->SetGrid();
  h_xsec8->Draw("E4");
  h_xsec8->SetFillColor(kRed-10);
  h_xsec13->Draw("E4 same");
  h_xsec13->SetFillColor(kBlue-10);
  h_xsec13_2->Draw("Hist C same");
  h_xsec13_2->SetLineColor(kBlue);
  leg->AddEntry(h_xsec13_2,"pp 13TeV NLO","l");

  h_xsec8_2->Draw("Hist C same");
  h_xsec8_2->SetLineColor(kRed);
  leg->AddEntry(h_xsec8_2,"pp 8TeV NLO","l");
  leg->Draw();
  h_xsec8->GetXaxis()->SetTitleOffset(1.2);
  h_xsec8->GetYaxis()->SetTitleOffset(1.2);
  h_xsec8->SetTitle(";m_{Stop}[GeV];Stop pair production #sigma [pb]");
  c->Print("xsec.pdf)");


  /*
  fin.open("crossSections/realStopMass.dat");

  while(1) {
    int mStop, mBino;
    double realMass;

    fin >> mStop >> mBino >> realMass;

    if(!fin.good()) break;

    if(mBino > mStop) continue;

    int bin = h_xsec->FindBin(realMass);

    double xsec_left = h_xsec->GetBinContent(bin);
    double error_left = h_errors->GetBinContent(bin);

    double xsec_right = h_xsec->GetBinContent(bin + 1);
    double error_right = h_errors->GetBinContent(bin + 1);

    double left = h_xsec->GetBinLowEdge(bin);
    double right = h_xsec->GetBinLowEdge(bin + 1);

    double alpha = (realMass - left) / (right - left);
    double beta = (right - realMass) / (right - left);

    double xsec = alpha * xsec_right + beta * xsec_left;
    double error = alpha * error_right + beta * error_left;

    h_real_xsec->SetBinContent(h_real_xsec->FindBin(mStop, mBino), xsec);
    h_real_errors->SetBinContent(h_real_errors->FindBin(mStop, mBino), error);
  }

  fin.close();
  */
  fOut->Write();
  fOut->Close();

}
