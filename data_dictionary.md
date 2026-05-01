# Data Dictionary

## Dataset: Hot Strip Rolling Process Dataset

This dataset represents operational parameters from a hot strip rolling process. It includes process conditions, material properties, and the resulting bending force applied during rolling.

The dataset is used to analyze how process variables influence rolling performance and mechanical load.

Source: https://www.kaggle.com/datasets/ziya07/hot-strip-rolling-process-dataset 

---

## Original Features

### entry_temperature
- Description: Temperature of the steel strip at entry to the rolling mill  
- Type: Numeric (°C)  
- Importance: Higher temperatures generally reduce deformation resistance  

---

### exit_temperature
- Description: Temperature of the strip after rolling  
- Type: Numeric (°C)  
- Importance: Indicates heat loss during the rolling process  

---

### rolling_speed
- Description: Speed at which the strip passes through the rolls  
- Type: Numeric (m/s)  
- Importance: Affects throughput and strain rate  

---

### strip_thickness
- Description: Thickness of the strip before rolling  
- Type: Numeric (mm)
- Importance: Strongly influences required rolling force  

---

### material_grade
- Description: Categorical label representing steel type/grade  
- Type: Categorical (A36, AISI 304, AISI 316, SS400)
- Importance: Different grades have different mechanical properties  

---

### deformation_resistance
- Description: Resistance of the material to deformation under load  
- Type: Numeric (MPa)
- Importance: Directly affects required bending force  

---

### friction_coefficient
- Description: Friction between the strip and the rolls  
- Type: Numeric  
- Importance: Higher friction increases rolling force  

---

### roll_diameter
- Description: Diameter of the rolling rolls  
- Type: Numeric (mm)
- Importance: Influences contact area and force distribution  

---

### reduction_ratio
- Description: Ratio of thickness reduction during rolling  
- Type: Numeric (0–1)  
- Importance: Higher reduction requires greater force  

---

### strain_rate
- Description: Rate of deformation applied to the material  
- Type: Numeric (1/s)
- Importance: Affects material behavior under stress  

---

### lubrication_type
- Description: Type of lubrication used during rolling  
- Type: Categorical (Dry, Oil, or Water-based)
- Importance: Impacts friction and process efficiency  

---

### material_grade_encoded
- Description: Numerical encoding of material grade  
- Type: Numeric  
- Importance: Used for modeling or correlation analysis  

---

### lubrication_type_encoded
- Description: Numerical encoding of lubrication type  
- Type: Numeric  
- Importance: Used for modeling or correlation analysis  

---

### bending_force (Target Variable)
- Description: Force applied to the strip during rolling  
- Type: Numeric (kN)
- Importance: Key performance metric for the rolling process  

---

## Engineered Features

### temperature_drop
- Description: Difference between entry and exit temperature  
- Formula: entry_temperature - exit_temperature  
- Importance: Measures heat loss during rolling  

---

### temperature_drop_percent
- Description: Percentage heat loss relative to entry temperature  
- Formula: temperature_drop / entry_temperature × 100  
- Importance: Normalized measure of thermal efficiency  

---

### estimated_exit_thickness
- Description: Estimated strip thickness after rolling  
- Formula: strip_thickness × (1 - reduction_ratio)  
- Importance: Approximation of final product thickness  

---

### thickness_reduction
- Description: Amount of thickness removed during rolling  
- Formula: strip_thickness - estimated_exit_thickness  
- Importance: Measures process intensity  

---

### force_per_thickness
- Description: Bending force normalized by strip thickness  
- Formula: bending_force / strip_thickness  
- Importance: Enables fair comparison across different input sizes  

---

### friction_load_proxy
- Description: Proxy for rolling difficulty due to friction and material resistance  
- Formula: friction_coefficient × deformation_resistance  
- Importance: Represents combined effect of friction and material strength  

---

### rolling_intensity
- Description: Proxy for overall process aggressiveness  
- Formula: rolling_speed × reduction_ratio × strain_rate  
- Importance: Captures combined operational intensity  

---

## Notes

- Encoded variables are primarily used for modeling and correlation analysis.
- Engineered features were created to better represent process behavior and support KPI analysis.
- Some engineered variables are approximations or proxies rather than direct physical equations.

---

## Use Case

This dataset supports:

- Process performance analysis  
- KPI development  
- Operational optimization  
- Identification of key drivers of bending force  