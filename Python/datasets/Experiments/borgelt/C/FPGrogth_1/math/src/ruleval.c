/*----------------------------------------------------------------------
  File    : ruleval.c
  Contents: rule evaluation measures
  Author  : Christian Borgelt
  History : 2011.07.22 file created from apriori.c
            2011.08.03 bug in re_fetprob fixed (roundoff error corr.)
            2012.02.15 function re_supp() added (rule support)
            2013.03.29 adapted to type changes in module tract (SUPP)
            2022.11.22 imbalance ratio and Kulczynski measure added
----------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <assert.h>
#include "gamma.h"
#include "chi2.h"
#include "ruleval.h"

#ifndef INFINITY
#define INFINITY    (DBL_MAX+DBL_MAX)
#endif                          /* in case C99 is not supported */

/*----------------------------------------------------------------------
  Preprocessor Definitions
----------------------------------------------------------------------*/
#define LN_2        0.69314718055994530942  /* ln(2) */

/*----------------------------------------------------------------------
  Type Definitions
----------------------------------------------------------------------*/
typedef struct {                /* --- rule evaluation info. --- */
  RULEVALFN *fn;                /* evaluation function */
  int       dir;                /* evaluation direction */
  int       chr;                /* indication character */
  char      *desc;              /* measure description */
} REINFO;                       /* (rule evaluation information) */

/*----------------------------------------------------------------------
  Rule Evaluation Measures
----------------------------------------------------------------------*/

double re_none (SUPP supp, SUPP body, SUPP head, SUPP base)
{ return 0; }                   /* --- no measure / constant zero */

/*--------------------------------------------------------------------*/

double re_supp (SUPP supp, SUPP body, SUPP head, SUPP base)
{ return (double)supp; }        /* --- rule support (body and head) */

/*--------------------------------------------------------------------*/

double re_conf (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- rule confidence */
  return (body > 0) ? (double)supp/(double)body : 0;
}  /* re_conf() */

/*--------------------------------------------------------------------*/

double re_confdiff (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- absolute confidence difference */
  if ((body <= 0) || (base <= 0)) return 0;
  return fabs((double)supp/(double)body -(double)head/(double)base);
}  /* re_confdiff() */

/*--------------------------------------------------------------------*/

double re_lift (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- lift value */
  if ((body <= 0) || (head <= 0)) return 0;
  return ((double)supp*(double)base) /((double)body*(double)head);
  /* =   ((double)supp/(double)body) /((double)head/(double)base) */
}  /* re_lift() */

/*--------------------------------------------------------------------*/

double re_liftdiff (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- abs. difference of lift to 1 */
  if ((body <= 0) || (head <= 0)) return 0;
  return fabs(((double)supp*(double)base)
             /((double)body*(double)head) -1);
}  /* re_liftdiff() */

/*--------------------------------------------------------------------*/

double re_liftquot (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- diff. of lift quotient to 1 */
  double t;                     /* temporary buffer */

  if ((body <= 0) || (head <= 0)) return 0;
  t = ((double)supp*(double)base) /((double)body*(double)head);
  return 1 -((t > 1) ? 1/t : t);
}  /* re_liftquot() */

/*--------------------------------------------------------------------*/

double re_cvct (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- conviction */
  if ((base <= 0) || (body <= supp)) return 0;
  return ((double)body*(double)(base-head))
       / ((double)(body-supp)*(double)base);
  /*   = ((double)body/(double)(body-supp))
       * ((double)(base-head)/(double)base); */
}  /* re_cvct() */

/*--------------------------------------------------------------------*/

double re_cvctdiff (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- abs. diff. of conviction to 1 */
  if (base <= 0)    return 0;
  if (body <= supp) return INFINITY;
  return fabs(((double)body*(double)(base-head))
             /((double)(body-supp)*(double)base)-1);
}  /* re_cvctdiff() */

/*--------------------------------------------------------------------*/

double re_cvctquot (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- diff. of conviction quot. to 1 */
  double t;                     /* temporary buffer */
  if (base <= 0)    return 0;
  if (body <= supp) return INFINITY;
  t = ((double)body*(double)(base-head))
     /((double)(body-supp)*(double)base);
  return 1 -((t > 1) ? 1/t : t);
}  /* re_cvctquot() */

/*--------------------------------------------------------------------*/

double re_imbal (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- imbalance ratio */
  double d = body +head -supp;  /* support of disjunction */
  if (d <= 0) return INFINITY;  /* avoid division by zero */
  return (double)abs(head -body) /d;
}  /* re_imbal() */

/*--------------------------------------------------------------------*/

double re_kulc (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Kulczynski measure */
  if ((body <= 0) || (head <= 0)) return INFINITY;
  return 0.5 *supp *(1.0/(double)body +1.0/(double)head);
}  /* re_kulc() */

/*--------------------------------------------------------------------*/

double re_kulcdiff (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- diff. of Kulczynski m. to 0.5 */
  if ((body <= 0) || (head <= 0)) return INFINITY;
  return fabs(supp *(1.0/(double)body +1.0/(double)head) -1);
}  /* re_kulcdiff() */

/*--------------------------------------------------------------------*/

double re_cprob (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- conditional probability ratio */
  if ((supp <= 0) || (body <= 0) || (base <= body)) return 0;
  if (head <= supp) return INFINITY;
  return ((double)supp*(double)(base-body))
       / ((double)body*(double)(head-supp));
}  /* re_cprob() */

/*--------------------------------------------------------------------*/

double re_import (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- importance */
  double r;                     /* conditional probability ratio */

  if ((supp <= 0) || (body <= 0) || (base <= body)) return 0;
  if (head <= supp) return INFINITY;
  r = ((double)supp*(double)(base-body))
    / ((double)body*(double)(head-supp));
  return (r > 0) ? log(r)/LN_2 : 0;
}  /* re_import() */

/*--------------------------------------------------------------------*/

double re_cert (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- certainty factor */
  double n, p;                  /* temporary buffers */

  if ((body <= 0) || (base <= 0)) return 0;
  p = (double)head/(double)base; n = (double)supp/(double)body -p;
  return n / ((n >= 0) ? 1-p : p);
}  /* re_cert() */

/*--------------------------------------------------------------------*/

double re_chi2 (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- normalized chi^2 measure */
  double t;                     /* temporary buffer */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 0;                   /* check for non-vanishing marginals */
  t = (double)head *(double)body -(double)supp *(double)base;
  return (t*t) /(((double)head)*(double)(base-head)
                *((double)body)*(double)(base-body));
}  /* re_chi2() */              /* compute and return chi^2 measure */

/*--------------------------------------------------------------------*/

double re_chi2pval (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- p-value from chi^2 measure */
  return chi2cdfQ((double)base *re_chi2(supp, body, head, base), 1);
}  /* re_chi2pval() */

/*--------------------------------------------------------------------*/

double re_yates (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Yates corrected chi^2 measure */
  double t;                     /* temporary buffer */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 0;                   /* check for non-vanishing marginals */
  t = fabs((double)head *(double)body -(double)supp *(double)base)
    - 0.5*(double)base;
  return (t*t) /(((double)head)*(double)(base-head)
                *((double)body)*(double)(base-body));
}  /* re_yates() */             /* compute and return chi^2 measure */

/*--------------------------------------------------------------------*/

double re_yatespval (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- p-value from chi^2 measure */
  return chi2cdfQ((double)base *re_yates(supp, body, head, base), 1);
}  /* re_yatespval() */

/*--------------------------------------------------------------------*/

double re_info (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- information diff. to prior */
  double sum, t;                /* result, temporary buffer */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 0;                   /* check for strict positivity */
  t = (double)supp; sum = 0;
  if (t > 0)                    /* support of     head and     body */
    sum += t *log(t /((double)      head  *(double)      body ));
  t = (double)(body -supp);
  if (t > 0)                    /* support of not head and     body */
    sum += t *log(t /((double)(base-head) *(double)      body ));
  t = (double)(head -supp);
  if (t > 0)                    /* support of     head and not body */
    sum += t *log(t /((double)      head  *(double)(base-body)));
  t = (double)(base -head -body +supp);
  if (t > 0)                    /* support of not head and not body */
    sum += t *log(t /((double)(base-head) *(double)(base-body)));
  return (log((double)base) +sum/(double)base) /LN_2;
}  /* re_info() */              /* return information gain in bits */

/*--------------------------------------------------------------------*/

double re_infopval (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- p-value from G statistic */
  return chi2cdfQ(2*LN_2 *(double)base
                  *re_info(supp, body, head, base), 1);
}  /* re_infopval() */

/*--------------------------------------------------------------------*/

double re_fetprob (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Fisher's exact test (prob.) */
  SUPP   rest, n;               /* counter for rest cases, buffer */
  double com;                   /* common probability term */
  double cut, p;                /* (cutoff value for) probability */
  double sum;                   /* probability sum of conting. tables */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 1;                   /* check for non-vanishing marginals */
  rest = base -head -body;      /* compute number of rest cases */
  if (rest < 0) {               /* if rest cases are less than supp, */
    supp -= rest = -rest;       /* exchange rows and exchange columns */
    body  = base -body; head = base -head;
  }                             /* complement/exchange the marginals */
  if (head < body) {            /* ensure that body <= head */
    n = head; head = body; body = n; }
  com = logGamma((double)(     head+1))
      + logGamma((double)(     body+1))
      + logGamma((double)(base-head+1))
      + logGamma((double)(base-body+1))
      - logGamma((double)(base+1));/* compute common probability term */
  cut = com                     /* and log of the cutoff probability */
      - logGamma((double)(body-supp+1))
      - logGamma((double)(head-supp+1))
      - logGamma((double)(     supp+1))
      - logGamma((double)(rest+supp+1));
  cut *= 1.0-DBL_EPSILON;       /* adapt for roundoff errors */
  /* cut must be multiplied with a value < 1 in order to increase it, */
  /* because it is the logarithm of a probability and hence negative. */
  for (sum = 0, supp = 0; supp <= body; supp++) {
    p = com                     /* traverse the contingency tables */
      - logGamma((double)(body-supp+1))
      - logGamma((double)(head-supp+1))
      - logGamma((double)(     supp+1))
      - logGamma((double)(rest+supp+1));
    if (p <= cut) sum += exp(p);/* sum probabilities greater */
  }                             /* than the cutoff probability */
  return sum;                   /* return computed probability */
}  /* re_fetprob() */

/*--------------------------------------------------------------------*/

double re_fetchi2 (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Fisher's exact test (chi^2) */
  SUPP   rest, n;               /* counter for rest cases, buffer */
  double com;                   /* common probability term */
  double exs;                   /* expected support value */
  double sum;                   /* probability sum of conting. tables */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 1;                   /* check for non-vanishing marginals */
  rest = base -head -body;      /* compute number of rest cases */
  if (rest < 0) {               /* if rest cases are less than supp, */
    supp -= rest = -rest;       /* exchange rows and exchange columns */
    body  = base -body; head = base -head;
  }                             /* complement/exchange the marginals */
  if (head < body) {            /* ensure that body <= head */
    n = head; head = body; body = n; }
  com = logGamma((double)(     head+1))
      + logGamma((double)(     body+1))
      + logGamma((double)(base-head+1))
      + logGamma((double)(base-body+1))
      - logGamma((double)(base+1));/* compute common probability term */
  exs = (double)head *(double)body /(double)base;
  if ((double)supp < exs)
       { n =              (SUPP)ceil (exs+(exs-(double)supp)); }
  else { n = supp; supp = (SUPP)floor(exs-((double)supp-exs)); }
  if (n > body) n = body+1;     /* compute the range of values and */
  if (supp < 0) supp = -1;      /* clamp it to the possible maximum */
  if (n-supp-4 < supp+body-n) { /* if fewer less extreme tables */
    for (sum = 1; ++supp < n;){ /* traverse the less extreme tables */
      sum -= exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)(     supp+1))
                     -logGamma((double)(rest+supp+1)));
    } }                         /* sum the probability of the tables */
  else {                        /* if fewer more extreme tables */
    for (sum = 0; supp >= 0; supp--) {
      sum += exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)(     supp+1))
                     -logGamma((double)(rest+supp+1)));
    }                           /* traverse the more extreme tables */
    for (supp = n; supp <= body; supp++) {
      sum += exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)(     supp+1))
                     -logGamma((double)(rest+supp+1)));
    }                           /* sum the probability of the tables */
  }                             /* (upper and lower table ranges) */
  return sum;                   /* return computed probability */
}  /* re_fetchi2() */

/*--------------------------------------------------------------------*/

double re_fetinfo (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Fisher's exact test (info.) */
  SUPP   rest, n;               /* counter for rest cases, buffer */
  double com;                   /* common probability term */
  double cut;                   /* cutoff value for information gain */
  double sum;                   /* probability sum of conting. tables */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 1;                   /* check for non-vanishing marginals */
  rest = base -head -body;      /* compute number of rest cases */
  if (rest < 0) {               /* if rest cases are less than supp, */
    supp -= rest = -rest;       /* exchange rows and exchange columns */
    body  = base -body; head = base -head;
  }                             /* complement/exchange the marginals */
  if (head < body) {            /* ensure that body <= head */
    n = head; head = body; body = n; }
  com = logGamma((double)(     head+1))
      + logGamma((double)(     body+1))
      + logGamma((double)(base-head+1))
      + logGamma((double)(base-body+1))
      - logGamma((double)(base+1));/* compute common probability term */
  cut = re_info(supp, body, head, base) *(1.0-DBL_EPSILON);
  for (sum = 0, supp = 0; supp <= body; supp++) {
    if (re_info(supp, body, head, base) >= cut)
      sum += exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)     (supp+1))
                     -logGamma((double)(rest+supp+1)));
  }                             /* sum probs. of less extreme tables */
  return sum;                   /* return computed probability */
}  /* re_fetinfo() */

/*--------------------------------------------------------------------*/

double re_fetsupp (SUPP supp, SUPP body, SUPP head, SUPP base)
{                               /* --- Fisher's exact test (support) */
  SUPP   rest, n;               /* counter for rest cases, buffer */
  double com;                   /* common probability term */
  double sum;                   /* probability sum of conting. tables */

  if ((head <= 0) || (head >= base)
  ||  (body <= 0) || (body >= base))
    return 1;                   /* check for non-vanishing marginals */
  rest = base -head -body;      /* compute number of rest cases */
  if (rest < 0) {               /* if rest cases are less than supp, */
    supp -= rest = -rest;       /* exchange rows and exchange columns */
    body  = base -body; head = base -head;
  }                             /* complement/exchange the marginals */
  if (head < body) {            /* ensure that body <= head */
    n = head; head = body; body = n; }
  com = logGamma((double)(     head+1))
      + logGamma((double)(     body+1))
      + logGamma((double)(base-head+1))
      + logGamma((double)(base-body+1))
      - logGamma((double)(base+1));/* compute common probability term */
  if (supp <= body -supp) {     /* if fewer lesser support values */
    for (sum = 1.0; --supp >= 0; )
      sum -= exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)(     supp+1))
                     -logGamma((double)(rest+supp+1))); }
  else {                        /* if fewer greater support values */
    for (sum = 0.0; supp <= body; supp++)
      sum += exp(com -logGamma((double)(body-supp+1))
                     -logGamma((double)(head-supp+1))
                     -logGamma((double)(     supp+1))
                     -logGamma((double)(rest+supp+1)));
  }                             /* sum the table probabilities */
  return sum;                   /* return computed probability */
}  /* re_fetsupp() */

/*--------------------------------------------------------------------*/

static const REINFO reinfo[] ={ /* --- rule evaluation functions */
  /* RE_NONE         0 */  { re_none,       0, 'x',
                    "no measure"                                      },
  /* RE_SUPP         1 */  { re_supp,      +1, 'o',
                    "rule support (original def.: body & head)"       },
  /* RE_CONF         2 */  { re_conf,      +1, 'c',
                    "rule confidence"                                 },
  /* RE_CONFDIFF     3 */  { re_confdiff,  +1, 'd',
                    "absolute confidence difference to prior"         },
  /* RE_LIFT         4 */  { re_lift,      +1, 'l',
                    "lift value (confidence divided by prior)"        },
  /* RE_LIFTDIFF     5 */  { re_liftdiff,  +1, 'a',
                    "absolute difference of lift value to 1"          },
  /* RE_LIFTQUOT     6 */  { re_liftquot,  +1, 'q',
                    "difference of lift quotient to 1"                },
  /* RE_CVCT         7 */  { re_cvct,      +1, 'v',
                    "conviction (inverse lift for negated head)"      },
  /* RE_CVCTDIFF     8 */  { re_cvctdiff,  +1, 'e',
                    "absolute difference of conviction to 1"          },
  /* RE_CVCTQUOT     9 */  { re_cvctquot,  +1, 'r',
                    "difference of conviction quotient to 1"          },
  /* RE_IMBAL       10 */  { re_imbal,     +1, 'b',
                    "imbalance ratio"                                 },
  /* RE_KULC        11 */  { re_kulc,      +1, 'k',
                    "Kulczynski measure"                              },
  /* RE_KULCDIFF    12 */  { re_kulcdiff,  +1, 'w',
                    "difference of Kulczynski measure to 0.5"         },
  /* RE_CPROB       13 */  { re_cprob,     +1, 'u',
                    "conditional probability ratio"                   },
  /* RE_IMPORT      14 */  { re_import,    +1, 'j',
                    "importance (binary log. of cond. prob. ratio)"   },
  /* RE_CERT        15 */  { re_cert,      +1, 'z',
                    "certainty factor (relative confidence change)"   },
  /* RE_CHI2        16 */  { re_chi2,      +1, 'n',
                    "normalized chi^2 measure"                        },
  /* RE_CHI2PVAL    17 */  { re_chi2pval,  -1, 'p',
                    "p-value from (unnormalized) chi^2 measure"       },
  /* RE_YATES       18 */  { re_yates,     +1, 'y',
                    "normalized chi^2 measure with Yates' correction" },
  /* RE_YATESPVAL   19 */  { re_yatespval, -1, 't',
                    "p-value from Yates-corrected chi^2 measure"      },
  /* RE_INFO        20 */  { re_info,      +1, 'i',
                    "information difference to prior"                 },
  /* RE_INFOPVAL    21 */  { re_infopval,  -1, 'g',
                    "p-value from G statistic/information difference" },
  /* RE_FETPROB     22 */  { re_fetprob,   -1, 'f',
                    "Fisher's exact test (table probability)"         },
  /* RE_FETCHI2     23 */  { re_fetchi2,   -1, 'h',
                    "Fisher's exact test (chi^2 measure)"             },
  /* RE_FETINFO     24 */  { re_fetinfo,   -1, 'm',
                    "Fisher's exact test (information gain)"          },
  /* RE_FETSUPP     25 */  { re_fetsupp,   -1, 's',
                    "Fisher's exact test (support)"                   },
};                              /* table of evaluation functions */
/* remaining characters: - */

static const int remap[] = {    /* --- character to identifier map */
  /*  0 a */  RE_LIFTDIFF,
  /*  1 b */  RE_IMBAL,
  /*  2 c */  RE_CONF,
  /*  3 d */  RE_CONFDIFF,
  /*  4 e */  RE_CVCTDIFF,
  /*  5 f */  RE_FETPROB,
  /*  6 g */  RE_INFOPVAL,
  /*  7 h */  RE_FETCHI2,
  /*  8 i */  RE_INFO,
  /*  9 j */  RE_IMPORT,
  /* 10 k */  RE_KULC,
  /* 11 l */  RE_LIFT,
  /* 12 m */  RE_FETINFO,
  /* 13 n */  RE_CHI2,
  /* 14 o */  RE_SUPP,
  /* 15 p */  RE_CHI2PVAL,
  /* 16 q */  RE_LIFTQUOT,
  /* 17 r */  RE_CVCTQUOT,
  /* 18 s */  RE_FETSUPP,
  /* 19 t */  RE_YATESPVAL,
  /* 20 u */  RE_CPROB,
  /* 21 v */  RE_CVCT,
  /* 22 w */  RE_KULCDIFF,
  /* 23 x */  RE_NONE,
  /* 24 y */  RE_YATES,
  /* 25 z */  RE_CERT,
};                              /* list of measure ids by character */

/*--------------------------------------------------------------------*/

int re_getid (int c)
{                               /* --- get function id from character */
  if ((c < 'a') || (c > 'z')) return -1;
  return remap[c -'a'];         /* get identifier from table */
}  /* re_getid() */

/*--------------------------------------------------------------------*/

RULEVALFN* re_function (int id)
{                               /* --- get a rule evalution function */
  assert((id >= 0) && (id <= RE_FNCNT));
  return reinfo[id].fn;         /* retrieve function from table */
}  /* re_function() */

/*--------------------------------------------------------------------*/

int re_dir (int id)
{                               /* --- get a rule evalution direction */
  assert((id >= 0) && (id <= RE_FNCNT));
  return reinfo[id].dir;        /* retrieve direction from table */
}  /* re_dir() */

/*--------------------------------------------------------------------*/

void re_help (void)
{                               /* --- print measure descriptions */
  int i;                        /* loop variable */
  for (i = 0; i < RE_FNCNT; i++) {
    printf("  %c   %-48s", reinfo[i].chr, reinfo[i].desc);
    if      (reinfo[i].dir > 0) printf("(+)");
    else if (reinfo[i].dir < 0) printf("(-)");
    printf("\n");               /* traverse evaluation measures */
  }                             /* and print their descriptions */
}  /* re_help() */
