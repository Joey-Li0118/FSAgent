# chatbot/demo_responses.py

DEMO_RESPONSES = [
    {
        "keywords": ["arc-co", "arc", "payment limit"],
        "answer": "Under ARC-CO, the payment limit is **$125,000 per person** per crop year for covered commodities. Payments are triggered when county revenue falls below the ARC-CO guarantee (86% of benchmark revenue).",
        "citations": [{"source": "2-CP Handbook", "section": "Section 4, Para 412", "text": "The per-person payment limitation for ARC-CO shall not exceed $125,000 per crop year for all covered commodities combined."}]
    },
    {
        "keywords": ["plc", "crops", "covered"],
        "answer": "PLC covers all **major covered commodities** including wheat, corn, grain sorghum, barley, oats, upland cotton, long-grain rice, soybeans, sunflower seed, rapeseed, canola, safflower, flaxseed, mustard seed, crambe, sesame, and pulse crops.",
        "citations": [{"source": "1-ARCPLC Handbook", "section": "Section 2, Para 201", "text": "Covered commodities eligible for PLC include wheat, feed grains, oilseeds, pulse crops, and rice as defined in the Agricultural Act of 2018."}]
    },
    {
        "keywords": ["crp", "enroll", "conservation"],
        "answer": "To enroll in CRP, visit your **local FSA office** during an open signup period. You'll submit an offer specifying the acres and conservation practice. FSA ranks offers using the Environmental Benefits Index (EBI) and accepts highest-ranked offers until the signup cap is reached.",
        "citations": [{"source": "2-CRP Handbook", "section": "Section 3, Para 311", "text": "Producers wishing to enroll must submit a CRP-1 form to their local FSA county office during an announced signup period."}]
    },

    # ── ARC-CO vs ARC-IC ────────────────────────────────────────────────────
    {
        "keywords": ["arc-co", "arc-ic", "difference", "compare"],
        "answer": (
            "**ARC-CO (County)** and **ARC-IC (Individual)** are both revenue-based safety nets, but they measure losses differently:\n\n"
            "- **ARC-CO** triggers a payment when *county-wide* average revenue for a crop falls below 86% of the county benchmark revenue. "
            "All enrolled acres in that county receive the same per-acre payment regardless of what happened on your individual farm.\n"
            "- **ARC-IC** triggers a payment when *your farm's* actual revenue across all covered commodities falls below 86% of your farm benchmark. "
            "It is whole-farm rather than crop-by-crop, and payments are made at 65% of base acres.\n\n"
            "ARC-CO is simpler and more predictable; ARC-IC may benefit farms whose yields diverge significantly from the county average."
        ),
        "citations": [{"source": "1-ARCPLC Handbook", "section": "Section 3, Para 302–303", "text": "ARC-CO guarantees are calculated using county benchmark revenue while ARC-IC guarantees are calculated using the individual producer's benchmark revenue across all covered commodities on the farm."}]
    },

    # ── PLC payment rate ────────────────────────────────────────────────────
    {
        "keywords": ["plc", "payment", "rate", "reference price", "effective"],
        "answer": (
            "PLC payments are calculated as:\n\n"
            "**Payment = (Effective Reference Price − MYA Price) × Payment Yield × Base Acres × 85%**\n\n"
            "The *effective reference price* is the higher of the statutory reference price or 85% of the Olympic average market year price over the prior 5 years, "
            "capped at 115% of the statutory reference price. For example, the statutory reference price for corn is **$3.70/bu**."
        ),
        "citations": [{"source": "1-ARCPLC Handbook", "section": "Section 5, Para 503", "text": "The PLC payment rate equals the effective reference price minus the marketing year average price, multiplied by the payment yield and 85 percent of base acres."}]
    },

    # ── Election deadline ───────────────────────────────────────────────────
    {
        "keywords": ["election", "deadline", "signup", "enroll", "when"],
        "answer": (
            "FSA program elections (ARC vs. PLC) are made **once per Farm Bill cycle** and remain in effect for the life of that Farm Bill unless a one-time election opportunity is offered. "
            "Under the 2018 Farm Bill, a re-election window was opened in 2019 for the 2019–2023 crop years. "
            "For the current cycle, check with your local FSA office for announced signup periods — deadlines typically fall in **March of the applicable crop year**."
        ),
        "citations": [{"source": "1-ARCPLC Handbook", "section": "Section 2, Para 215", "text": "Program elections made during the signup period are irrevocable for the remainder of the Farm Bill cycle unless a new election period is announced by the Secretary."}]
    },

    # ── Payment acres ───────────────────────────────────────────────────────
    {
        "keywords": ["base acres", "payment acres", "how many", "eligible acres"],
        "answer": (
            "Payments under ARC and PLC are calculated on **85% of base acres** for a given crop on a farm. "
            "Base acres are established from historical plantings and are a property of the farm, not the producer. "
            "They do not need to be planted to the covered commodity to receive payments — they are fixed acreage figures on file with FSA."
        ),
        "citations": [{"source": "1-ARCPLC Handbook", "section": "Section 2, Para 210", "text": "Payments are made on 85 percent of the base acres for each covered commodity, regardless of what is actually planted on the farm in the program year."}]
    },

    # ── CRP rental rates ────────────────────────────────────────────────────
    {
        "keywords": ["crp", "rental", "rate", "payment", "how much"],
        "answer": (
            "CRP annual rental payments are based on the **county average dry land cash rent** (or irrigated cash rent, where applicable), "
            "adjusted by a soil rental rate that reflects the productivity of the specific soils being enrolled. "
            "FSA publishes county-level soil rental rates annually. Additional **incentive payments** of up to 20% above the soil rental rate "
            "may be offered for high-priority practices or continuous signup practices such as filter strips and riparian buffers."
        ),
        "citations": [{"source": "2-CRP Handbook", "section": "Section 4, Para 401", "text": "Annual rental payments shall be based on the average county dry land cash rental rate adjusted by the relative productivity of the soils being enrolled, as published in the county soil rental rate schedule."}]
    },

    # ── CRP contract length ─────────────────────────────────────────────────
    {
        "keywords": ["crp", "contract", "length", "years", "how long"],
        "answer": (
            "CRP contracts are generally **10 to 15 years** in length. Most general signup contracts are set at 10 years. "
            "Continuous signup practices (such as filter strips, grassed waterways, and pollinator habitat) are typically offered at 10–15 years. "
            "Early termination is permitted in limited circumstances but may require refund of some or all rental payments received."
        ),
        "citations": [{"source": "2-CRP Handbook", "section": "Section 3, Para 325", "text": "CRP contracts shall be for a period of not less than 10 years nor more than 15 years, as determined appropriate by the county committee."}]
    },

    # ── NAP coverage ────────────────────────────────────────────────────────
    {
        "keywords": ["nap", "noninsured", "crop assistance", "non-insured"],
        "answer": (
            "The **Noninsured Crop Disaster Assistance Program (NAP)** provides financial assistance to producers of non-insurable crops "
            "when low yields, loss of inventory, or prevented planting occur due to natural disasters. "
            "Basic NAP coverage is set at **50% of expected production at 55% of the average market price**. "
            "Producers may purchase **buy-up coverage** of up to 65% of production at prices up to 100% of the average market price for an additional premium."
        ),
        "citations": [{"source": "1-NAP Handbook", "section": "Section 1, Para 103", "text": "Basic NAP coverage provides protection at 50 percent of expected production valued at 55 percent of the applicable average market price for the crop."}]
    },

    # ── Adjusted Gross Income (AGI) limit ───────────────────────────────────
    {
        "keywords": ["agi", "adjusted gross income", "income limit", "eligibility", "wealthy"],
        "answer": (
            "To be eligible for most FSA commodity program payments (ARC, PLC, CRP), a person or legal entity must have an "
            "**average adjusted gross income (AGI) of $900,000 or less** over the three preceding tax years. "
            "There is an exception: if more than 75% of AGI is derived from farming, ranching, or forestry, the cap does not apply for certain programs. "
            "FSA verifies AGI compliance through IRS data-sharing."
        ),
        "citations": [{"source": "5-PL Handbook", "section": "Section 2, Para 203", "text": "A person or legal entity with an average adjusted gross income exceeding $900,000 is ineligible for FSA commodity program payments unless at least 75 percent of that income is derived from farming, ranching, or forestry operations."}]
    },

    # ── WHIP+ / Disaster programs ───────────────────────────────────────────
    {
        "keywords": ["disaster", "whip", "emergency", "flood", "drought", "elap", "livestock"],
        "answer": (
            "FSA administers several disaster assistance programs:\n\n"
            "- **ELAP** (Emergency Livestock Assistance Program) — covers losses to livestock, honeybees, and farm-raised fish due to adverse weather.\n"
            "- **LFP** (Livestock Forage Disaster Program) — compensates for grazing losses on drought-affected pastureland.\n"
            "- **LIP** (Livestock Indemnity Program) — payments for livestock deaths in excess of normal mortality caused by adverse weather.\n"
            "- **TAP** (Tree Assistance Program) — assists orchardists and nursery growers who lose trees, bushes, or vines to natural disasters.\n\n"
            "Applications must typically be filed within **30 days** of when the loss is first apparent."
        ),
        "citations": [{"source": "1-DAP Handbook", "section": "Section 1, Para 102", "text": "Producers must submit a notice of loss to their local FSA county office within 30 calendar days of when the loss of production or livestock is first apparent."}]
    },

    # ── Highly Erodible Land (HEL) compliance ───────────────────────────────
    {
        "keywords": ["hel", "highly erodible", "wetland", "conservation compliance", "swampbuster", "sodbuster"],
        "answer": (
            "To receive most USDA program benefits, producers must comply with **conservation compliance** provisions:\n\n"
            "- **Sodbuster**: Prohibits producing agricultural commodities on highly erodible land (HEL) without an approved conservation system.\n"
            "- **Swampbuster**: Prohibits converting wetlands for crop production. Violations can result in full loss of FSA program benefits for the year.\n\n"
            "Producers file **Form AD-1026** with FSA to certify compliance. NRCS makes the technical determinations on HEL and wetland status."
        ),
        "citations": [{"source": "6-CP Handbook", "section": "Section 2, Para 201", "text": "Producers who wish to receive USDA program payments must certify compliance with highly erodible land and wetland conservation provisions by filing Form AD-1026 with their local FSA office."}]
    },

    # ── Farm records / tracts ───────────────────────────────────────────────
    {
        "keywords": ["farm number", "tract", "farm record", "clu", "field"],
        "answer": (
            "FSA maintains farm records through the **Farm Records system**, which assigns every farm a unique **farm serial number (FSN)**. "
            "Each farm is composed of one or more **tracts** (contiguous land under the same ownership) and **CLUs** (Common Land Units — individual fields). "
            "Farm records establish base acres, payment yields, and operator/owner relationships. "
            "Producers should review their farm records annually at their local FSA office to ensure accuracy."
        ),
        "citations": [{"source": "10-CM Handbook", "section": "Section 3, Para 305", "text": "Each farm shall be assigned a unique farm serial number and shall consist of one or more tracts of land under common ownership as recorded in the FSA farm records system."}]
    }

]

FALLBACK_RESPONSE = {
    "answer": "This is a **judge/demo mode** response. In production, this answer would be retrieved from ingested USDA FSA handbook PDFs using a RAG pipeline. The system searches across official handbooks (ARC/PLC, CRP, NAP, etc.) and returns cited excerpts.",
    "citations": [{"source": "Demo Mode", "section": "N/A", "text": "No real documents are loaded. Upload FSA handbook PDFs to enable live retrieval."}]
}

def get_demo_response(query: str) -> dict:
    query_lower = query.lower()
    for resp in DEMO_RESPONSES:
        if any(kw in query_lower for kw in resp["keywords"]):
            return {"answer": resp["answer"], "citations": resp["citations"]}
    return FALLBACK_RESPONSE