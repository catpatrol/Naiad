# D5 case windows — engine event sequences (v11_faithful, BTCUSDT_swing)

Replay window 2025-10-06 -> 2026-07-07 (the spent window — plumbing check only, never evidence). Exec = 5m chart, governor = 4H, per the swing mandate.

**How to check (operator sign-off for F6):** open BTCUSDT.P (Binance) on TradingView, 5m chart, SS Cascade v11.0.2 with default inputs, **chart timezone UTC**. For each table below, step through the bars and confirm the same events print on the same bars (a REGIME row here = the bar where the governor cross first becomes visible on the exec chart; TradingView may paint the arrow across the whole following governor bar). Grades and zones must match exactly; stop levels within 0.05%.

Whipsaw-suppressed arrows: REGIME rows carry `arrow_visible` — when false, TradingView shows no arrow (the tint still flips; that is the whipsaw display filter, arming is unaffected).

## May 16 -> 26 '26 — the marquee short

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-16T04:00:00Z | REGIME | short | - | - | 0 | provisional | 1 | - | - | shown |
| 2026-05-17T11:15:00Z | PRIME | short | B | Z1 | 1 | provisional | 1 | 0.198098 | 78378.80109139 |  |
| 2026-05-17T12:50:00Z | PRIME | short | B | Z1 | 2 | provisional | 1 | 0.198098 | 78378.80109139 |  |
| 2026-05-17T13:50:00Z | CONFIRM | short | - | Z1 | 2 | provisional | 1 | - | 78279.13605978 |  |
| 2026-05-17T20:10:00Z | PRIME | short | B | Z1 | 3 | provisional | 1 | 0.170869 | 78279.13605978 |  |
| 2026-05-17T22:05:00Z | PRIME | short | B | Z1 | 4 | provisional | 1 | 0.175191 | 78279.13605978 |  |
| 2026-05-18T13:05:00Z | PRIME | short | B | Z1 | 5 | provisional | 1 | 0.032046 | 77563.32089605 |  |
| 2026-05-18T13:50:00Z | CONFIRM | short | - | - | 5 | provisional | 1 | - | 77206.32862527 |  |
| 2026-05-18T20:45:00Z | PRIME | short | B | Z1 | 6 | provisional | 1 | -0.090868 | 76993.91747721 |  |
| 2026-05-18T22:45:00Z | PRIME | short | B | Z1 | 7 | provisional | 1 | -0.085311 | 76993.91747721 |  |
| 2026-05-18T23:15:00Z | PRIME | short | B | Z1 | 8 | provisional | 1 | -0.085311 | 76993.91747721 |  |
| 2026-05-19T01:00:00Z | PRIME | short | B | Z1 | 9 | provisional | 1 | -0.044703 | 76993.91747721 |  |
| 2026-05-19T01:35:00Z | CONFIRM | short | - | Z1 | 9 | provisional | 1 | - | 76962.94917598 |  |
| 2026-05-19T05:15:00Z | CONFIRM | short | - | - | 9 | provisional | 1 | - | 76875.54705907 |  |
| 2026-05-19T07:00:00Z | PRIME | short | B | Z1 | 10 | provisional | 1 | -0.109371 | 76875.54705907 |  |
| 2026-05-19T08:05:00Z | PRIME | short | B | Z1 | 11 | provisional | 1 | -0.07288 | 76875.54705907 |  |
| 2026-05-19T08:55:00Z | PRIME | short | B | Z1 | 12 | provisional | 1 | -0.063906 | 76875.54705907 |  |
| 2026-05-19T09:25:00Z | CONFIRM | short | - | Z1 | 12 | provisional | 1 | - | 76875.54705907 |  |
| 2026-05-19T11:20:00Z | CONFIRM | short | C | Z1 | 12 | provisional | 1 | - | 76875.54705907 |  |
| 2026-05-19T17:30:00Z | PRIME | short | B | Z1 | 13 | provisional | 1 | -0.125383 | 76875.54705907 |  |
| 2026-05-19T18:25:00Z | PRIME | short | B | Z1 | 14 | provisional | 1 | -0.125383 | 76873.61136583 |  |
| 2026-05-19T19:25:00Z | PRIME | short | B | Z1 | 15 | provisional | 1 | -0.115154 | 76873.61136583 |  |
| 2026-05-19T22:00:00Z | PRIME | short | B | Z1 | 16 | provisional | 1 | -0.115154 | 76873.61136583 |  |
| 2026-05-20T00:05:00Z | CONFIRM | short | - | Z1 | 16 | provisional | 1 | - | 76862.21735166 |  |
| 2026-05-20T01:25:00Z | PRIME | short | B | Z1 | 17 | provisional | 1 | -0.115154 | 76831.81138178 |  |
| 2026-05-20T04:35:00Z | CONFIRM | short | C | Z1 | 17 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-20T07:35:00Z | PRIME | short | B | Z1 | 18 | provisional | 1 | -0.032478 | 76769.66535653 |  |
| 2026-05-20T10:40:00Z | PRIME | short | B | Z1 | 19 | provisional | 1 | 0.007718 | 76769.66535653 |  |
| 2026-05-20T13:10:00Z | PRIME | short | B | Z1 | 20 | provisional | 1 | 0.027003 | 76769.66535653 |  |
| 2026-05-20T13:35:00Z | CONFIRM | short | - | Z1 | 20 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-20T15:40:00Z | PRIME | short | B | Z1 | 21 | provisional | 1 | 0.046103 | 76769.66535653 |  |
| 2026-05-20T16:25:00Z | CONFIRM | short | - | Z1 | 21 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-20T18:25:00Z | PRIME | short | B | Z1 | 22 | provisional | 1 | 0.046103 | 76769.66535653 |  |
| 2026-05-20T22:05:00Z | CONFIRM | short | - | Z1 | 22 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-20T23:05:00Z | PRIME | short | B | Z1 | 23 | provisional | 1 | 0.046103 | 76769.66535653 |  |
| 2026-05-21T02:50:00Z | PRIME | short | B | Z1 | 24 | provisional | 1 | 0.112829 | 76769.66535653 |  |
| 2026-05-21T04:10:00Z | PRIME | short | B | Z1 | 25 | provisional | 1 | 0.112829 | 76769.66535653 |  |
| 2026-05-21T06:05:00Z | CONFIRM | short | - | Z1 | 25 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-21T08:35:00Z | PRIME | short | B | Z1 | 26 | provisional | 1 | 0.119003 | 76769.66535653 |  |
| 2026-05-21T09:20:00Z | PRIME | short | B | Z1 | 27 | provisional | 1 | 0.119003 | 76769.66535653 |  |
| 2026-05-21T11:35:00Z | PRIME | short | B | Z1 | 28 | provisional | 1 | -0.053306 | 76769.66535653 |  |
| 2026-05-21T12:10:00Z | PRIME | short | B | Z1 | 29 | provisional | 1 | -0.071624 | 76769.66535653 |  |
| 2026-05-21T13:15:00Z | PRIME | short | B | Z1 | 30 | provisional | 1 | -0.056167 | 76769.66535653 |  |
| 2026-05-21T16:20:00Z | PRIME | short | B | Z1 | 31 | provisional | 1 | -0.045835 | 76769.66535653 |  |
| 2026-05-21T21:40:00Z | PRIME | short | B | Z1 | 32 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-21T22:10:00Z | PRIME | short | B | Z1 | 33 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-21T22:35:00Z | PRIME | short | B | Z1 | 34 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-22T00:10:00Z | CONFIRM | short | - | Z1 | 34 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-22T05:25:00Z | CONFIRM | short | - | Z1 | 34 | provisional | 1 | - | 76769.66535653 |  |
| 2026-05-22T05:55:00Z | PRIME | short | B | Z1 | 35 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-22T06:55:00Z | PRIME | short | B | Z1 | 36 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-22T08:35:00Z | PRIME | short | B | Z1 | 37 | provisional | 1 | 0.095087 | 76769.66535653 |  |
| 2026-05-22T11:10:00Z | PRIME | short | B | Z1 | 38 | provisional | 1 | -0.055941 | 76769.66535653 |  |
| 2026-05-22T13:20:00Z | PRIME | short | B | Z1 | 39 | provisional | 1 | -0.01097 | 76769.66535653 |  |
| 2026-05-23T16:20:00Z | PRIME | short | B | Z1 | 40 | provisional | 1 | -0.410645 | 75534.55561881 |  |
| 2026-05-24T00:05:00Z | PRIME | short | B | Z1 | 41 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T01:10:00Z | PRIME | short | B | Z1 | 42 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T03:35:00Z | PRIME | short | B | Z1 | 43 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T04:25:00Z | PRIME | short | B | Z1 | 44 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T06:20:00Z | PRIME | short | B | Z1 | 45 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T08:45:00Z | PRIME | short | B | Z1 | 46 | provisional | 1 | -0.035977 | 75534.55561881 |  |
| 2026-05-24T12:05:00Z | PRIME | short | B | Z1 | 47 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-24T13:25:00Z | PRIME | short | B | Z1 | 48 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-24T16:35:00Z | PRIME | short | B | Z1 | 49 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-24T18:45:00Z | PRIME | short | B | Z1 | 50 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-24T20:15:00Z | CONFIRM | short | - | Z1 | 50 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-25T01:00:00Z | PRIME | short | B | Z1 | 51 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-25T01:40:00Z | PRIME | short | B | Z1 | 52 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-25T02:25:00Z | PRIME | short | B | Z1 | 53 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-25T03:45:00Z | PRIME | short | B | Z1 | 54 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-25T06:00:00Z | PRIME | short | B | Z1 | 55 | provisional | 1 | -0.00037 | 75534.55561881 |  |
| 2026-05-25T07:10:00Z | PRIME | short | B | Z2 | 56 | provisional | 1 | -0.021446 | 75534.55561881 |  |
| 2026-05-25T10:25:00Z | PRIME | short | B | Z2 | 57 | provisional | 1 | 0.020005 | 75534.55561881 |  |
| 2026-05-25T11:45:00Z | PRIME | short | B | Z2 | 58 | provisional | 1 | -0.02406 | 75534.55561881 |  |
| 2026-05-25T12:10:00Z | CONFIRM | short | - | Z2 | 58 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-25T15:25:00Z | PRIME | short | B | Z2 | 59 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-25T17:15:00Z | PRIME | short | B | Z2 | 60 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-25T18:45:00Z | PRIME | short | B | Z2 | 61 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-25T19:35:00Z | PRIME | short | B | Z2 | 62 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-25T20:30:00Z | PRIME | short | B | Z2 | 63 | provisional | 1 | -0.026715 | 75534.55561881 |  |
| 2026-05-25T21:20:00Z | PRIME | short | B | Z1 | 64 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-25T22:30:00Z | PRIME | short | B | Z1 | 65 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-26T00:05:00Z | PRIME | short | B | Z1 | 66 | provisional | 1 | 0.058884 | 75534.55561881 |  |
| 2026-05-26T06:40:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T06:45:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T06:50:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T06:55:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:00:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:05:00Z | CONFIRM | short | C | Z1 | 66 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:05:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:10:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:15:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:20:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:25:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:30:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:35:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T07:40:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:30:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:35:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:40:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:45:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:50:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T10:55:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:00:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:05:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:10:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:15:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:20:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:25:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:30:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:35:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:40:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:45:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:50:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T11:55:00Z | TPW | short | - | - | 66 | - | 1 | - | 75534.55561881 |  |
| 2026-05-26T13:25:00Z | CONFIRM | short | C | Z1 | 66 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-26T14:40:00Z | PRIME | short | B | Z2 | 67 | provisional | 1 | 0.097825 | 75534.55561881 |  |
| 2026-05-26T15:05:00Z | CONFIRM | short | - | Z1 | 67 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-27T09:15:00Z | CONFIRM | short | - | - | 67 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-27T11:50:00Z | CONFIRM | short | - | - | 67 | provisional | 1 | - | 75534.55561881 |  |
| 2026-05-27T12:45:00Z | CONFIRM | short | C | Z1 | 67 | provisional | 1 | - | 75534.55561881 |  |

*121 events in this window.*

## Jul 2 -> 6 '26 — provisional longs

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-07-01T03:15:00Z | PRIME | short | A | Z1 | 76 | full | 2 | -0.613163 | 58667.04197887 |  |
| 2026-07-01T05:25:00Z | PRIME | short | A | Z1 | 77 | full | 2 | -0.554934 | 58667.04197887 |  |
| 2026-07-01T06:25:00Z | CONFIRM | short | - | Z1 | 77 | full | 2 | - | 58667.04197887 |  |
| 2026-07-01T10:05:00Z | PRIME | short | A | Z1 | 78 | full | 2 | -0.629546 | 58667.04197887 |  |
| 2026-07-01T18:10:00Z | PRIME | short | B | Z1 | 79 | full | 2 | -0.340832 | 58667.04197887 |  |
| 2026-07-01T22:30:00Z | PRIME | short | B | Z3 | 80 | full | 2 | -0.181176 | 58667.04197887 |  |
| 2026-07-01T23:50:00Z | CONFIRM | short | - | Z1 | 80 | full | 2 | - | 58667.04197887 |  |
| 2026-07-02T03:20:00Z | PRIME | short | B | Z1 | 81 | full | 2 | -0.181176 | 58667.04197887 |  |
| 2026-07-02T04:25:00Z | PRIME | short | B | Z1 | 82 | full | 2 | -0.181176 | 58667.04197887 |  |
| 2026-07-02T05:00:00Z | PRIME | short | B | Z1 | 83 | full | 2 | -0.181176 | 58667.04197887 |  |
| 2026-07-02T05:25:00Z | PRIME | short | B | Z1 | 84 | full | 2 | -0.181176 | 58667.04197887 |  |
| 2026-07-02T06:50:00Z | CONFIRM | short | - | Z1 | 84 | full | 2 | - | 58667.04197887 |  |
| 2026-07-02T14:20:00Z | PRIME | short | B | Z3 | 85 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-02T15:05:00Z | PRIME | short | B | Z3 | 86 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-02T18:55:00Z | PRIME | short | B | Z3 | 87 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-02T20:00:00Z | PRIME | short | B | Z3 | 88 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-02T20:00:00Z | CONFIRM | short | - | Z3 | 88 | full | 2 | - | 58667.04197887 |  |
| 2026-07-02T22:05:00Z | CONFIRM | short | - | Z3 | 88 | full | 2 | - | 58667.04197887 |  |
| 2026-07-02T22:35:00Z | CONFIRM | short | - | Z3 | 88 | full | 2 | - | 58667.04197887 |  |
| 2026-07-02T23:00:00Z | PRIME | short | B | Z3 | 89 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T00:00:00Z | CONFIRM | short | - | Z3 | 89 | full | 2 | - | 58667.04197887 |  |
| 2026-07-03T00:55:00Z | PRIME | short | B | Z3 | 90 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T02:30:00Z | CONFIRM | short | - | Z3 | 90 | full | 2 | - | 58667.04197887 |  |
| 2026-07-03T03:10:00Z | PRIME | short | B | Z3 | 91 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T04:50:00Z | PRIME | short | B | Z3 | 92 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T06:30:00Z | PRIME | short | B | Z3 | 93 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T08:00:00Z | PRIME | short | B | Z3 | 94 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T08:35:00Z | PRIME | short | B | Z3 | 95 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T09:35:00Z | PRIME | short | B | Z3 | 96 | full | 2 | -0.010372 | 58667.04197887 |  |
| 2026-07-03T14:05:00Z | PRIME | short | B | Z3 | 97 | full | 2 | 0.007923 | 58667.04197887 |  |
| 2026-07-03T18:05:00Z | PRIME | short | B | Z3 | 98 | full | 2 | 0.030777 | 58667.04197887 |  |
| 2026-07-03T19:10:00Z | PRIME | short | B | Z3 | 99 | full | 2 | 0.030777 | 58667.04197887 |  |
| 2026-07-03T20:00:00Z | REGIME | long | - | - | 0 | provisional | 1 | - | - | shown |
| 2026-07-05T06:20:00Z | PRIME | long | B | Z1 | 1 | provisional | 1 | 0.144428 | 62722.44118589 |  |
| 2026-07-05T06:50:00Z | PRIME | long | B | Z1 | 2 | provisional | 1 | 0.144428 | 62722.44118589 |  |
| 2026-07-05T07:35:00Z | PRIME | long | B | Z1 | 3 | provisional | 1 | 0.144428 | 62789.96175256 |  |
| 2026-07-05T10:10:00Z | PRIME | long | B | Z1 | 4 | provisional | 1 | 0.182714 | 62789.96175256 |  |
| 2026-07-05T10:45:00Z | PRIME | long | B | Z1 | 5 | provisional | 1 | 0.182714 | 62789.96175256 |  |
| 2026-07-05T12:20:00Z | PRIME | long | B | Z1 | 6 | provisional | 1 | 0.182714 | 62789.96175256 |  |
| 2026-07-05T13:55:00Z | CONFIRM | long | - | Z1 | 6 | provisional | 1 | - | 62789.96175256 |  |
| 2026-07-05T15:00:00Z | CONFIRM | long | - | Z1 | 6 | provisional | 1 | - | 62789.96175256 |  |
| 2026-07-05T18:05:00Z | PRIME | long | B | Z1 | 7 | provisional | 1 | 0.182714 | 62789.96175256 |  |
| 2026-07-05T18:45:00Z | CONFIRM | long | - | Z1 | 7 | provisional | 1 | - | 62789.96175256 |  |
| 2026-07-05T21:15:00Z | CONFIRM | long | - | Z1 | 7 | provisional | 1 | - | 62789.96175256 |  |
| 2026-07-06T07:40:00Z | PRIME | long | B | Z1 | 8 | provisional | 1 | 0.103946 | 62945.55781026 |  |
| 2026-07-06T10:05:00Z | PRIME | long | B | Z1 | 9 | provisional | 1 | 0.147591 | 62945.55781026 |  |
| 2026-07-06T11:20:00Z | PRIME | long | B | Z1 | 10 | provisional | 1 | 0.147591 | 62945.55781026 |  |
| 2026-07-06T12:50:00Z | X | long | - | - | 10 | - | 1 | - | - |  |

*48 events in this window.*

## Jun 14 - 16 '26 — the provisional trap

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-13T02:25:00Z | PRIME | short | B | Z1 | 153 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T03:25:00Z | CONFIRM | short | - | Z1 | 153 | full | 2 | - | 60783.58714742 |  |
| 2026-06-13T05:50:00Z | PRIME | short | B | Z1 | 154 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T09:30:00Z | PRIME | short | B | Z1 | 155 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T13:45:00Z | PRIME | short | B | Z1 | 156 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T15:45:00Z | PRIME | short | B | Z1 | 157 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T16:45:00Z | CONFIRM | short | - | Z1 | 157 | full | 2 | - | 60783.58714742 |  |
| 2026-06-13T17:55:00Z | CONFIRM | short | - | Z1 | 157 | full | 2 | - | 60783.58714742 |  |
| 2026-06-13T20:20:00Z | PRIME | short | B | Z1 | 158 | full | 2 | -2.724844 | 60783.58714742 |  |
| 2026-06-13T22:55:00Z | PRIME | short | B | Z1 | 159 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T00:05:00Z | PRIME | short | B | Z1 | 160 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T01:35:00Z | PRIME | short | B | Z1 | 161 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T02:25:00Z | PRIME | short | B | Z1 | 162 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T04:10:00Z | PRIME | short | B | Z1 | 163 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T04:40:00Z | CONFIRM | short | - | Z1 | 163 | full | 2 | - | 60783.58714742 |  |
| 2026-06-14T09:10:00Z | PRIME | short | B | Z1 | 164 | full | 2 | -2.647581 | 60783.58714742 |  |
| 2026-06-14T12:35:00Z | CONFIRM | short | - | Z1 | 164 | full | 2 | - | 60783.58714742 |  |
| 2026-06-14T15:30:00Z | PRIME | short | B | Z1 | 165 | full | 2 | -2.773993 | 60783.58714742 |  |
| 2026-06-14T16:50:00Z | PRIME | short | B | Z1 | 166 | full | 2 | -2.761726 | 60783.58714742 |  |
| 2026-06-15T00:35:00Z | PRIME | short | B | Z3 | 167 | full | 2 | -2.412538 | 60783.58714742 |  |
| 2026-06-15T02:45:00Z | PRIME | short | B | Z3 | 168 | full | 2 | -2.412538 | 60783.58714742 |  |
| 2026-06-15T04:05:00Z | PRIME | short | B | Z3 | 169 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T06:35:00Z | PRIME | short | B | Z3 | 170 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T07:00:00Z | PRIME | short | B | Z3 | 171 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T07:35:00Z | PRIME | short | B | Z3 | 172 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T08:55:00Z | PRIME | short | B | Z3 | 173 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T09:25:00Z | PRIME | short | B | Z3 | 174 | full | 2 | -2.388499 | 60783.58714742 |  |
| 2026-06-15T13:40:00Z | PRIME | short | B | Z3 | 175 | full | 2 | -2.199477 | 60783.58714742 |  |
| 2026-06-15T16:00:00Z | REGIME | long | - | - | 0 | provisional | 1 | - | - | shown |
| 2026-06-16T03:30:00Z | PRIME | long | B | Z2 | 1 | provisional | 1 | 0.166714 | 65884.93102744 |  |
| 2026-06-16T06:20:00Z | CONFIRM | long | C | Z1 | 1 | provisional | 1 | - | 66134.99816433 |  |
| 2026-06-16T15:10:00Z | PRIME | long | B | Z2 | 2 | provisional | 1 | 0.210855 | 66134.99816433 |  |
| 2026-06-16T17:15:00Z | PRIME | long | B | Z2 | 3 | provisional | 1 | 0.210855 | 66134.99816433 |  |
| 2026-06-16T20:15:00Z | PRIME | long | B | Z2 | 4 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-16T22:10:00Z | PRIME | long | B | Z2 | 5 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-16T23:00:00Z | PRIME | long | B | Z2 | 6 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-16T23:30:00Z | PRIME | long | B | Z2 | 7 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-17T00:10:00Z | PRIME | long | B | Z2 | 8 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-17T00:35:00Z | PRIME | long | B | Z2 | 9 | provisional | 1 | 0.179102 | 66134.99816433 |  |
| 2026-06-17T01:25:00Z | X | long | - | - | 9 | - | 1 | - | - |  |
| 2026-06-17T20:00:00Z | REGIME | short | - | - | 0 | full | 2 | - | - | shown |

*41 events in this window.*

## Jun 22 '26 — Capitulation V

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-06-21T01:10:00Z | PRIME | short | B | Z1 | 19 | full | 2 | 0.425776 | 63041.35116899 |  |
| 2026-06-21T02:40:00Z | PRIME | short | B | Z1 | 20 | full | 2 | 0.425776 | 63041.35116899 |  |
| 2026-06-21T04:50:00Z | PRIME | short | B | Z3 | 21 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T05:45:00Z | PRIME | short | B | Z1 | 22 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T07:15:00Z | CONFIRM | short | - | Z1 | 22 | full | 2 | - | 63041.35116899 |  |
| 2026-06-21T07:50:00Z | PRIME | short | B | Z1 | 23 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T12:10:00Z | CONFIRM | short | - | Z1 | 23 | full | 2 | - | 63041.35116899 |  |
| 2026-06-21T14:10:00Z | PRIME | short | B | Z1 | 24 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T16:10:00Z | PRIME | short | B | Z1 | 25 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T16:35:00Z | CONFIRM | short | - | Z1 | 25 | full | 2 | - | 63041.35116899 |  |
| 2026-06-21T17:25:00Z | CONFIRM | short | - | Z1 | 25 | full | 2 | - | 63041.35116899 |  |
| 2026-06-21T18:00:00Z | PRIME | short | B | Z1 | 26 | full | 2 | 0.465013 | 63041.35116899 |  |
| 2026-06-21T20:25:00Z | CONFIRM | short | - | Z1 | 26 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T02:00:00Z | TPW | short | - | - | 26 | - | 2 | - | 63041.35116899 |  |
| 2026-06-22T02:05:00Z | TPW | short | - | - | 26 | - | 2 | - | 63041.35116899 |  |
| 2026-06-22T02:10:00Z | TPW | short | - | - | 26 | - | 2 | - | 63041.35116899 |  |
| 2026-06-22T02:45:00Z | PRIME | short | A+ | Z3 | 27 | full | 2 | 0.508809 | 63041.35116899 |  |
| 2026-06-22T03:30:00Z | PRIME | short | B | Z1 | 28 | full | 2 | 0.508809 | 63041.35116899 |  |
| 2026-06-22T04:05:00Z | CONFIRM | short | - | Z1 | 28 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T06:15:00Z | PRIME | short | B | Z1 | 29 | full | 2 | 0.508809 | 63041.35116899 |  |
| 2026-06-22T06:40:00Z | CONFIRM | short | - | Z1 | 29 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T08:30:00Z | PRIME | short | B | Z1 | 30 | full | 2 | 0.508809 | 63041.35116899 |  |
| 2026-06-22T09:35:00Z | CONFIRM | short | - | Z1 | 30 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T10:40:00Z | CONFIRM | short | - | Z1 | 30 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T14:10:00Z | PRIME | short | A+ | Z3 | 31 | full | 2 | 0.669898 | 63041.35116899 |  |
| 2026-06-22T15:50:00Z | PRIME | short | A+ | Z3 | 32 | full | 2 | 0.669898 | 63041.35116899 |  |
| 2026-06-22T16:30:00Z | CONFIRM | short | - | Z3 | 32 | full | 2 | - | 63041.35116899 |  |
| 2026-06-22T18:30:00Z | PRIME | short | A+ | Z3 | 33 | full | 2 | 0.669898 | 63041.35116899 |  |
| 2026-06-22T20:25:00Z | PRIME | short | B | Z3 | 34 | full | 2 | 0.478769 | 63041.35116899 |  |
| 2026-06-22T22:15:00Z | PRIME | short | B | Z1 | 35 | full | 2 | 0.669898 | 63041.35116899 |  |
| 2026-06-23T01:35:00Z | PRIME | short | B | Z1 | 36 | full | 2 | 0.400275 | 63041.35116899 |  |
| 2026-06-23T03:05:00Z | PRIME | short | B | Z1 | 37 | full | 2 | 0.401151 | 63041.35116899 |  |
| 2026-06-23T03:35:00Z | PRIME | short | B | Z1 | 38 | full | 2 | 0.401151 | 63041.35116899 |  |
| 2026-06-23T17:00:00Z | CONFIRM | short | - | - | 38 | full | 2 | - | 62590.60641026 |  |
| 2026-06-23T17:45:00Z | CONFIRM | short | - | - | 38 | full | 2 | - | 62586.80125516 |  |
| 2026-06-23T20:45:00Z | CONFIRM | short | - | - | 38 | full | 2 | - | 62490.5049746 |  |

*36 events in this window.*

## Feb 6 '26 — Capitulation V

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-02-06T14:20:00Z | PRIME | short | A | Z1 | 84 | full | 2 | -1.983795 | 67025.88795643 |  |
| 2026-02-06T18:05:00Z | PRIME | short | A | Z1 | 85 | full | 2 | -1.610228 | 67025.88795643 |  |
| 2026-02-06T18:55:00Z | PRIME | short | A | Z1 | 86 | full | 2 | -1.610228 | 67025.88795643 |  |
| 2026-02-06T20:40:00Z | PRIME | short | A | Z1 | 87 | full | 2 | -1.610228 | 67025.88795643 |  |
| 2026-02-06T23:15:00Z | PRIME | short | A | Z1 | 88 | full | 2 | -1.584323 | 67025.88795643 |  |
| 2026-02-07T00:40:00Z | CONFIRM | short | - | Z1 | 88 | full | 2 | - | 67025.88795643 |  |
| 2026-02-07T04:40:00Z | PRIME | short | A | Z1 | 89 | full | 2 | -1.584323 | 67025.88795643 |  |
| 2026-02-07T05:45:00Z | CONFIRM | short | - | Z1 | 89 | full | 2 | - | 67025.88795643 |  |
| 2026-02-07T06:45:00Z | PRIME | short | A | Z1 | 90 | full | 2 | -1.584323 | 67025.88795643 |  |
| 2026-02-07T09:30:00Z | PRIME | short | A | Z1 | 91 | full | 2 | -1.871817 | 67025.88795643 |  |
| 2026-02-07T13:35:00Z | PRIME | short | A | Z1 | 92 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T14:10:00Z | PRIME | short | A | Z1 | 93 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T14:45:00Z | CONFIRM | short | - | Z1 | 93 | full | 2 | - | 67025.88795643 |  |
| 2026-02-07T16:45:00Z | PRIME | short | A | Z1 | 94 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T17:15:00Z | CONFIRM | short | - | Z1 | 94 | full | 2 | - | 67025.88795643 |  |
| 2026-02-07T19:10:00Z | PRIME | short | A | Z1 | 95 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T21:05:00Z | PRIME | short | A | Z1 | 96 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T21:40:00Z | PRIME | short | A | Z1 | 97 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T22:20:00Z | PRIME | short | A | Z1 | 98 | full | 2 | -1.753314 | 67025.88795643 |  |
| 2026-02-07T23:05:00Z | CONFIRM | short | - | Z1 | 98 | full | 2 | - | 67025.88795643 |  |

*20 events in this window.*

## Dec 4 - 13 '25 — chop / whipsaw

| bar open (UTC) | evt | dir | grade | zone | rc | tier | stage | retr | stop | arrow |
|---|---|---|---|---|---|---|---|---|---|---|
| 2025-12-04T12:35:00Z | PRIME | long | B | Z1 | 1 | provisional | 1 | 0.146062 | 92810.18176044 |  |
| 2025-12-04T15:10:00Z | PRIME | long | B | Z1 | 2 | provisional | 1 | 0.233003 | 92810.18176044 |  |
| 2025-12-04T16:20:00Z | CONFIRM | long | - | Z1 | 2 | provisional | 1 | - | 92810.18176044 |  |
| 2025-12-04T17:50:00Z | PRIME | long | B | Z1 | 3 | provisional | 1 | 0.238965 | 92810.18176044 |  |
| 2025-12-04T19:35:00Z | PRIME | long | B | Z2 | 4 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-04T21:05:00Z | CONFIRM | long | - | Z1 | 4 | provisional | 1 | - | 92810.18176044 |  |
| 2025-12-04T22:40:00Z | CONFIRM | long | - | Z1 | 4 | provisional | 1 | - | 92810.18176044 |  |
| 2025-12-05T00:20:00Z | PRIME | long | B | Z1 | 5 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-05T00:45:00Z | CONFIRM | long | - | Z1 | 5 | provisional | 1 | - | 92810.18176044 |  |
| 2025-12-05T02:15:00Z | PRIME | long | B | Z1 | 6 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-05T03:05:00Z | PRIME | long | B | Z1 | 7 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-05T06:05:00Z | PRIME | long | B | Z1 | 8 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-05T07:10:00Z | CONFIRM | long | - | Z1 | 8 | provisional | 1 | - | 92810.18176044 |  |
| 2025-12-05T08:55:00Z | PRIME | long | B | Z1 | 9 | provisional | 1 | 0.323348 | 92810.18176044 |  |
| 2025-12-05T10:25:00Z | PRIME | long | B | Z2 | 10 | provisional | 1 | 0.312011 | 92810.18176044 |  |
| 2025-12-05T11:05:00Z | PRIME | long | B | Z2 | 11 | provisional | 1 | 0.312011 | 92810.18176044 |  |
| 2025-12-05T13:25:00Z | X | long | - | - | 11 | - | 1 | - | - |  |
| 2025-12-06T00:00:00Z | REGIME | short | - | - | 0 | full | 2 | - | - | shown |
| 2025-12-06T15:05:00Z | PRIME | short | A | Z1 | 1 | full | 2 | 0.217449 | 89960.12121972 |  |
| 2025-12-06T16:30:00Z | PRIME | short | A | Z1 | 2 | full | 2 | 0.154291 | 89888.65558495 |  |
| 2025-12-06T17:35:00Z | CONFIRM | short | - | - | 2 | full | 2 | - | 89730.88592377 |  |
| 2025-12-06T18:35:00Z | CONFIRM | short | - | - | 2 | full | 2 | - | 89730.84703032 |  |
| 2025-12-07T01:50:00Z | CONFIRM | short | - | - | 2 | full | 2 | - | 89454.63331822 |  |
| 2025-12-07T02:35:00Z | CONFIRM | short | - | - | 2 | full | 2 | - | 89454.63331822 |  |
| 2025-12-07T07:05:00Z | PRIME | short | A | Z1 | 3 | full | 2 | 0.105955 | 89454.63331822 |  |
| 2025-12-07T08:55:00Z | PRIME | short | A | Z1 | 4 | full | 2 | 0.06545 | 89380.72998507 |  |
| 2025-12-07T13:20:00Z | CONFIRM | short | C | Z1 | 4 | full | 2 | - | 89380.72998507 |  |
| 2025-12-07T19:20:00Z | PRIME | short | A+ | Z3 | 5 | full | 2 | 0.509275 | 89380.72998507 |  |
| 2025-12-07T20:05:00Z | PRIME | short | A+ | Z3 | 6 | full | 2 | 0.509275 | 89380.72998507 |  |
| 2025-12-07T21:05:00Z | PRIME | short | A+ | Z3 | 7 | full | 2 | 0.509275 | 89380.72998507 |  |
| 2025-12-07T21:55:00Z | CONFIRM | short | - | Z3 | 7 | full | 2 | - | 89380.72998507 |  |
| 2025-12-07T22:55:00Z | PRIME | short | B | Z1 | 8 | full | 2 | 0.509275 | 89380.72998507 |  |
| 2025-12-08T00:15:00Z | PRIME | short | B | Z3 | 9 | full | 2 | 0.254727 | 89380.72998507 |  |
| 2025-12-08T02:00:00Z | PRIME | short | B | Z3 | 10 | full | 2 | 0.494929 | 89380.72998507 |  |
| 2025-12-08T03:35:00Z | PRIME | short | B | Z3 | 11 | full | 2 | 0.494929 | 89380.72998507 |  |
| 2025-12-08T05:05:00Z | PRIME | short | B | Z3 | 12 | full | 2 | 0.494929 | 89380.72998507 |  |
| 2025-12-08T07:50:00Z | PRIME | short | A+ | Z3 | 13 | full | 2 | 0.538363 | 89380.72998507 |  |
| 2025-12-08T09:50:00Z | PRIME | short | A+ | Z3 | 14 | full | 2 | 0.616983 | 89380.72998507 |  |
| 2025-12-08T11:30:00Z | PRIME | short | A+ | Z3 | 15 | full | 2 | 0.616983 | 89380.72998507 |  |
| 2025-12-08T12:00:00Z | REGIME | long | - | - | 0 | provisional | 1 | - | - | shown |
| 2025-12-08T15:15:00Z | X | long | - | - | 0 | - | 1 | - | - |  |
| 2025-12-08T16:00:00Z | REGIME | short | - | - | 0 | full | 2 | - | - | hidden |
| 2025-12-08T22:10:00Z | PRIME | short | B | Z3 | 1 | full | 2 | 0.320929 | 91150.70711762 |  |
| 2025-12-08T23:15:00Z | PRIME | short | B | Z3 | 2 | full | 2 | 0.320929 | 90911.23908873 |  |
| 2025-12-08T23:45:00Z | CONFIRM | short | - | Z3 | 2 | full | 2 | - | 90690.31856755 |  |
| 2025-12-09T00:30:00Z | PRIME | short | B | Z3 | 3 | full | 2 | 0.320929 | 90690.31856755 |  |
| 2025-12-09T01:30:00Z | PRIME | short | B | Z3 | 4 | full | 2 | 0.320929 | 90310.96222104 |  |
| 2025-12-09T02:55:00Z | PRIME | short | B | Z3 | 5 | full | 2 | 0.082463 | 90194.71274027 |  |
| 2025-12-09T04:35:00Z | PRIME | short | A | Z3 | 6 | full | 2 | 0.114522 | 90192.85615653 |  |
| 2025-12-09T09:00:00Z | PRIME | short | A | Z3 | 7 | full | 2 | 0.141215 | 90192.85615653 |  |
| 2025-12-09T09:45:00Z | CONFIRM | short | - | Z3 | 7 | full | 2 | - | 90192.85615653 |  |
| 2025-12-09T13:05:00Z | PRIME | short | A | Z3 | 8 | full | 2 | 0.167645 | 90192.85615653 |  |
| 2025-12-09T13:40:00Z | PRIME | short | A | Z3 | 9 | full | 2 | 0.19751 | 90192.85615653 |  |
| 2025-12-09T14:15:00Z | PRIME | short | A | Z3 | 10 | full | 2 | 0.19751 | 90192.85615653 |  |
| 2025-12-09T16:00:00Z | REGIME | long | - | - | 0 | provisional | 1 | - | - | hidden |
| 2025-12-10T01:45:00Z | PRIME | long | B | Z1 | 1 | provisional | 1 | 0.194784 | 92021.34660875 |  |
| 2025-12-10T02:15:00Z | PRIME | long | B | Z1 | 2 | provisional | 1 | 0.194784 | 92089.21372857 |  |
| 2025-12-10T05:00:00Z | CONFIRM | long | - | - | 2 | provisional | 1 | - | 92446.66234949 |  |
| 2025-12-10T09:45:00Z | CONFIRM | long | - | - | 2 | provisional | 1 | - | 92501.01039798 |  |
| 2025-12-10T16:20:00Z | CONFIRM | long | C | Z1 | 2 | provisional | 1 | - | 92501.01039798 |  |
| 2025-12-10T18:35:00Z | PRIME | long | B | Z1 | 3 | provisional | 1 | 0.232494 | 92501.01039798 |  |
| 2025-12-10T19:10:00Z | PRIME | long | B | Z1 | 4 | provisional | 1 | 0.232494 | 92501.01039798 |  |
| 2025-12-11T01:20:00Z | X | long | - | - | 4 | - | 1 | - | - |  |
| 2025-12-11T16:00:00Z | REGIME | short | - | - | 0 | full | 2 | - | - | shown |
| 2025-12-11T20:25:00Z | PRIME | short | A | Z3 | 1 | full | 2 | 0.193126 | 91216.17146657 |  |
| 2025-12-11T22:20:00Z | PRIME | short | A+ | Z3 | 2 | full | 2 | 0.738599 | 91216.17146657 |  |
| 2025-12-12T00:00:00Z | REGIME | long | - | - | 0 | provisional | 1 | - | - | hidden |
| 2025-12-12T12:55:00Z | PRIME | long | B | Z1 | 1 | provisional | 1 | 0.129885 | 92249.92097212 |  |
| 2025-12-12T14:50:00Z | CONFIRM | long | C | Z1 | 1 | provisional | 1 | - | 92249.92097212 |  |
| 2025-12-12T15:25:00Z | V | short | V | - | 0 | full | 2 | - | 91680.07214593 |  |
| 2025-12-12T19:00:00Z | PRIME | short | A | Z3 | 1 | full | 2 | - | 90488.79831378 |  |
| 2025-12-13T00:00:00Z | REGIME | short | - | - | 0 | full | 2 | - | - | hidden |
| 2025-12-13T09:20:00Z | PRIME | short | A | Z1 | 1 | full | 2 | 0.071438 | 90456.14338298 |  |
| 2025-12-13T09:55:00Z | PRIME | short | A | Z1 | 2 | full | 2 | 0.071438 | 90413.85875814 |  |
| 2025-12-13T11:10:00Z | PRIME | short | A | Z3 | 3 | full | 2 | 0.085994 | 90413.85875814 |  |
| 2025-12-13T11:50:00Z | CONFIRM | short | - | Z1 | 3 | full | 2 | - | 90412.80999301 |  |
| 2025-12-13T12:25:00Z | PRIME | short | A | Z1 | 4 | full | 2 | 0.049697 | 90368.55931226 |  |
| 2025-12-13T13:25:00Z | PRIME | short | A | Z1 | 5 | full | 2 | 0.049697 | 90311.80056631 |  |
| 2025-12-13T16:20:00Z | PRIME | short | A | Z1 | 6 | full | 2 | 0.002264 | 90133.0528285 |  |
| 2025-12-13T20:15:00Z | CONFIRM | short | C | Z1 | 6 | full | 2 | - | 90133.0528285 |  |
| 2025-12-14T01:00:00Z | PRIME | short | A | Z1 | 7 | full | 2 | 0.049258 | 90133.0528285 |  |
| 2025-12-14T04:45:00Z | CONFIRM | short | - | Z1 | 7 | full | 2 | - | 90133.0528285 |  |
| 2025-12-14T06:25:00Z | PRIME | short | A | Z1 | 8 | full | 2 | 0.049258 | 90114.72160604 |  |
| 2025-12-14T06:50:00Z | PRIME | short | A | Z1 | 9 | full | 2 | 0.049258 | 90114.72160604 |  |
| 2025-12-14T08:35:00Z | CONFIRM | short | C | Z1 | 9 | full | 2 | - | 90114.72160604 |  |
| 2025-12-14T10:30:00Z | PRIME | short | A | Z1 | 10 | full | 2 | -0.029065 | 90014.62773916 |  |

*86 events in this window.*

---

## Known open parity question for sign-off: the two V signatures

This 5m replay prints **no Capitulation V on Feb 6 or Jun 22**. The builder's diagnostic found the climax bars present on both days (Feb 5–6: multiple red bars ≥3.5× volume MA, lows 6–9 governor-ATRs beyond the governor 89), but the far-band reclaim can then never arrive within capWindow = 10 **5m** bars (50 minutes) — in this engine *and* in the Pine's arithmetic, which are line-identical for this gate. On a **4H exec chart** the same 10-bar window is 40 hours, and the doctrine's Feb 6 observation predates the study's 5m era (Playbook §12: 5m evidence from Apr 26 '26 on).

**Operator: please check Feb 6 and Jun 22 on BOTH charts** — the 5m (governor input 240) and the plain 4H chart — and note which one actually prints the V arrow. If the V only prints on the 4H chart, this engine is faithful and the signature list simply refers to the governor-chart view; if TradingView prints it on the 5m chart, paste the bar timestamp and the builder will trace the gate bar-by-bar.

*Numeric tolerance (F6): cross timestamps exact to the bar; EMA/ATR within 0.05% after F7 warm-up. Sign-off = the operator confirms the two cross lists and these six windows against TradingView.*
