# Product scope

## Intended users

- Chemical, process, water-treatment, corrosion, and geochemical engineers.
- Laboratory chemists working with saline or concentrated aqueous solutions.
- Students and researchers who need an inspectable Pitzer calculation.

## First useful release

The first public release should let a user define one supported aqueous solution, understand
whether the input is coherent, calculate activities with the bundled Pitzer model, inspect
the conventions used, and download enough information to reproduce the result.

## In scope

- Molality-based composition input.
- Clearly enumerated supported components.
- A collapsed extended-component section for Br, Li, Sr, Ba, B, Si, fixed Fe(II), and
  fixed Mn(II), each with an audited limitation shown before calculation.
- Dynamic warnings for known mixture, pH, redox, and precipitation-related limitations.
- pH and temperature input within a validated envelope.
- Ionic strength, charge-balance diagnostics, activities, and activity coefficients.
- Mean activity coefficients for explicitly selected electrolytes.
- Presets, reproducible PHREEQC input, and tabular export.
- Scientific explanations attached to the relevant result.

## Initially out of scope

- Reactive transport, kinetics, mixing, or inverse modeling.
- Arbitrary user-supplied PHREEQC programs.
- Confidential composition storage or user accounts.
- Claims of validity outside tested species, temperature, pressure, or concentration ranges.
- Fe(III), Al, arbitrary redox equilibration, and unreviewed database master components.
- Replacing professional judgment or validated commercial process simulation.

## Positioning

The defensible promise is a modern, free, transparent, engineer-friendly Pitzer calculator.
The product should not claim to be the first online implementation because earlier
interactive Pitzer tools exist.
