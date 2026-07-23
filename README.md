# scan-to-oces-pipeline
![An excerpt from this repository's associated paper showing the process of converting a 3D scan to an OCES-format eye.](docs/scan-to-eye-process.png)  
*The process of converting a scan to a 3D OCES-compliant model, as seen in figure 2 of the paper.*

This is a repository that stores the tools and instructions to convert an x-ray microtomography scan of an insect head/eye to an OCES-compliant glTF file.
This markdown file outlines the process taken to produce the OCES/glTF eye file used in the paper [PAPER NAME HERE](PAPER LINK HERE), and should serve as a guide to recreating the work with other x-ray microtomographic data.

The majority of large files are stored within [ORDA](https://orda.shef.ac.uk/articles/dataset/Dataset_Reconstructing_the_visual_histories_of_desert_ants/32860832) under the "Eye Mapping and Modelling" folder. Below are tables outlining their purposes:

In the *"1. Scan to Mesh Data"* folder:  
| Filename | Description |
|----------|-------------|
| original-velox-head-full-scan.tif | An x-ray microtomography scan of the full head of a sample *Cataglyphis Velox*, stored as a stack of material density slices. |
| original-full-eye-scan.tif | A higher-resolution x-ray microtomography scan of just the eye region of the **Cataglyphis Velox** head stored in `original-velox-head-full-scan.tif`. |
| original-eye-scan (300-800).tif | An image stack that is identical to `original-full-eye-scan.tif` but only the images within its stack that contain the surface lens of the eye (sub-images indexed between 300 and 800). |
| lens mask.tif | A binary image stack that forms a 3D mask around the surface lens of the eye. |
| cropped-to-lens.tif | `original-eye-scann (300-800).tif` cropped to the mask found in `lens mask.tif`. |
| exported-head-surface.stl | The `original-velox-head-full-scan.tif` scan, converted to a 3D mesh. |
| exported-eye-surface.stl | The `cropped-to-lens.tif` image stack, converted to a 3D mesh. |

In the *"2. Mesh to Eye Model Data"* folder:  
| Filename | Description |
|----------|-------------|
|oces-gltf-eye-model | A folder containing the 3 files that make up a single OCES/glTF file describing the *Cataglyphis Velox* eye scanned in the previously described folder. This is the end result of the process described on this page.
| aligned-scan-data | A folder cntaining the `.stl` files found in the previously described folder, but sharing a common coordinate space. These should be loaded into the `.blend` file that this repository makes use of to estimate lens placement data if you are looking to recreate the steps taken to generate the OCES/glTF file used in our paper. |

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
