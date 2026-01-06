# addons-to-upgrade-from-v16-to-v18

This repository contains a set of Odoo custom addons being migrated from **Odoo 16** to **Odoo 18** for upgrade testing and production readiness.

## Purpose
- Prepare existing Odoo 16 custom modules to run correctly on Odoo 18.
- Fix common upgrade-breaking issues in:
  - XML views (inheritance targets, XPath changes, deprecated structures like `tree` → `list`).
  - Missing/changed external IDs after upgrade.
  - Client-side crashes caused by views referencing undefined fields.
  - Python constraints / small API adjustments where needed.

## What was done
- Updated module manifests and dependencies where required.
- Cleaned view inheritance to avoid inheriting from database-specific Studio views (e.g., `studio_customization.*`) when not guaranteed to exist.
- Disabled or refactored views that reference missing fields or missing external IDs to prevent installation/upgrade failures.
- Kept changes minimal and focused on compatibility.

## How to use (local/dev)
1. Add this repository path to your `addons_path` in `odoo.conf`.
2. Restart the Odoo server.
3. In Odoo:
   - Enable Developer Mode.
   - Apps → Update Apps List.
   - Install/Upgrade the target modules one by one (recommended on a test database first).

## Notes / Important
- These addons are intended for migration and upgrade validation; behavior may depend on which official modules are installed in your database.
- Avoid hard dependencies on Studio-generated XML IDs unless you control the exact same database where those IDs exist.
- If you encounter:
  - **External ID not found**: a view is inheriting from a missing XML ID (fix the `inherit_id` or adjust dependencies).
  - **field is undefined (OwlError)**: a view references a field that is not present (install the module providing the field or remove the field from the view).

## Repository structure
- Each addon is located in its own folder (standard Odoo addon layout).
- Typical structure:
  - `__manifest__.py`
  - `models/`
  - `views/`
  - `security/` (if needed)

## Status
- Migrated modules: (fill in)
- Remaining modules: (fill in)

## License
Each addon includes its own license information (e.g., AGPL-3) where applicable.
