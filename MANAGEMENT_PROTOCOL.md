# Management Protocol: Technical Operations Standards

This protocol establishes the mandatory technical practices and institutional standards for all Content Management Dashboard (CMD) development.

## Standard 1: Analyze Root Cause Before Execution 

Before any code modification or bug resolution:
- **Mandatory Step:** The exact root cause for a failure must be identified and documented.
- **Goal:** Avoid "patchwork" fixes or recursive errors (like template syntax crashes).
- **Practice:** Use a browser subagent or console test to verify that the identified solution *actually* resolves the symptom before applying it to the production templates.

## Standard 2: Simple, Direct, and Token Efficient Logic 

CMD development must prioritize minimalism and scalability:
- **Generic Controllers:** Use model-independent logic where possible (as seen in `dashboard_views.py`). Single views should handle multiple modules to reduce codebase bloat.
- **Zero-Tag Philosophy:** Avoid complex, fragile template tag registrations. Pre-format data in the View to keep Templates clean, stable, and readable.
- **Token Saving:** Minimize redundant templates and styles. Each new module should integrate into existing universal structures rather than spawning new code files.

## Standard 3: Safe-to-Fail Operations (Soft Deletion Only) 

Institutional data must be protected against accidental loss:
- **Rule:** Staff-level content managers *never* perform hard deletions (destructive).
- **Mechanism:** All CMS models must inherit from `BaseModel` for soft-deletion.
- **Authority:** Only the Super Administrator has access to the **Recycle Bin** for permanent purges or content restoration.

## Standard 4: Branded Consistency & Premium UI

The CMD is an institutional tool and must reflect it:
- **Aesthetics:** Designs must be modern, functional, and visually premium (Maroon/Gold theme).
- **Accessibility:** All management tools must be responsive and labeled correctly (e.g., "Staff Access Portal").
- **Clutter-Free:** Institutional content must be organized into logical, hub-based navigation (Publications, Resources, etc.).

---
*Authorized for institutional use. Last Revised: 2026-03-31*
