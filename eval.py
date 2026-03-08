"""
Evaluation harness for FSA Navigator.

Add known Q&A pairs to EVAL_SET below, then run:
    python eval.py

This gives you a score and a failure report — very useful for
iterating on your chunking strategy and system prompt.

IMPROVEMENT OPPORTUNITY:
The current eval just checks if keywords appear in the answer.
A better eval would:
- Use Claude to grade answers against a rubric
- Check factual accuracy against the source paragraph
- Track which chunks were retrieved (retrieval recall)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import time
from chatbot.rag import FSANavigator

# ------------------------------------------------------------------ #
#  ADD YOUR EVAL QUESTIONS HERE                                        #
#  Find correct answers by reading the actual FSA handbooks           #
# ------------------------------------------------------------------ #
EVAL_SET = [
    {
        "question": "What is the payment limit for ARC-CO for a single person?",
        "must_contain": ["125,000", "payment limit"],
        "notes": "Per 2018 Farm Bill, $125,000 per person for ARC/PLC combined"
    },
    {
        "question": "What does ARC stand for?",
        "must_contain": ["agricultural risk coverage"],
        "notes": "Basic program name"
    },
    {
        "question": "What does PLC stand for?",
        "must_contain": ["price loss coverage"],
        "notes": "Basic program name"
    },
    {
        "question": "Can a farmer switch between ARC-CO and PLC every year?",
        "must_contain": ["election", "year"],
        "notes": "Elections are made for the life of the farm bill with some exceptions"
    },
    {
        "question": "What crops are covered under PLC?",
        "must_contain": ["covered commodity"],
        "notes": "Should reference 'covered commodities'"
    },     
    {
        "question": "What is the purpose of FSA Handbook 1-PL?",
        "must_contain": ["person", "payment eligibility"],
        "notes": "Should reference determining 'persons' and payment eligibility for producers"
    },
    {
        "question": "What is the statutory authority for payment limitation and payment eligibility provisions?",
        "must_contain": ["Food Security Act", "7 CFR", "1400"],
        "notes": "Should cite Food Security Act of 1985 and 7 CFR Part 1400"
    },
    {
        "question": "When were the first payment limitation provisions established, and what was the original limit?",
        "must_contain": ["1970", "55,000"],
        "notes": "Agricultural Act of 1970, $55,000 limit for 1971-1973 crops"
    },
    {
        "question": "What did the Omnibus Budget Reconciliation Act of 1987 add to payment limitation rules?",
        "must_contain": ["actively engaged", "cash-rent tenant", "foreign"],
        "notes": "Should mention actively engaged in farming, cash-rent tenant rule, and foreign person limits"
    },
    {
        "question": "Under the 2002 Farm Security and Rural Investment Act, what were the DCP payment limits?",
        "must_contain": ["40,000", "65,000", "75,000"],
        "notes": "Direct payments $40k, counter-cyclical $65k, marketing loan gains/LDPs $75k"
    },
    {
        "question": "What six eligibility and limitation rules can apply to a program under 1-PL?",
        "must_contain": ["payment limitation", "actively engaged", "cash-rent tenant", "permitted entity", "foreign person"],
        "notes": "Should name all 6: Payment Limitation, Actively Engaged, Cash-Rent Tenant, Permitted Entity, Foreign Person, AGI"
    },
    {
        "question": "What is the CRP annual rental payment limitation per person?",
        "must_contain": ["50,000"],
        "notes": "CRP annual rental payment limit is $50,000 per person"
    },
    {
        "question": "What are the payment limits for DCP direct payments, counter-cyclical payments, and NAP?",
        "must_contain": ["40,000", "65,000", "100,000"],
        "notes": "Direct payments $40k, counter-cyclical $65k, NAP $100k"
    },
    {
        "question": "What is the Adjusted Gross Income limitation for receiving FSA program benefits?",
        "must_contain": ["2.5 million", "ineligible"],
        "notes": "AGI exceeding $2.5 million makes a producer ineligible for most FSA benefits"
    },
    {
        "question": "Do the AGI provisions apply to CRP contracts effective before October 1, 2002?",
        "must_contain": ["no", "october", "2002"],
        "notes": "AGI limitation does NOT apply to CRP contracts effective before October 1, 2002"
    },
    {
        "question": "Can FSA staff give casual advice on how to structure a farming operation to maximize payments?",
        "must_contain": ["no", "casual advice"],
        "notes": "Par. 37 explicitly prohibits giving casual advice on possible determinations or structuring operations"
    },
    {
        "question": "Is there a specific deadline for filing the CCC-502 Farm Operating Plan?",
        "must_contain": ["no", "deadline", "eligible"],
        "notes": "No specific deadline, but forms must be filed and determinations made before benefits are issued"
    },
    {
        "question": "If one producer on a multi-party contract fails to file a CCC-502, what happens to the other producers?",
        "must_contain": ["ineligible", "other", "eligible"],
        "notes": "Only the non-filing producer is ineligible; other producers who comply remain eligible"
    },
    {
        "question": "Must producers file a new CCC-502 every year?",
        "must_contain": ["no", "continuous", "changes"],
        "notes": "CCC-502 is a continuous certification; no annual resubmission required unless operation changes"
    },
    {
        "question": "What types of changes require a producer to update their CCC-502?",
        "must_contain": ["cash-rent", "capital", "income"],
        "notes": "Should mention lease changes, contribution changes, new farming interests, income changes affecting AGI"
    },
    {
        "question": "What is adequate documentation for a COC determination?",
        "must_contain": ["actively engaged", "person", "AGI"],
        "notes": "Whatever is needed to make 'actively engaged', 'person', and AGI compliance determinations"
    },
    {
        "question": "What documentation is required for trusts receiving FSA payments?",
        "must_contain": ["trust agreement", "revocable"],
        "notes": "Must provide copy of trust agreement unless trust is revocable; trusts must be scrutinized"
    },
    {
        "question": "Does requesting additional documentation from a producer extend the 60-day determination deadline?",
        "must_contain": ["no", "60"],
        "notes": "Requesting additional documents does NOT extend the 60-day determination period"
    },
    {
        "question": "What happens if a producer is determined not to be actively engaged in farming?",
        "must_contain": ["ineligible", "payment"],
        "notes": "Producer becomes completely ineligible for any payment requiring an 'actively engaged' determination"
    },
    {
        "question": "Can a husband and wife be considered separate persons for payment limitation purposes?",
        "must_contain": ["yes", "separate", "farming operation"],
        "notes": "Yes, if each brought separate farming operations into marriage and maintained them throughout"
    },
    {
        "question": "What does the Cash-Rent Tenant rule do when provisions are violated?",
        "must_contain": ["ineligible", "cash-rent tenant"],
        "notes": "The cash-rent tenant (not the landowner) is determined ineligible if provisions are not met"
    },
    {
        "question": "For programs requiring person but not actively engaged determinations, what must a producer's share be?",
        "must_contain": ["commensurate", "contributions", "at risk"],
        "notes": "Share of profits/losses must be commensurate with contributions, and contributions must be at risk"
    },
    {
        "question": "Which CRP contracts are subject to the provisions of handbook 1-PL?",
        "must_contain": ["1988", "july"],
        "notes": "CRP contracts initially approved after July 31, 1988 are subject to 1-PL provisions"
    },
    {
        "question": "What is the CRP inheritance exception to payment limits?",
        "must_contain": ["inherit", "without regard"],
        "notes": "Inherited CRP land allows payments under that contract without regard to other contract payments"
    },
    {
        "question": "Son B receives $40,000 in CRP payments. Father D is alive and transfers his land to Son B. How much additional CRP payment can Son B receive?",
        "must_contain": ["10,000", "50,000"],
        "notes": "Only $10,000 more to reach the $50,000 limit; no inheritance exception since Father D is alive"
    },
    {
        "question": "What must County Offices notify producers about annually regarding payment limitations?",
        "must_contain": ["payment limitation", "actively engaged", "foreign person", "AGI"],
        "notes": "Must cover payment limits, actively engaged rules, cash-rent tenant, permitted entities, foreign person, and AGI"
    },
    {
        "question": "What are the responsibilities of an entity receiving FSA program benefits regarding its members?",
        "must_contain": ["names", "addresses", "permitted entities"],
        "notes": "Must provide member names/addresses/IDs to COC and inform members of permitted entity designation requirements"
    },
]


def run_eval():
    print("FSA Navigator — Evaluation Run")
    print("=" * 50)

    navigator = FSANavigator()
    db_size = navigator.collection_size()
    print(f"Documents in DB: {db_size} chunks\n")

    if db_size == 0:
        print("⚠️  No documents loaded. Run ingestion first.")
        print("   python ingestion/ingest.py data/pdfs/")
        return

    passed = 0
    failed = []

    for i, item in enumerate(EVAL_SET):
        q = item["question"]
        result = navigator.query(q)
        answer = result["answer"].lower()

        all_found = all(kw.lower() in answer for kw in item["must_contain"])

        status = "✅" if all_found else "❌"
        print(f"{status} Q{i+1}: {q}")

        if all_found:
            passed += 1
            failed.append({
                "question": q,
                "missing_keywords": "nothing",
                "answer_preview": result["answer"][:200],
                "notes": item["notes"]
            })
            print(f"   Missing: nothing")
            print(f"   Answer preview: {result['answer'][:150]}...")
        else:
            missing = [kw for kw in item["must_contain"] if kw.lower() not in answer]
            failed.append({
                "question": q,
                "missing_keywords": missing,
                "answer_preview": result["answer"][:200],
                "notes": item["notes"]
            })
            print(f"   Missing: {missing}")
            print(f"   Answer preview: {result['answer'][:150]}...")
        time.sleep(2)
    print(f"\nScore: {passed}/{len(EVAL_SET)}")

    if failed:
        print("\n--- FAILURES ---")
        for f in failed:
            print(f"\nQ: {f['question']}")
            print(f"Expected keywords: {f['missing_keywords']}")
            print(f"Notes: {f['notes']}")
            print(f"Got: {f['answer_preview']}...")

    print("\nNext steps:")
    print("- If score is low, try adjusting CHUNK_SIZE in rag.py")
    print("- Check if the right documents are loaded for each question")
    print("- Improve the system prompt for specific failure patterns")


if __name__ == "__main__":
    run_eval()
