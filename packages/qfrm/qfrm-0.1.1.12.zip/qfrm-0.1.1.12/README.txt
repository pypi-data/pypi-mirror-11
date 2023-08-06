*****
QFRM, Quantitative Financial Risk Management
*****
QFRM project contains a set of analytical tools to measure, manage and visualize identified risks of financial instruments
and portfolios. We apply `OOP <https://en.wikipedia.org/wiki/Object-oriented_programming>`_ platform
and lots of examples (textbook and otherwise) to ease the use of and learning with our package.

History
---------
This project started as a `QFRM R package <https://cran.r-project.org/web/packages/QFRM/index.html>`_
in Spring 2015 QFRM course (STAT 449 and STAT 649) at Rice University.

Underlying textbook (source of financial calculations and algorithms):
---------
J.C.Hull textbook Options, Futures and other derivatives, 9ed, 2014, ISBN: 0133456315, http://amzn.com/0133456315,
http://www-2.rotman.utoronto.ca/~hull/ofod/index.html

Our Team
=========
These are ambitious and dedicated Rice University science students studying statistics, mathematics, physics, chemistry,
computer science, engineering, and other fields. The doctoral, masters and undergraduate students are united in their work in
QFRM course, led by Oleg Melnikov, a doctoral student and instructor at Stat Dept of Rice U.
#. Oleg Melnikov (author, creator), Department of Statistics, Rice University, Oleg.Rice.edu, <xisreal@gmail.com>
#. TBA
#. ...
#.
#.
#.
#.
#.
#.
#.
#.
#.

Currently implemented:
---------
PVCF, bond analytics (Ch.4) and visualization, calculations are based on time to maturity (not the day count).

Planned implementation:
---------
Fixed income portfolio analytics, exotic option pricing, and visualization.

Install
---------
Directly from PyPI with pip command in a terminal window:

.. code:: bash

    $ pip install yahoo-finance

Typical usage:
---------
Textbook example (default) of 6% SA bond with 2 years/time to maturity (TTM), see p.83 in Hull's OFOD/9ed

.. code:: python

    >>> Bond().analytics()
    ------------------ Bond analytics: ------------------------
    * Annual coupon, $: 6
    * Coupon frequency, p.a.: 2
      Time to maturity (ttm), yrs: 2
    * Cash flows, $ p.a.: (3.0, 3.0, 3.0, 103.0)
      Time to cash flows (ttcf), yrs: (0.5, 1.0, 1.5, 2.0)
      Dirty price (PVCF), $: 98.38506
    * Clean price (PVCF - AI), $: 95.38506
      YTM, CC rate: 0.06762
      YTM, rate at coupon frequency: 0.06878
      Current yield, rate at coupon frequency: 0.0629
    * Par yield, rate at coupon frequency: 0.06873
      Yield curve, CC rate: (0.05, 0.058, 0.064, 0.068)
      Macaulay duration, yrs: 1.91277
      Modified duration, yrs: 1.84917
      Effective duration, yrs: 1.91363
    * Convexity, yrs^2: 3.75368
      Desc: {}
    ------------------------------------------------------------------------------
    Median run time (microsec) for 1 iteration(s): 11788.894628807611

3% annually-paying bond with 3.1 TTM (in years), evaluated at 5% continuously compounded (CC) yield-to-maturity (YTM),
i.e. flat yield curve (YC)

.. code:: python

    >>> Bond(3,1,3.1, pyz=.05).analytics()

.. figure:: ../images/bond_3_1_3.1_pyz_.05.jpg
    :width: 400px
    :align: center
    :height: 300px
    :alt: alternate text
    :figclass: align-center

    figure are like images but with a caption

    and whatever else youwish to add

    .. code-block:: python
        ------------------ Bond analytics: ------------------------
        * Annual coupon, $: 3
        * Coupon frequency, p.a.: 1
          Time to maturity (ttm), yrs: 3.1
        * Cash flows, $ p.a.: (3.0, 3.0, 3.0, 103.0)
          Time to cash flows (ttcf), yrs: (0.10000000000000009, 1.1, 2.1, 3.1)
          Dirty price (PVCF), $: 96.73623
        * Clean price (PVCF - AI), $: 94.03623
          YTM, CC rate: 0.05
          YTM, rate at coupon frequency: 0.05127
          Current yield, rate at coupon frequency: 0.0319
        * Par yield, rate at coupon frequency: 0.03883
          Yield curve, CC rate: (0.05, 0.05, 0.05, 0.05)
          Macaulay duration, yrs: 2.9208
          Modified duration, yrs: 2.77835
          Effective duration, yrs: 2.92126
        * Convexity, yrs^2: 8.92202
          Desc: {}
        ------------------------------------------------------------------------------
        Median run time (microsec) for 1 iteration(s): 11604.918843659107


    # 4% semi-annually (SA) bond with 4.25 ttm (4 years and 3 mo), evaluated at $97.5 PVCF (which computes to 4.86% ytm or flat YC)
    b = Bond(4,2,4.25, pyz=97.5)
    b.ytm()
    b.analytics()
    # The same 4% SA bond evaluated with a specific YC.
    # Zero rates are assumed to have TTM matching those of cash flows (CF), left to right.
    # Insufficient rates are extrapolated with a constant.
    b.set_pyz(pyz=(.05,.06,.07,.08)).analytics()
    # The same 4% SA bond evaluated with a specific YC. User provides zero rates with corresponding TTM.
    # TTM required to evaluate CF are extra/inter-polated from existing curve with constant rates on each side.
    b.set_pyz(pyz=(.05,.06,.04,.03), ttz=(.5,1,2,6)).analytics()


Common acronyms used in documentation
=========
AI: accrued interest
APT: arbitrage pricing theorem
ASP: active server pages (i.e. HTML scripting on server side) by Microsoft
b/w: between
bip: basis points
BM: Brownian motion (aka Wiener Process)
BOPM: binomial option pricing model
bp: basis points
BSM: Black-Scholes model or Black-Scholes-Merton model
c.c.: continuous compounding
CC: continuous compounding
CCP: central counterparty
CCRR: continuously compounded rate of return
CDS: credit default swap
CDO: credit default obligation
CF: cash flows
Cmdt: commodity
Corp: corporate
CP: counterparty
CUSIP: Committee on Uniform Security Identification Procedures , North-American financial security identifier (like ISIN), w
ESO: employee stock option
ETD: exchange-traded derivative
FE: financial engineering
FRA: forward rate agreement
FRN: floating rate notes
Fwd: forward
FX: foreign currency or foreign currency exchange
FV: future value
GBM: geometric Brownian motion
Gvt: government
Hld: holding
IM: initial margin
IR: interest rate
IRD: interest rate derivatives
IRTS: interest rate term structure
ISIN: International Securities Identification Number
LIBID: London Interbank bid rate
LIBOR: London Interbank Offered Rate
MA: margin account; moving average
MC: margin call
Mgt: management
Mkt: market
MM: maintenance margin
MP: Markov process
MTM: marking to market
Mtge: mortgage
MV: multivariate
OFOD: Options, Futures, and Other Derivatives
OFOD9e: Options, Futures, and Other Derivatives, 9th edition
OIS: overnight index SWAP rate
OOP: object oriented programming
p.a.: per annum
PD: probability of default
PDE: partial differential equation
PM: portfolio manager
PORTIA: portfolio accounting system by Thomson Financial
Pts: points
PV: present value
PVCF: present value of cash flows
QFRM: quantitative financial risk management
REPO: Repurchase agreement rate
RFR: risk free rate
RN: risk-neutral
RNW: risk-neutral world
RoI: return on investment
RoR: rate of return
r.v.: random variable
s.a.: semi-annual
SA: semi-annual
SAC: semi-annual compounding
SP: stochastic process
SQL: sequel query language
SQP: standard Wiener process
SURF: step up recovery floaters (floating rate notes)
TBA: to be announced
TBD: To be determined
TOMS: Trade Order Management Solution (or System)
Trx: transaction
TS: time series
TSA: time series analysis
TTCF: time to cash flows
TTM: time to maturity
TVM: time value of money
UDF: user defined function
URL: universe resource locator
VaR: value at risk
Var: variance
VB: Visual Basic (by Microsoft)
VBA: Visual Basic for Applications
Vol: volatility
WAC: weighted-average coupon
WAM: weighted-average maturity
WP: Wiener process (aka Brownian motion)
YC: yield curve
Yld: yield
ZCB: zero coupon bond


