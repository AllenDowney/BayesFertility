# JupyterBook Publication Directory

This directory contains the source files for building an HTML site using [JupyterBook](https://jupyterbook.org/), a documentation framework built on MyST.

## Structure

```
jb/
├── myst.yml          # Configuration file
├── Makefile          # Build commands
├── index.md          # Landing page
├── tech_report.md    # Technical report (main content)
├── figs/             # Figures generated from notebooks
├── tables/           # Tables generated from notebooks
└── _build/           # Generated site (created by build process)
```

## Building the Site

### Prerequisites

Install JupyterBook:
```bash
pip install jupyter-book
```

Optional (for deployment):
```bash
pip install ghp-import
```

### Commands

```bash
# Build the site
make build

# Build and serve locally (opens browser at http://localhost:8000)
make serve

# Clean build artifacts
make clean

# Deploy to GitHub Pages (requires repository setup)
make deploy
```

## Workflow

1. **Generate figures and tables** from notebooks:
   - Run the analysis notebooks in `../notebooks/`
   - Save figures to `figs/` directory
   - Save tables (as HTML or CSV) to `tables/` directory

2. **Update content** in markdown files:
   - Edit `tech_report.md` to add text, embed figures, reference tables
   - Use MyST syntax: `![caption](figs/figure.png)` for figures
   - Use `{include}` directive for tables: `{include} tables/table.html`

3. **Build and preview**:
   ```bash
   make serve
   ```
   This builds the site and opens it in a browser for preview.

4. **Deploy** (when ready):
   ```bash
   make deploy
   ```
   This builds and pushes to GitHub Pages.

## MyST Syntax Examples

### Embedding Figures

```markdown
![Cohort effects over time](figs/cohort_effects.png)
```

### Including Tables

```markdown
{include} tables/model_parameters.html
```

### Math

Inline: `$\alpha_i \sim \text{Normal}(\alpha_{i-1}, \sigma_\alpha)$`

Block:
```markdown
$$
\lambda_{ij} = \exp(\alpha_i + \beta_j)
$$
```

### Cross-references

```markdown
See the [Technical Report](tech_report.md) for details.
```

## Next Steps

1. Modify notebooks to generate publication-ready figures and tables
2. Save outputs to `figs/` and `tables/` directories
3. Update `tech_report.md` to include generated figures and tables
4. Build and preview the site
5. Iterate until satisfied
6. Deploy to GitHub Pages

## Resources

- [JupyterBook Documentation](https://jupyterbook.org/)
- [MyST Markdown Guide](https://mystmd.org/guide/quickstart-myst-markdown) (JupyterBook uses MyST syntax)
- [Example: EqualityWEF/HALE project](https://github.com/AllenDowney/EqualityWEF)

