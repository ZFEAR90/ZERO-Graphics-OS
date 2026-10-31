# Bundled assets

Screenshot reading runs locally using Tesseract.js 7.0.0 and its matching Tesseract.js-core 7.0.0, under Apache-2.0. English and Arabic data are published as @tesseract.js-data/eng and @tesseract.js-data/ara 1.0.0 (MIT). The upstream language-data license is included. Their original licenses are in screenshot-reader/.

Platform vectors are from Simple Icons 16.36.0 (CC0-1.0). Official brand-source references, exact package versions, npm integrity digests and file SHA256 digests are recorded in vendor-sources.json. The upstream icon license is in platform-logos/. Brand names and marks belong to their owners.

The editor loads the platform vectors locally. Screenshot images, recognition models and extracted text are not sent to a remote recognition service. Automatic screenshot reading uses the local editor started by START_ZE_OS.bat; file:// editing retains manual review and cropping.
