import json
import os
import pandas as pd

# Contar caracteres para evitar frases muy cortas
results = []
near_limit = []
with open(
    f"{os.path.dirname(__file__)}/todas_las_citas.json", "r", encoding="utf-8"
) as f:
    data = json.load(f)

for idx, item in enumerate(data, 1):
    texto = item.get("texto", "")
    publicado = item.get("publicado", "")
    libro = item.get("libro", "")
    total_length = len(texto) + len(libro) + 6
    if total_length > 275:
        near_limit.append({"id": idx, "texto": len(texto), "total": total_length})
    if len(texto) < 40 and not publicado and libro == "Ars Amandi":
        results.append({"id": idx, "text": texto, "count": len(texto)})

# crear el df ordenando los valores para ver bien las frases demasiado cortas
df = pd.DataFrame(results).sort_values(by=["count"], ascending=False)
pd.set_option("display.max_rows", None)  # No truncar el print
print(df)
print(f"por cortar: {len(results)}")
for item in near_limit:
    print(item)


# Look for: \s*\n\s* and replace by: \\n
