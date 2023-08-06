insheet using GDP.csv, clear

gen gdp = log(value)

gen tq = qofd(date(date, "YMD"))
format tq %tq
tsset tq

arima gdp, arima(1,1,1) vce(oim)

insheet using FEDFUNDS.csv, clear

gen ffr = log(value)

gen tm = mofd(date(date, "YMD"))
format tm %tm
tsset tm

arima ffr, arima(1,1,1) vce(oim)

// Estimate via a state-space model
constraint 1 [D.ffr]u1 = 1
constraint 2 [u2]L.u1 = 1
constraint 3 [u3]L.u2 = 1

sspace (u1 L.u1 L.u2 L.u3, state noconstant) ///
       (u2 L.u1, state noconstant noerror) ///
       (u3 L.u2, state noconstant noerror) ///
       (D.ffr u1, noconstant noerror), ///
       constraints(1/3) covstate(diagonal)

insheet using NorwayFinland.csv, clear
yofd(date(v1, "YMD"))
tsset date
