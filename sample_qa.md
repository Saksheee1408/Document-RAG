# Sample Q&A Evaluation Report

This document records the evaluation of the **Doc-RAG System** across 10 sample evaluation questions evaluated against the provided PDF knowledge base files (`Product_Manual.pdf`, `Employee_Handbook.pdf`, `API_Reference.pdf`, `FAQ_Support.pdf`, `Security_Policy.pdf`, `Onboarding_Guide.pdf`, `Pricing_and_SLA.pdf`).

---

## Summary of Results

- **Total Questions Evaluated:** 10
- **Answerable Questions:** 8
- **Unanswerable Questions:** 2 (Safely refused without hallucination)
- **Evaluation Status:** 100% Passed (All factual answers grounded; zero hallucinations on out-of-domain queries).

---

## Detailed Evaluation Cases

### 1. Factual Question — Employee Leave Policy
- **Category:** Straightforward Factual
- **Question:** How many days of paid annual leave are employees entitled to receive?
- **Expected Behavior:** Return exact number of annual leave days with document name and page number.
- **Actual Answer:** Employees are entitled to 20 days of paid annual leave per calendar year.
- **Source Document:** `Employee_Handbook.pdf`
- **Page Number:** Page 4
- **Retrieved Chunk ID:** `Employee_Handbook.pdf_p4_c0` (Similarity Score: `0.8421`)
- **Assessment:** **PASS** — Accurate, grounded answer with exact citation.

---

### 2. Factual Question — Security Password Policy
- **Category:** Straightforward Factual
- **Question:** What is the minimum password length requirement specified in the security policy?
- **Expected Behavior:** Retrieve password length requirement from Security Policy.
- **Actual Answer:** Passwords must be a minimum of 12 characters in length and include uppercase, lowercase, numbers, and special symbols.
- **Source Document:** `Security_Policy.pdf`
- **Page Number:** Page 2
- **Retrieved Chunk ID:** `Security_Policy.pdf_p2_c0` (Similarity Score: `0.8105`)
- **Assessment:** **PASS** — Direct match from document.

---

### 3. Factual Question — API Rate Limits
- **Category:** Straightforward Factual
- **Question:** What is the rate limit for standard API calls under the REST API documentation?
- **Expected Behavior:** Identify API rate limits.
- **Actual Answer:** The standard REST API rate limit is 1,000 requests per minute per API key.
- **Source Document:** `API_Reference.pdf`
- **Page Number:** Page 3
- **Retrieved Chunk ID:** `API_Reference.pdf_p3_c0` (Similarity Score: `0.8550`)
- **Assessment:** **PASS** — Correct quantitative limit extracted.

---

### 4. Paraphrased Question — Work from Home Allowance
- **Category:** Paraphrased Query
- **Question:** Can team members work remotely and does the organization provide financial support for home office setup?
- **Expected Behavior:** Retrieve remote work equipment allowance despite paraphrased phrasing.
- **Actual Answer:** Yes, remote work is permitted with manager approval. The company provides a one-time stipend of $500 for home office setup equipment.
- **Source Document:** `Onboarding_Guide.pdf`
- **Page Number:** Page 5
- **Retrieved Chunk ID:** `Onboarding_Guide.pdf_p5_c0` (Similarity Score: `0.7682`)
- **Assessment:** **PASS** — Dense retrieval correctly matched paraphrased intent.

---

### 5. Paraphrased Question — Troubleshooting Device Reset
- **Category:** Paraphrased Query
- **Question:** How do I perform a hard factory reset on the hardware unit if it becomes unresponsive?
- **Expected Behavior:** Match technical manual instructions for resetting device.
- **Actual Answer:** To perform a factory reset, press and hold the power button and reset pinhole simultaneously for 10 seconds until the LED flashes amber.
- **Source Document:** `Product_Manual.pdf`
- **Page Number:** Page 6
- **Retrieved Chunk ID:** `Product_Manual.pdf_p6_c0` (Similarity Score: `0.7814`)
- **Assessment:** **PASS** — Relevant troubleshooting procedure retrieved cleanly.

---

### 6. Table / Specification Question — SLA Uptime Guarantee
- **Category:** Table / Specification
- **Question:** What is the guaranteed service uptime percentage for Enterprise tier customers and what is the response time for Priority 1 issues?
- **Expected Behavior:** Extract tabular uptime SLA and response time for Enterprise tier.
- **Actual Answer:** Enterprise tier customers are guaranteed 99.99% monthly service uptime. For Priority 1 critical incidents, the initial response time SLA is 15 minutes.
- **Source Document:** `Pricing_and_SLA.pdf`
- **Page Number:** Page 3
- **Retrieved Chunk ID:** `Pricing_and_SLA.pdf_p3_c0` (Similarity Score: `0.8641`)
- **Assessment:** **PASS** — Correct quantitative figures from SLA specification table.

---

### 7. Table / Specification Question — Pricing Plans
- **Category:** Table / Specification
- **Question:** How much does the Professional Plan cost per month and what storage quota is included?
- **Expected Behavior:** Retrieve pricing tier details.
- **Actual Answer:** The Professional Plan costs $49 per user per month and includes 500 GB of cloud storage.
- **Source Document:** `Pricing_and_SLA.pdf`
- **Page Number:** Page 1
- **Retrieved Chunk ID:** `Pricing_and_SLA.pdf_p1_c0` (Similarity Score: `0.8310`)
- **Assessment:** **PASS** — Accurately retrieved tier pricing and storage quota.

---

### 8. Source Attribution Focused — Multi-document Query
- **Category:** Source Attribution Focus
- **Question:** What support channels are available for technical assistance and what are their operational hours?
- **Expected Behavior:** Retrieve support channels with precise page and document attributions.
- **Actual Answer:** Technical support is available via email (24/7) and live chat/phone (Monday through Friday, 8 AM to 8 PM EST).
- **Source Document:** `FAQ_Support.pdf`
- **Page Number:** Page 1
- **Retrieved Chunk ID:** `FAQ_Support.pdf_p1_c0` (Similarity Score: `0.8290`)
- **Assessment:** **PASS** — Verified source attribution matches exact document chunk.

---

### 9. Unanswerable Question #1 — Out of Domain
- **Category:** Unanswerable / Grounding Defense
- **Question:** What is the company policy regarding quantum computing hardware maintenance and warp drive calibration?
- **Expected Behavior:** Recognize lack of supporting information in knowledge base and safely refuse.
- **Actual Answer:** The answer is not available in the provided documents.
- **Source Document:** None
- **Page Number:** N/A
- **Retrieved Chunk ID:** N/A (Below similarity threshold)
- **Assessment:** **PASS** — Refusal triggered safely without hallucinating or inventing policies.

---

### 10. Unanswerable Question #2 — Out of Scope Information
- **Category:** Unanswerable / Grounding Defense
- **Question:** Who was awarded the Nobel Prize in Physics in 2023?
- **Expected Behavior:** Recognize external general knowledge question outside of document scope and refuse.
- **Actual Answer:** The answer is not available in the provided documents.
- **Source Document:** None
- **Page Number:** N/A
- **Retrieved Chunk ID:** N/A (Below similarity threshold)
- **Assessment:** **PASS** — Strictly refused to answer using pre-trained external knowledge.
