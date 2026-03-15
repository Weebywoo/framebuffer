# framebuffer

#### Install

`pip install .`

#### Formating

`python -m ruff format`

#### Linting

`python -m mypy  . --strict`

## Checklist + TODOs: convert the current project into a function-based terminal render **library**

This is organized as an actionable migration plan: **MVP library**, then **polish**, then **extensibility**. Each item
is phrased as a TODO you can check off.

---

# Phase 0 — Set the target (one-time decisions)

- [x] **Pick package name** (import name and distribution name)
    - e.g. distribution: `framebuffer` / import: `framebuffer`
- [x] Decide **public color format** (library contract)
    - [ ] Option A: `0..255` floats/ints (terminal-friendly)
    - [x] Option B: `0..1` floats (rendering-friendly)
- [x] Decide **public angle units** and document it
    - [x] radians
    - [ ] degrees
- [x] Decide whether the terminal size is:
    - [x] pulled from the backend each frame (supports resize), or
    - [ ] fixed on renderer creation (simpler)

---

# Phase 1 — Packaging & public API skeleton (MVP)

### 1. Create a real importable package

- [x] Create `src/framebuffer/` (new package root)
- [x] Create `/examples/`
- [x] Create `/resources/`
- [x] Create `/tests/`
- [x] Add `src/framebuffer/__init__.py` that exports the *public API only*
    - [x] `Renderer`, `Scene`, `Camera`, `Model`, `Mesh`, `Texture`, `Transform`, `Material`, `RenderOptions`
- [ ] Move existing code under `src/framebuffer/...`

### 2. Add `pyproject.toml` for library packaging

- [x] Add `pyproject.toml` with:
    - [x] name/version/description/readme/license
    - [x] dependencies (keep minimal)
    - [x] optional extras (dev)

### 3. Add a license and minimal docs scaffolding

- [x] Add `LICENSE`
- [ ] Update `README.md` to include:
    - [x] install
    - [ ] 10-line quickstart
    - [ ] simple custom shader example (function-based)
    - [ ] limitations (OBJ support subset, etc.)

---

# Phase 2 — Core API: Renderer + Material + shader contracts (MVP)

### 4. Define function-based shader contracts (public)

- [ ] Create `framebuffer/scene/material.py`:
    - [x] `VertexShaderFn` Protocol
    - [x] `FragmentShaderFn` Protocol
    - [ ] `Varyings` dataclass (must include `clip_position` + interpolants like `uv`)
    - [ ] `ShaderContext` dataclass (time, matrices, frame size, textures access)
- [ ] Decide how “uniforms” work:
    - [x] `Material.uniforms: dict[str, Any]`
    - [ ] `ShaderContext.uniforms` (global/per-frame)
    - [ ] a helper `ctx.get(name, default)` that checks material → global

### 5. Introduce `Material` and `RenderState` (public)

- [ ] Create `framebuffer/material.py`:
    - [ ] `RenderState` (depth test/write, cull mode, etc.)
    - [ ] `Material(vertex_shader, fragment_shader, uniforms, state)`

### 6. Create `Renderer` as the main entrypoint (public)

- [ ] Create `framebuffer/renderer.py`:
    - [ ] `Renderer(backend=..., options=...)`
    - [ ] `Renderer.render(scene, frame=None)` (frame optional if renderer owns it)
    - [ ] `Renderer.frame()` context manager (clears + presents)
    - [ ] `Renderer.frames(fps=...)` generator/iterator (optional but very convenient)

---

# Phase 3 — Backend separation (terminal output becomes a backend)

### 7. Split “frame buffer” from “presenting to terminal”

- [ ] Create `framebuffer/frame.py`:
    - [ ] `Frame` (color buffer + depth buffer + dimensions + draw/compare methods)
    - [ ] No printing inside `Frame`
- [ ] Create `framebuffer/backends/base.py`:
    - [ ] `Backend` Protocol/ABC:
        - [ ] `get_size() -> (w, h)` or `size` property
        - [ ] `present(frame: Frame) -> None`
- [ ] Create `framebuffer/backends/ansi_terminal.py`:
    - [ ] Move ANSI printing logic here
    - [ ] Implement resize strategy
- [ ] Ensure the renderer depends only on `Backend`, not terminal-specific code.

**Why this matters:** it makes your library usable in other projects (and testable), and later you can add windowed
backends without changing the renderer core.

---

# Phase 4 — Make assets and IO library-grade

### 8. Path handling and resource loading

- [ ] Convert file APIs to accept `str | pathlib.Path`
- [ ] Stop assuming `./resources/...` inside library code
- [ ] Add clear constructors:
    - [ ] `Mesh.from_obj(path)`
    - [ ] `Texture.from_image(path)`
    - [ ] `Model(mesh=..., material=..., transform=...)` (avoid “magic filepaths” in constructor)
- [ ] Keep demo assets in `resources/`, but access them only from `examples/`.

### 9. Separate IO helpers cleanly

- [ ] Create `framebuffer/io/obj.py` for OBJ loader
- [ ] Create `framebuffer/io/image.py` for texture loading (Pillow)
- [ ] Create `framebuffer/io/export.py` for video/image export (optional extras)

---

# Phase 5 — Public extension points (without exposing pipeline internals)

### 10. Add render options and hooks (public)

- [ ] Create `framebuffer/options.py`:
    - [ ] `RenderOptions` (clear color, depth behavior, culling, etc.)
- [ ] Create `framebuffer/hooks.py`:
    - [ ] `PipelineHooks` with optional callbacks:
        - [ ] `before_draw(model, ctx)`
        - [ ] `after_vertex(varyings, ctx)`
        - [ ] `after_clip(tris, ctx)`
        - [ ] `after_frame(frame, ctx)`
- [ ] Wire hooks into the renderer (no-op by default).

### 11. “Fixed stages” configurability (controlled)

Pick a small set of stable strategies:

- [ ] Clipping strategy: `Clipper` interface
- [ ] Rasterizer strategy: `Rasterizer` interface
- [ ] Interpolator strategy (optional v1; you can keep internal for now)

Expose these via:

- [ ] `Renderer(pipeline=Pipeline(clipper=..., rasterizer=...))`  
  or
- [ ] `RenderOptions` toggles + hooks (lighter v1)

---

# Phase 6 — Tests & quality gates (so it’s safe to evolve)

### 12. Offscreen backend for tests

- [ ] Create `framebuffer/backends/offscreen.py` that stores frames instead of printing
- [ ] Write deterministic tests:
    - [ ] render a single triangle → assert pixel colors at known coords
    - [ ] depth test behavior
    - [ ] culling behavior
- [ ] Avoid tests that depend on real terminal size.

### 13. Type checking + linting

- [ ] Ensure `mypy` runs cleanly on public modules (`framebuffer/*`)
- [ ] Keep `ruff` config and add CI-like commands in docs
- [ ] Consider adding `py.typed` if you ship typing info

---

# Phase 7 — Developer experience (polish)

### 14. Examples become the “front door”

- [ ] Ensure `examples/` contains:
    - [ ] `spinning_cube.py` (default shaders)
    - [ ] `custom_shader_tint_scroll.py` (function-based shader)
    - [ ] `offscreen_render_to_image.py` (optional)
- [ ] Make root `main.py` either:
    - [ ] a thin wrapper that calls an example or
    - [ ] removed in favor of `python -m framebuffer.examples...` (your choice)

### 15. Versioning + stability

- [ ] Adopt a semver-like approach for public API
- [ ] Document what is public vs. internal (simple rule: only things re-exported in `framebuffer/__init__.py` are
  “stable”)

---

# “MVP Done” definition (so you can stop and ship v0.1)

You’re ready to call it a usable library when:

- [x] `pip install .` works (via `pyproject.toml`)
- [ ] A user can write:
    - [ ] create `Renderer()`, `Scene()`, `Model(mesh, material)`
    - [ ] supply custom `vertex_shader` and `fragment_shader` functions
    - [ ] render to terminal backend
- [ ] There is at least **one example** using a custom shader
- [ ] There is at least **one offscreen test** that asserts pixels deterministically

---

## Optional but recommended: first migration order (minimize breakage)

1) package namespace + public API shell
2) `Material` + shader contracts
3) renderer uses material shaders
4) backend split (printing moves out)
5) path cleanup and IO separation
6) hooks/options + tests

---

- https://stackoverflow.com/questions/54143142/3d-intersection-between-segment-and-triangle
- https://joshortner.github.io/raytracing-part-one
- https://paulbourke.net/geometry/polygonise/
- https://www.youtube.com/watch?v=ih20l3pJoeU
- https://youtu.be/yyJ-hdISgnw
- https://jsantell.com/model-view-projection/
- https://benedictnghk.github.io/Graphics/Pipeline/
- https://de.wikipedia.org/wiki/Windows_Bitmap
- https://www.cs.ucr.edu/~shinar/courses/cs130-winter-2021/content/clipping.pdf
  Clock-wise vertex definition
