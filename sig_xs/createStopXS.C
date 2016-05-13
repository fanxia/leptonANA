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

  TH1D * h_xsec = new TH1D("xsec", "stop_xsec", 380, 100, 2000);
  h_xsec->Sumw2();

  TH2D * h2_xsec = new TH2D("h2_xsec","stop_bino_xs",380,100,2000,200,0,1000);
  h2_xsec->Sumw2();
  
  TH1D * h_errors = (TH1D*)h_xsec->Clone("errors");

  ifstream fin;
  fin.open("xsec/stop_pair_13TeVxs.dat");

  while(1) {
    int mStop;
    int mBino;
    double xsec, xsecErr;

    fin >> mStop >> xsec >> xsecErr;
    
    if(!fin.good()) break;

    h_xsec->SetBinContent(h_xsec->FindBin(mStop), xsec);
    h_xsec->SetBinError(h_xsec->FindBin(mStop), xsec*xsecErr*0.01);
    h_errors->SetBinContent(h_errors->FindBin(mStop), xsecErr);
  
    for(mBino=0;mBino<mStop;mBino+=5)
      {h2_xsec->SetBinContent(h2_xsec->FindBin(mStop,mBino),xsec);
	if(mBino>1000) break;}

  }
  //  gStyle->SetOptStat(0)
  //gPad->SetLogy()

  fin.close();
  TCanvas *c=new TCanvas("c","c",1000,800);
  TLine * virtualLine = new TLine(100, 100, 1000, 1000);
  virtualLine->SetLineStyle(2);
  virtualLine->SetLineWidth(2);
  TLatex * nlspComment = new TLatex(250, 260, "mStop < mBino");
  nlspComment->SetTextAngle(49);
  nlspComment->SetTextSize(0.02);

  TPaveText *Header = new TPaveText(0.1, 0.901, 0.45, 0.94, "NDC");
  Header->SetFillColor(0);
  Header->SetFillStyle(0);
  Header->SetLineColor(0);
  Header->SetBorderSize(0);
  Header->AddText("pp  #sqrt{s} = 13 TeV  NLO-NLL  ");

  c->SetRightMargin(0.14);
  h2_xsec->Draw("colz");
  h2_xsec->SetTitle(";m_{Stop}[GeV];m_{Bino}[GeV];Cross Section [pb]");
  h2_xsec->SetMinimum(0.0001);
  h2_xsec->SetMaximum(2000);
  h2_xsec->GetXaxis()->SetRangeUser(100,1500);
  h2_xsec->GetXaxis()->SetLabelSize(0.025);
  h2_xsec->GetYaxis()->SetTitleOffset(1.2);
  h2_xsec->GetYaxis()->SetLabelSize(0.025);
  h2_xsec->GetZaxis()->SetTitleOffset(1.0);
  h2_xsec->GetZaxis()->SetLabelSize(0.02);
  gStyle->SetOptStat(0);
  gPad->SetLogz();
  virtualLine->Draw("same");
  nlspComment->Draw("same");
  Header->Draw("same");
  c->Print("stopbinoXS.pdf","pdf");

  c->Clear();
  gPad->SetLogy();
  gPad->SetGrid();
  TH1D * h_xsec2=(TH1D*)h_xsec->Clone("sec");
  h_xsec->Draw("E4");

  h_xsec->SetFillColor(kBlue-10);
 

  h_xsec2->Draw("Hist C same");
  h_xsec2->SetLineColor(kBlue);

  h_xsec->GetXaxis()->SetTitleOffset(1.2);
  h_xsec->GetYaxis()->SetTitleOffset(1.2);
  h_xsec->SetTitle(";m_{Stop}[GeV];Stop pair production #sigma [pb]");

  Header->Draw("same");
  c->Print("stopXS.pdf","pdf");

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
