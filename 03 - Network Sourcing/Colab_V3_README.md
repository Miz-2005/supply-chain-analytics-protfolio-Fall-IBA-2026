# EFERT Network Optimisation | Colab V3

1. Download the `.ipynb` file.
2. Open https://colab.research.google.com/ and choose File > Upload notebook.
3. Choose Runtime > Run all.
4. The network map appears directly below section 02 as a Matplotlib image. No server, tunnel, Streamlit or external map tiles.
5. To change the displayed map, run `network_map("2025-06", "All DCs", "Outbound")` in a new code cell.

All data are embedded in the notebook. Outputs are derived from precomputed Phase 4 model results, not a fresh MILP run. The illustrative network is not actual EFERT data. Map connections are straight lines between approximate city coordinates.

The map PNG is saved at `/content/efert_colab_data/EFERT_Network_Map_V3.png` in Colab. Tests check nonempty raster content, route count, flow reconciliation and existing model checks.

**Not included:** final HTML conversion.
