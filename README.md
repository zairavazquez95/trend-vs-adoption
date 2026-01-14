# Style Signals: The Hype-Adjusted Trend Algorithm

> **"Views on TikTok doesn't equal units sold."**
<img width="800" height="500" alt="mobwife_style_signal" src="https://github.com/user-attachments/assets/f6808d98-fac8-4cc2-866d-f26b6357ce87" />

## The Problem
Modern fashion marketing suffers from **"Viral Inflation."** Micro-trends like *"Mob Wife Aesthetic"* or *"Coquette Core"* generate massive social media engagement (High Volatility) but often yield low real-world product adoption (Low Conversion). Brands that chase every viral spike waste inventory and budget.

## The Solution: Signal Scoring
This Python engine simulates a "Hype vs. Reality" filter. It ingests two data streams, **Viral Intensity** (Social Mentions) and **Adoption Signal** (Retail/Street Data), to calculate a proprietary **Signal Score**.

Is this trend actually selling, or is it just algorithm noise?"*

## Methodology & Logic
This repository demonstrates the algorithmic logic using **synthetic data generators** to model 4 distinct trend archetypes:

### 1. The Archetypes (Modeled Behavior)
* ** Adopted (High Value):** Trends like *Clean Look* or *Sneakers*.
    * *Behavior:* Steady, cumulative growth in adoption, regardless of viral spikes.
* ** Performative (High Risk):** Trends like *Coquette* or *Balletcore*.
    * *Behavior:* High viral noise, but adoption remains flat. People post it, but don't wear it.
* ** Burnout (Avoid):** Trends like *Mob Wife*.
    * *Behavior:* Massive initial spike followed by immediate adoption collapse.
* ** Dormant (Watch):** Low noise, stable usage.

### 2. The Math: "Signal Score"
I developed a scoring formula that penalizes empty hype. A trend is only valuable if adoption outpaces virality.

$$\text{Signal Score} = \frac{\% \text{ Adoption Growth}}{\text{Normalized Viral Intensity}}$$

* **High Score (>40):** The trend is growing faster than the hype (Real Demand).
* **Low Score (<15):** The hype is louder than the adoption (Noise).

##  Visual Output
The script generates comparison charts for each trend, visualizing the gap between "Posting" and "Wearing."
> *Note: Blue line represents viral noise (high volatility). Orange line represents actual adoption (crashing).*
 
Running the simulation across 10 distinct aesthetic cohorts revealed three critical market behaviors:

### 1. The "Engagement Trap" (e.g., Mob Wife, Coquette)
* **Data Signal:** Extremely high viral volatility (Blue Line > 150) paired with flat or negative adoption slopes (Orange Line < 20).
* **Business Implication:** These trends generate "Empty Impressions." They are valuable for brand awareness (top-of-funnel) but toxic for inventory depth. The algorithm flags these as **"High Risk / Low Conversion."**

<img width="800" height="500" alt="mobwife_style_signal" src="https://github.com/user-attachments/assets/0f128073-5c2a-4d7f-b190-76e83f5f2edc" />
<img width="800" height="500" alt="coquette_style_signal" src="https://github.com/user-attachments/assets/29b705bc-abb7-4ea4-90a0-f9a8a0a4959e" />


### 2. The "Silent Growth" Anomaly (e.g., Clean Look, Sneakers)
* **Data Signal:** Viral volume is often 50% lower than "hype" trends, yet the **Adoption Signal** (Orange Line) shows a consistent positive coefficient ($r > 0.8$).
* **Business Implication:** This represents the "Core" business. The algorithm identifies these as **"Safe Bets"** for long-lead manufacturing, as demand is decoupled from social media volatility.

<img width="800" height="500" alt="cleanlook_style_signal" src="https://github.com/user-attachments/assets/7446577a-e562-4774-be4a-d3df8e93f989" />

<img width="800" height="500" alt="sneakers_style_signal" src="https://github.com/user-attachments/assets/4da5211f-1904-4ccf-a681-b1a50b7852da" />


### 3. The "Burnout Velocity"
* **Observation:** Trends that reached a viral score of 200+ in Week 1 (like *Mob Wife*) experienced the fastest adoption decay by Week 6 (-15%).
* **Rule:** The algorithm suggests an inverse relationship between **Initial Viral Velocity** and **Trend Longevity**.

## Code Structure
The engine is built to be modular. In a production environment, the `synthetic_data` module would be replaced by API calls to TikTok Creative Center (Virality) and internal POS data (Adoption).

```python
# The Core Logic: Penalizing "Empty Noise"
signal_df["signal_score"] = (
    signal_df["adoption_growth_pct"] / signal_df["viral_norm"]
).round(2)
