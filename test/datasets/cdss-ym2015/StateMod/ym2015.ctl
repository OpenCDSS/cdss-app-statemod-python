#>
#> StateMod Control file(see StateMod documentation)
#>
#> First 2 lines are headers(title, description)
#> Remaining lines use first 8 characters for values.
#>
 YAMPA RIVER BASIN
 Historic Diversions
    1909 : iystr   STARTING YEAR OF SIMULATION
    2013 : iyend   ENDING YEAR OF SIMULATION
       2 : iresop  OUTPUT UNITS 1=cfs,2-acft,3=KAF,4=cfs day acft mon,5=cms
       1 : moneva  TYPE OF EVAP/PRECIP. DATA. 0=monthly, 1=average
       1 : iopflo  TYPE OF STREAM INFLOW. 1=Total, 2=Gains
       0 : numpre  NO. OF PRECIPITATION STATIONS
      12 : numeva  NO. OF EVAPORATION STATIONS
      -1 : interv  INTERVALS IN DELAY TABLE n=fixed, %;-1=var, %; -100=var, dec.
  1.9835 : factor  FACTOR TO CONVERT CFS TO AC-FT/DAY (1.9835)
  1.9835 : rfacto  DIVISOR FOR STREAM FLOW DATA. 0 FOR DATA IN cfs, 1.9835 af/mo
  1.9835 : dfacto  DIVISOR FOR DIVERSION DATA. 0 FOR DATA IN cfs, 1.9835 af/mo
  0.0000 : ffacto  DIVISOR FOR INSTREAM FLOW DATA. 0 FOR DATA IN cfs, 1.9835 af/mo
  1.0000 : cfacto  FACTOR TO CONVERT RESERVOIR CONTENT TO AC-FT
  1.0000 : efacto  FACTOR TO CONVERT EVAPORATION DATA TO FEET
  1.0000 : pfacto  FACTOR TO CONVERT PRECIPITATION DATA TO FEET
  WYR    : cyr1    YEAR TYPE (a5, All caps, right justified!) CYR, WYR, or IYR
       1 : icondem Demand type. 1=HistDem,2=HistSum,3=StrDem,4=SupDem,5=DecDem
       0 : ichk    Detailed print. 0=off,1=net,4=calls,5=dem,6=day,7=ret,91=well,92=soil,-NodeId)
      -1 : ireopx  Reoperation. (0=reoperate,1=no reop,-n=reop for releases>n) 
       1 : ireach  ISF approach. 0=Phase II,1=Phase III,2=0+.ifm,3=1+.ifm
       0 : icall   Detailed call data. 0=no, 1=yes
0               :ccall Detailed call water right ID (if icall != 0)
       0 : iday    Daily calculations. 0=monthly, 1=daily
       0 : iwell   Wells -1=no,in .rsp;0=no;1=no gwmaxrc,2=gwmaxrc,3=var gwmaxrc
     0.0 : gwmaxrc Constanct max recharge, CFS (if iwell=2)
       0 : isjrip  (SJRIP) sediment file. -1=no but in .rsp, 0=no, 1=yes
      10 : itsfile Use *.tsp file -1=no,in .rsp;0=no;1=annual GW lim,10=all data
       1 : ieffmax Use IWR file. -1=no but in .rsp, 0=no, 1=yes
       0 : isprink Use sprinkler data. 0=no, 1=yes
       3 : soild   Soil moist acct. -1=no,.par in .rsp;0=no;+n=soil zone dep,ft
       0 : isig    0=none, 1=one, 2=two
