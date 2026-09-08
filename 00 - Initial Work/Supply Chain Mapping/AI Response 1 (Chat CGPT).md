Illustrative supply chain map, calibrated to EFERT's disclosed sector and scale — not actual company supplier, distribution, or process information.

## EFERT — Engro Urea Supply Chain Map

**Product assumption:** I am using **Engro Urea** as the product for this map. This is the most appropriate working assumption because EFERT identifies Engro Urea as a core product, produces it in prilled form, markets it in 50 kg bags, and reports annual urea production of roughly 2.2 million tonnes. ([Engro Fertilizers][1])

### 1. UPSTREAM — Tier 2 and Tier 1

For urea, the upstream chain is substantially different from a conventional manufactured consumer product. The **key feedstock is natural gas**, which functions both as a raw material/feedstock and as an energy source. EFERT itself states that natural gas is used as feedstock and fuel in its urea production process. ([Engro Fertilizers][2])

| Input category                                        | Plausible Tier 1 supplier                                                        | Plausible Tier 2 source                                                                  | Status                        |
| ----------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------- |
| **Natural gas**                                       | Natural-gas transmission/distribution company or upstream gas supplier           | Domestic gas fields, particularly Sindh/Balochistan/Pakistan's natural-gas system        | **Industry-based assumption** |
| **Industrial water**                                  | Local/industrial water-treatment and utility systems                             | Municipal/industrial water sources                                                       | **Industry-based assumption** |
| **Packaging bags**                                    | Local polypropylene/HDPE woven-bag manufacturer and printing/lamination supplier | Polymer/resin producers; polypropylene/PE resin may be domestically produced or imported | **Industry-based assumption** |
| **Plant chemicals/catalysts & maintenance materials** | Industrial chemical, catalyst and engineering/MRO suppliers                      | Domestic chemical manufacturers and imported industrial chemicals/equipment              | **Industry-based assumption** |

**Important distinction:** unlike a textile or automobile supply chain, EFERT does not simply purchase a finished chemical and assemble it. Its Daharki operation is an integrated **ammonia–urea manufacturing complex**. EFERT's EnVen facility is explicitly described as a single-train ammonia-urea plant. ([Engro Fertilizers][3])

---

# 2. MANUFACTURING — Internal Operations

A simplified industrial process can be represented as:

### Stage 1 — Natural gas preparation

Natural gas enters the plant and is processed/conditioned before being used as feedstock and fuel.

**Output:** hydrogen-containing synthesis gas stream + process energy.

### Stage 2 — Ammonia production

The hydrogen-containing gas is processed to produce **ammonia (NH₃)**.

This is a major upstream chemical-production stage within the integrated plant rather than an externally purchased input.

### Stage 3 — Urea synthesis

Ammonia reacts with carbon dioxide under high-pressure conditions to produce **urea**.

Simplified reaction:

**2NH₃ + CO₂ → CO(NH₂)₂ + H₂O**

The CO₂ required for synthesis is generated within the ammonia process, making the integrated ammonia-urea configuration particularly important.

### Stage 4 — Concentration and prilling

The urea solution is concentrated and converted into solid **prills**. EFERT specifically describes Engro Urea as a **prilled** fertilizer. ([Engro Fertilizers][1])

### Stage 5 — Quality control, bagging and dispatch

Finished urea is tested against quality specifications, packed into its marketed **50 kg bags**, stored and prepared for distribution. ([Engro Fertilizers][1])

### Likely bottleneck

The most important bottleneck is **the integrated ammonia–urea production system**, rather than packaging.

This is a continuous-process chemical operation involving high-pressure equipment, gas processing, ammonia synthesis and urea synthesis. A disruption in a critical process unit can therefore affect the entire downstream production chain. EFERT's 2024 EnVen turnaround illustrates the scale of this operational dependency: the scheduled maintenance lasted **55 days** and involved more than 5,000 technical activities across major equipment. ([Engro Fertilizers][4])

---

# 3. DOWNSTREAM — Factory to Farmer

EFERT has a large nationwide distribution structure rather than a simple factory → retailer model.

The company has historically disclosed a network of **100+ warehouses and around 4,000 dealers across Pakistan**. Its 2024 annual report also describes its warehouse and dealer network as a major mechanism for making products available throughout Pakistan. ([Engro Fertilizers][5])

A plausible downstream structure is:

**Daharki factory → regional warehouse → distributor/dealer → farmer**

However, not every transaction necessarily follows every tier.

EFERT has also introduced direct digital purchasing. Its **UgAi** platform allows farmers to purchase fertilizers directly from EFERT, with the company delivering from its warehouses to farmers. ([Engro Fertilizers][6])

So there are effectively **two downstream channels**:

### Traditional channel

**Factory → Warehouse → Dealer/Distributor → Farmer**

Approximately **3 intermediary stages** after manufacturing.

### Direct/digital channel

**Factory → Warehouse → Farmer**

Approximately **1 intermediary stage** after manufacturing.

EFERT's Engro Markaz outlets provide another more direct access point for farmers, with four locations disclosed in 2025: Muridke, Bahawalpur, Sargodha and Sahiwal. ([Engro Fertilizers][7])

---

# 4. INFORMATION & FINANCIAL FLOW

### Information flow

**Farmer demand → Dealer/Distributor → Regional sales/warehouse network → EFERT planning & production → Raw-material/feedstock requirements**

Demand information would therefore move **upstream**, while replenishment and product availability information move downstream.

EFERT's digital systems also create a more direct information channel between farmers and the company, particularly through UgAi, which supports direct purchasing. ([Engro Fertilizers][6])

### Financial flow

**Farmer → Dealer/Distributor → EFERT**

In the traditional channel, payment would typically move upstream through the commercial chain under agreed credit/payment terms, while in direct digital purchasing the farmer can pay through the platform/payment mechanism associated with the transaction. EFERT has also publicly discussed digital payment solutions and online ordering. ([Engro Fertilizers][5])

---

# 5. SIMPLE TEXT SUPPLY CHAIN DIAGRAM

### Traditional channel

```text
Domestic Natural Gas Source
        ↓
Gas Supplier / Transmission Network
        ↓
EFERT Daharki Integrated Ammonia-Urea Plant
        ↓
Ammonia Production
        ↓
Urea Synthesis
        ↓
Concentration & Prilling
        ↓
Quality Control + 50 kg Bagging
        ↓
Regional Warehouses
        ↓
Distributor / Dealer
        ↓
Farmer
```

### Including the broader upstream chain

```text
Domestic Gas Fields
        ↓
Gas Supplier / Transmission System
        ↓
Natural Gas
        ↓
EFERT Daharki Plant
        ↓
Ammonia
        ↓
Urea Synthesis
        ↓
Prilling
        ↓
Bagging
        ↓
Regional Warehouses
        ↓
Dealers / Distributors
        ↓
Farmers
```

### Alternative direct channel

```text
Natural Gas Source
        ↓
EFERT Daharki Plant
        ↓
Urea Production
        ↓
Warehouse
        ↓
UgAi / Engro Direct Channel
        ↓
Farmer
```

---

# 6. PLAUSIBLE LEAD-TIME ESTIMATES

These are **illustrative planning estimates**, not EFERT's disclosed operating lead times.

| Supply-chain link                                    |                    Plausible lead time | Reasoning                                                                                                                                                                                                                                |
| ---------------------------------------------------- | -------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Natural-gas supplier → EFERT plant**               | **1–3 days operational replenishment** | Gas is delivered through a continuous pipeline/network rather than conventional truck shipment. The actual physical movement is effectively continuous; the range reflects scheduling, allocation and operational availability.          |
| **Packaging/material supplier → EFERT**              |                          **3–10 days** | Domestic packaging materials can generally be transported by road relatively quickly, although production schedules and inventory buffers can increase the effective lead time.                                                          |
| **EFERT manufacturing → finished product warehouse** |                           **1–3 days** | The product is manufactured at scale and then moved into strategically positioned storage/warehousing. EFERT has specifically discussed strategically located containment warehousing for product availability. ([Engro Fertilizers][8]) |
| **Warehouse → dealer/distributor**                   |                           **1–5 days** | Mostly domestic road transportation; distance and seasonal fertilizer demand are the main variables.                                                                                                                                     |
| **Dealer → farmer**                                  |                           **1–3 days** | Usually a relatively short local movement, depending on the dealer's location and farmer order.                                                                                                                                          |
| **Warehouse → direct farmer via UgAi**               |                           **1–5 days** | Delivery is made from warehouses directly to farmers; actual timing would vary by location and order volume. ([Engro Fertilizers][6])                                                                                                    |

### Overall illustrative physical lead time

For a conventional order:

**Factory → Warehouse → Dealer → Farmer ≈ 3–11 days**

The **manufacturing process itself should not be interpreted as a 3–11 day batch process**. Urea production is an integrated continuous chemical process; the lead-time estimate above is primarily describing movement through the downstream logistics network.

---

# 7. What is actually verified vs. what we are assuming

### Publicly supported EFERT facts

* EFERT produces **Engro Urea**.
* Engro Urea contains **46% nitrogen** and is produced in **prilled form**.
* It is marketed in **50 kg bags**. ([Engro Fertilizers][1])
* EFERT has major urea manufacturing operations at **Daharki, District Ghotki**. ([Engro Fertilizers][9])
* The EnVen facility is an integrated **ammonia-urea** plant with **1.3 million tonnes annual capacity**. ([Engro Fertilizers][3])
* EFERT's total urea production capacity has historically been around **2.3 million tonnes**, with current production described by the company as approximately **2.2 million tonnes annually**. ([Engro Fertilizers][3])
* EFERT has a substantial nationwide warehouse/dealer network and has disclosed **100+ warehouses and 4,000 dealers** in its sustainability reporting. ([Engro Fertilizers][5])
* EFERT has developed direct farmer channels including **UgAi**. ([Engro Fertilizers][6])

### Illustrative assumptions

The **specific suppliers, exact transportation routes, inventory policies, safety-stock levels, procurement contracts, individual warehouse assignments, dealer replenishment rules and exact lead times are not being presented as EFERT facts**.

---

## Assumptions

This map assumes that the forecasting product from Session 4 was **Engro Urea**; because the Session 4 dataset is not available in this conversation, that product identification is the main assumption. The upstream supplier names are deliberately omitted because publicly available information does not establish a complete supplier-by-supplier EFERT procurement chain. The natural-gas pathway is treated as domestic and pipeline-based because EFERT's urea operations use natural gas as both feedstock and fuel, but the exact current upstream gas-source configuration is not mapped here. The warehouse, dealer and transportation stages are based on EFERT's disclosed distribution footprint and normal fertilizer-industry logistics rather than a confidential EFERT routing map. A real internal supply-chain map would additionally contain specific suppliers, contracts, purchase orders, gas allocations, production schedules, inventory levels, warehouse capacities, transportation providers, dealer-level demand, credit terms and real-time lead-time data that are not publicly disclosed.

[1]: https://www.engrofertilizers.com/brands/?utm_source=chatgpt.com "Engro Fertilizers"
[2]: https://www.engrofertilizers.com/themes/engro/documents/efert-sustainability-report-2024_1.pdf?utm_source=chatgpt.com "EFERT Sustainability Report 2024"
[3]: https://www.engrofertilizers.com/trust/press-release-detail/2011/worlds-largest-urea-plant-starts-production-in-pakistan/?utm_source=chatgpt.com "Engro Fertilizers"
[4]: https://www.engrofertilizers.com/trust/press-release-detail/2024/Engro%20Fertilizers%20completes%20largest%20ever%20turnaround?utm_source=chatgpt.com "Engro Fertilizers"
[5]: https://www.engrofertilizers.com/trust/press-release-detail/2022/engro-fertilizers-releases-first-ever-sustainability-report?utm_source=chatgpt.com "Engro Fertilizers"
[6]: https://www.engrofertilizers.com/trust/press-release-detail/2024/engro-launches-ugai-app-farmers-tech?utm_source=chatgpt.com "Engro Fertilizers"
[7]: https://www.engrofertilizers.com/trust/press-release-detail/2025/engro-fertilizers-establishes-markaz-centres-to-provide-quality-fertilizers-and-services-to-farmers?utm_source=chatgpt.com "Engro Fertilizers"
[8]: https://www.engrofertilizers.com/themes/engro/documents/EFERT-Annual-Report-2022.pdf?utm_source=chatgpt.com "ab | out | th | e |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |"
[9]: https://www.engrofertilizers.com/contact-us?utm_source=chatgpt.com "Engro Fertilizers"

