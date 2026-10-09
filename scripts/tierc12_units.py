# TIER-C12 · THE UNITS MODULE [LEANS L-0.17, allow-list rule (B)].
#
# The one place the tier fixes numbers no file states: three unit conversions.  This module holds
# exactly these three module-level assignments and nothing else — no import, no function, no
# docstring.  Its name -> value map must EQUAL the fixture-typed table UNITS_T (F-TYPED, the
# closure suite's second object); the table moves only by a dated amendment in LEANS_AMENDMENTS.md.
#
#   PCT_PER_UNIT   percent per unit fraction
#   BPS_PER_UNIT   basis points per unit fraction
#   BYTES_PER_MB   bytes per megabyte, DECIMAL — TC11-X's filed reading of the ferry's "2 MB"
#                  (x_rec/scripts/tc11x_ferry.py: `CAP_BYTES`, with the binary megabyte beside it
#                  as the rival not taken)
PCT_PER_UNIT = 100
BPS_PER_UNIT = 10000
BYTES_PER_MB = 1000000
