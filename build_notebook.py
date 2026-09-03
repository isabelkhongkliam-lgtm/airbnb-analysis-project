"""Build a fully-executed .ipynb from the jupytext percent-format source,
without jupytext/nbformat (offline). Executes each code cell, capturing
stdout, last-expression display, and matplotlib figures as embedded outputs."""
import ast, io, json, base64, contextlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "airbnb_eda_src.py"
OUT = "airbnb_eda.ipynb"

# ---- parse the percent file into (celltype, source) ----
lines = open(SRC, encoding="utf-8").read().splitlines()
# skip everything before the first '# %%' (jupytext YAML header)
start = next(i for i, l in enumerate(lines) if l.startswith("# %%"))
lines = lines[start:]

cells, cur_type, cur = [], None, []
def flush():
    if cur_type is not None:
        cells.append((cur_type, list(cur)))
for l in lines:
    if l.startswith("# %%"):
        flush(); cur.clear()
        cur_type = "markdown" if "[markdown]" in l else "code"
    else:
        cur.append(l)
flush()

# convert markdown comment lines back to markdown text
def md_text(block):
    out = []
    for l in block:
        if l.startswith("# "): out.append(l[2:])
        elif l == "#": out.append("")
        else: out.append(l)
    # trim leading/trailing blank lines
    while out and out[0] == "": out.pop(0)
    while out and out[-1] == "": out.pop()
    return "\n".join(out)

def code_text(block):
    b = list(block)
    while b and b[0].strip() == "": b.pop(0)
    while b and b[-1].strip() == "": b.pop()
    return "\n".join(b)

# ---- execute code cells, capture outputs ----
ns = {"__name__": "__main__"}
nb_cells = []
exec_count = 0

def src_lines(text):
    # nbformat wants a list of lines each ending in \n except the last
    s = text.splitlines(keepends=True)
    return s if s else [""]

for ctype, block in cells:
    if ctype == "markdown":
        txt = md_text(block)
        if not txt.strip():
            continue
        nb_cells.append({"cell_type": "markdown", "metadata": {},
                         "source": src_lines(txt)})
        continue

    code = code_text(block)
    if not code.strip():
        continue
    exec_count += 1
    outputs = []
    buf = io.StringIO()
    val = None
    err = None
    try:
        tree = ast.parse(code)
        last_expr = None
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            last_expr = tree.body.pop()
        with contextlib.redirect_stdout(buf):
            if tree.body:
                exec(compile(ast.Module(body=tree.body, type_ignores=[]),
                             "<cell>", "exec"), ns)
            if last_expr is not None:
                val = eval(compile(ast.Expression(last_expr.value),
                                   "<cell>", "eval"), ns)
    except Exception as e:  # capture, but we expect none
        err = f"{type(e).__name__}: {e}"

    text = buf.getvalue()
    if text:
        outputs.append({"output_type": "stream", "name": "stdout",
                        "text": src_lines(text)})

    # figures created by this cell
    for num in plt.get_fignums():
        fig = plt.figure(num)
        b = io.BytesIO()
        fig.savefig(b, format="png", dpi=110, bbox_inches="tight")
        b64 = base64.b64encode(b.getvalue()).decode()
        outputs.append({"output_type": "display_data", "metadata": {},
                        "data": {"image/png": b64}})
    plt.close("all")

    # last-expression display (DataFrame etc.)
    if val is not None:
        data = {"text/plain": src_lines(repr(val))}
        html = getattr(val, "_repr_html_", None)
        if callable(html):
            try: data["text/html"] = src_lines(html())
            except Exception: pass
        outputs.append({"output_type": "execute_result",
                        "execution_count": exec_count,
                        "metadata": {}, "data": data})
    if err:
        outputs.append({"output_type": "stream", "name": "stderr",
                        "text": [err]})
        print("CELL ERROR:", err)

    nb_cells.append({"cell_type": "code", "execution_count": exec_count,
                     "metadata": {}, "outputs": outputs,
                     "source": src_lines(code)})

notebook = {
    "cells": nb_cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4, "nbformat_minor": 5,
}
json.dump(notebook, open(OUT, "w", encoding="utf-8"), indent=1)
print("Wrote", OUT, "with", len(nb_cells), "cells",
      f"({sum(c['cell_type']=='code' for c in nb_cells)} code,",
      f"{sum(c['cell_type']=='markdown' for c in nb_cells)} markdown)")
