# Ascend

A browser-local scheduling and focus MVP based on the supplied Ascend Figma dashboard.

## Run

Serve `dist` using a static HTTP server:

```sh
python3 -m http.server 4317 --directory dist
```

Open http://localhost:4317. No build or package installation is required.

## Verification

```sh
node --check dist/app.js
node --test tests/core.test.mjs
```

## Included

- Manual goals and scheduled tasks/commitments, date navigation, and conflict validation.
- Current task preparation based on device time; start/pause/resume/finish and independent sessions.
- Clock-based countdown and session persistence across reloads. Only elapsed running time is logged.
- Goal completion tracking and daily progress snapshots, separate from focus hours.
- Locally generated rain, brown noise, and ocean ambience using Web Audio.
- Local browser persistence with backup export/restore and an optional labelled sample day.
- Responsive layout and keyboard-accessible dialogs and dropdowns.
- Calendar zoom with minute-based, checkable substeps.
- Full-screen blue focus view with button-origin reveal, live countdown ring, pause/resume, and Escape to return.
- Original motivational quotes rotate every three minutes; headline varies on page load.
- Weekly focus bars, compact white cards, and two-font typography.

## Limits

Data lives in localStorage on the current origin and browser; there is no account or device sync. Background browser execution may delay the visible end-of-session prompt; the stored deadline still determines elapsed time. Device clock changes affect scheduling. No AI, calendar integration, system notifications, or native mobile application is included. Full Goals and Planning workspaces are deferred; MVP creation uses dialogs. Fonts load from Google Fonts with system fallbacks.
