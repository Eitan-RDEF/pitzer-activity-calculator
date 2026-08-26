
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

try:
    from phreeqc import Phreeqc
except ImportError:
    raise SystemExit(
        "The 'phreeqc' package is not installed.\n"
        "Install it with:\n\n"
        "    python -m pip install phreeqc"
    )

FIELDS = [
    ("pH", "pH"),
    ("Temperature (°C)", "temp"),

    # Cations
    ("Na⁺ [mol/kg(H2O)]", "Na"),
    ("K⁺ [mol/kg(H2O)]", "K"),
    ("Li⁺ [mol/kg(H2O)]", "Li"),
    ("Ca²⁺ [mol/kg(H2O)]", "Ca"),
    ("Mg²⁺ [mol/kg(H2O)]", "Mg"),
    ("Sr²⁺ [mol/kg(H2O)]", "Sr"),
    ("Ba²⁺ [mol/kg(H2O)]", "Ba"),
    ("Fe²⁺ [mol/kg(H2O)]", "Fe2"),
    ("Fe³⁺ [mol/kg(H2O)]", "Fe3"),
    ("Al³⁺ [mol/kg(H2O)]", "Al"),

    # Anions / acid-base components
    ("Cl⁻ [mol/kg(H2O)]", "Cl"),
    ("Br⁻ [mol/kg(H2O)]", "Br"),
    ("SO₄²⁻ [mol/kg(H2O)]", "SO4"),
    ("Total inorganic carbon (CO₃²⁻, HCO₃⁻, CO₂) [mol/kg(H2O)]", "C4"),
]


class PitzerHActivityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PHREEQC Pitzer — H+ Activity Coefficient")
        self.geometry("650x810")
        self.minsize(650, 810)

        self.entries = {}
        self.database_path = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer,
            text="Pitzer calculation of H+ activity coefficient",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(0, 10))

        db_frame = ttk.Frame(outer)
        db_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(db_frame, text="pitzer.dat:").pack(side="left")
        ttk.Entry(db_frame, textvariable=self.database_path).pack(
            side="left", fill="x", expand=True, padx=8
        )
        ttk.Button(db_frame, text="Browse...", command=self.browse_database).pack(
            side="right"
        )

        input_box = ttk.LabelFrame(outer, text="Solution composition", padding=10)
        input_box.pack(fill="x")

        ttk.Label(
            input_box,
            text="Leave optional components blank if absent.",
            font=("Segoe UI", 9, "italic"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        for row, (label, key) in enumerate(FIELDS, start=1):
            ttk.Label(input_box, text=label + ":").grid(
                row=row, column=0, sticky="e", padx=(0, 10), pady=3
            )
            entry = ttk.Entry(input_box, width=24)
            entry.grid(row=row, column=1, sticky="w", pady=3)
            self.entries[key] = entry

        ttk.Button(
            outer,
            text="Calculate",
            command=self.calculate,
        ).pack(pady=12)

        result_frame = ttk.LabelFrame(outer, text="Results", padding=10)
        result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            result_frame,
            height=11,
            state="disabled",
            font=("Consolas", 10),
            wrap="none",
        )
        self.result_text.pack(fill="both", expand=True)

    def browse_database(self):
        filename = filedialog.askopenfilename(
            title="Select pitzer.dat",
            filetypes=[("PHREEQC database", "*.dat"), ("All files", "*.*")]
        )
        if filename:
            self.database_path.set(filename)

    def required_float(self, key, label):
        raw = self.entries[key].get().strip()
        if not raw:
            raise ValueError(f"{label} is required.")
        try:
            return float(raw)
        except ValueError:
            raise ValueError(f"Invalid numeric value for {label}: {raw}")

    def optional_float(self, key, label):
        raw = self.entries[key].get().strip()
        if not raw:
            return 0.0
        try:
            value = float(raw)
        except ValueError:
            raise ValueError(f"Invalid numeric value for {label}: {raw}")
        if value < 0:
            raise ValueError(f"{label} cannot be negative.")
        return value

    def calculate(self):
        try:
            db_raw = self.database_path.get().strip()
            if not db_raw:
                raise ValueError("Please select the pitzer.dat database file.")

            db_path = Path(db_raw)
            if not db_path.exists():
                raise FileNotFoundError(f"Database not found:\n{db_path}")

            pH = self.required_float("pH", "pH")
            temp = self.required_float("temp", "Temperature")

            labels = {
                "Na": "Na", "K": "K", "Li": "Li", "Ca": "Ca", "Mg": "Mg",
                "Sr": "Sr", "Ba": "Ba", "Fe2": "Fe(II)", "Fe3": "Fe(III)",
                "Al": "Al", "Cl": "Cl", "Br": "Br", "SO4": "SO4",
                "C4": "HCO3/CO3 total C(4)",
            }
            values = {
                key: self.optional_float(key, label)
                for key, label in labels.items()
            }

            solution_lines = [
                "SOLUTION 1",
                f"    temp {temp}",
                f"    pH {pH}",
                "    units mol/kgw",
            ]

            component_map = [
                ("Na", "Na"),
                ("K", "K"),
                ("Li", "Li"),
                ("Ca", "Ca"),
                ("Mg", "Mg"),
                ("Sr", "Sr"),
                ("Ba", "Ba"),
                ("Fe2", "Fe(2)"),
                ("Fe3", "Fe(3)"),
                ("Al", "Al"),
                ("Cl", "Cl"),
                ("Br", "Br"),
                ("SO4", "S(6)"),
                ("C4", "C(4)"),
            ]

            for key, phreeqc_name in component_map:
                if values[key] != 0:
                    solution_lines.append(f"    {phreeqc_name} {values[key]}")

            phreeqc_input = "\n".join(solution_lines) + '''

SELECTED_OUTPUT
    -reset false
    -solution true
    -pH true
    -ionic_strength true

USER_PUNCH
    -headings loga_H logm_H loggamma_H gamma_H mol_H act_H
    10 PUNCH LA("H+")
    20 PUNCH LM("H+")
    30 PUNCH LA("H+") - LM("H+")
    40 PUNCH 10^(LA("H+") - LM("H+"))
    50 PUNCH MOL("H+")
    60 PUNCH 10^LA("H+")

END
'''

            p = Phreeqc()
            p.LoadDatabase(str(db_path))
            p.RunString(phreeqc_input)
            out = p.GetSelectedOutput()

            ionic_strength = out["mu"][0]
            returned_pH = out["pH"][0]
            loga_h = out["loga_H"][0]
            logm_h = out["logm_H"][0]
            loggamma_h = out["loggamma_H"][0]
            gamma_h = out["gamma_H"][0]
            mol_h = out["mol_H"][0]
            act_h = out["act_H"][0]

            result = (
                f"pH                  = {returned_pH:.8g}\n"
                f"Ionic strength      = {ionic_strength:.8g} mol/kg(H2O)\n"
                f"log10(a_H+)          = {loga_h:.10g}\n"
                f"log10(m_H+)          = {logm_h:.10g}\n"
                f"log10(gamma_H+)      = {loggamma_h:.10g}\n"
                f"\n"
                f"gamma_H+             = {gamma_h:.10g}\n"
                f"H+ molality          = {mol_h:.10g} mol/kg(H2O)\n"
                f"H+ activity          = {act_h:.10g}\n"
                f"\n"
                f"Check: a_H+ = gamma_H+ × m_H+\n"
                f"       {act_h:.5e} ≈ {gamma_h:.5e} × {mol_h:.5e}"
            )

            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, result)
            self.result_text.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Calculation error", str(exc))


if __name__ == "__main__":
    app = PitzerHActivityApp()
    app.mainloop()
