# scan-to-oces-pipeline
![An excerpt from this repository's associated paper showing the process of converting a 3D scan to an OCES-format eye.](docs/scan-to-eye-process.png)  
*The process of converting a scan to a 3D OCES-compliant model, as seen in figure 2 of the paper.*

This is a repository that stores the tools and instructions to convert an x-ray microtomography scan of an insect head/eye to an OCES-compliant glTF file.
This markdown file outlines the process taken to produce the OCES/glTF eye file used in the paper [PAPER NAME HERE](PAPER LINK HERE), and should serve as a guide to recreating the work with other x-ray microtomographic data.

The majority of large files are stored within [ORDA](NEEDS LINK). Below is a table outlining their purposes:

| Subfolder | Filename | Description |
|-----------|----------|-------------|
|1. Scan To Mesh Data | original-velox-head-full-scan.tif | TODO DESC |
|                     | lens mask.tif | TODO DESC |
|                     | original-full-eye-scan.tif | TODO DESC |
|---------------------|----------------------------|-----------|


## Converting an x-ray microtomography slice stack to a mesh
- using fiji
- loading x-ray data
- exporting as 3D mesh
- cleanup in blender using cleanup script
- positioning
    - Precomputed meshes are stored in XYZ

## Converting a mesh to a OCES/glTF file format
- Loading in the precomputed meshes if needed
- Building a facetmap
- exporting to OCES.
