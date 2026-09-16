"""Validación científica mínima sin dependencias de testing externas."""
from models.kinetics import validate_model_cases

if __name__ == "__main__":
    cases = validate_model_cases()
    for row in cases:
        print(f"Caso {row['Caso']}: {row['Resultado esperado']} | {row['Resultado obtenido']} | {'OK' if row['Estado'] else 'FALLA'}")
    if not all(row["Estado"] for row in cases):
        raise SystemExit("Hay casos científicos que no superaron la validación.")
    print("Todos los casos científicos superaron la validación.")
